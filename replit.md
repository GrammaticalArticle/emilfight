# Emil Boss Fight Simulator

A browser-playable Python console RPG served as a web terminal.

## Architecture

- `main.py` — the console game (pure Python, uses colorama for ANSI colors)
- `server.py` — Flask + flask-sock web server that wraps the game in a browser terminal
- `templates/index.html` — xterm.js terminal UI with WebSocket client

## How it works

1. User opens the browser; the page loads an xterm.js terminal
2. JavaScript connects to the `/ws` WebSocket endpoint
3. The server spawns `main.py` inside a PTY (pseudo-terminal) subprocess
4. PTY output is streamed to the browser via WebSocket; keyboard input is sent back
5. The game runs exactly as in a real terminal, including ANSI colors and `clear` screen

## Stack

- Python 3.11
- Flask + flask-sock (WebSocket)
- xterm.js 5.3 + xterm-addon-fit (browser terminal)
- colorama (ANSI color output in the game)

## Running

The `Run` workflow executes `python server.py`, which starts the server on port 5000.

## Notes

- Each browser tab gets its own isolated game subprocess
- Refreshing the page starts a new game session
- `os.system("cls"/"clear")` in main.py works because the game runs in a real PTY
