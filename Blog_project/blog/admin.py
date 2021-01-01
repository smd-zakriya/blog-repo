from django.contrib import admin
from .models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','slug','author','publish','status']
    list_filter=['status','author']
    prepopulated_fields={'slug':('title',)}
    search_fields=('title',)
    raw_id_fields=('author',)
    ordering=['status','publish']
    date_hierarchy='publish'

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','comment','added','status']
    search_fields=('name','comment')
    date_hierarchy='added'
    ordering=['status','added']
    list_filter=['status','name']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)


