from django_unicorn.components import UnicornView


class SearchView(UnicornView):
    search = ""

    def updated_search(self, query):
        self.parent.load_emojis(search=query)
        self.parent.force_render = True
