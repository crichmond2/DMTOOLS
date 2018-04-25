from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User

def home(request):
	return render(request,"home.html")
def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		print(str(form.is_valid()))
		if not form.is_valid():
			print("HTLL")
			User.objects.create_user(username=form.cleaned_data['Username'],
															 email=form.cleaned_data['email'],
															 password=form.cleaned_data['Password'])
#			data = {'user':form.cleaned_data['username']
#			user = RegistrationForm()
#			user.username = form.cleaned_data['username']
#			user.save(commit=True)
			return redirect("/")
	else:
		form = RegistrationForm()
	context = {"form":form,"Users":User.objects.all()}
	return render(request,"home.html",context)
		
# Create your views here.
