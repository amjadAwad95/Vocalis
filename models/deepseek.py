from openai import OpenAI
import os
import re
from dotenv import load_dotenv
from module.model import Model
from prompts.deepseek_prompt import DeepSeekArabicPrompt, DeepSeekEnglishPrompt

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")


class DeepSeek(Model):
    def __init__(self, transcription: str):
        self.transcription = transcription
        self.prompt = ""
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY
        )

    def __detect_language(self, transcription):
        arabic_chars = re.findall(r"[\u0600-\u06FF]", transcription)
        english_chars = re.findall(r"[a-zA-Z]", transcription)

        arabic_ratio = len(arabic_chars) / (len(arabic_chars) + len(english_chars) + 1)

        if arabic_ratio > 0.7:
            return "arabic"
        elif arabic_ratio < 0.3:
            return "english"
        else:
            return "mixed"

    async def run(self):
        language_style = self.__detect_language(self.transcription)
        arabic_prompt = DeepSeekArabicPrompt().generate(self.transcription)
        english_prompt = DeepSeekEnglishPrompt().generate(self.transcription)

        if language_style == "arabic":
            self.prompt = arabic_prompt

        elif language_style == "english":
            self.prompt = english_prompt

        else:
            self.prompt = arabic_prompt

        completion = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": self.prompt}],
            temperature=0.6,
            top_p=0.7,
            max_tokens=4096,
            stream=False,
        )

        response = completion.choices[0].message.content
        return response.split("</think>")[-1] if "</think>" in response else response
