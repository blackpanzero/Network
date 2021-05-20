from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Pic(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE, related_name='photos')
    photolink=models.CharField(max_length=255,default='https://i.stack.imgur.com/34AD2.jpg')


class Profile(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='folowers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    @property
    def num_likes(self):
        return self.liked.all().count()

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user":self.user.username,
            "timestamp": self.date.strftime("%b %-d %Y, %-I:%M %p"),
           
   
        }
        


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.post)






