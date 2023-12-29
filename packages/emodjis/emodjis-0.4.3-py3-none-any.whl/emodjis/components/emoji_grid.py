# grid.py
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Emoji
from ..serializers import EmojiSerializer

PAGE_SIZE = 100


class EmojiGridView(UnicornView):
    name_search = ""
    emodjis = None
    page_range = 0
    page = 1

    def mount(self):
        self.load_emojis()

    def load_emojis(self, search="", page=1):
        self.name_search = search
        if search:
            emodjis = Emoji.objects.filter(name__icontains=search).order_by(
                "name"
            )
        else:
            emodjis = Emoji.objects.filter(
                name__icontains=self.name_search
            ).order_by("name")
        p = Paginator(emodjis, PAGE_SIZE)
        self.page_range = list(p.page_range)
        self.page = page
        self.emodjis = EmojiSerializer(
            p.page(page).object_list,
            many=True,
            context={"request": self.request},
        ).data

    def get_page_range(self):
        return self.page_range
