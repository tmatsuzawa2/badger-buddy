from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.index, name='user_dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
]