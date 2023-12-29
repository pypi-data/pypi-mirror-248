from django_unicorn.components import UnicornView


class SearchView(UnicornView):
    search = ""
    nsfw = False
    private = False

    def updated_search(self, query):
        self.parent.load_emojis(
            search=query, nsfw=self.nsfw, private=self.private
        )
        self.parent.force_render = True

    def updated_nsfw(self, query):
        self.nsfw = query
        self.parent.load_emojis(
            search=self.search, nsfw=query, private=self.private
        )
        self.parent.force_render = True

    def updated_private(self, query):
        self.private = query
        self.parent.load_emojis(
            search=self.search, nsfw=self.nsfw, private=query
        )
        self.parent.force_render = True
