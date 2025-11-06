from flask import Flask
import platform
import os

app = Flask(__name__)

@app.route("/")
def index():
    os_info = platform.platform()
    hostname = platform.node()
    uptime = os.popen("uptime -p").read().strip()
    return f"""
    <html>
        <head><title>Linux Testisivu</title></head>
        <body>
            <h1>✅ Linux Testisivu</h1>
            <p><strong>Käyttöjärjestelmä:</strong> {os_info}</p>
            <p><strong>Koneen nimi:</strong> {hostname}</p>
            <p><strong>Käynnissäoloaika:</strong> {uptime}</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
