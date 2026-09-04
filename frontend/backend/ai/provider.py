import httpx

from core.config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_MODEL,
    provider_configured,
)


class ProviderError(Exception):
    def __init__(
        self,
        error_type: str,
        message: str,
    ):
        self.error_type = error_type
        self.message = message
        super().__init__(message)


async def generate_reply(
    messages: list[dict],
) -> str:

    if not provider_configured():
        raise ProviderError(
            "configuration",
            "AI provider is not configured.",
        )

    url = f"{GROQ_BASE_URL.rstrip('/')}/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.65,
        "max_tokens": 700,
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=45.0,
        write=10.0,
        pool=10.0,
    )

    try:
        async with httpx.AsyncClient(
            timeout=timeout
        ) as client:

            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )

    except httpx.ConnectError as exc:
        raise ProviderError(
            "connection",
            "Could not connect to the AI provider.",
        ) from exc

    except httpx.TimeoutException as exc:
        raise ProviderError(
            "timeout",
            "The AI provider took too long to respond.",
        ) from exc

    except httpx.RequestError as exc:
        raise ProviderError(
            "connection",
            "The AI provider request failed.",
        ) from exc

    if response.status_code == 401:
        raise ProviderError(
            "authentication",
            "The AI provider rejected the API key.",
        )

    if response.status_code == 429:
        raise ProviderError(
            "rate_limit",
            "The AI provider rate limit was reached.",
        )

    if response.status_code == 404:
        raise ProviderError(
            "model_not_found",
            "The configured AI model was not found.",
        )

    if response.status_code >= 500:
        raise ProviderError(
            "provider",
            "The AI provider is temporarily unavailable.",
        )

    if response.status_code >= 400:
        raise ProviderError(
            "provider_request",
            "The AI provider rejected the request.",
        )

    try:
        data = response.json()

        reply = data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ProviderError(
            "invalid_response",
            "The AI provider returned an unexpected response.",
        ) from exc

    if not isinstance(reply, str) or not reply.strip():
        raise ProviderError(
            "empty_response",
            "The AI provider returned an empty response.",
        )

    return reply.strip()