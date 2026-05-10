from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

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
            request.POST = request.POST.copy()
            request.POST['username'] = user.username
            request.POST['password'] = password
        except User.DoesNotExist:
            pass
        return super().post(request, *args, **kwargs)