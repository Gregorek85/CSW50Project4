from django.core.management.base import BaseCommand, CommandError
from network.models import User, Post


class Command(BaseCommand):
    help = "Used to make 10 test posts per user that does NOT have any posts"

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            if not user.number_of_posts:
                for i in range(10):
                    Post.objects.create(
                        author=user,
                        content=f"This is test post no {i} by user {user.username}",
                    )
