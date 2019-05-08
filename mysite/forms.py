from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):

    username = forms.CharField(label="User name",widget=forms.TextInput(attrs={'class':'form-control'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError('Please check your infomation.')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data

class RegisterForm(forms.Form):

    username = forms.CharField(label="Username", min_length=3, max_length=30, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'3-30 characters.'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'At least 6 characters.'}))
    password_confirm = forms.CharField(label = "Password Confirmation",min_length = 6,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The user name already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email already exists.')
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm =self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError('Please enter the same password as before.')
        return password_confirm