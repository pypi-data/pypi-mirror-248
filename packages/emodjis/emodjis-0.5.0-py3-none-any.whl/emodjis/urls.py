"""Emoticons URLs."""

from django.conf.urls import include
from django.urls import path

from .viewsets import EmojiViewSet
from .routers import EmojiRouter
from .views import IndexView

app_name = "emojis"

router = EmojiRouter(trailing_slash=False)
router.register("emoticon", EmojiViewSet, basename="emoticons")

urlpatterns = [
    path("", include(router.urls)),
    path("", IndexView.as_view(), name="index"),
]
