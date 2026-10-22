from flask import Flask, render_template, request, redirect, url_for
from flask_sock import Sock
import pty
import os
import sys
import select
import subprocess
import threading
import json

app = Flask(__name__)
sock = Sock(app)

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')

# Håller koll på alla aktiva spelsessioner med rik data
ACTIVE_SESSIONS = {}
sessions_lock = threading.Lock()

ADMIN_PASSWORD = "hemligt123"


@app.route('/')
def index():
    return render_template('index.html')


# --- ADMIN PANEL ---
@app.route('/admin-announce', methods=['GET', 'POST'])
def admin_announce():
    status_msg = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        password = request.form.get('password', '')
        
        if password != ADMIN_PASSWORD:
            status_msg = "<h3 style='color:red;'>Fel lösenord!</h3>"
        else:
            # Hantera globalt meddelande till alla anslutna WebSockets
            if action == "broadcast":
                message = request.form.get('message', '')
                if message:
                    formatted_msg = f"\r\n\r\n\x1b[41m\x1b[37m[MEDDELANDE FRÅN UTVECKLAREN]: {message}\x1b[0m\r\n> "
                    count = 0
                    with sessions_lock:
                        for sid, session in list(ACTIVE_SESSIONS).items():
                            try:
                                session['ws'].send(formatted_msg)
                                count += 1
                            except Exception:
                                del ACTIVE_SESSIONS[sid]
                    status_msg = f"<h3 style='color:green;'>Meddelande skickat till {count} spelare!</h3>"
            
            # Hantera att stänga av ett specifikt spel för uppdatering
            elif action == "kick_session":
                target_sid = request.form.get('session_id')
                with sessions_lock:
                    if target_sid in ACTIVE_SESSIONS:
                        try:
                            # Skicka ett snyggt tprint-meddelande innan vi stänger
                            update_msg = "\r\n\r\n\x1b[33m[UPDATE]: Spelet stängs tillfälligt för en uppdatering. Försök igen om ett par minuter!\x1b[0m\r\n"
                            ACTIVE_SESSIONS[target_sid]['ws'].send(update_msg)
                            # Döda processen
                            ACTIVE_SESSIONS[target_sid]['proc'].terminate()
                        except Exception:
                            pass
                        status_msg = "<h3 style='color:orange;'>Sessionen avslutades för uppdatering!</h3>"

    return render_template('admin.html', sessions=ACTIVE_SESSIONS, status_msg=status_msg, password=ADMIN_PASSWORD)


@sock.route('/ws')
def terminal(ws):
    master_fd, slave_fd = pty.openpty()
    session_id = str(id(ws)) # Unikt ID för just denna flik/spelare

    env = os.environ.copy()
    env['TERM'] = 'xterm-256color'
    proc = subprocess.Popen(
        [sys.executable, '-u', SCRIPT_PATH],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        cwd=os.path.dirname(SCRIPT_PATH),
        env=env
    )
    os.close(slave_fd)

    # Spara sessionen med standardvärden tills main.py skickar riktiga namnet
    with sessions_lock:
        ACTIVE_SESSIONS[session_id] = {
            'id': session_id,
            'name': 'Väljer namn...',
            'lang': 'Okänt',
            'ws': ws,
            'proc': proc
        }

    stop_event = threading.Event()

    def reader():
        while not stop_event.is_set():
            try:
                r, _, _ = select.select([master_fd], [], [], 0.05)
                if r:
                    data = os.read(master_fd, 4096)
                    if data:
                        text_data = data.decode('utf-8', errors='replace')
                        
                        # --- FÅNGA UPP DATA FRÅN SPELET UTAN ATT VISA DET PÅ SKÄRMEN ---
                        if "__SERVER_DATA__" in text_data:
                            for line in text_data.split('\r\n'):
                                if "__SERVER_DATA__:LANG:" in line:
                                    lang = line.split("__SERVER_DATA__:LANG:")[1].strip()
                                    with sessions_lock:
                                        if session_id in ACTIVE_SESSIONS:
                                            ACTIVE_SESSIONS[session_id]['lang'] = lang
                                elif "__SERVER_DATA__:NAME:" in line:
                                    name = line.split("__SERVER_DATA__:NAME:")[1].strip()
                                    with sessions_lock:
                                        if session_id in ACTIVE_SESSIONS:
                                            ACTIVE_SESSIONS[session_id]['name'] = name
                            continue # Hoppa över att skicka detta råa kommando till spelarens skärm!
                        
                        try:
                            ws.send(text_data)
                        except Exception:
                            break
                if proc.poll() is not None:
                    # Hantera när spelet tar slut normalt
                    try:
                        ws.send('\r\n\r\n\x1b[31m[Game ended. Refresh to play again.]\x1b[0m\r\n')
                    except Exception:
                        pass
                    break
            except Exception:
                break
        try:
            os.close(master_fd)
        except OSError:
            pass
        with sessions_lock:
            ACTIVE_SESSIONS.pop(session_id, None)

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    try:
        while True:
            data = ws.receive()
            if data is None:
                break
            try:
                os.write(master_fd, data.encode('utf-8') if isinstance(data, str) else data)
            except OSError:
                break
    except Exception:
        pass
    finally:
        stop_event.set()
        proc.terminate()
        with sessions_lock:
            ACTIVE_SESSIONS.pop(session_id, None)
