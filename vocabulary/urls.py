from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('save/', views.save_word_view, name='save_word'),
    path('my-words/', views.my_words_view, name='my_words'),
    path('remove/<int:pk>/', views.remove_word_view, name='remove_word'),
]