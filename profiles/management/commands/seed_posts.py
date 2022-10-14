from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth.models import User
from posts.models import posts
import random


class Command(BaseCommand):

    help = "This command creates many posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many posts do you want to create"

        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        for i in range(number):
            user = random.choice(users)
            seeder.add_entity(posts, 1, {"user": user})
            seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} posts created!"))
