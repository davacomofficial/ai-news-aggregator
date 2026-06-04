from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_article(title):

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",

                    "content": """
                    You are an AI news summarizer.
                    Summarize headlines briefly in 2 short sentences.
                    """
                },

                {
                    "role": "user",

                    "content": title
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"AI Summary Error: {str(e)}"