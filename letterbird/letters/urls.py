from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexHtml.as_view(), name='homepage'),

    path('letters/bookmarks/', ShowBookmarks.as_view(), name='bookmarks'),
    path('letters/recently/', ShowRecently.as_view(), name='recently'),
    path('letters/sent/', ShowMy.as_view(), name='my'),

    path('add-letter/', CreateLetter.as_view(), name='add-letter'),
    path('get-letter/<str:value>', GetLetter.as_view(), name='get-letter'),

    path('send-spam/', add_spam_count, name='send-spam'),

    path('super/users/', ShowUsers.as_view(), name='users'),
    path('super/letters/', ShowAll.as_view(), name='all'),
    path('super/spam/', ShowSpam.as_view(), name='spam'),

    path('super/spam/id<int:letter_pk>-d<int:decide>', spam_decide, name='spam_decide'),

    path('post/change_bookmarks/', change_bookmarks, name='change_bookmarks'),
]
