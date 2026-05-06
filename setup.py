import os
import venv
import subprocess
import sys

VENV_DIR = ".venv"

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    if not os.path.exists(VENV_DIR):
        print("creating .venv")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print(".venv exists")

    if os.name == "nt":
        python_bin = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_bin = os.path.join(VENV_DIR, "bin", "python")

    run(f'"{python_bin}" -m pip install --upgrade pip setuptools wheel')

    if os.path.exists("requirements.txt"):
        run(f'"{python_bin}" -m pip install -r requirements.txt')
    else:
        print("no requirements found")

    print("\nActivate with:")
    if os.name == "nt":
        print(r".venv\Scripts\activate")
    else:
        print("source .venv/bin/activate")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("\nSetup failed.")
        print("Scroll up — the real pip error is above this.")
        sys.exit(1)