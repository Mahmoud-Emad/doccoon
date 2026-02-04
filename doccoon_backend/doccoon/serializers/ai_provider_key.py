from rest_framework import serializers

from doccoon.models.ai_provider_key import AIProviderKey


class AIProviderKeySerializer(serializers.ModelSerializer):
    masked_key = serializers.CharField(read_only=True)

    class Meta:
        model = AIProviderKey
        fields = [
            "id",
            "provider",
            "label",
            "masked_key",
            "model",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "masked_key", "created_at"]


class AIProviderKeyCreateSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(write_only=True)

    class Meta:
        model = AIProviderKey
        fields = ["provider", "label", "api_key", "model", "is_active"]

    def create(self, validated_data):
        plaintext_key = validated_data.pop("api_key", "")
        instance = AIProviderKey(**validated_data)
        instance.set_api_key(plaintext_key)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        plaintext_key = validated_data.pop("api_key", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if plaintext_key:
            instance.set_api_key(plaintext_key)
        instance.save()
        return instance
