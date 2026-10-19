from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
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


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/ws')
def terminal(ws):
    master_fd, slave_fd = pty.openpty()
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
