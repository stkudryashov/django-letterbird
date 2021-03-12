from django.views.generic import ListView, CreateView
from django.http.response import HttpResponse

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Letter
from users.models import User

from .forms import LetterForm
from random import choice


class IndexHtml(ListView):
    model = Letter
    template_name = 'letters/views/index.html'


class ShowLetters(ListView):
    model = Letter
    template_name = 'letters/views/letters.html'
    context_object_name = 'letters'


class ShowBookmarks(ShowLetters):
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['title'] = 'сохраненные'
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)
            saves_letters = current_user.bookmarks.all()
            return saves_letters


class ShowRecently(ShowLetters):
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['title'] = 'недавние'
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)
            recently_letters = current_user.recently.all().order_by('-datetime')[:10]
            return recently_letters


class ShowMy(ShowLetters):
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['title'] = 'мои'
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Letter.objects.filter(author_id=self.request.user.pk)


class CreateLetter(CreateView):
    form_class = LetterForm
    template_name = 'letters/forms/add_letter.html'
    success_url = reverse_lazy('my')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Письмо успешно отправлено')
        return super(CreateLetter, self).form_valid(form)


class GetLetter(ShowLetters):
    template_name = 'letters/forms/get_letter.html'
    context_object_name = 'letter'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['title'] = 'получить'
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = User.objects.get(pk=self.request.user.pk)

            if current_user.current_letter == 0 or self.kwargs['value'] == 'new-letters':
                old_letters = current_user.recently.values_list('pk', flat=True)
                all_letters = Letter.objects.filter(is_spam=False)
                all_letters = all_letters.values_list('pk', flat=True)
                new_letters = all_letters.exclude(pk__in=old_letters)
                new_letters = new_letters.exclude(author_id=current_user.pk)

                if new_letters:
                    rand_letter_id = choice(new_letters)
                    rand_letter = Letter.objects.get(pk=rand_letter_id)
                    rand_letter.views += 1
                    rand_letter.save()
                    current_user.recently.add(rand_letter)
                    current_user.current_letter = rand_letter.pk
                    current_user.save()
                    return rand_letter
                else:
                    current_user.current_letter = 0
                    current_user.save()
            else:
                return Letter.objects.get(pk=current_user.current_letter)


class ShowUsers(ShowLetters):
    template_name = 'letters/admin/user_list.html'
    context_object_name = 'users'

    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_staff:
            context = super().get_context_data(**kwargs)
            context['title'] = 'пользователи'
            return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()


class ShowSpam(ShowLetters):
    template_name = 'letters/admin/spam_list.html'
    context_object_name = 'letter'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_staff:
            context = super().get_context_data(**kwargs)
            context['title'] = 'спам'
            return context

    def get_queryset(self):
        if self.request.user.is_staff:
            spam_letters = Letter.objects.filter(spam__gt=0).filter(is_spam=False)
            spam_letters = spam_letters.order_by('-spam')
            return spam_letters.first()


class ShowAll(ShowLetters):
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_staff:
            context = super().get_context_data(**kwargs)
            context['title'] = 'все письма'
            return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Letter.objects.all()


def change_bookmarks(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.pk)
        letter_id = request.POST.get('letter_id')
        letter = Letter.objects.get(pk=letter_id)

        status = request.POST.get('status')
        if status == 'true':
            current_user.bookmarks.add(letter_id)
            letter.saves += 1
        elif status == 'false':
            current_user.bookmarks.remove(letter_id)
            letter.saves -= 1

        letter.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


def add_spam_count(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)

        if user.current_letter == 0:
            messages.error(request, 'Вы не можете этого сделать')
            return redirect('get-letter', value='next')

        letter = Letter.objects.get(pk=user.current_letter)
        letter.spam += 1
        letter.save()
        user.current_letter = 0
        user.save()
        messages.warning(request, 'Предыдущее сообщение отправлено на проверку')
        return redirect('get-letter', value='next')
    else:
        return HttpResponse(status=401)


def spam_decide(request, letter_pk, decide):
    if request.user.is_staff:
        letter = Letter.objects.get(pk=letter_pk)
        if decide == 0:
            letter.spam = 0
            letter.save()
        else:
            letter.is_spam = True
            letter.save()
        return redirect('spam')
    else:
        return HttpResponse(status=401)
