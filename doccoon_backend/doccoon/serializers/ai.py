from rest_framework import serializers


class AIRefineRequestSerializer(serializers.Serializer):
    content = serializers.CharField()
    mode = serializers.ChoiceField(choices=["refine", "rewrite"], default="refine")
    context = serializers.CharField(required=False, default="", allow_blank=True)


class AIRefineResponseSerializer(serializers.Serializer):
    original = serializers.CharField()
    refined = serializers.CharField()
    mode = serializers.CharField()
