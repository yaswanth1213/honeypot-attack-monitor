
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from database import initialize_database, save_attempt

HOST = "127.0.0.1"
PORT = 8080

initialize_database()


class HoneypotHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        page = """
        <!DOCTYPE html>
        <html>
        <head><title>Security Login Portal</title></head>
        <body>
            <h2>Security Login Portal</h2>
            <form method="POST" action="/login">
                Username: <input name="username" required>
                <br><br>
                Password: <input type="password" name="password" required>
                <br><br>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode(
            "utf-8", errors="replace"
        )
        form = parse_qs(body)

        username = form.get("username", [""])[0][:100]
        timestamp = datetime.now().isoformat(timespec="seconds")
        client_ip = self.client_address[0]

        # Store the event, never the submitted password.
        save_attempt(
            timestamp, client_ip, username, "Login attempt"
        )

        print(
            f"[ALERT] {timestamp} | "
            f"IP: {client_ip} | Username: {username}"
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<h2>Login failed</h2>"
            b"<p>Demo honeypot recorded the attempt.</p>"
            b'<a href="/">Try again</a>'
        )

    def log_message(self, format, *args):
        pass


server = HTTPServer((HOST, PORT), HoneypotHandler)

print("Honeypot is running!")
print("Open http://127.0.0.1:8080")
print("Login attempts are stored in honeypot.db")
print("Press Ctrl+C to stop.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nHoneypot stopped.")
finally:
    server.server_close()
