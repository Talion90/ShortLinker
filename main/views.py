from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView, CreateView, DeleteView
from django.db import IntegrityError

from main.forms import ChangeUserInfoForm, RegisterUserForm
from main.link_shorter import UrlShorten
from main.utilities import signer
from main.forms import LinkForm
from main.models import Link


def home(request):
    if request.method == 'POST':
        link_form = LinkForm(request.POST)
        context = {'form': link_form}
        if link_form.is_valid():
            token = UrlShorten.create_unique(str(link_form['long_link']))
            short_link = request.get_host() + '/' + token
            long_link = link_form.cleaned_data['long_link']
            if request.user.is_authenticated:
                try:
                    Link.objects.get_or_create(
                        user=request.user,
                        long_link=long_link,
                        short_link=short_link,
                        token=token
                    )
                except IntegrityError:
                    pass
            context['long_link'] = long_link
            context['short_link'] = short_link
            return render(request, 'main/index.html', context)
        return render(request, 'main/index.html', context)
    else:
        form = LinkForm()
        context = {'form': form}
        return render(request, 'main/index.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def redirect_page(request, token):
    redirect_link = get_object_or_404(Link, token=token).long_link
    return redirect(redirect_link)


class SLLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    links = Link.objects.filter(user=request.user.id).all()
    if links:
        context = {'links': links}
        return render(request, 'main/profile.html', context)
    return render(request, 'main/profile.html')


class SLLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя успешно изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class SLPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


class SLPasswordResetView(PasswordResetView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'main/password_reset_form.html'
    subject_template_name = 'templates/email/reset_subject.txt'
    email_template_name = 'templates/email/reset_email.txt'
    success_url = reverse_lazy('main:password_reset_done')
    success_message = 'Пароль пользователя сброшен'


class SLPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class SLPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/confirm_password.html'


class SLPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_confirmed.html'


class PasswordDoneView(TemplateView):
    template_name = 'main/password_reset_form.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
