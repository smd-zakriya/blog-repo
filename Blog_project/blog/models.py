from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publish')

class Post(models.Model):
    STATUS_CHOICES=(('draft','DRAFT'),('publish','PUBLISH'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=256,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

#Comments Model
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=64)
    email=models.EmailField()
    comment=models.TextField()
    added=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    

    class Meta:
        ordering=('added',)

    def __str__(self):
        return 'Commented by {} on {}'.format(self.name,self.post)