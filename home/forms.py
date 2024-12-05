from django import forms
from .models import Post , Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        
        
        
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
        
        
class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
        
class PostSearchForm(forms.Form):
    search = forms.CharField()