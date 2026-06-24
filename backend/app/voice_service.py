from app.speech_to_text import speech_to_text
from app.tts import text_to_speech

from app.llm import (
    generate_response,
    classify_query,
    small_reply
)

from app.rag import search_medical_data


async def voice_chat(audio_path, history):

    stt_result = speech_to_text(audio_path)

    query = stt_result["text"]

    language = stt_result["language"]

    history_context = ""

    for msg in history:

        history_context += f"""
User: {msg["question"]}
Assistant: {msg["answer"]}
"""

    search_query = history_context + "\nUser: " + query

    context = search_medical_data(
        search_query,
        limit=3
    )

    query_type = classify_query(query)

    if query_type in [
        "GREETINGS",
        "THANKS",
        "GOODBYES",
        "ACKNOWLEDGEMENTS"
    ]:

        answer = small_reply(
            query,
            """
Respond naturally and briefly.
Reply in the user's language.
"""
        )

    else:

        answer = generate_response(
            query,
            context,
            history
        )

    audio_file = await text_to_speech(
        answer,
        language
    )

    return {
        "query": query,
        "language": language,
        "response": answer,
        "audio_file": audio_file
    }