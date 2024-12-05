from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .models import Post , Comment , Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm , CreateCommentForm , ReplyCommentForm  , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    form_class = PostSearchForm

    def get(self , request):
        posts = Post.objects.all()
        if request.GET.get('search'):
           posts = posts.filter(body__contains = request.GET['search'])
        return render(request , 'home/first.html' , {'posts': posts , 'form':self.form_class})
    
    
    
class PostView(View):
    
    form_class = CreateCommentForm
    form_class_reply = ReplyCommentForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post , pk=kwargs['post_id'], slug=kwargs['post_slug']) 
        return super().setup(request, *args, **kwargs)
    def get(self , request , *args , **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply = False)
        return render(request , 'home/detail.html' , {'post': self.post_instance ,
                                                      'comments': comments ,
                                                      'form' : self.form_class ,
                                                      'reply_form':self.form_class_reply
                                                      })
    @method_decorator(login_required)
    def post(self , request , *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request , 'you have successfully send a message')
            return redirect('post_page' ,  self.post_instance.id , self.post_instance.slug)
        
        
class ReplyView(LoginRequiredMixin , View):
    form_class = ReplyCommentForm
    
    def post(self , request , post_id , comment_id):
        post = get_object_or_404(Post , id = post_id)
        comment = get_object_or_404(Comment , id = comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment 
            reply.is_reply = True
            reply.save()
            messages.success(request , 'you have replied this message')
        return redirect('post_page' , post.id , post.slug)
    
class DeleteView(LoginRequiredMixin,  View):
    def get(self , request , post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , 'you have successfully deleted this post')
        else:
            messages.error(request , 'you do not have permission to delete this')
        return redirect('home_page')
    
    
class UpdateView(LoginRequiredMixin , View):
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you do not have permission to update')
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request, *args , **kwargs): 
       post = self.post_instance
       form = PostCreateUpdateForm(instance=post)
       return render(request, 'home/update.html', {'form': form})
    
    def post(self, request, *args , **kwargs):
        post = self.post_instance
        form = PostCreateUpdateForm(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.slug = slugify(form.cleaned_data['body'][:10])  # تولید اسلاگ جدید
            updated_post.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('post_page', post_id=updated_post.id, post_slug=updated_post.slug)
        else:
            return render(request, 'home/update.html', {'form': form})
        
        
class CreateView(LoginRequiredMixin , View):
    def get(self, request, *args, **kwargs):
        form = PostCreateUpdateForm
        return render(request , 'home/create.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = PostCreateUpdateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:10])
            new_post.user = request.user  # تنظیم کاربر به عنوان نویسنده پست
            new_post.save()
            messages.success(request , 'you have successfully created a post')
            return redirect('post_page', post_id=new_post.id, post_slug=new_post.slug)
        else:
            return render(request , 'home/create.html', {'form':form})
        
        
        
        
class PostLikeView(LoginRequiredMixin , View):
    def get(self , request , post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(post = post , user=request.user)
        if like.exists():
            messages.error(request , 'you have already liked this post')
        else:
            Like.objects.create(post=post , user=request.user)
            messages.success(request , 'you have successfully liked this post')
        return redirect('post_page' , post.id , post.slug)


