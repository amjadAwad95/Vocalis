import discord
import datetime
import os
import codecs
import json
from dotenv import load_dotenv
from models.gemini import Gemini
from prompts.gemini_prompt import GeminiPrompt
from utils.html_structure import html_structure

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
        feedback_file_path = None
        filename = None

        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/{user_id}_{timestamp}.wav"

            with open(filename, "wb") as f:
                f.write(audio.file.read())

            prompt = GeminiPrompt().generate()

            feedback_text = await Gemini(
                filename,
                api_key=os.getenv("GOOGLE_API_KEY"),
                model="gemini-2.0-flash",
                prompt=prompt,
            ).run()
            json_text = feedback_text.replace("```json\n", "").replace("```", "")
            json_object = json.loads(json_text)
            feedback_text = html_structure(json_object)
            print("📜 Feedback Done")

            feedback_file_path = f"recordings/{user_id}_{timestamp}_feedback.html"
            with codecs.open(
                feedback_file_path, "w", encoding="utf-8-sig"
            ) as feedback_file:
                feedback_file.write(feedback_text)

            with open(feedback_file_path, "rb") as file:
                await channel.send(
                    f"🎤 Feedback for <@{user_id}>:",
                    file=discord.File(file, "feedback.html"),
                )

        except Exception as e:
            await channel.send(f"❌ Error processing feedback: {e}")
            print(f"Error: {e}")

        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)
            if feedback_file_path and os.path.exists(feedback_file_path):
                os.remove(feedback_file_path)

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
