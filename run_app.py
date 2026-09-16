import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
PYTHON_EXE = Path(r"C:\Users\ahnan\AppData\Local\Programs\Python\Python312\python.exe")
NPM_EXE = Path(r"C:\Program Files\nodejs\npm.cmd")


# ---------------------------------------------------------------------------
# Start backend and frontend in separate console windows.
# ---------------------------------------------------------------------------
def start_process(cmd, cwd, name):
    print(f"Starting {name}...")
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        shell=False,
    )
    return process


# ---------------------------------------------------------------------------
# Wait until a URL responds successfully.
# ---------------------------------------------------------------------------
def wait_for_url(url, timeout=45):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            import urllib.request

            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status < 500:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False


# ---------------------------------------------------------------------------
# Main entry point.
# ---------------------------------------------------------------------------
def main():
    if not PYTHON_EXE.exists():
        raise FileNotFoundError(f"Python executable not found: {PYTHON_EXE}")
    if not NPM_EXE.exists():
        raise FileNotFoundError(f"npm executable not found: {NPM_EXE}")

    backend_cmd = [
        str(PYTHON_EXE),
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ]

    frontend_cmd = [
        str(NPM_EXE),
        "run",
        "dev",
        "--",
        "--host",
        "127.0.0.1",
        "--port",
        "5173",
    ]

    backend = start_process(backend_cmd, BACKEND_DIR, "backend")
    frontend = start_process(frontend_cmd, FRONTEND_DIR, "frontend")

    backend_ready = wait_for_url("http://127.0.0.1:8000/", timeout=45)
    frontend_ready = wait_for_url("http://127.0.0.1:5173/", timeout=45)

    if backend_ready:
        print("Backend is running at http://127.0.0.1:8000")
    else:
        print("Backend did not start in time.")

    if frontend_ready:
        print("Frontend is running at http://127.0.0.1:5173")
    else:
        print("Frontend did not start in time.")

    print("\nPress Ctrl+C in this terminal to stop both services.")

    try:
        while True:
            if backend.poll() is not None or frontend.poll() is not None:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")

    for process in (backend, frontend):
        if process.poll() is None:
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()

    print("Services stopped.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Failed to start app: {exc}", file=sys.stderr)
        input("Press Enter to exit...")
        raise
