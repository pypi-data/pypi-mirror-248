from django_unicorn.components import UnicornView
from django.contrib.auth import login, authenticate, logout


class LoginView(UnicornView):
    user = None
    username = None
    password = None
    authenticated = False

    def mount(self):
        self.authenticated = self.request.user.is_authenticated

    def connect(self):
        if user := authenticate(
            request=self.request,
            username=self.username,
            password=self.password,
        ):
            login(request=self.request, user=user)
            self.user = user
            self.authenticated = user.is_authenticated
        self.parent.load_emojis()
        self.parent.force_render = True

    def disconnect(self):
        self.user = None
        self.authenticated = False
        logout(request=self.request)
        self.parent.load_emojis()
        self.parent.force_render = True
