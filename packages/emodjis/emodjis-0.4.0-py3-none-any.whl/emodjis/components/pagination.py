from django_unicorn.components import UnicornView


class PaginationView(UnicornView):
    page = 1
    page_range = None

    def hydrate(self, *args, **kwargs):
        self.page_range = self.parent.get_page_range()
        self.page = self.parent.page

    def updated_page(self, query=1):
        self.page = query
        self.parent.load_emojis(page=query)
        self.page_range = self.parent.get_page_range()
        self.parent.force_render = True
