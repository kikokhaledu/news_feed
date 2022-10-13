from .models import posts
from rest_framework import serializers
from django.contrib.auth.models import User




class Posts_Serializer(serializers.ModelSerializer):
	class Meta:
		model = posts
		fields = ('id','title','post_text','publish_date','user')
