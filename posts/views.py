import genericpath
import imp
from rest_framework import viewsets
from .models import posts
from .serializers import Posts_Serializer
from rest_framework.response import Response
# from rest_framework.decorators import action
from rest_framework import filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# ,IsAdminUser,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.permissions import IsAuthenticated
# from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from posts import serializers

import collections
import yaml
from rest_framework import fields


@api_view(['POST'])
def add_post(request):
    """this is where we post a new post entry title limted to 100 char 
    body is limited to 1000 chars 
    """
    serializer = Posts_Serializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_my_posts(request, title=None):
    """
    the default of this endpoint will return all posts of the logged in user 
    if query paramters are passed it will automatically search by them
    it will only use title  or  date filters not together 
    for dates it will take start or start ~ end  or end dates 
    """

    if request.query_params.get('title'):
        title_to_search = request.query_params.get('title')
        try:
            my_posts = posts.objects.filter(
                title__icontains=title_to_search, user=request.user)
            serializer = Posts_Serializer(my_posts, many=True)
            if my_posts.count() > 0:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {'message': "no posts matching your search title!"}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
    # start date  and end date
    elif request.query_params.get('start_date') and request.query_params.get('end_date'):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date > end_date:
            json = {'message': "start date can't be after the end date"}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
        try:
            my_posts = posts.objects.filter(
                publish_date__range=[start_date, end_date])
            serializer = Posts_Serializer(my_posts, many=True)
            if my_posts.count() > 0:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {'message': "no posts in the date range you searched!"}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
    # only  start date
    elif request.query_params.get('start_date'):
        start_date = request.query_params.get('start_date')
        try:
            my_posts = posts.objects.filter(publish_date__gte=start_date)
            serializer = Posts_Serializer(my_posts, many=True)
            if my_posts.count() > 0:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {'message': "no posts after the start date provided!"}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
    # only end date
    elif request.query_params.get('end_date'):
        end_date = request.query_params.get('end_date')
        try:
            my_posts = posts.objects.filter(publish_date__lte=end_date)
            serializer = Posts_Serializer(my_posts, many=True)
            if my_posts.count() > 0:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {'message': "no posts before the date provided!"}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            my_posts = posts.objects.filter(user=request.user)
            serializer = Posts_Serializer(my_posts, many=True)
            if my_posts.count() > 0:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                json = {'message': "you don't have any posts yet!"}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            json = {'error': str(e)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
