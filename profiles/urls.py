from django.urls import path ,re_path ,include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token





#these are the urls that redirect to the function that actually runs the application
router = DefaultRouter()
router.register('users',views.user_view_set)

urlpatterns = [
    path ('',include(router.urls)),# include the registred viwes 
    path('update_bio/',views.update_bio,name = 'update_bio'),  # update bio PATCH request
    path('get_user_subscribers/<int:user_id>/',views.get_user_subscribers,name = 'get_user_subscribers'),  # will show the subscribers for the user with the given id 
    path('get_user_subscriptions/<int:user_id>/',views.get_user_subscriptions,name = 'get_user_subscriptions'),  # will show the subscriptions of the user with the id provided 
    path('subscribe/<int:user_id>/',views.subscribe,name = 'subscribe'),  # get logged in users profile
    path('unsubscribe/<int:sub_id>/',views.unsubscribe,name = 'unsubscribe'),  # subscribe to the user with the provided id 
    path('request_token/', obtain_auth_token),  # request a token for a username and password

]