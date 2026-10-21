import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

# --- AAPKI CREDENTIALS ---
API_ID = 34440739
API_HASH = "ddf763b867f4db1afdd6c9004be47c93"
BOT_TOKEN = "8928278869:AAG-ACzdrpLfoXJQIyaI-bUk2f8k6POgEo8"

app = Client("railway_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("🤖 **Railway Music Bot is Online!**\n\nMuje group me add karke admin banao aur `/play [song name]` command do!")

@app.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply_text("❓ Usage: `/play song_name`")
        return

    query = " ".join(message.command[1:])
    msg = await message.reply_text(f"🔎 Searching for: **{query}**...")

    ydl_opts = {"format": "bestaudio/best", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            audio_url = info['url']
            title = info['title']
        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
            return

    chat_id = message.chat.id
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(audio_url)
        )
        await msg.edit(f"🎶 **Playing Now in Voice Chat:**\n[{title}]({audio_url})")
    except Exception as e:
        await msg.edit(f"❌ Voice Chat Error: {e}\n\n⚠️ Ensure Voice Chat is active in the group.")

async def main():
    await app.start()
    await call_py.start()
    print("🚀 Music Bot started successfully on Railway!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
  
