from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.get("/")
def index():
    return (
        "<h1>Hello AppSec World</h1>"
        "<p>Docker Compose demo is running ✅</p>"
        "<p>Try: <a href='/health'>/health</a> or <a href='/ip'>/ip</a></p>"
    )

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/ip")
def ip():
    # демонстрируем подключаемую библиотеку requests
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=3)
        return jsonify(source="api.ipify.org", data=r.json())
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    # важно слушать 0.0.0.0, иначе контейнер не пробросится наружу
    app.run(host="0.0.0.0", port=8000)
