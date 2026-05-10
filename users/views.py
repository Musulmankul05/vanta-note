import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from websidian.security import get_fernet_key

from users.models import User


def logout_view(request):
    logout(request)
    return redirect('note-menu')


class LoginUserView(LoginView):
    template_name = 'login.html'
    model = User
    success_url = "note-menu"

    def post(self, request, *args, **kwargs):
        email_or_phone = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email_or_phone)
            key = get_fernet_key(password, user.salt)
            request.POST = request.POST.copy()
            request.POST['username'] = user.username
            request.POST['password'] = password
            request.session['master_key'] = key.decode()
        except User.DoesNotExist:
            pass
        return super().post(request, *args, **kwargs)


class SignupView(View):
    template_name = 'signup.html'
    model = User
    success_url = reverse_lazy('login')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")

        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.is_active:
                return render(request, self.template_name, {"error": "Пользователь с таким именем уже существует."})
            else:
                existing_user.delete()

        user = User(username=request.POST.get("username"),
                    email=request.POST.get("email"),
                    password = request.POST.get("password1"),
                    salt = os.urandom(16))
        user.save()
        return redirect('login')
