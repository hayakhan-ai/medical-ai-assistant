import os
from groq import Groq
from dotenv import load_dotenv
from typing import Any, cast

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
- hey there
- hii
- hlo
- yo
- sup
- wassup
- what's up
- whassup
- howdy
- good morning
- good afternoon
- good evening
- good night
- salam
- assalamualaikum
- assalamu alaikum
- aoa
- aslam o alaikum
- how are you
- how are u
- how's it going
- how r u


THANKS:
- thanks
- thank you
- thx
- appreciated
- shukriya
- jazakallah
- thanks a lot
- many thanks
- no thanks
- ty


GOODBYE:
- bye
- goodbye
- see you
- take care
- allah hafiz
- khuda hafiz
- catch you later
- see you later
- okay bye


ACKNOWLEDGEMENT:
- okay
- ok
- alright
- fine
- understood
- got it
- i see
- interesting
- hmm
- hmmm
- acha
- theek
- theek hai
- jee
- ji


FOLLOW_UP:
# Basic confirmations
- yes
- yeah
- yep
- yup
- sure
- please
- continue
- go on
- carry on
- proceed

# More information
- tell me more
- more
- more details
- details
- explain
- elaborate
- expand
- describe
- further
- next

# Risks and side effects
- risks
- risk
- side effects
- complications
- drawbacks
- disadvantages
- danger
- harmful effects
- what are the risks
- what are the side effects

# Benefits
- benefits
- advantages
- pros
- positive effects
- how does it help
- why is it done

# Cost
- cost
- price
- charges
- expenses
- how much
- how much does it cost

# Recovery
- recovery
- healing
- recovery time
- duration
- when will i recover

# Medicines
- medicines
- medication
- drugs
- tablets
- which medicine

# Causes and symptoms
- causes
- symptoms
- signs
- reasons
- why does it happen

# Diagnosis and tests
- tests
- diagnosis
- investigations
- lab tests
- which test

# Treatment
- treatment
- therapy
- procedure
- operation
- surgery

# Doctors and hospitals
- doctor
- specialist
- hospital
- laboratory
- lab

# Pronoun follow-ups
- what about it
- what about this
- what about that
- what are its benefits
- what are its risks
- what are the complications
- is it dangerous
- is it safe
- can it be cured
- can it spread
- can it come back
- how is it treated
- what should i do
- what happens next

# Urdu
- haan
- han
- acha
- aur batao
- mazeed
- mazeed bataen
- phir
- agay
- continue karo
- aur
- aur kya
- kya faide hain
- kya nuqsanat hain
- kya side effects hain


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
- Tests
- Laboratory tests
- Fever
- Pain
- Infection
- Surgery
- Medication

IGNORE_FOR_TITLE = (
    "GREETING",
    "THANKS",
    "GOODBYE",
    "ACKNOWLEDGEMENT",
    "FOLLOW_UP"
)


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
        temperature=0.1,
        messages=cast(Any, [
            {
                "role": "user",
                "content": prompt
            }
        ])
    )

    return (response.choices[0].message.content or "").strip().upper()


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
{item.get("location","")} city

Address:
{item.get("location","")} address

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

Emergency Number:
{item.get("emergencyNo","")}

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

Phone:
{item.get("phone","")}

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
{item.get('testDescription','')}

Duration:
{item.get('duration','')}

Price:
{item.get('price','')}

------------------------------------
"""

    messages = [
        {
            "role": "system",
            "content": """

You are a multiligual Medical AI Assistant.

Rules:

1. Use supplied context and recent history.
2. Never invent doctors, hospitals, tests, costs, or treatments.
3. Reply entirely in the user's language and script.
4. Translate headings and section titles.
5. Discuss possibilities, not diagnoses.
6. Ask 1-2 follow-up questions when needed.
7. If doctor entries exist in context and the user asks for a doctor,
recommend them.If hospital entries exist and the user asks for hospitals,
recommend them.
8. Ignore unrelated retrieved information.
9. Avoid repetition.
10. If information is unavailable, say so rather than guessing.

"""
        }
    ]

    # Previous conversation
    history = history[-5:]
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
    messages.append(
         {
           "role":"system",
           "content":f"""
Relevant medical context:

{medical_context}

Use only the relevant parts.
Ignore unrelated information.
Do not mention information absent from the context.
"""
}
)

    messages.append(
         {
          "role":"user",
          "content":query
}
)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        messages=cast(Any, messages)
    )

    return (response.choices[0].message.content or "").strip()

def generate_chat_title(text: str):

    prompt = f"""
Generate a short chat title (3-6 words).

Ignore IGNORE_FOR_TITLE.

Conversation:

{text}

Return ONLY the title.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (response.choices[0].message.content or "").strip()