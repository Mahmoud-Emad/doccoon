from django.db import migrations


def encrypt_existing_keys(apps, schema_editor):
    """Encrypt any existing plaintext API keys."""
    from doccoon.utils.encryption import encrypt_value

    AIProviderKey = apps.get_model("doccoon", "AIProviderKey")
    for key in AIProviderKey.objects.all():
        # Check if already encrypted (Fernet tokens start with 'gAAAAA')
        if key.api_key and not key.api_key.startswith("gAAAAA"):
            key.api_key = encrypt_value(key.api_key)
            key.save(update_fields=["api_key"])


def decrypt_existing_keys(apps, schema_editor):
    """Reverse: decrypt API keys back to plaintext."""
    from doccoon.utils.encryption import decrypt_value

    AIProviderKey = apps.get_model("doccoon", "AIProviderKey")
    for key in AIProviderKey.objects.all():
        if key.api_key and key.api_key.startswith("gAAAAA"):
            try:
                key.api_key = decrypt_value(key.api_key)
                key.save(update_fields=["api_key"])
            except Exception:
                pass  # Skip if decryption fails


class Migration(migrations.Migration):
    dependencies = [
        ("doccoon", "0013_sharedbook_pages_snapshot"),
    ]

    operations = [
        migrations.RunPython(encrypt_existing_keys, decrypt_existing_keys),
    ]
