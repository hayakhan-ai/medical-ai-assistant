import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = Groq(api_key=GROQ_API_KEY)

def generate_response(query, context):
    prompt = f'''
    User symptoms: {query}

    Relevant medical context:
    {context}

    Suggest:
    1. Which doctor to consult
    2. Possible issue
    3. General advice
    '''

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return chat.choices[0].message.content