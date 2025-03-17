import discord
import datetime
import os
import codecs
from dotenv import load_dotenv
from models.gemini import Gemini  # Replace Whisper with Gemini

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
        feedback_file_path = None  # Initialize feedback_file_path
        filename = None  # Initialize filename

        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/{user_id}_{timestamp}.wav"

            # Save the recorded audio to a file
            with open(filename, "wb") as f:
                f.write(audio.file.read())

            # Define the prompt for Gemini
            prompt = """
        أنت مدرب عروض تقديمية محترف. قدم تقييمًا مفصلاً بناءً على المعايير التاليةوبناءا على (transcription)، واستخدم تنسيق واضحًا مع عناوين H1 و H2 وقوائم مرتبة وغير مرتبة:
        
        <h1>📝 التقييم (Feedback)</h1>
        <h2>🔹 التقييم التفصيلي للعرض التقديمي</h2>
        
        <h3>1️⃣ المحتوى والهيكلة (Content and Structure)</h3>
        <ul>
            <li><strong>هل كان العرض منظمًا بشكل جيد؟</strong> اذكر ملاحظاتك حول الترتيب والتسلسل.</li>
            <li><strong>هل تم تقديم المعلومات بوضوح وتسلسل منطقي؟</strong> وضح إذا كانت هناك حاجة لإعادة ترتيب المحتوى.</li>
        </ul>
        
        <h3>2️⃣ وضوح الرسالة (Clarity and Message)</h3>
        <ul>
            <li><strong>هل كانت الأفكار واضحة وسهلة الفهم؟</strong> أضف أمثلة إذا لزم الأمر.</li>
            <li><strong>هل كانت المصطلحات التقنية (technical terms) مناسبة؟</strong> قم بالإشارة إلى استخدام المصطلحات التقنية بشكل فعال.</li>
        </ul>
        
        <h3>3️⃣ الطلاقة والكلمات الفارغة (Fluency and Filler Words)</h3>
        <ul>
            <li><strong>هل كان هناك تكرار لكلمات مثل "يعني" أو "آه"؟</strong> قدم ملاحظات حول استخدام الكلمات الفارغة.</li>
            <li><strong>هل كان هناك استخدام جيد للتوقفات والتأكيد؟</strong> اذكر كيف يمكن تحسين الإلقاء.</li>
        </ul>
        
        <h2>🎯 نقاط القوة (Strengths)</h2>
        <ul>
            <li>اذكر ما تم القيام به بشكل جيد.</li>
        </ul>
        
        <h2>⚡ نقاط التحسين (Areas for Improvement)</h2>
        <ul>
            <li>حدد المجالات التي يمكن تحسينها.</li>
            <li>اقترح توصيات عملية لتحسين الأداء.</li>
        </ul>
        
        <h2>📌 التوصية النهائية</h2>
        <p>قدم ملخصًا عامًا حول العرض التقديمي والتوصيات لتحسينه.</p>
        """

            # Generate feedback using Gemini
            feedback_text = await Gemini(filename,api_key=os.getenv("GOOGLE_API_KEY"),model='gemini-2.0-flash',prompt=prompt).run()
            print("📜 Feedback:\n", feedback_text)

            # Save feedback to an HTML file
            feedback_file_path = f"recordings/{user_id}_{timestamp}_feedback.html"
            with codecs.open(feedback_file_path, "w", encoding="utf-8-sig") as feedback_file:
                feedback_file.write(feedback_text)

            # Send the feedback file to the channel
            with open(feedback_file_path, "rb") as file:
                await channel.send(
                    f"🎤 Feedback for <@{user_id}>:",
                    file=discord.File(file, "feedback.html"),
                )

        except Exception as e:
            await channel.send(f"❌ Error processing feedback: {e}")
            print(f"Error: {e}")

        finally:
            # Clean up files
            if filename and os.path.exists(filename):
                os.remove(filename)
            if feedback_file_path and os.path.exists(feedback_file_path):
                os.remove(feedback_file_path)

    # Remove the connection from the dictionary
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
