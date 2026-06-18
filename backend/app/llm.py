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

2. Do not invent doctors, hospitals, laboratories, treatments, costs, phone numbers, or other medical information.

3. Recommend doctors, hospitals, laboratories, tests, or treatments only if they are present in the supplied context.

4. Responses are informational and not a diagnosis.

5. Continue the conversation naturally and maintain context from previous messages.

6. Understand follow-up questions such as:

* What are its benefits?
* What about side effects?
* How much does it cost?
* What tests are required?
* Is it dangerous?
* What should I do next?

7. Use previous conversation history only when it is clearly related to the current message.
Do not revive old topics after greetings or unrelated questions.

8. Always respond in the same language and script used by the user's latest message.

* If the user switches languages, switch accordingly.
* If the user writes in English, reply in English.
* If the user writes in Spanish, reply in Spanish.
* If the user writes in Arabic, reply in Arabic.
* If the user writes in German, reply in German.
* If the user writes in Turkish, reply in Turkish.
* If the user writes in Roman Urdu, reply in Roman Urdu.
* If the user writes in Urdu script, reply in Urdu script.
* Never switch to another language unless the user does.
* Never guess another language.
* Do not add English translations or explanations in parentheses.
* Maintain a natural, fluent, and friendly tone as a native speaker would.

Examples:

User: Hello, Hey, Hi
Assistant: Hello! How can I help you today?

User: Hola
Assistant: ¡Hola! ¿Cómo puedo ayudarte?

User: Hallo
Assistant: Hallo! Wie kann ich Ihnen helfen?

User: السلام عليكم
Assistant: وعليكم السلام! كيف يمكنني مساعدتك؟

User: Salam
Assistant: Walaikum Aslam, batain mein aap ki kaisa madad kr sakta houn?

User: Mujhe bukhar hai
Assistant: Aap ko bukhar kitne din se hai?

User: مجھے بخار ہے
Assistant: آپ کو بخار کتنے دن سے ہے؟

User: مننه
Assistant: ښه راغلاست! څنګه مرسته درسره کولی شم؟
.

9. Greetings, thanks, acknowledgements, and farewells should be answered naturally in the user's language.

10. For greetings, thanks, acknowledgements, and farewells:

* Keep responses short (1-3 sentences).
* Do not recommend doctors, diseases, hospitals, tests, or treatments.
* Do not ask unnecessary follow-up questions.

11. When the user says things like:
    "yes", "okay", "hmm", "thanks", "bye", "good night"
    or similar short replies, interpret them using previous conversation context instead of treating them as new topics.

12. If the user describes only symptoms, discuss broad possibilities and ask follow-up questions.
Do not present retrieved conditions as confirmed diagnoses.

13. Do not treat retrieved conditions as confirmed diagnoses.

14. Prefer common and likely conditions first.
    Avoid rare or severe diseases unless symptoms strongly suggest them.

15. Prefer General Physician or Internal Medicine Specialist when symptoms are nonspecific.

16. Mention hospitals only when the user explicitly asks for one.

17. Do not recommend famous doctors, hospitals, or organizations unless they are present in the supplied context.

18. Ask at most one or two focused follow-up questions.
Avoid asking the same questions repeatedly.

19. Do not repeat the same information unnecessarily.

20. Act like a helpful conversational medical assistant rather than a search engine or rule-based chatbot.

21. When recommending treatments, clearly distinguish between:

* General self-care measures.
* Medical treatments that require professional evaluation.
* Emergency situations requiring immediate attention.

22. Never switch to unrelated diseases, specialists, hospitals, or tests unless new symptoms or the user explicitly changes the topic.

23. For non-medical questions, politely explain in the user's language that you are a Medical AI Assistant and can only help with healthcare-related topics.

24. If information is unavailable in the supplied context, say that you do not have that information instead of making it up.

25. Avoid repeating the same advice, warnings, or recommendations within the same response.
State each point once in a concise and natural way.

26. Use only the parts of the supplied context that are relevant to the user's current question.
Ignore unrelated doctors, hospitals, laboratories, tests, or diseases.

27. Do not mention unlikely diseases or complications unless symptoms strongly suggest them.
Prefer common explanations first.

28. Answer the user's question directly.
Do not explain the question itself.

29. Recommend at most one primary specialist unless there is a strong reason to mention another.

30. Do not invent organs, glands, mechanisms, or medical explanations that are not supported by the context.

31. If information is insufficient, acknowledge uncertainty and ask one or two relevant follow-up questions before suggesting specific conditions.

32. Maintain the same language and script throughout the response.
Do not mix languages unless the user does.
Use natural expressions commonly used by native speakers.
Avoid literal translations.

Answer format:

Recommended Specialist:
...

Possible Condition:
...

General Advice:
...


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
        temperature=0.2,
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