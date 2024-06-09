from django import template
import urllib
from backend.models import *

register = template.Library()

@register.simple_tag
def school_image_url(author):
    # assuming you have a dictionary that maps school names to image URLs
    post = Post.objects.get(headline=author.school)
    return post.thumbnail.url

@register.simple_tag
def commentsss(post):
    # assuming you have a dictionary that maps school names to image URLs
    post = DienDanComment.objects.filter(post=post)
    return post