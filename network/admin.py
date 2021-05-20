from django.contrib import admin
from .models import User, Post, Profile, Like,Pic

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Pic)


