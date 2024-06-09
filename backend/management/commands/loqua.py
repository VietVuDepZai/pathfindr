from django.core.management.base import BaseCommand
import json
from django.core.files import File
from backend.models import Post

class Command(BaseCommand):
    help = 'Import schools from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data from a file
        with open('lolang.json', 'r') as file:
            schools_data = json.load(file)

        # Iterate over the JSON objects and create database entries
        
        for post_data in schools_data:
            post = Post.objects.create(
                headline=post_data.get('headline'),
                sub_headline = post_data.get('sub_headline'),
                body = post_data.get('body'),
                active = post_data.get('active', False),
                featured = post_data.get('featured', False),
                thumbnail = post_data.get('thumbnail')
            )
            
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully imported schools'))
