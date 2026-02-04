from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.user import User
from doccoon.utils.encryption import decrypt_value, encrypt_value


class AIProviderKey(DoccoonBaseModel):
    PROVIDER_CHOICES = [
        ("openai", "ChatGPT / OpenAI"),
        ("gemini", "Google Gemini"),
    ]

    OPENAI_MODELS = [
        ("gpt-4o-mini", "GPT-4o Mini"),
        ("gpt-4o", "GPT-4o"),
        ("gpt-4.1-nano", "GPT-4.1 Nano"),
        ("gpt-4.1-mini", "GPT-4.1 Mini"),
        ("gpt-4.1", "GPT-4.1"),
    ]

    GEMINI_MODELS = [
        ("gemini-2.0-flash", "Gemini 2.0 Flash"),
        ("gemini-2.5-flash", "Gemini 2.5 Flash"),
        ("gemini-2.5-pro", "Gemini 2.5 Pro"),
    ]

    MODEL_CHOICES = OPENAI_MODELS + GEMINI_MODELS

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_keys")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    label = models.CharField(max_length=100, blank=True, default="")
    api_key = models.TextField()
    model = models.CharField(
        max_length=50, default="gpt-4o-mini", choices=MODEL_CHOICES
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.provider} key for {self.user.email}"

    def set_api_key(self, plaintext: str) -> None:
        """Encrypt and store the API key."""
        if plaintext:
            self.api_key = encrypt_value(plaintext)
        else:
            self.api_key = ""

    def get_api_key(self) -> str:
        """Decrypt and return the API key."""
        if not self.api_key:
            return ""
        try:
            return decrypt_value(self.api_key)
        except Exception:
            # If decryption fails (old unencrypted key), return as-is
            return self.api_key

    @property
    def masked_key(self) -> str:
        key = self.get_api_key()
        if len(key) <= 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"
