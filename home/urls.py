from django.urls import path
from . import views

urlpatterns = [
    path('home/' , views.HomeView.as_view() , name='home_page'),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostView.as_view() , name='post_page'),
    path('delete/<int:post_id>' , views.DeleteView.as_view() , name='delete_page'),
    path('update/<int:post_id>', views.UpdateView.as_view() , name='update_page'),
    path('create/' , views.CreateView.as_view() , name='create_page'),
    path('reply/<int:post_id>/<int:comment_id>' , views.ReplyView.as_view() , name='reply_page'),
    path('like/<int:post_id>', views.PostLikeView.as_view() , name='like_page'),
]
