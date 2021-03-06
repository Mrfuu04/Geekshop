from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from adminapp.mixin import AuthorisationDispatchMixin, AdminContextMixin
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from basketapp.models import Basket


class ProfileView(UpdateView, AuthorisationDispatchMixin):
    """Отображение профиля"""
    form_class = UserProfileForm
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('authapp:profile')

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return super(ProfileView, self).post(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        messages.set_level(self.request, 25)
        messages.success(self.request, 'Изменения успешно внесены')
        super(ProfileView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.set_level(self.request, 40)
        messages.error(
            self.request, *(error for error in form.errors.values()))
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль {self.request.user.username}'
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context


# FBV вариант ProfileView
# @login_required(login_url='/login')
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Изменения успешно внесены!')
#         else:
#             errors = [error for error in form.errors.values()]
#             messages.error(request, *errors)
#
#     context = {
#         'title': 'Profile',
#         'form': UserProfileForm(instance=request.user),
#         'basket': Basket.objects.filter(user=request.user)
#     }
#
#     return render(request, 'authapp/profile.html', context=context)

class GSloginView(LoginView):
    """Логин"""
    template_name = 'authapp/login.html'
    form_class = UserLoginForm


# FBV вариант GSloginView
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('mainapp:index'))
#             else:
#                 print('User inactive')
#         else:
#             print(form.errors)
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'Авторизация',
#         'form': form,
#     }
#
#     return render(request, 'authapp/login.html', context=context)

class GSRegisterView(FormView, AdminContextMixin):
    """Регистрация нового пользователя"""
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')
    title = 'Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Письмо подтверждения отправлено!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.error(request, 'Ошибка при отправке письма')
        else:
            messages.error(
                request, *(error for error in form.errors.values()))
            return HttpResponseRedirect(reverse('authapp:register'))

    def send_verify_mail(self, user):
        """Отправляет письмо с подтверждение на почту"""
        verify_link = reverse('authapp:verify', args=[
            user.email, user.activation_key])
        subject = None
        message = f'Для подтверждения учетной записи на портале {settings.DOMAIN_NAME}\nПерейдите по ссылке\n{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, key):
        """Верификация при переходе по ссылке из письма подтверждения"""
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == key and not user.is_user_key_expires():
                user.is_active = True
                user.activation_key = ''
                user.is_key_expires = None
                user.save()
                auth.login(
                    self, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(self, 'authapp/verification.html')
            else:
                return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('mainapp:index'))


# FBV вариант GSRegisterView (Подтверждения по почте нет!)
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('authapp:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#
#     context = {
#         'title': 'Регистрация',
#         'form': form
#     }
#
#     return render(request, 'authapp/register.html', context=context)

class GSLogout(LogoutView):
    """Логаут"""
    next_page = 'mainapp:index'

# FBV вариант GSLogout
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('mainapp:index'))
