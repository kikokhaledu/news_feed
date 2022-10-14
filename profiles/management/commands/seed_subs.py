from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth.models import User
from profiles.models import subscriptions
import random


class Command(BaseCommand):

    help = "This command creates many subs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many subs do you want to create"

        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        for i in range(number):
            user1 = random.choice(users)
            user2 = random.choice(users)
            seeder.add_entity(subscriptions, 1, {
                              "subscriber_user": user1, "subscribed_to_user": user2})
            seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} subs created!"))
