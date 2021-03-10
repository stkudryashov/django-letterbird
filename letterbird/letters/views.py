from django.views.generic import ListView, CreateView
from django.http.response import HttpResponse
from .models import Letter
from .forms import LetterForm
from django.contrib import messages
from users.models import User
from random import choice


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
            recently_letters = current_user.recently.all().order_by('-datetime')[:10]
            return recently_letters


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


class GetLetter(ShowLetters):
    template_name = 'letters/get_letter.html'
    context_object_name = 'letter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'получить'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)
            old_letters = current_user.recently.values_list('pk', flat=True)
            all_letters = Letter.objects.values_list('pk', flat=True)
            new_letters = all_letters.exclude(pk__in=old_letters)
            new_letters = new_letters.exclude(author_id=current_user.pk)

            if new_letters:
                rand_letter_id = choice(new_letters)
                rand_letter = Letter.objects.get(pk=rand_letter_id)
                rand_letter.views += 1
                rand_letter.save()
                current_user.recently.add(rand_letter)
                return rand_letter


class ShowAllUsers(ShowLetters):
    template_name = 'letters/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()


class ShowSpamLetters(ShowLetters):
    template_name = 'letters/spam_list.html'
    context_object_name = 'letters'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'спам'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()


class ShowAllLetters(ShowLetters):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'все письма'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Letter.objects.all()


def change_saves(request):
    current_user = User.objects.get(pk=request.user.pk)
    letter_id = request.POST.get('letter_id')
    letter = Letter.objects.get(pk=letter_id)

    status = request.POST.get('status')

    if status == 'true':
        current_user.saves.add(letter_id)
        letter.saves += 1
    elif status == 'false':
        current_user.saves.remove(letter_id)
        letter.saves -= 1

    letter.save()

    return HttpResponse(status=200)


def add_spam_count(request):
    letter_id = request.POST.get('letter_id')
    letter = Letter.objects.get(pk=letter_id)
    letter.spam += 1
    letter.save()
    return HttpResponse(status=200)
