from model.prompt import Prompt


class DeepSeekArabicPrompt(Prompt):
    def generate(self, text: str) -> str:
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
        {text}
        """

        return prompt


class DeepSeekEnglishPrompt(Prompt):
    def generate(self, text: str) -> str:
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
        {text}
        ---
        """

        return prompt
