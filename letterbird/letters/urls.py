from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexHtml.as_view(), name='homepage'),
    path('letters/saves/', ShowSavesLetters.as_view(), name='saves'),
    path('letters/recently/', ShowRecentlyLetters.as_view(), name='recently'),
    path('letters/my/', ShowMyLetters.as_view(), name='my'),
    path('action/add-letter/', CreateLetter.as_view(), name='add-letter'),
    path('action/get-letter/', GetLetter.as_view(), name='get-letter'),
    path('super/users/', ShowAllUsers.as_view(), name='users'),
    path('super/all/', ShowAllLetters.as_view(), name='all'),
    path('super/spam/', ShowSpamLetters.as_view(), name='spam'),
    path('post/change/', change_saves, name='change_saves'),
]
