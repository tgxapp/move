import asyncio
import json
import os
from http.server import BaseHTTPRequestHandler

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError

WEBHOOK_URL = "https://move-omega-one.vercel.app/api/telegram"
TEXT = (
    "<b>Pemberitahuan layanan</b>\n\n"
    "Bot ini akan diistirahatkan.\n"
    "Silakan melanjutkan melalui bot baru dengan menekan tombol di bawah.\n\n"
    "Seluruh data Anda telah dipindahkan secara otomatis."
)
KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Buka bot baru", url="https://t.me/tgXapp_bot?start=hallo")]]
)


def tokens():
    return [part.strip() for part in os.environ.get("BOT_TOKEN", "").split(",") if part.strip()]


async def register_webhooks():
    for token in tokens():
        async with Bot(token) as bot:
            await bot.set_webhook(url=WEBHOOK_URL, allowed_updates=["message"])


async def reply(payload):
    for token in tokens():
        try:
            async with Bot(token) as bot:
                update = Update.de_json(payload, bot)
                message = update.effective_message if update else None
                if message is None:
                    return
                await message.reply_text(TEXT, parse_mode="HTML", reply_markup=KEYBOARD)
                return
        except TelegramError as error:
            print(f"Bot {token.split(':', 1)[0]}: {error}")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not tokens():
            self._json(500, {"ok": False, "error": "BOT_TOKEN kosong"})
            return
        try:
            asyncio.run(register_webhooks())
        except TelegramError as error:
            self._json(500, {"ok": False, "error": str(error)})
            return
        self._json(200, {"ok": True, "bots": len(tokens())})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            payload = {}
        try:
            asyncio.run(reply(payload))
        except Exception as error:
            print(error)
        self._json(200, {"ok": True})

    def _json(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)
