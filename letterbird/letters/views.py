from django.shortcuts import render
from django.views.generic import ListView
from .models import Letter


class ShowLetters(ListView):
    model = Letter
    template_name = 'letters/index.html'
