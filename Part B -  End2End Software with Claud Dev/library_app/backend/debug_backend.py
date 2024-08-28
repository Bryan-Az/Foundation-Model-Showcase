import sys
import subprocess
import threading
import time
import requests

def run_command(command, timeout=10):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return stdout, stderr, process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        return "", "Command timed out after {} seconds".format(timeout), -1

def run_app_py():
    print("\nTrying to run app.py:")
    stdout, stderr, return_code = run_command("python app.py")
    print("STDOUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)
    print(f"Return code: {return_code}")

def test_backend_connection():
    print("\nTesting connection to backend API:")
    try:
        response = requests.get('http://127.0.0.1:5000/api/books', timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to backend: {e}")

def main():
    print("Debugging Flask Backend")
    print("======================")

    print("\nPython version:")
    print(sys.version)

    print("\nInstalled packages:")
    stdout, stderr, _ = run_command("pip list")
    print(stdout)

    print("\nTesting Flask import:")
    try:
        import flask
        print(f"Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"Error importing Flask: {e}")

    print("\nTesting Flask-CORS import:")
    try:
        import flask_cors
        print(f"Flask-CORS version: {flask_cors.__version__}")
    except ImportError as e:
        print(f"Error importing Flask-CORS: {e}")

    print("\nTesting Werkzeug import:")
    try:
        import werkzeug
        print(f"Werkzeug version: {werkzeug.__version__}")
    except ImportError as e:
        print(f"Error importing Werkzeug: {e}")

    # Run app.py in a separate thread
    app_thread = threading.Thread(target=run_app_py)
    app_thread.start()

    # Wait for the app to start
    time.sleep(5)

    # Test the connection to the backend
    test_backend_connection()

    # Wait for the app thread to finish
    app_thread.join(timeout=15)
    if app_thread.is_alive():
        print("Warning: app.py is still running after 15 seconds. It may be stuck.")

if __name__ == "__main__":
    main()