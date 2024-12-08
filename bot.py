import os
import subprocess
from dotenv import load_dotenv
from pyrogram import Client, filters
import yt_dlp

# .env file se environment variables load karna
load_dotenv()

API_ID = os.getenv("26512850")
API_HASH = os.getenv("a51477d8c5205718ddec7dd922f36e57")
BOT_TOKEN = os.getenv("7604201457:AAEhfcE3FAKPxwWgStzCdpcjy1ILO6Z7bL8")
ADMIN_ID = int(os.getenv("5692922977,6710024903"))  # Admin ID ko .env file mein set karein

app = Client("music_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# /help command - Bot ka usage help dikhayega
@app.on_message(filters.command("help"))
def help(client, message):
    help_text = """
    Hello! I'm your Telegram Music Bot. Here's how you can use me:
    
    /play <song_name_or_youtube_url> - To play a song from YouTube.
    /stop - To stop the song and leave the voice chat.
    /reload - To restart the bot (Admin only).
    """
    app.send_message(message.chat.id, help_text)

# /reload command - Admin ke liye bot restart karne ka option
@app.on_message(filters.command("reload") & filters.user(ADMIN_ID))
def reload(client, message):
    try:
        app.send_message(message.chat.id, "Restarting the bot...")
        subprocess.Popen(["python3", "bot.py"])  # Bot ko restart karne ke liye subprocess use karna
        app.stop()  # Bot ko stop karna
    except Exception as e:
        app.send_message(message.chat.id, f"Error while restarting: {str(e)}")

# /stop command - Song ko stop karne aur voice chat se exit karne ka option
@app.on_message(filters.command("stop"))
def stop(client, message):
    try:
        # Bot ko song stop karne aur voice chat se exit karne ka command
        app.send_message(message.chat.id, "Stopping the song and leaving the voice chat...")

        # Agar bot kisi song ko play kar raha ho toh, usse stop karne ke liye
        app.leave_chat(message.chat.id)  # Voice chat ko leave karna

    except Exception as e:
        app.send_message(message.chat.id, f"Error: {str(e)}")
        print(e)

# /play command - YouTube se audio play karna
@app.on_message(filters.command("play"))
def play(client, message):
    try:
        # Agar message mein YouTube URL hai toh usse download karne ki koshish karein
        url = message.text.split(" ", 1)[1]
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '/tmp/%(id)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            file = ydl.prepare_filename(info)

            # File ko voice chat mein play karen
            app.send_message(message.chat.id, f"Now playing: {title}")
            app.send_audio(message.chat.id, file)
    except Exception as e:
        app.send_message(message.chat.id, "Error: Unable to play the song!")
        print(e)

app.run()
