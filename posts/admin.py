from django.contrib import admin
from posts.models import Hashtag, Post, Comment
# Register your models here.


admin.site.register(Hashtag)
admin.site.register(Post)
admin.site.register(Comment)

