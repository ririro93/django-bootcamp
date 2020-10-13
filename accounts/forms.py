from django import forms
from django.contrib.auth import get_user_model

non_allowed_usernames = ['abc']
# check for unique email & username
# from auth.models import User 이렇게 하지 말고
User = get_user_model() # 이렇게 하기

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    ) 
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password",
            }
        )
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    )
    
    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
        
        
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username) # iexact -> capitalization 무시
        if username in non_allowed_usernames:
            raise forms.ValidationError("this is a invalid user.")
        if qs.exists():
            raise forms.ValidationError("this is a invalid user.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email) # iexact -> capitalization 무시
        if qs.exists():
            raise forms.ValidationError("this is a invalid user.")
        return email