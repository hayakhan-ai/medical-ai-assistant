import edge_tts
import uuid
import asyncio


async def get_voice(language):

    voices = await edge_tts.list_voices()

    for voice in voices:

        locale = voice["Locale"][:2].lower()

        if locale == language.lower():
            return voice["ShortName"]

    return "en-US-AriaNeural"


async def text_to_speech(text, language):

    voice = await get_voice(language)

    filename = f"{uuid.uuid4()}.mp3"

    filepath = f"audio/{filename}"

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await communicate.save(filepath)

    return filename