from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.index, name='user_dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('post_history/', views.post_history, name='posts_profile'),
    path('reply_history/', views.reply_history, name='reply_profile'),
]