from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import pty
import os
import sys
import select
import subprocess
import threading
import re

app = Flask(__name__)
sock = Sock(app)

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')

ACTIVE_SESSIONS = {}
sessions_lock = threading.Lock()

# Turnerings-tillstånd
TOURNAMENT = {
    "paused": False,
    "commentary": "",
    "competitor_1": "", # Session ID för spelare 1
    "competitor_2": "", # Session ID för spelare 2
    "cheers": {}        # {session_id_tävlande: antal_hejarop}
}

ADMIN_PASSWORD = "hemligt123"

def clean_ansi(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text).strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sessions')
def api_sessions():
    with sessions_lock:
        simplified = {}
        for sid, s in ACTIVE_SESSIONS.items():
            simplified[sid] = {
                'id': s['id'], 'name': s['name'], 'lang': s['lang'], 
                'stage': s['stage'], 'hp': s['hp']
            }
        return jsonify({
            "sessions": simplified,
            "tournament": TOURNAMENT
        })

@app.route('/admin-announce', methods=['GET', 'POST'])
def admin_announce():
    global TOURNAMENT
    status_msg = ""
    if request.method == 'POST':
        action = request.form.get('action')
        password = request.form.get('password', '')
        
        if password != ADMIN_PASSWORD:
            status_msg = "<h3 style='color:red;'>Fel lösenord!</h3>"
        else:
            if action == "broadcast":
                message = request.form.get('message', '')
                if message:
                    formatted_msg = f"\r\n\r\n\x1b[41m\x1b[37m[MEDDELANDE FRÅN UTVECKLAREN]: {message}\x1b[0m\r\n> "
                    with sessions_lock:
                        for sid, session in list(ACTIVE_SESSIONS.items()):
                            try: session['ws'].send(formatted_msg)
                            except Exception: del ACTIVE_SESSIONS[sid]
                    status_msg = "<h3 style='color:green;'>Meddelande skickat!</h3>"
            
            elif action == "tournament_control":
                t_action = request.form.get('t_action')
                if t_action == "pause":
                    TOURNAMENT["paused"] = True
                    TOURNAMENT["commentary"] = request.form.get('commentary', '')
                elif t_action == "resume":
                    TOURNAMENT["paused"] = False
                    TOURNAMENT["commentary"] = ""
                elif t_action == "set_competitors":
                    TOURNAMENT["competitor_1"] = request.form.get('comp1', '')
                    TOURNAMENT["competitor_2"] = request.form.get('comp2', '')
                    # Nollställ hejarop
                    TOURNAMENT["cheers"] = {TOURNAMENT["competitor_1"]: 0, TOURNAMENT["competitor_2"]: 0}
                status_msg = "<h3 style='color:purple;'>Turneringsstatus uppdaterad!</h3>"
                
            elif action == "kick_session":
                target_sid = request.form.get('session_id')
                with sessions_lock:
                    if target_sid in ACTIVE_SESSIONS:
                        try:
                            ACTIVE_SESSIONS[target_sid]['ws'].send("\r\n\x1b[33m[UPDATE]: Avstängd för uppdatering!\x1b[0m\r\n")
                            ACTIVE_SESSIONS[target_sid]['proc'].terminate()
                        except Exception: pass

    return render_template('admin.html', sessions=ACTIVE_SESSIONS, status_msg=status_msg, password=ADMIN_PASSWORD, tournament=TOURNAMENT)

