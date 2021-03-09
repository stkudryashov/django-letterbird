from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexHtml.as_view(), name='homepage'),
    path('letters/saves/', ShowSavesLetters.as_view(), name='saves'),
    path('letters/recently/', ShowRecentlyLetters.as_view(), name='recently'),
    path('letters/my/', ShowMyLetters.as_view(), name='my'),
]
