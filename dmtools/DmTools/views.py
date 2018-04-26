from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import UserCreationForm

def home(request):
  loggedin_user = "NULL"
  #if request.user.is_authenticated():
  loggedin_user = request.user.get_username()
  context = {"Users":User.objects.all(),"User":loggedin_user}
  return render(request,"home.html",context)
def signin(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    print(user)
    if user is not None:
      login(request,user)
      return redirect("home")
    #print(str(form.is_valid()))

    #if form.is_valid():
     # username = form.cleaned_data.get("Username")
     # password = form.cleaned_data.get("Password")
     # user = authenticate(username=username,password=password)
     # login(request,user)
     # return redirect("home")
  else:
    form = LoginForm()
  context = {"SIform":form}
  return render(request,"signin.html",context)
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
    form2 = LoginForm()    
  context = {"form":form,"SIform":form2}
  return render(request,"register.html",context)
def profile(request,USER):
  form = CampaignForm()
  Dmfor = Campaigns.objects.all().filter(DmName=USER).values_list('Name',flat=True)
  DmFor = list(Dmfor)

  context = {"Username":USER,"form":form,"DmFor":DmFor}
  return render(request,"profile.html",context)
		
def Logout(request):
  logout(request)
  return redirect("/")
# Create your views here.
