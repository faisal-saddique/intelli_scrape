import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_chat_model = os.getenv("OPENAI_CHAT_MODEL")
openai_completion_model = os.getenv("OPENAI_COMPLETION_MODEL")
use_gpt4 = os.getenv("GPT_4_COMPLETION").lower() == "true"


def gpt_completion(prompt: str, max_tokens=1350, temperature=0):

    if use_gpt4:

        response = openai.ChatCompletion.create(
            model=openai_chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who works similarly to the GPT completion model. Just complete the content written by the user and stop. Don't write extra."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    else:

        response = openai.Completion.create(
            model=openai_completion_model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].text.strip()
