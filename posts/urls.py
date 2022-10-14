from django.urls import path, re_path, include
# from django.conf.urls import url
from . import views


urlpatterns = [
    path('add_post/', views.add_post, name='add_post'),  # create a post
    path('get_my_posts/', views.get_my_posts,
         name='get_my_posts'),  # get a post

]