@sock.route('/ws')
def terminal(ws):
    master_fd, slave_fd = pty.openpty()
    session_id = str(id(ws))

    env = os.environ.copy()
    env['TERM'] = 'xterm-256color'
    proc = subprocess.Popen(
        [sys.executable, '-u', SCRIPT_PATH],
        stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
        close_fds=True, cwd=os.path.dirname(SCRIPT_PATH), env=env
    )
    os.close(slave_fd)

    with sessions_lock:
        ACTIVE_SESSIONS[session_id] = {
            'id': session_id, 'name': 'Startar...', 'lang': 'Väljer...', 
            'stage': 'Intro/Meny', 'hp': 'N/A', 'ws': ws, 'proc': proc
        }

    stop_event = threading.Event()

    # Kontrollera löpande om spelet är pausat av admin eller om det finns nya hejarop
    def tournament_checker():
        last_pause_state = False
        last_cheer_count = 0
        while not stop_event.is_set():
            try:
                # Paus-hantering
                if TOURNAMENT["paused"] != last_pause_state:
                    last_pause_state = TOURNAMENT["paused"]
                    if last_pause_state:
                        # Injicera en dold flagga till main.py:s input-loop
                        os.write(master_fd, b"__TOURNAMENT_PAUSE__\n")
                        # Skicka kommentarsbannern direkt till skärmen via WebSocket
                        comm = TOURNAMENT["commentary"]
                        ws.send(f"\r\n\x1b[45m\x1b[37m[KOMMENTATOR]: {comm}\x1b[0m\r\n\x1b[33m[SPELET ÄR PAUSAT AV ADMIN]\x1b[0m\r\n")
                    else:
                        os.write(master_fd, b"__TOURNAMENT_RESUME__\n")
                        ws.send(f"\r\n\x1b[42m[SPELET ÅTERSTÄLLT – KÖR PÅ!]\x1b[0m\r\n> ")
                
                # Hejarops-hantering (om denna session är en competitor)
                if session_id in TOURNAMENT["cheers"]:
                    current_cheers = TOURNAMENT["cheers"][session_id]
                    if current_cheers > last_cheer_count:
                        diff = current_cheers - last_cheer_count
                        last_cheer_count = current_cheers
                        ws.send(f"\r\n\x1b[46m\x1b[30m🔥 SPELARE HEJAR PÅ DIG! (+{diff} Hype) 🔥\x1b[0m\r\n> ")
                        
                threading.Event().wait(0.5)
            except Exception: break

    threading.Thread(target=tournament_checker, daemon=True).start()

    def reader():
        while not stop_event.is_set():
            try:
                r, _, _ = select.select([master_fd], [], [], 0.05)
                if r:
                    data = os.read(master_fd, 4096)
                    if data:
                        text_data = data.decode('utf-8', errors='replace')
                        if "__SERVER_DATA__" in text_data:
                            for line in text_data.split('\n'):
                                cleaned_line = clean_ansi(line)
                                if "__SERVER_DATA__:LANG:" in cleaned_line:
                                    lang = cleaned_line.split("__SERVER_DATA__:LANG:")[1].strip()
                                    with sessions_lock: ACTIVE_SESSIONS[session_id]['lang'] = lang
                                elif "__SERVER_DATA__:NAME:" in cleaned_line:
                                    name = cleaned_line.split("__SERVER_DATA__:NAME:")[1].strip()
                                    with sessions_lock: ACTIVE_SESSIONS[session_id]['name'] = name
                                elif "__SERVER_DATA__:STAGE:" in cleaned_line:
                                    stage = cleaned_line.split("__SERVER_DATA__:STAGE:")[1].strip()
                                    with sessions_lock: ACTIVE_SESSIONS[session_id]['stage'] = stage
                                elif "__SERVER_DATA__:HP:" in cleaned_line:
                                    hp_val = cleaned_line.split("__SERVER_DATA__:HP:")[1].strip()
                                    with sessions_lock: ACTIVE_SESSIONS[session_id]['hp'] = hp_val
                            continue
                        try: ws.send(text_data)
                        except Exception: break
                if proc.poll() is not None: break
            except Exception: break
        try: os.close(master_fd)
        except OSError: pass
        with sessions_lock: ACTIVE_SESSIONS.pop(session_id, None)

    threading.Thread(target=reader, daemon=True).start()

    try:
        while True:
            data = ws.receive()
            if data is None: break
            
            # Kolla om en åskådare klickar för att heja på någon (skickas via JS från klienten)
            if isinstance(data, str) and data.startswith("__CHEER__:"):
                target_comp = data.split(":")[1]
                if target_comp in TOURNAMENT["cheers"]:
                    TOURNAMENT["cheers"][target_comp] += 1
                continue
                
            try: os.write(master_fd, data.encode('utf-8') if isinstance(data, str) else data)
            except OSError: break
    except Exception: pass
    finally:
        stop_event.set()
        proc.terminate()
        with sessions_lock: ACTIVE_SESSIONS.pop(session_id, None)
