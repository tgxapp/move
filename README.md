# move0bot

Setiap ada pesan masuk, bot membalas bahwa bot ini diistirahatkan, plus tombol ke bot baru.

1. Di Vercel, isi `BOT_TOKEN` pada environment Production. Untuk beberapa bot, pisahkan token dengan koma.
2. Setelah deploy selesai, buka tautan ini sekali untuk setiap token (ganti `TOKEN`):

```
https://api.telegram.org/botTOKEN/setWebhook?url=https://move-omega-one.vercel.app/api/telegram
```

Kalau muncul `{"ok":true}`, kirim `/start` ke bot. Balasan akan langsung masuk.
