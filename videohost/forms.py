from django import forms
from django.contrib.auth.models import *

from .models import *


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password don\'t match")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick', 'name', 'surname', 'age', 'avatar', 'cover', 'about']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'preview', 'video_file', 'description', 'tags', 'cat']

class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'preview', 'video_file', 'description', 'tags', 'cat']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']