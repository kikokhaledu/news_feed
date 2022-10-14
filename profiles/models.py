from enum import auto
from django.db import models
from django.contrib.auth.models import User
from posts.models import posts
# token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


class profiles(models.Model):
    user = models.ForeignKey(
        User, related_name="profile_owner", on_delete=models.CASCADE, blank=True)
    biography = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username + "'"+" "+"profile"

    def num_of_subscribers(self):
        subs = subscriptions.objects.filter(
            subscribed_to_user=self.user).count()
        return subs

    def num_of_subscriptions(self):
        subs = subscriptions.objects.filter(subscriber_user=self.user).count()
        return subs

    def num_of_posts(self):
        post_count = posts.objects.filter(user=self.user).count()
        return post_count

    class Meta:
        verbose_name_plural = 'profiles'


class subscriptions(models.Model):
    subscriber_user = models.ForeignKey(
        User, related_name="subscriber", on_delete=models.CASCADE, blank=True)
    subscribed_to_user = models.ForeignKey(
        User, related_name="subscibed_to", on_delete=models.CASCADE, blank=True)
    subscribed_since = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subscriber_user.username + " "+"sub"+" "+"to"+" "+self.subscribed_to_user.username

    class Meta:
        unique_together = (('subscriber_user', 'subscribed_to_user'),)
        verbose_name_plural = 'subscriptions'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_toekn(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        profiles.objects.create(user=instance)
