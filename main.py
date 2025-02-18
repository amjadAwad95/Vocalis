import discord
import datetime
import os
from dotenv import load_dotenv
from utils.whisper import extract_text_from_audio
from utils.deepseek import generate_feedback

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

connections = {}

if not os.path.exists("recordings"):
    os.makedirs("recordings")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def record(ctx):
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("⚠️ You aren't in a voice channel!")
        return

    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        discord.sinks.WaveSink(),
        once_done,
        ctx.channel,
    )
    await ctx.respond("🔴 Recording started. Use /stop_recording to save the audio.")


async def once_done(sink: discord.sinks.WaveSink, channel: discord.TextChannel, *args):
    await sink.vc.disconnect()

    for user_id, audio in sink.audio_data.items():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/{user_id}_{timestamp}.wav"

        with open(filename, "wb") as f:
            f.write(audio.file.read())

        transcription = await extract_text_from_audio(filename)
        print(transcription)
        feedback = await generate_feedback(transcription)

        # Save feedback as a .md file
        feedback_filename = f"recordings/{user_id}_{timestamp}_feedback.md"
        with open(feedback_filename, "w", encoding="utf-8") as feedback_file:
            feedback_file.write(feedback)  # Write the feedback content

        # Send the feedback file to the user
        with open(feedback_filename, "rb") as file:
            await channel.send(f"🎤 Feedback for <@{user_id}>:", file=discord.File(file, "feedback.md"))

        # Clean up files
        os.remove(filename)
        os.remove(feedback_filename)

    if sink.vc.guild.id in connections:
        del connections[sink.vc.guild.id]


@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        await ctx.respond("⏹️ Recording stopped. Saving audio...")
    else:
        await ctx.respond("🚫 No active recording in this server.")


bot.run(TOKEN)
