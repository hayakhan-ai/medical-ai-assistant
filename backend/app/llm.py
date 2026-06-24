import os
from groq import Groq
from dotenv import load_dotenv
from typing import Any, cast

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GREETINGS = {
    "hi", "hello", "hey", "good morning", "good evening"
}

THANKS = {
    "thanks", "thank you", "thx", "ty"
}

GOODBYES = {
    "bye", "goodbye", "see you", "take care"
}

ACKNOWLEDGEMENTS = {
    "ok", "okay", "alright", "got it", "hmm"
}

FOLLOW_UP_KEYWORDS = [
    "which doctor",
    "which specialist",
    "doctor?",
    "specialist?",
    "name and location",
    "location",
    "country",
    "tests",
    "what should i do",
    "is it dangerous",
    "how urgent",
    "can i wait",
    "medicine",
    "treatment",
    "more options",
    "female doctor",
    "hospital",
    "doctor name",
    "which one",
    "what about that"
]


def classify_query(query: str, history=None):
    q = query.lower().strip()

    if q in GREETINGS:
        return "GREETING"

    if q in THANKS:
        return "THANKS"

    if q in GOODBYES:
        return "GOODBYE"

    if q in ACKNOWLEDGEMENTS:
        return "ACKNOWLEDGEMENT"

    # Very short questions after previous medical conversation
    if history and len(history) > 0:
        if len(q.split()) <= 8:
            for keyword in FOLLOW_UP_KEYWORDS:
                if keyword in q:
                    return "FOLLOW_UP"

    return "MEDICAL_QUERY"


def generate_response(query, context, history):

    medical_context = ""

    for item in context:

        entity_type = item.get("type", "")

        if entity_type == "treatment":

             medical_context += f"""
TYPE: Treatment

Name:
{item.get("name","")}

Description:
{item.get("description","")}

------------------------------------
"""

        elif entity_type == "doctor":

             medical_context += f"""
TYPE: Doctor

Name:
{item.get("name","")}

Specialities:
{item.get("speciality","")}

City:
{item.get("city","")} 

Address:
{item.get("address","")} 

Country:
{item.get("country","")}

About:
{item.get("about","")}

Phone:
{item.get("phone","")}

Qualifications:
{item.get("qualifications","")}

Experience:
{item.get("experience","")} years


------------------------------------
"""

        elif entity_type == "hospital":

             medical_context += f"""
TYPE: Hospital

Name:
{item.get("name","")}

City:
{item.get("city","")}

Address:
{item.get("address","")}

Phone:
{item.get("phone","")}

Open Time:
{item.get("open time","")}

Emergency Number:
{item.get("emergencyNo","")}

Email:
{item.get("email","")}

Country:
{item.get("country","")}

------------------------------------
"""

        elif entity_type == "laboratory":

             medical_context += f"""
TYPE: Laboratory

Name:
{item.get("name","")}

Description:
{item.get("description","")}

City:
{item.get("city","")}

Address:
{item.get("address","")}

Phone:
{item.get("phone","")}

Emergency Number:
{item.get("emergencyNo","")}

Open Time:
{item.get("open time","")}

Email:
{item.get("email","")}

------------------------------------
"""

        elif entity_type == "speciality":

             medical_context += f"""
TYPE: Speciality

Name:
{item.get("name","")}

------------------------------------
"""
        
        elif entity_type == "test":
          
             medical_context += f"""
TYPE: Test

Description:
{item.get('description','')}

Duration:
{item.get('duration','')}

Discount:
{item.get('discount','')} %

------------------------------------
"""

    messages = [
        {
            "role": "system",
            "content": """
You are a multilingual Medical AI Assistant.

Rules:

Use the supplied medical context and recent conversation history.
Reply entirely in the user's language and script.
Discuss possibilities, not diagnoses.
Ignore unrelated retrieved information.
Ask follow-up questions only when necessary.
Never invent doctor names, hospitals, phone numbers, addresses, prices, tests, or treatments.
You may use general medical knowledge to recommend the appropriate medical specialty.
If doctors, hospitals, laboratories, or tests are present in the supplied context, always mention them explicitly.
Never say information is unavailable when these entities are present.
Prioritize retrieved entities over general medical advice.
If no doctor, hospital, laboratory, or test is found in the context, recommend the appropriate specialty instead.
Never repeat or paraphrase the user's question as the answer.
Always answer the user's question before asking additional questions.
Use recent conversation history to infer follow-up questions such as:
Which doctor?
Which specialist?
Is it dangerous?
What should I do?
Which tests should I get?
Should I consult a doctor?
How urgent is this?
If exact information is unavailable, explain what is known and provide general guidance.
If symptoms suggest a potentially serious condition, advise seeking prompt medical evaluation.
Never claim certainty when the information is insufficient.
Never say "that information is unavailable" if general medical knowledge can answer the question safely.
Do not ask unnecessary questions after already providing an answer.
When a user asks a short follow-up question, interpret it in the context of previous symptoms and previous answers rather than treating it as an isolated question.

"""
        }
    ]

    # Previous conversation
    history = history[-4:]
    for msg in history:

        messages.append(
            {
                "role": "user",
                "content": msg["question"]
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": msg["answer"]
            }
        )

    # Current question
    messages.append({
             "role":"system",
             "content":f"""
             Medical Context (retrieved data):
                {medical_context}

                 User question:
                {query}
            """
             })

    messages.append(
         {
          "role":"user",
          "content":f"""
    Question: {query}
    """
}
)

    response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
           temperature=0.2,
           max_completion_tokens=500,
           messages=cast(Any, messages)
        )

    return (response.choices[0].message.content or "").strip()

def small_reply(user_message, instruction):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_completion_tokens=40,
        messages=[
        {
            "role":"system",
            "content":f"""
{instruction}

Reply in exactly the same language and script as the user.
Keep the response short.
"""
        },
        {
            "role":"user",
            "content":user_message
        }
        ]
    )

    return (
        response.choices[0].message.content or ""
    ).strip()

def generate_title(history):

    text = "\n".join(
        [f"User: {m['question']}\nAssistant: {m['answer']}"
         for m in history]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_completion_tokens=15,
        messages=[
            {
                "role":"system",
                "content":"""
Generate a very short chat title (3-6 words).

Examples:
Joint Pain Consultation
Kidney Stone Symptoms
Finding Female Gynecologist
Stomach Pain and Fever

Return only the title.
"""
            },
            {
                "role":"user",
                "content":text
            }
        ]
    )

    return (response.choices[0].message.content or "").strip()   