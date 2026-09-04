import asyncio

from ai.provider import generate_reply, ProviderError
from core.config import GROQ_MODEL


async def main():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Reply briefly.",
        },
        {
            "role": "user",
            "content": "Say hello to HerVoice.",
        },
    ]

    try:
        reply = await generate_reply(messages)

        print("\nSUCCESS!")
        print("MODEL:", GROQ_MODEL)
        print("REPLY:", reply)

    except ProviderError as error:
        print("\nGROQ ERROR")
        print("TYPE:", error.error_type)
        print("MESSAGE:", error.message)

    except Exception as error:
        print("\nUNEXPECTED ERROR")
        print("TYPE:", type(error).__name__)
        print("MESSAGE:", str(error))


asyncio.run(main())
