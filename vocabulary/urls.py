from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('save/', views.save_word_view, name='save_word'),
]