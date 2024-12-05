from django.urls import path
from . import views

urlpatterns = [
    path('register/' , views.UserRegisterView.as_view() , name ='register_page'),
    path('login/' , views.UserLoginView.as_view() , name ='login_page'),
    path('logout/' , views.UserLogoutView.as_view() , name ='logout_page'),
    path('profile/<int:user_id>' , views.UserProfileView.as_view() , name ='profile_page'),
    path('reset/' , views.UserPasswordResetView.as_view() , name ='reset_password_page'),
    path('done/' , views.UserPasswordResetDoneView.as_view() , name = 'password_reset_done'),
    path('confirm/<uidb64>/<token>/' , views.UserPasswordResetConfirmView.as_view() , name = 'password_reset_confirm'),
    path('confirm/complete' , views.UserPasswordResetCompleteView.as_view() , name = 'password_reset_complete'),
    path('follow/<int:user_id>' , views.UserFollowView.as_view() , name = 'follow_page'),
    path('unfollow/<int:user_id>' , views.UserUnfollowView.as_view() , name = 'unfollow_page'),
    path('edit_user/' , views.UserEditView.as_view() , name = 'edit_page')
]
