from django.urls import path
from . import views

# app_name = 'discussion_board'
urlpatterns = [
    path('', views.index, name='index'),
    path('create-post', views.create_post, name='create-post'),
    path('create-reply/<int:post_id>', views.create_reply, name='create-reply'),
]