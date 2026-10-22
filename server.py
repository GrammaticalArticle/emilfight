from flask import Flask, render_template, request
from flask_sock import Sock
import pty
import os
import sys
import select
import subprocess
import threading

app = Flask(__name__)
sock = Sock(app)

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')

# --- Håller koll på alla spelares aktiva terminaler ---
ACTIVE_TERMINALS = set()
terminals_lock = threading.Lock()

# --- ÄNDRA DITT LÖSENORD HÄR ---
ADMIN_PASSWORD = "hemligt123"


@app.route('/')
def index():
    return render_template('index.html')


# --- Din nya dolda admin-sida ---
# Gå till /admin-announce i webbläsaren för att skicka meddelanden!
@app.route('/admin-announce', methods=['GET', 'POST'])
def admin_announce():
    status_msg = ""
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        message = request.form.get('message', '')
        
        if password != ADMIN_PASSWORD:
            status_msg = "<h3 style='color:red;'>Fel lösenord!</h3>"
        elif not message:
            status_msg = "<h3 style='color:orange;'>Du kan inte skicka ett tomt meddelande.</h3>"
        else:
            # Formaterar meddelandet med röd bakgrund (\x1b[41m) och vit text (\x1b[37m)
            # \r\n rensar raden och hoppar ner snyggt i spelarens terminal
            formatted_msg = f"\r\n\r\n\x1b[41m\x1b[37m[MEDDELANDE FRÅN UTVECKLAREN]: {message}\x1b[0m\r\n> "
            
            with terminals_lock:
                count = 0
                for master_fd in list(ACTIVE_TERMINALS):
                    try:
                        os.write(master_fd, formatted_msg.encode('utf-8'))
                        count += 1
                    except OSError:
                        ACTIVE_TERMINALS.remove(master_fd)
                status_msg = f"<h3 style='color:green;'>Succé! Meddelandet skickades till {count} aktiva spelare.</h3>"
                
    return f'''
        <div style="max-width: 500px; margin: 50px auto; font-family: sans-serif; padding: 20px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h2>Skicka live-meddelande till alla spelare</h2>
            {status_msg}
            <form method="post">
                <label><b>Admin-lösenord:</b></label><br>
                <input type="password" name="password" style="width:100%; padding: 8px; font-size:14px; margin-top:5px; margin-bottom:15px;" placeholder="Lösenord"><br>
                
                <label><b>Meddelande:</b></label><br>
                <textarea name="message" rows="4" style="width:100%; padding: 8px; font-size:16px; margin-top:5px;" placeholder="Skriv din uppdatering här..."></textarea><br><br>
                
                <input type="submit" value="Skicka ut till alla!" style="padding: 10px 20px; background: #ff4d4d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%;">
            </form>
        </div>
    '''


@sock.route('/ws')
def terminal(ws):
    master_fd, slave_fd = pty.openpty()
    
    # --- Spara spelarens terminal när de ansluter ---
    with terminals_lock:
        ACTIVE_TERMINALS.add(master_fd)

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

    stop_event = threading.Event()

    def reader():
        while not stop_event.is_set():
            try:
                r, _, _ = select.select([master_fd], [], [], 0.05)
                if r:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            try:
                                ws.send(data.decode('utf-8', errors='replace'))
                            except Exception:
                                break
                    except OSError:
                        break
                if proc.poll() is not None:
                    try:
                        while True:
                            r2, _, _ = select.select([master_fd], [], [], 0.1)
                            if r2:
                                data = os.read(master_fd, 4096)
                                if data:
                                    ws.send(data.decode('utf-8', errors='replace'))
                                else:
                                    break
                            else:
                                break
                    except Exception:
                        pass
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
        
        # --- Ta bort terminalen när spelet stängs eller tar slut ---
        with terminals_lock:
            ACTIVE_TERMINALS.discard(master_fd)

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
        # --- Säkerhetskopia för att ta bort terminalen om loopen dör ---
        with terminals_lock:
            ACTIVE_TERMINALS.discard(master_fd)
