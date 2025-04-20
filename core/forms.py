from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'What’s on your mind?',
                'class': 'w-full p-2 rounded border border-gray-300',
                'maxlength': 280
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'class': 'w-full p-2 rounded border border-gray-300'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Password'
    }))


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Username'}),
            'email': forms.EmailInput(
                attrs={'class': 'w-full p-2 rounded border border-gray-300', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
