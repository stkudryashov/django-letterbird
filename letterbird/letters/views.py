from django.shortcuts import render
from django.views.generic import ListView
from .models import Letter


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
        context['title'] = 'сохраненные письма'
        return context

    def get_queryset(self):
        return Letter.objects.all()


class ShowRecentlyLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'недавние письма'
        return context

    def get_queryset(self):
        return Letter.objects.all()


class ShowMyLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'мои письма'
        return context

    def get_queryset(self):
        return Letter.objects.filter(author_id=self.request.user.pk)
