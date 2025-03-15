import discord
import datetime
import os
import codecs
from dotenv import load_dotenv
from utils.whisper import Whisper
from utils.deepseek import DeepSeek
from utils.converter import convert_to_html
from utils.language_detect import detect_main_language

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

connections = {}

if not os.path.exists("recordings"):
    os.makedirs("recordings")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def record(ctx):
    """Starts recording audio in a voice channel."""
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("⚠️ You aren't in a voice channel!")
        return

    if ctx.guild.id in connections and connections[ctx.guild.id].is_connected():
        await ctx.respond(
            "✅ Already connected to a voice channel. Starting recording..."
        )
        vc = connections[ctx.guild.id]
    else:
        vc = await voice.channel.connect()
        connections[ctx.guild.id] = vc

    vc.start_recording(
        discord.sinks.WaveSink(),
        once_done,
        ctx.channel,
    )
    await ctx.respond("🔴 Recording started. Use /stop_recording to save the audio.")


async def once_done(sink: discord.sinks.WaveSink, channel: discord.TextChannel, *args):
    """Processes the recorded audio and generates feedback."""
    await sink.vc.disconnect()

    for user_id, audio in sink.audio_data.items():
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/{user_id}_{timestamp}.wav"

            with open(filename, "wb") as f:
                f.write(audio.file.read())

            transcription = await Whisper(filename).run()
            print("📜 Transcription:\n", transcription)

            main_language = detect_main_language(transcription)

            feedback = await DeepSeek(transcription).run()

            feedback_html = convert_to_html(feedback, main_language)

            feedback_filename = f"recordings/{user_id}_{timestamp}_feedback.html"

            with codecs.open(
                feedback_filename, "w", encoding="utf-8-sig"
            ) as feedback_file:
                feedback_file.write(feedback_html)

            with open(feedback_filename, "rb") as file:
                await channel.send(
                    f"🎤 Feedback for <@{user_id}>:",
                    file=discord.File(file, "feedback.html"),
                )

        except Exception as e:
            await channel.send(f"❌ Error processing feedback: {e}")
            print(f"Error: {e}")

        finally:
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(feedback_filename):
                os.remove(feedback_filename)

    if sink.vc.guild.id in connections:
        del connections[sink.vc.guild.id]


@bot.command()
async def stop_recording(ctx):
    """Stops the recording."""
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        await ctx.respond("⏹️ Recording stopped. Saving audio...")
    else:
        await ctx.respond("🚫 No active recording in this server.")


bot.run(TOKEN)
