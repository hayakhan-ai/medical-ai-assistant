import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_query(query: str) -> str:
    prompt = f"""
You are a query classifier.

Classify the user message into exactly ONE category.

GREETING:
- hi
- hello
- hey
- good morning
- good evening
- salam
- assalamualaikum
- aoa
- how are you

MEDICAL:
- Diseases
- Symptoms
- Treatments
- Medicines
- Doctors
- Hospitals
- Healthcare
- Diagnostics
- Medical specialties

NON_MEDICAL:
Everything unrelated to healthcare.

User Message:
{query}

Reply with ONLY one word:

GREETING
MEDICAL
NON_MEDICAL
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (response.choices[0].message.content or "").strip().upper()




def generate_response(query, context):
    """
    context = list returned from search_medical_data()
    """

    print("\nCONTEXT RECEIVED:")
    print(context)

    if not context:
        return "I could not find sufficient medical information in my dataset."

    medical_context = ""

    for item in context:
        medical_context += f"""
Treatment: {item.get('treatment', '')}

Category: {item.get('category', '')}

Description:
{item.get('description', '')}

------------------------------------
"""

    print("\nMEDICAL CONTEXT:")
    print(medical_context)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
You are a Medical AI Assistant.

Rules:
1. Use ONLY the supplied medical context.
2. Do not invent diseases or treatments.
3. If information is insufficient, say:
'I could not find sufficient medical information in my dataset.'
4. Mention that the response is informational and not a diagnosis.

Answer format:

Recommended Specialist:
...

Possible Condition:
...

General Advice:
...

"""
            },
            {
                "role": "user",
                "content": f"""
Medical Context:

{medical_context}

User Question:

{query}
"""
            }
        ]
    )

    answer = response.choices[0].message.content or ""

    print("\nLLM RESPONSE:")
    print(answer)

    return answer.strip()
