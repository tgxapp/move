# move0bot

Setiap ada pesan masuk, bot membalas bahwa bot ini diistirahatkan, plus tombol ke bot baru. Balasan dikirim lewat library [python-telegram-bot](https://pypi.org/project/python-telegram-bot/).

1. Di Vercel, isi `BOT_TOKEN` pada environment Production. Untuk beberapa bot, pisahkan token dengan koma, lalu redeploy.
2. Setelah deployment berstatus Ready, buka sekali:

```
https://move-omega-one.vercel.app/api/telegram
```

Kalau muncul `{"ok":true,"bots":1}`, kirim `/start` ke bot.
