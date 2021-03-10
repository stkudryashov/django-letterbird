from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Letter
from .forms import LetterForm
from django.contrib import messages
from users.models import User


from django.urls import reverse_lazy


class IndexHtml(ListView):
    model = Letter
    template_name = 'letters/index.html'


class ShowLetters(ListView):
    model = Letter
    template_name = 'letters/letters.html'
    context_object_name = 'letters'


class ShowSavesLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'сохраненные'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)
            saves_letters = current_user.saves.all()
            return saves_letters


class ShowRecentlyLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'недавние'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)
            views_letters = current_user.views.all()
            return views_letters


class ShowMyLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'мои'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Letter.objects.filter(author_id=self.request.user.pk)


class CreateLetter(CreateView):
    form_class = LetterForm
    template_name = 'letters/add_letter.html'
    success_url = reverse_lazy('my')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Письмо успешно отправлено')
        return super(CreateLetter, self).form_valid(form)


class ShowAllUsers(ShowLetters):
    template_name = 'letters/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи'
        return context

    def get_queryset(self):
        return User.objects.all()


class ShowAllLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'все письма'
        return context

    def get_queryset(self):
        return Letter.objects.all()

