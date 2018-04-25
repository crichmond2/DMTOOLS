from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class RegistrationForm(UserCreationForm):
	Email = forms.EmailField(widget = forms.TextInput(attrs={'placeholder':'example@example.com'}),required = True)
	Username = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Username'}),required = True)
	Firstname = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'First Name'}),required = True)
	Lastname = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Last Name'}),required = True)
	Password1 = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Password'}),required = True)
	Password2 = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'re-enter Password'}),required = True) 
	class Meta:
		model = User
		fields = ("Email","Username","Firstname","Lastname","Password1","Password2")
	def save(self,commit=True):
		user = super(RegistrationForm,self).save(commit=False)
		user.first_name = self.cleaned_data["Firstname"]
		user.last_name = self.cleaned_data["Lastname"]
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

