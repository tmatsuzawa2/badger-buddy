from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-post', views.create_post, name='create-post'),
    path('create-reply', views.create_reply, name='create-reply'),
]