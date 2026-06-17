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
        model="llama-3.1-8b-instant",
        temperature=0,
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

Treatment:
{item.get("treatment","")}

Description:
{item.get("description","")}

------------------------------------
"""

        elif entity_type == "doctor":

             medical_context += f"""
TYPE: Doctor

Name:
{item.get("name","")}

Qualifications:
{item.get("qualifications","")}

Specialities:
{item.get("speciality","")}

Experience:
{item.get("experience","")} years

Location:
{item.get("city","")}

About:
{item.get("about","")}

------------------------------------
"""

        elif entity_type == "hospital":

             medical_context += f"""
TYPE: Hospital

Name:
{item.get("name","")}

City:
{item.get("city","")}

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
{item.get("phoneNumber","")}

------------------------------------
"""

        elif entity_type == "speciality":

             medical_context += f"""
TYPE: Speciality

Name:
{item.get("speciality","")}

------------------------------------
"""
        
        elif entity_type == "test":
          
             medical_context += f"""
TYPE: Test

Name:
{item.get('name','')}

Category:
{item.get('category','')}

Speciality:
{item.get('speciality','')}

City:
{item.get('city','')}

Description:
{item.get('description','')}

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
You are a Medical AI Assistant.

Rules:

1. Use the supplied medical context and previous conversation history.
2. Do not invent doctors, hospitals, laboratories or treatments.
3. If the context contains doctor information, recommend those doctors.
4. If the context contains hospitals, mention their names and locations.
5. If the context contains laboratories, provide lab information.
6. Responses are informational and not a diagnosis.
7. Continue the conversation naturally.
8. Responses are informational and not a diagnosis.
9. Continue the conversation naturally.
10. Understand follow-up questions like:
   - What are its benefits?
   - What about side effects?
   - How much does it cost?
11. If current context is empty, use previous conversation history.
12. Respond in the same language as the user.
   - English → English
   - Urdu or Roman Urdu → Urdu
   - Arabic → Arabic
   - Turkish → Turkish
   Maintain a natural and friendly tone.
13. If the user describes only symptoms, do not assume a specific disease. Suggest broad possibilities and ask follow-up questions before narrowing down
14. When the user says "okay", "thank you", "bye", "good night", or similar expressions, respond naturally like a helpful assistant instead of treating them as new medical queries.
15. If the user describes only symptoms, do not assume a specific disease.
Suggest broad possibilities and ask follow-up questions before narrowing down.

16. Do not treat retrieved conditions as confirmed diagnoses.

17. Avoid rare or severe diseases unless symptoms strongly suggest them. Prefer common conditions first.

18. Mention hospitals only if the user explicitly asks for one.

19. Do not recommend famous doctors, hospitals, or organizations unless they are present in the supplied context.

20. Avoid rare or severe diseases unless symptoms strongly suggest them.
Prefer common conditions first.

Answer format:

Recommended Specialist:
...

Possible Condition:
...

General Advice:
...
"""
        }
    ]

    # Previous conversation
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
            "role": "user",
            "content": f"""
Medical Context:

{medical_context}

Current User Question:

{query}
"""
        }
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=cast(Any, messages)
    )

    return (response.choices[0].message.content or "").strip()

def generate_chat_title(message: str):

    prompt = f"""
Generate a very short chat title.

Examples:

User: I have fever for three days
Title: Fever for Three Days

User: Best treatment for kidney stones
Title: Kidney Stone Treatment

User: Diabetes symptoms
Title: Diabetes Symptoms

Message:
{message}

Return ONLY the title.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (response.choices[0].message.content or "").strip()