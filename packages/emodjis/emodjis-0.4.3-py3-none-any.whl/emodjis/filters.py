import django_filters
from django_filters import FilterSet
from .models import Emoji


class EmojiFilter(FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Search by emoticon name",
    )
    team = django_filters.CharFilter(
        field_name="team__name",
        lookup_expr="icontains",
        label="Search by team name",
    )
    creator = django_filters.CharFilter(
        field_name="created_by__username",
        lookup_expr="iexact",
        label="Search by creator username",
    )

    class Meta:
        model = Emoji
        fields = ["name", "nsfw", "team", "private", "creator"]
