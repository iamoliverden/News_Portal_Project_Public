from django.core.management.base import BaseCommand, CommandError
from fake_news_site.models import Post

class Command(BaseCommand):
    help = "Set post ratings to zero in the database"

    def handle(self, *args, **options):
        # take input y/n
        response = input("Are you sure you want to set all post ratings to 0? (y/n): ")
        if response != 'y':
            self.stdout.write(self.style.SUCCESS('Command cancelled'))
            return

        # set all likes to 0
        for post in Post.objects.all():
            post.rating_post = 0
            post.save()

        self.stdout.write(self.style.SUCCESS('Successfully set post ratings to 0'))