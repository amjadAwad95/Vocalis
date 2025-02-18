from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = API_KEY
)

async def generate_feedback(transcription) :
    
    prompt = f"""
    You are an AI presentation coach analyzing a user's speech. Below is the transcription of their presentation. Provide a detailed, structured evaluation focusing on:

    1. **Content and Structure**: Is the presentation well-organized, with a clear introduction, body, and conclusion? Are key points easy to follow?
    2. **Clarity and Message**: How clear and concise is the delivery? Are the main ideas effectively communicated?
    3. **Filler Words and Fluency**: Note any overuse of filler words ("um," "like," "you know") and assess fluency.

    Provide specific, actionable feedback with examples, highlighting both strengths and areas for improvement. Avoid generic comments and suggest concrete ways to enhance their presentation skills.

    **Important Notes**:
    - The feedback should be in the same language as the transcript. If the transcript is mainly Arabic with some English words, the feedback should also be mainly Arabic with the same English words included.
    - Use the same tone and style as the transcript (e.g., if the transcript is informal, keep the feedback informal).

    Transcript: {transcription}

    Feedback:
    """
        
    
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1",
        messages=[{"role":"user","content":prompt}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=False
        )
    
    print(prompt)
    
    response = completion.choices[0].message.content
    
    if "</think>" in response :
        return response.split("</think>")[-1]
    else : return response
    




