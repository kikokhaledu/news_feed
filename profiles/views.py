from tkinter import E
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, porfiles_Serializer, subscriptions_Serializer
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import profiles, subscriptions
from posts.models import posts


@api_view(['PATCH'])
def update_bio(request):
    """will take the biography as "biography"  char or numbers with only 200 char and update the 
    user porfile to that
    """
    user = request.user
    profile = profiles.objects.get(user=user)
    serializer = porfiles_Serializer(profile, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_profile(request, profile_id):
    """this will show the user profile with the given profile id"""
    try:
        profile = profiles.objects.get(id=profile_id)
        serializer = porfiles_Serializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        json = {'error': str(e)}
        return Response(json, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_subscribers(request, user_id):
    """
    people subscribed to that user
    will return the user subscriptions to the user with the given id
    """
    try:
        user = User.objects.get(id=user_id)
        subs = subscriptions.objects.filter(subscribed_to_user=user)
        if not subs.count() <= 0:
            serializer = subscriptions_Serializer(subs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            json = {"message": "user doesn't have any subscribers"}
            return Response(json, status=status.HTTP_200_OK)
    except Exception as e:
        json = {'error': str(e)}
        return Response(json, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_subscriptions(request, user_id):
    """
    that user is subscribed to those people
    will return the user subscriptions of the user with the given id
    if you pass a query paramter "user_name" it will search the user
    subs for that username and return otherwise it will say that it was not found
    """
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        json = {'error': str(e)}
        return Response(json, status=status.HTTP_404_NOT_FOUND)
    if request.query_params.get('user_name'):
        user_name = request.query_params.get('user_name')
        try:
            subscribee = User.objects.get(username=user_name)
            subs = subscriptions.objects.filter(
                subscriber_user=user, subscribed_to_user=subscribee)
            if not subs.count() <= 0:
                serializer = subscriptions_Serializer(subs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {
                    "message": "user doesn't have any subscriptions with those details"}
                return Response(json, status=status.HTTP_200_OK)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            user = User.objects.get(id=user_id)
            subs = subscriptions.objects.filter(subscriber_user=user)
            if not subs.count() <= 0:
                serializer = subscriptions_Serializer(subs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {"message": "user doesn't have any subscriptions"}
                return Response(json, status=status.HTTP_200_OK)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def subscribe(request, user_id):
    """
    will take a user id and subscribe the currently logged in user to him/her
    note this will only work if the user has 100 or less subs
    """
    subscriber = request.user
    subs_count = subscriptions.objects.filter(
        subscriber_user=subscriber).count()
    try:
        subscribee = User.objects.get(id=user_id)
        if subs_count < 100:
            new_sub = subscriptions.objects.create(
                subscriber_user=subscriber, subscribed_to_user=subscribee)
            json = {"message": "successfully subscribed!"}
            return Response(json, status=status.HTTP_202_ACCEPTED)
        else:
            json = {"message": "you can't have more than 100 subscriptions"}
            return Response(json, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        json = {'error': str(e)}
        return Response(json, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE', 'GET'])
def unsubscribe(request, sub_id):
    """takes a subscription id and deletes it only if the user 
    making the request is the subscriber
    """
    subscriber = request.user
    try:
        subscription = subscriptions.objects.get(id=sub_id)
    except Exception as e:
        json = {'error': str(e)}
        return Response(json, status=status.HTTP_404_NOT_FOUND)
    if subscription.subscriber_user == subscriber:
        subscription.delete()
        json = {"message": "successfully unsubscribed!"}
        return Response(json, status=status.HTTP_204_NO_CONTENT)
    else:
        json = {"message": "No such subsciprtion for you to unsubscribe from"}
        return Response(json, status=status.HTTP_403_FORBIDDEN)


class user_view_set(viewsets.ModelViewSet):
    """used to create users only"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        json = {}
        if serializer.is_valid():
            user = serializer.save()
            token = get_token(user.username)
            json['message'] = 'User created successfully!'
            json['email'] = user.email
            json['username'] = user.username
            json['token'] = token.key
        else:
            json = serializer.errors
        return Response(json, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        json = {'message': 'you are not allowed to do that'}
        return Response(json, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        json = {'message': 'you are not allowed to do that'}
        return Response(json, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        json = {'message': 'you are not allowed to do that'}
        return Response(json, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        json = {'message': 'you are not allowed to do that'}
        return Response(json, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        json = {'message': 'you are not allowed to do that'}
        return Response(json, status=status.HTTP_403_FORBIDDEN)


def get_token(username):
    """post a username and a password and this will retun the token of that user"""
    new_user = User.objects.get(username=username)
    token = Token.objects.get(user=new_user)
    return token
