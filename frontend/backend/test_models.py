import asyncio
import httpx

from core.config import GROQ_API_KEY, GROQ_BASE_URL


async def main():
    url = f"{GROQ_BASE_URL.rstrip('/')}/models"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                url,
                headers=headers,
            )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR:")
            print(response.text)
            return

        data = response.json()

        print("\nAVAILABLE MODELS:\n")

        for model in data.get("data", []):
            print(model.get("id"))

    except Exception as error:
        print("ERROR TYPE:", type(error).__name__)
        print("ERROR:", str(error))


asyncio.run(main())