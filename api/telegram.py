import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.error import URLError
from urllib.request import Request, urlopen

TEXT = (
    "<b>Pemberitahuan layanan</b>\n\n"
    "Bot ini akan diistirahatkan.\n"
    "Silakan melanjutkan melalui bot baru dengan menekan tombol di bawah.\n\n"
    "Seluruh data Anda telah dipindahkan secara otomatis."
)
BUTTON = {
    "inline_keyboard": [
        [{"text": "Buka bot baru", "url": "https://t.me/tgXapp_bot?start=hallo"}]
    ]
}


def tokens():
    raw = os.environ.get("BOT_TOKEN", "")
    return [part.strip() for part in raw.split(",") if part.strip()]


def send(token, chat_id):
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": TEXT,
            "parse_mode": "HTML",
            "reply_markup": BUTTON,
        }
    ).encode()
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode())
    return bool(data.get("ok"))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._json(200, {"ok": True})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            update = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            update = {}

        chat_id = (update.get("message") or {}).get("chat", {}).get("id")
        if chat_id:
            for token in tokens():
                try:
                    if send(token, chat_id):
                        break
                except (URLError, TimeoutError, json.JSONDecodeError):
                    continue

        self._json(200, {"ok": True})

    def _json(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)
