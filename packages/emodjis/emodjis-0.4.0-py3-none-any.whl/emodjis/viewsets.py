"""Emoticons viewsets"""
import uuid
import logging
from PIL import Image, UnidentifiedImageError
from django.http import HttpResponse
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiTypes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Emoji
from .serializers import (
    EmojiSerializer,
    EmojiListSerializer,
    EmojiDestroySerializer,
    EmojiCreateSerializer,
    EmojiFilterSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .filters import EmojiFilter

BASE_WIDTH = 130


class EmojiViewSet(viewsets.ModelViewSet):
    """Emoji viewset."""

    lookup_field = "name"
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmojiFilter

    def get_queryset(self):
        qs = Emoji.objects.sfw(user=self.request.user)
        if self.action in [
            "list",
            "retrieve",
        ] and self.request.query_params.get("nsfw", False):
            qs = Emoji.objects.nsfw(user=self.request.user)
        if self.action in ["create", "update", "partial_update", "destroy"]:
            qs = Emoji.updates.filter(created_by=self.request.user)
        qs = self.filter_queryset(qs)
        return qs

    queryset = Emoji.objects.all()
    serializer_class = EmojiSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def handle_file_upload(uploaded_file) -> bytes:
        upload = uploaded_file
        if upload:
            tmp_file_name = str(uuid.uuid4())
            gif_file_name = tmp_file_name + ".gif"
            with open(f"/tmp/{tmp_file_name}", "wb") as tmp_file:
                for chunk in upload.chunks():
                    tmp_file.write(chunk)
            content = Image.open(f"/tmp/{tmp_file_name}")
            width_ratio = BASE_WIDTH / float(content.size[0])
            hsize = int((float(content.size[1]) * float(width_ratio)))
            content = content.resize(
                (BASE_WIDTH, hsize), Image.Resampling.LANCZOS
            )
            content.save(f"/tmp/{gif_file_name}", format="GIF")
            content.close()
            with open(f"/tmp/{gif_file_name}", "rb") as f:
                content = f.read()
            return content

    def get_serializer_class(self):
        match self.action:
            case "list":
                return EmojiListSerializer
            case "retrieve":
                return EmojiSerializer
            case "create":
                return EmojiCreateSerializer
            case "destroy":
                return EmojiDestroySerializer

        return super().get_serializer_class()

    @extend_schema(
        summary=_("List emoticons"),
        description=_("""Filter emoticons."""),
        responses={200: OpenApiTypes.BINARY, 404: OpenApiTypes.OBJECT},
        parameters=[EmojiFilterSerializer],
        tags=[
            "emoticons",
        ],
        methods=["GET"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary=_("Retrieve emoticon"),
        description=_("""Retrieve visible emoticon image by name."""),
        responses={200: OpenApiTypes.BINARY, 404: OpenApiTypes.OBJECT},
        tags=[
            "emoticons",
        ],
        methods=["GET"],
    )
    def retrieve(self, request, name, *args, **kwargs):
        try:
            instance = self.get_queryset().get(pk=name)
            instance.uses = instance.uses + 1
            instance.save()
            return HttpResponse(instance.image, content_type="image/gif")
        except Emoji.DoesNotExist:
            return Response(
                {"detail": _("Emoji does not exist.")},
                status=404,
                content_type="application/json",
            )

    @extend_schema(
        summary=_("Create a new emoticon"),
        description=_(
            """
            Create a new icon with or without icon.

            Upload can happen later,
            but only icons with content will be visible.
            """
        ),
        request=EmojiCreateSerializer,
        responses={
            201: EmojiSerializer,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        tags=[
            "emoticons",
        ],
        methods=["POST"],
    )
    def create(self, request, name, *args, **kwargs):
        if self.get_queryset().filter(pk=name).exists():
            return Response(
                {"detail": _("Emoji already exists.")},
                status=400,
                content_type="application/json",
            )
        create_serializer = self.get_serializer_class()(data=request.data)
        if not create_serializer.is_valid():
            return Response(
                create_serializer.errors,
                status=400,
                content_type="application/json",
            )
        if uploaded_file := request.FILES.get("image"):
            try:
                content = self.handle_file_upload(uploaded_file=uploaded_file)
            except UnidentifiedImageError:
                logger = logging.getLogger("django")
                logger.error("Uploaded file is not an image.")
                return Response(
                    {"detail": _("Uploaded file is not an image.")},
                    status=400,
                    content_type="application/json",
                )
            except IOError:
                logger = logging.getLogger("django")
                logger.error("I/O error.")
                return Response(
                    {"detail": _("I/O error.")},
                    status=500,
                    content_type="application/json",
                )
            emoticon = create_serializer.save(
                name=name, created_by=request.user, image=content
            )
        else:
            emoticon = create_serializer.save(
                name=name, created_by=request.user
            )
        serializer = EmojiSerializer(emoticon)
        return Response(
            serializer.data, status=201, content_type="application/json"
        )

    @extend_schema(
        summary=_("Delete an emoticon"),
        description=_("""Delete an emoticon you own."""),
        request=EmojiDestroySerializer,
        responses={204: OpenApiTypes.NONE, 400: OpenApiTypes.OBJECT},
        tags=[
            "emoticons",
        ],
        methods=["DELETE"],
    )
    def destroy(self, request, name, *args, **kwargs):
        try:
            instance = self.get_queryset().get(pk=name)
            instance.deleted_by = request.user
            instance.deleted_at = now()
            instance.save(update_fields=["deleted_by", "deleted_at"])
            return Response(status=204)
        except Emoji.DoesNotExist:
            return Response(
                {"detail": _("Emoji does not exist.")},
                status=404,
                content_type="application/json",
            )
