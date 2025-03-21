from google import genai
from module.model import Model
from google.genai import types


class Gemini(Model):
    def __init__(self, audio_path, api_key, model, prompt):
        self.audio_path = audio_path
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.prompt = prompt

    async def run(self):
        myfile = self.client.files.upload(file=self.audio_path)
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=[self.prompt, myfile],
            config=generate_content_config,
        )

        return response.text
