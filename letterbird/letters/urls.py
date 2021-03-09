from django.urls import path
from .views import *


urlpatterns = [
    path('', ShowLetters.as_view(), name='homepage')
]
