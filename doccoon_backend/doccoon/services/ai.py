from typing import Optional

from django.conf import settings
from google import genai
from openai import OpenAI

from doccoon.models.user import User

GEMINI_MODELS = {
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
}

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


def _get_active_key(user: Optional[User]) -> tuple[str, str, str]:
    """Return (api_key, provider, model) for the user's active key."""
    if user:
        from doccoon.models.ai_provider_key import AIProviderKey

        user_key = (
            AIProviderKey.objects.filter(user=user, is_active=True, is_deleted=False)
            .order_by("-created_at")
            .first()
        )
        if user_key:
            decrypted_key = user_key.get_api_key()
            if decrypted_key:
                return decrypted_key, user_key.provider, user_key.model

    # Fall back to server's Gemini key
    server_key = getattr(settings, "GEMINI_API_KEY", "")
    if server_key:
        return server_key, "gemini", DEFAULT_GEMINI_MODEL

    raise ValueError(
        "No active API key found. Please add an API key in Settings > AI Configuration."
    )


def _build_prompt(mode: str, context: str = "") -> str:
    if mode == "rewrite":
        system_prompt = (
            "You are a professional writer and editor. "
            "Rewrite the following content completely while preserving its meaning. "
            "Improve clarity, structure, and readability. "
            "Output in Markdown format."
        )
    else:
        system_prompt = (
            "You are a professional writer and editor. "
            "Refine the following content by fixing grammar, improving word choice, "
            "and enhancing readability without changing the overall structure. "
            "Output in Markdown format."
        )

    if context:
        system_prompt += f"\n\nContext about this content: {context}"

    return system_prompt


def _refine_openai(api_key: str, model: str, content: str, system_prompt: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def _refine_gemini(api_key: str, model: str, content: str, system_prompt: str) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=f"{system_prompt}\n\n{content}",
    )
    return response.text


def refine_content(
    content: str, mode: str, context: str = "", user: Optional[User] = None
) -> str:
    api_key, provider, model = _get_active_key(user)
    system_prompt = _build_prompt(mode, context)

    # Safety: ensure model matches provider
    is_gemini_model = model in GEMINI_MODELS
    if provider == "gemini" and not is_gemini_model:
        model = DEFAULT_GEMINI_MODEL
    elif provider != "gemini" and is_gemini_model:
        model = DEFAULT_OPENAI_MODEL

    if provider == "gemini":
        return _refine_gemini(api_key, model, content, system_prompt)
    return _refine_openai(api_key, model, content, system_prompt)
