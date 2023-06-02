from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from core.models import Profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50,)
	last_name = forms.CharField(max_length=70)
	class Meta:
		model = User
		fields = ["username",'first_name','last_name','email',"password1","password2"]

class AddProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['profile_pic','bio',]

class PrivacyForm(UserChangeForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50,)
	last_name = forms.CharField(max_length=70)
	class Meta:
		model = User
		fields = ["username",'first_name','last_name','email',]

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2',)