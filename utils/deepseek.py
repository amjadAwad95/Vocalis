from openai import OpenAI
import os 
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY
)

def detect_language(transcription):
    arabic_chars = re.findall(r'[\u0600-\u06FF]', transcription)
    english_chars = re.findall(r'[a-zA-Z]', transcription)

    arabic_ratio = len(arabic_chars) / (len(arabic_chars) + len(english_chars) + 1)

    if arabic_ratio > 0.7:
        return "arabic"
    elif arabic_ratio < 0.3:
        return "english"
    else:
        return "mixed"

async def generate_feedback(transcription):
    language_style = detect_language(transcription)
    
    if language_style == "arabic":
        prompt = f"""
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

        **🔹 النص المقدم:**
        {transcription}
        """
    
    elif language_style == "english":
        prompt = f"""
        You are a professional presentation coach. Provide a detailed evaluation using structured , including H1, H2 headings, and bullet points about of transcription:
        
        <h1>📝 Feedback</h1>
        <h2>🔹 Detailed Evaluation of the Presentation</h2>
        
        <h3>1️⃣ Content and Structure</h3>
        <ul>
          <li><strong>Was the presentation well-organized?</strong> Provide observations on structure.</li>
          <li><strong>Was the information delivered in a clear, logical sequence?</strong> Suggest improvements if needed.</li>
        </ul>
        
        <h3>2️⃣ Clarity and Message</h3>
        <ul>
          <li><strong>Were the main ideas easy to follow?</strong> Offer insights into clarity.</li>
          <li><strong>Were technical terms (المصطلحات التقنية) used effectively?</strong> Highlight appropriate or excessive use.</li>
        </ul>
        
        <h3>3️⃣ Fluency and Filler Words</h3>
        <ul>
          <li><strong>Was there excessive use of filler words like "um" or "you know"?</strong> Note any improvements needed.</li>
          <li><strong>Were pauses and emphasis used effectively?</strong> Give suggestions for better delivery.</li>
        </ul>
        
        <h2>🎯 Strengths</h2>
        <ul>
          <li>Mention what worked well in the presentation.</li>
        </ul>
        
        <h2>⚡ Areas for Improvement</h2>
        <ul>
          <li>Highlight areas that need refinement.</li>
          <li>Provide practical recommendations for improvement.</li>
        </ul>
        
        <h2>📌 Final Recommendation</h2>
        <p>Summarize the overall assessment and key takeaways for the presenter.</p>
        **🔹 Submitted Transcript:**
        {transcription}
        ---
        """
    else:  
        prompt = f"""
        انت مدرب عروض تقديمية محترف. قم بتحليل النص التالي الذي يحتوي على مزيج من اللغتين العربية والإنجليزية، وقدم تقييمًا متوازنًا. حافظ على نفس أسلوب اللغة الموجود في النص الأصلي:

        1️⃣ **المحتوى والهيكلة (Content and Structure):**
        - هل كان العرض منظمًا بشكل جيد؟ (Was the content structured logically?)
        - هل تم تقديم المعلومات بوضوح؟ (Was the information clear and well-delivered?)

        2️⃣ **وضوح الرسالة (Clarity and Message):**
        - هل كانت الأفكار واضحة؟ (Were the main ideas easy to follow?)
        - هل تم استخدام المصطلحات المناسبة؟ (Was terminology used correctly?)

        3️⃣ **الطلاقة والكلمات الفارغة (Fluency and Filler Words):**
        - هل كان هناك تكرار مفرط لكلمات مثل "يعني"؟ (Was there excessive use of filler words?)
        - هل كان الأسلوب سلسًا؟ (Was the speech fluent?)

        4️⃣ **نقاط القوة ونقاط التحسين (Strengths and Areas for Improvement):**
        - ما الجوانب الإيجابية في العرض؟ (What strengths stood out in the presentation?)
        - ما الجوانب التي يمكن تحسينها؟ (What areas need improvement?)

        ---
        **🔹 النص المقدم (Transcript):**
        {transcription}
        ---
        """
    
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=False
    )

    response = completion.choices[0].message.content
    print(response)
    return response.split("</think>")[-1] if "</think>" in response else response
