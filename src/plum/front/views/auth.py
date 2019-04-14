from django.contrib.auth.views import LoginView, LogoutView


class Login(LoginView):
    template_name = 'front/auth/login.html'


class Logout(LogoutView):
    pass
