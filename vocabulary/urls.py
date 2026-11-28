from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('search/', views.search_view, name='search'),
]