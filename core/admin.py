from django.contrib import admin

from .models import Profile, Post, Like

admin.site.register(Profile)
admin.site.register(Like)


# add search fields to the admin panel
class PostAdmin(admin.ModelAdmin):
    search_fields = ['author', 'caption']
    list_filter = ['created_at', 'author']
    list_display = ['author', 'caption', 'created_at']


admin.site.register(Post, PostAdmin)
