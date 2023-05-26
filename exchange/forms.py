from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Book
from django import forms
from django.contrib.auth import authenticate,get_user_model



class myUserCreationform(UserCreationForm):
    email = forms.EmailField(required=True)
    has_books = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'has_books']


class myUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')
            
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
        
        return super(UserLoginForm, self).clean(*args,**kwargs)
user=get_user_model()

class add_book(forms.ModelForm):
    author=forms.CharField()
    title=forms.CharField()
    class Meta:
        model=Book
        fields=["author","title"]


class AcceptForm(forms.Form):
    request_id = forms.IntegerField(widget=forms.HiddenInput())

class RejectForm(forms.Form):
    request_id = forms.IntegerField(widget=forms.HiddenInput())

class CancelForm(forms.Form):
    request_id = forms.IntegerField(widget=forms.HiddenInput())


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='')




       