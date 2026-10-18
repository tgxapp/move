import json
import os
import threading
import time
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


def load_env():
    path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def bot_tokens():
    raw = os.environ.get("BOT_TOKEN", "")
    tokens = [part.strip() for part in raw.split(",") if part.strip()]
    if not tokens:
        raise SystemExit("Isi BOT_TOKEN di file .env. Beberapa token dipisah dengan koma.")
    return tokens


def call(token, method, payload=None, timeout=40):
    data = None if payload is None else json.dumps(payload).encode()
    request = Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def listen(token):
    label = token.split(":", 1)[0]
    offset = None
    print(f"Bot {label} menyala. Menunggu pesan...")

    while True:
        try:
            updates = call(
                token,
                "getUpdates",
                {"timeout": 30, "offset": offset, "allowed_updates": ["message"]},
            )
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                chat_id = (update.get("message") or {}).get("chat", {}).get("id")
                if not chat_id:
                    continue
                call(
                    token,
                    "sendMessage",
                    {
                        "chat_id": chat_id,
                        "text": TEXT,
                        "parse_mode": "HTML",
                        "reply_markup": BUTTON,
                    },
                )
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"Bot {label}: {error}")
            time.sleep(3)


def main():
    load_env()
    threads = []
    for token in bot_tokens():
        thread = threading.Thread(target=listen, args=(token,), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
