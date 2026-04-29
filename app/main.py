from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route("/")
def hello():
    # hostname tells us which pod responded
    hostname = socket.gethostname()
    # GREETING is what we will change via Kubernetes later
    greeting = os.environ.get("GREETING", "Hello!")
    return f"{greeting} from {hostname}!\n"

@app.route("/health")
def health():
    # k8s check if the app is still alive
    return "ok\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

