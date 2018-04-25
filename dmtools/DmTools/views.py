from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def home(request):
  loggedin_user = "NULL"
  #if request.user.is_authenticated():
  loggedin_user = request.user.get_username()
  context = {"Users":User.objects.all(),"User":loggedin_user}
  return render(request,"home.html",context)
def register(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username,password=raw_password)
      login(request,user)
      return redirect("home")
  else:
	  form = UserCreationForm()
  context = {"form":form,"Users":User.objects.all()}
  return render(request,"register.html",context)
		
# Create your views here.
