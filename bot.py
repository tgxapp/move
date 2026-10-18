import asyncio
import os

from telegram import Bot
from telegram.error import TelegramError

from api.telegram import KEYBOARD, TEXT


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


def tokens():
    found = [part.strip() for part in os.environ.get("BOT_TOKEN", "").split(",") if part.strip()]
    if not found:
        raise SystemExit("Isi BOT_TOKEN di file .env. Beberapa token dipisah dengan koma.")
    return found


async def listen(token):
    label = token.split(":", 1)[0]
    print(f"Bot {label} menyala. Menunggu pesan...")
    offset = None
    async with Bot(token) as bot:
        while True:
            try:
                updates = await bot.get_updates(
                    timeout=30,
                    offset=offset,
                    allowed_updates=["message"],
                )
                for update in updates:
                    offset = update.update_id + 1
                    if update.effective_message is None:
                        continue
                    await update.effective_message.reply_text(
                        TEXT,
                        parse_mode="HTML",
                        reply_markup=KEYBOARD,
                    )
            except (TelegramError, TimeoutError) as error:
                print(f"Bot {label}: {error}")
                await asyncio.sleep(3)


async def main():
    load_env()
    await asyncio.gather(*(listen(token) for token in tokens()))


if __name__ == "__main__":
    asyncio.run(main())
