"""Emoticons serializer."""
import base64
from django.utils.translation import gettext_lazy as _
from .models import Emoji
from rest_framework import serializers


class EmojiFilterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label=_("Search by name"), required=False)
    team = serializers.CharField(
        label=_("Search by team name"), required=False
    )
    nsfw = serializers.BooleanField(
        label=_("Show NSFW emoticons"), required=False
    )
    private = serializers.BooleanField(
        label=_("Show private emoticons only"), required=False
    )

    class Meta:
        model = Emoji
        fields = ["name", "team", "nsfw", "private"]


class EmojiSerializer(serializers.ModelSerializer):
    b64image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Emoji
        fields = "__all__"

    def get_b64image(self, obj):
        return base64.b64encode(obj.image).decode("utf-8")

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            host = request.META.get("HTTP_HOST")
            return f"{request.scheme}://{host}/emoticon/{obj.name}"
        else:
            return f"emoticon/{obj.name}"


class EmojiListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Emoji
        fields = ["name", "url"]

    def get_url(self, obj):
        host = self.request.META.get("HTTP_HOST")
        return f"{self.request.scheme}://{host}/emoticon/{obj.name}"


class EmojiDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = []


class EmojiCreateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(label=_("File"), required=False)

    class Meta:
        model = Emoji
        fields = ["image", "private", "nsfw", "team"]
