
# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# client = Groq(api_key=GROQ_API_KEY)


# def is_medical_query(query: str) -> bool:
#     """
#     Returns True if the question is medical/healthcare related.
#     """

#     prompt = f"""
# You are a medical query classifier.

# Classify the user's question as either:

# MEDICAL:
# - Diseases
# - Symptoms
# - Treatments
# - Medicines
# - Doctors
# - Healthcare
# - Medical specialties
# - Hospitals
# - Diagnostics
# - Mental health

# NON_MEDICAL:
# - Programming
# - Sports
# - Politics
# - Entertainment
# - General knowledge
# - Mathematics
# - History
# - Finance
# - Any topic unrelated to healthcare

# User Question:
# {query}

# Reply with ONLY one word:

# MEDICAL

# or

# NON_MEDICAL
# """

#     chat = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         temperature=0,
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     result = chat.choices[0].message.content.strip().upper()

#     return result == "MEDICAL"


# def generate_response(query, context):
#     """
#     Generate a medical response using only retrieved context.
#     """

#     if not context:
#         return (
#             "I could not find sufficient medical information in my dataset "
#             "to answer this question."
#         )

#     prompt = f"""
# You are a medical AI assistant.

# Use ONLY the medical context provided below.

# MEDICAL CONTEXT:
# {context}

# USER QUESTION:
# {query}

# IMPORTANT RULES:
# 1. Answer ONLY using the provided context.
# 2. Do NOT make up diseases, treatments, or diagnoses.
# 3. If the context is insufficient, say:
#    "I could not find sufficient medical information in my dataset."
# 4. Do not answer non-medical questions.
# 5. Remind the user that this is informational and not a medical diagnosis.

# Provide:
# - Recommended specialist
# - Possible condition
# - General advice
# """

#     chat = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a medical assistant. "
#                     "Use only the provided medical context."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return chat.choices[0].message.content.strip()

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def classify_query(query: str) -> str:
    """
    Returns one of:
    - GREETING
    - MEDICAL
    - NON_MEDICAL
    """

    prompt = f"""
You are a query classifier.

Classify the user message into exactly ONE category.

GREETING:
- hi
- hello
- hey
- good morning
- good afternoon
- good evening
- salam
- assalamualaikum
- aoa
- how are you
- greetings

MEDICAL:
- Diseases
- Symptoms
- Treatments
- Medicines
- Doctors
- Healthcare
- Medical specialties
- Hospitals
- Diagnostics
- Mental health
- Medical advice
- Health concerns

NON_MEDICAL:
- Programming
- Sports
- Politics
- Entertainment
- Mathematics
- History
- Finance
- General knowledge
- Any topic unrelated to healthcare

User Message:
{query}

Reply with ONLY one word:

GREETING
MEDICAL
NON_MEDICAL
"""

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return chat.choices[0].message.content.strip().upper()


def generate_response(query, context):
    """
    Generate a medical response using retrieved context.
    """

    if not context:
        return (
            "I could not find sufficient medical information in my dataset "
            "to answer this question."
        )

    prompt = f"""
You are a Medical AI Assistant.

Use ONLY the medical context provided below.

Medical Context:
{context}

User Question:
{query}

Rules:
1. Answer only medical questions.
2. Use only the provided context.
3. Do not invent diagnoses, diseases, medicines, or treatments.
4. If the context is insufficient, respond:
   "I could not find sufficient medical information in my dataset."
5. Do not answer non-medical questions.
6. Mention that the response is informational and not a medical diagnosis.

Provide your answer in this format:

Recommended Specialist:
...

Possible Condition:
...

General Advice:
...

Disclaimer:
This information is for educational purposes only and is not a medical diagnosis.
"""

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical assistant. "
                    "Use only the provided medical context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return chat.choices[0].message.content.strip()