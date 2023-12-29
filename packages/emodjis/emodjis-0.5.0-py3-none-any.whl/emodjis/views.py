"""Main page."""
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Emoticons",
        }
        return render(request, self.template_name, context)
