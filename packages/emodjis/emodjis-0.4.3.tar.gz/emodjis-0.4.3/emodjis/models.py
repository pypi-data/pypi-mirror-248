"Emoji model"
from django.db import models
from django.contrib.auth.models import User, Group


class EmojiAdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def sfw(self, user):
        qs = self.nsfw(user=user)
        qs = qs.filter(nsfw=False)
        return qs

    def nsfw(self, user):
        qs = self.get_queryset()
        if user.is_authenticated:
            qs = qs.filter(models.Q(created_by=user) | models.Q(private=False))
        else:
            qs = qs.filter(private=False)
        return qs


class EmojiManager(EmojiAdminManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True, image__isnull=False)
        )


class EmojiUpdateManager(EmojiAdminManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Emoji(models.Model):
    EXPORT_FIELDS = [
        "name",
        "team",
        "private",
        "uses",
        "nsfw",
        "created_at",
        "created_by",
        "deleted_at",
        "deleted_by",
    ]

    name = models.CharField(max_length=255, primary_key=True)
    uses = models.IntegerField(default=0)
    image = models.BinaryField(null=True)
    team = models.ForeignKey(
        Group,
        related_name="emojis",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    nsfw = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="created_emojis", on_delete=models.CASCADE
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User,
        related_name="deleted_emojis",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    objects = EmojiManager()
    updates = EmojiUpdateManager()
    admin = models.Manager()
