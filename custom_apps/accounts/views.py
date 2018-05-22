from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View

from django.http import request

from django.core.mail import send_mail, BadHeaderError

from django.conf import settings



MyUser = get_user_model()

def signup_user(request):
    context={}
    template_name='registration/signup.html'

    if request.method == 'POST':
        nom         = request.POST['nom']
        prenom      = request.POST['prenom']
        email       = request.POST['email']
        password    = request.POST['password']

        if MyUser.objects.filter(email__iexact=email).exists():
            context['message_class']    ='danger'
            context['message']          ='Il semblerait que vous avez déjà un compte chez nous.'
        else:
            user = MyUser.objects.create_user(email, nom=nom, prenom=prenom, password=password)

            if user:
                # Message and render login
                context['message_class']    ='success'
                context['message']          ='Votre compte a bien été créer'
                return redirect('/accounts/login/')

    return render(request, template_name, context)


def login_user(request):
    context={}
    template_name   = 'registration/login.html'

    if request.method == 'POST':
        email       = request.POST['email']
        password    = request.POST['password']
        user        = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect(request.GET.get('next') or 'profile')

        else:
            context['message_class']    ='danger'
            context['message']          ='Votre adresse mail ou mot de pass ne sont pas correctes'

    return render(request, template_name, context)


def logout_user(request):
    logout(request)
    return redirect('login.html')


def forgot_password(request):
    context = {}
    template_name = 'registration/forgot-password.html'

    if request.method == 'POST':
        email = request.POST['email']

        user = MyUser.objects.get(email=email)

        if user:
            # Get user password
            # user = user.password
             
            try:
                # TODO Email password and username to user
                send_mail(
                    'Restauration',
                    'Veuillez suivre ce lien pour ...',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except BadHeaderError:
                context['message_type'] = 'danger'
                context['message'] = ''
                template_name = 'registration/forgot.html'
                # return render(request, 'forgot.html', context)
            else:
                context['message_type'] = 'success'
                context['message'] = ''
                template_name = 'registration/login.html'
                # return render(request, 'login.html', context)
        
        else:
            context['message_type'] = 'danger'
            context['message'] = ''
            # Could not find user
            template_name = 'registration/forgot-password.html'
            # return redirect('')

    return render(request, template_name, context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return redirect('/admin/')
        
        return render(request, 'accounts/profile.html', {})

    def post(self, request, *args, **kwargs):
        pass

