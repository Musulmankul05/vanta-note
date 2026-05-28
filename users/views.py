import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from notes.models import Note

from users.models import User


def logout_view(request):
    logout(request)
    return redirect('note-menu')


class LoginUserView(LoginView):
    template_name = 'login.html'
    model = User
    success_url = "note-menu"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            request.POST = request.POST.copy()
            request.POST['username'] = user.username
            request.POST['password'] = password
            print(f"{request.POST['username']}\n{request.POST['password']}")
        except User.DoesNotExist as e:
            print(e)
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
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password_confirm = request.POST.get("password2")

        if password != password_confirm:
            return render(request, self.template_name, {"error": "Security keys do not match."})
        
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.is_active:
                return render(request, self.template_name, {"error": "Identifier is already in use."})
            else:
                existing_user.delete()
        
        user = User.objects.create_user(
            username = username, email = email, password = password
        )

        user.salt = os.urandom(16)
        user.save()
        welcome_note = Note.objects.create(author = user, title = "welcome to vanta",
                                           content = "**welcome my friend to vanta.**\n"
                                                     "# you can add notes and write with markdown expressions.\n *enjoy!*")
        welcome_note.save()
        return redirect('login')
