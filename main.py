import discord
import datetime
import os
import codecs  
import re  
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
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def record(ctx):
    """Starts recording audio in a voice channel."""
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("⚠️ You aren't in a voice channel!")
        return

    if ctx.guild.id in connections and connections[ctx.guild.id].is_connected():
        await ctx.respond("✅ Already connected to a voice channel. Starting recording...")
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

            transcription = await extract_text_from_audio(filename)
            print("📜 Transcription:\n", transcription)

            main_language = detect_main_language(transcription)

            feedback = await generate_feedback(transcription)

            feedback_html = convert_to_html(feedback, main_language)

            feedback_filename = f"recordings/{user_id}_{timestamp}_feedback.html"

            with codecs.open(feedback_filename, "w", encoding="utf-8-sig") as feedback_file:
                feedback_file.write(feedback_html)

            with open(feedback_filename, "rb") as file:
                await channel.send(f"🎤 Feedback for <@{user_id}>:", file=discord.File(file, "feedback.html"))

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

def detect_main_language(text):
    """Detects if the main language is Arabic or English based on character ratio."""
    arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
    english_chars = re.findall(r'[a-zA-Z]', text)

    arabic_ratio = len(arabic_chars) / (len(arabic_chars) + len(english_chars) + 1)

    return "ar" if arabic_ratio > 0.7 else "en"

def convert_to_html(feedback, main_language):
    """Converts feedback into structured HTML format with RTL or LTR direction."""
    
    dir_attr = "rtl" if main_language == "ar" else "ltr"
    lang_attr = "ar" if main_language == "ar" else "en"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="{lang_attr}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                direction: {dir_attr};
                text-align: {'right' if dir_attr == 'rtl' else 'left'};
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {feedback}
        </div>
    </body>
    </html>
    """

    return html_template

bot.run(TOKEN)