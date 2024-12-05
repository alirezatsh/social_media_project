from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts_shell')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ('-created',)
    
    
    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('post_page', args=(self.id, self.slug))
    
    def likes_count(self):
        self.plike.count()
    
    
class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE , related_name='rcomments' , blank=True , null=True)
    is_reply = models.BooleanField(default=False) 
    body = models.TextField(max_length=400)
    created = models.DateField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.user}-{self.body[:20]}'
    
    
class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ulike')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='plike')
    
    
    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    