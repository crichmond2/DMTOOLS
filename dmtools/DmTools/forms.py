from django import forms
from .models import *
from django.core.validators import validate_unicode_slug
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import PasswordInput

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
class LoginForm(AuthenticationForm):
  username = forms.CharField(label="Username",
                             widget=forms.TextInput(attrs={'placeholder':"Username"}),required = True,
                             validators=[validate_unicode_slug]
                             )
  password = forms.CharField(label="Password",widget=PasswordInput(),required = True) 
class CampaignForm(forms.Form):
  Name = forms.CharField(label="Campaign Name")
  NumPlayer = forms.IntegerField()
  DmName = forms.CharField(label="Dm Name")
  class Meta:
    model = Campaigns
    fields = ("Name","Num_Players","DmName")
  def save(self,commit=True):
    Camp = Campaigns()
    Camp.Name = self.cleaned_data['Name']
    Camp.Num_Players = self.cleaned_data['NumPlayer']
    Camp.DmName = self.cleaned_data['DmName']
    if(commit==True):
      Camp.save()
    return Camp
