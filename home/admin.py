from django.contrib import admin
from .models import Post , Comment , Like


# @admin.register('post')
class PostAdmin(admin.ModelAdmin):
    list_display = ('user' , 'slug' , 'update')
    search_fields = ('user',)
    list_filter = ['update']
    prepopulated_fields = {'slug' : ('body',)}
    raw_id_fields = ('user',)
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user' , 'post' , 'created' , 'is_reply')
    raw_id_fields = ('user', 'post' , 'reply') 
    

admin.site.register(Post , PostAdmin)
admin.site.register(Comment , CommentAdmin)
admin.site.register(Like)