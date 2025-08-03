import os
import subprocess
from pyrogram import Client, filters

# Ambil API_ID dan API_HASH dari variabel lingkungan
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.video)
async def handle_video(client, message):
    print(f"📥 Menerima video dari @{message.from_user.username or message.from_user.id}")

    # Download video masuk
    input_path = await message.download(file_name="input.mp4")
    output_path = "output.mp4"
    thumb_path = "thumb.jpg"

    # Ambil thumbnail (frame detik ke-1)
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ss", "00:04:01.000", "-vframes", "1", thumb_path
    ])

    # Proses percepat video 4x
    command = [
        "ffmpeg", "-i", input_path,
        "-filter_complex", "[0:v]setpts=0.25*PTS[v];[0:a]atempo=2.0,atempo=2.0[a]",
        "-map", "[v]", "-map", "[a]",
        "-r", "24", "-preset", "fast", "-crf", "28",
        output_path
    ]

    subprocess.run(command)

    # Kirim ulang ke pengirim
    await message.reply_video(
        video=output_path,
        caption="✅ Video kamu sudah dipercepat 4x",
        thumb=thumb_path
    )

    # Hapus file sementara
    os.remove(input_path)
    os.remove(output_path)
    os.remove(thumb_path)

app.run()
