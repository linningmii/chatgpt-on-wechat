from flask import Flask, request
from verify import verify
from config import load_config

app = Flask(__name__)
config = load_config()

@app.route("/")
def hello_world():
    name = request.args.get("name", "")
    return f"<p>Hello, {name}!</p>"

@app.route("/verify")
def api_verify():
    return verify()
