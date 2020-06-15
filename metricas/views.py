from django.shortcuts import render, redirect
from metricas.forms import UserCreationFormEmail , UserResetPasswordForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetView , PasswordContextMixin, FormView, PasswordChangeView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import resolve_url
import datetime
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
User = get_user_model()

def index(request):
    return render(request, 'user_example/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationFormEmail(request.POST)


        if form.is_valid():
            password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
            user = form.save()
            user.set_password(password)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            mensagem = "A sua senha temporaria é : " + password + " \n Você deve logar no site dentro de 1 minuto, caso contrario será necessario re-cadastrar sua conta e email."
            user.email_user("Sua Conta Django", mensagem, "eriksegecs@yahoo.com.br")
            raw_pass = form.cleaned_data.get(password)
            user.last_login2 = user.date_joined
            user.save()
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('index')
        
        else:
            print(form.errors)
    else:
        form = UserCreationFormEmail()

    context = {'form' : form}
    return render(request, 'registration/register.html', context)


def MyPasswordResetView(request):
    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        email = request.POST['email']
        password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            username = user.username
            mensagem = "A sua senha foi resetada para : " + password
            user.email_user("Sua Conta Django", mensagem, "eriksegecs@yahoo.com.br")
            raw_pass = password
            user.save()
        except:
            pass
        return redirect('index')
            

    else:
        form = UserResetPasswordForm()

    context = {'form' : form}
    return render(request, 'registration/resetpass.html', context)

class MyLoginView(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        u =  form.get_user()
        try:
            usern = User.objects.get(username=u.username)
        except:
            return HttpResponseRedirect(reverse_lazy('expired'))

        if timezone.now() - u.last_login2 > datetime.timedelta(minutes=2):
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(reverse_lazy('password_change'))
        else:
            auth_login(self.request, form.get_user())
            usern.last_login2 = timezone.now()
            usern.save()
            return HttpResponseRedirect(self.get_success_url())


class MyPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        form.save()
        u = form.user
        u.previous_password = u.password
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

def Passdone(request):
    return render(request, 'user_example/passdone.html')

def Expired(request):
    return render(request, 'user_example/expired.html')