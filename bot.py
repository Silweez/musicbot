import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = "8652104351:AAHRZU4OrLd4oJuJCxz6_afouMy7MchIIPc"

# 🎵 Скачування музики
def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'quiet': True,
        'noplaylist': True,

       
        'ffmpeg_location': r'C:\\ffmpeg-2026-05-06-git-f2e5eff3ff-full_build\\bin',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        file = ydl.prepare_filename(info['entries'][0])
        return os.path.splitext(file)[0] + ".mp3"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 Привіт! Надішли назву пісні або слова — я знайду музику 🔥"
    )


# текстові повідомлення
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔎 Шукаю музику...")

    try:
        mp3 = download_music(query)

        await update.message.reply_audio(
            audio=open(mp3, 'rb'),
            title=query
        )

        os.remove(mp3)

    except Exception as e:
        await update.message.reply_text(f"❌ Не знайшов: {e}")


# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("🎧 Music Bot запущений...")
import os

app.run_polling()