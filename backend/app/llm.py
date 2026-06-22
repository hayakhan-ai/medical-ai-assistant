import os
from groq import Groq
from dotenv import load_dotenv
from typing import Any, cast

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


GREETINGS = {
    "hi","hello","hey","good morning",
    "good evening"
}

THANKS = {
    "thanks","thank you","ty","thnx"
}

GOODBYES = {
    "bye","goodbye","see ya","later"
}

ACKNOWLEDGEMENTS = {
    "ok","okay","alright","got it","hmm"
}

MEDICAL= {
"Diseases",
"Symptoms",
"Treatments",
"Doctors",
 "Hospitals",
 "Healthcare",
 "Diagnostics",
 "Medical specialities",
 "Tests"      
}

FOLLOW_UPS = {
    "yes","yeah","tell me more",
    "details","explain",
    "side effects","risks",
    "benefits","location","price",
    "recovery","duration",
    "treatment","doctor",
    "hospital","tests",
    "what about it",
    "what about this",
    "is it dangerous",
    "how much","tell me more"
}

NON_MEDICAL ={ "every thing unrelated to medical data"}
def classify_query(query):
    q = query.lower().strip()

    if q in GREETINGS:
        return "GREETING"

    if q in THANKS:
        return "THANKS"

    if q in GOODBYES:
        return "GOODBYE"

    if q in ACKNOWLEDGEMENTS:
        return "ACKNOWLEDGEMENT"
    
    if q in FOLLOW_UPS:
        return "FOLLOW_UP"
    
    if q in NON_MEDICAL:
        return "Non_Medical"


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

- Use supplied medical context and recent conversation.
- Never invent doctors, hospitals, tests, prices, phone numbers, or treatments.
- Reply entirely in the user's language and script, if their GREETINGS, GOODBYES, THANKS, ACKNOWLEDGEMENTS, FOLLOW_UPS in their language reply in that specific language.
- Discuss possibilities, not diagnoses.
- Ignore unrelated retrieved information.
- Ask follow-up questions when necessary.
- Recommend doctors, hospitals, tests, or laboratories only if present in the supplied context.
- If information is unavailable, clearly state that it is unavailable.

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
             Medical context:

              {medical_context}

             Only use information found above.
             Ignore irrelevant entries.
             Do not invent missing information.
             """
             })

    messages.append(
         {
          "role":"user",
          "content":query
}
)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        max_completion_tokens=400,
        messages=cast(Any, messages)
    )

    return (response.choices[0].message.content or "").strip()
