from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import UserCreationForm

def home(request):
  loggedin_user = "NULL"
  #if request.user.is_authenticated():
  DmFor = list()
  Playerfor = list()
  if request.user.is_authenticated:
    user = request.user.get_username()
    print(user)
    Dmfor = Campaigns.objects.all().filter(DmName=user).values_list('Name',flat=True)
    playerfor = Players.objects.all().filter(user=request.user.get_username()).values_list('Campaign',flat=True)
    DmFor = list(Dmfor)
    Playerfor = list(playerfor)
    print(DmFor)
  loggedin_user = request.user.get_username()
  context = {"Users":User.objects.all(),"User":loggedin_user,"DM":DmFor,"Player":Playerfor}
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
  if request.method == "POST":
    form = InviteForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
      if form.cleaned_data['accept'] == "Accept":
        Tcamp = Campaigns.objects.get(Name=form.cleaned_data['Campaign'])
        player = Players.objects.create(Campaign=camp,user = USER)
        invites = Invitations.objects.filter(Campaign=form.cleaned_data['Campaign']).filter(User=USER).delete()

        
  form = CampaignForm()
  Dmfor = Campaigns.objects.all().filter(DmName=USER).values_list('Name',flat=True)
  playerfor = Players.objects.all().filter(user=USER).values_list('Campaign',flat=True)
  invites = Invitations.objects.all().filter(User=USER).values_list('Campaign',flat=True)
  DmFor = list(Dmfor)
  Playerfor = list(playerfor)
  Invites = list(invites)
  if Invites ==  None:
    camp = {"Campaign":Invites[0]}
    Form = InviteForm(camp)
  Form = InviteForm()
  context = {"Username":USER,"Form":Form,"form":form,"DmFor":DmFor,"Player":Playerfor,"Invites":Invites}
  return render(request,"profile.html",context)

def AddCamp(request):
	if request.method == "POST":
		form = CampaignForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get("Name")
			form.save()
			return redirect("/Campaign/"+name)
	form = CampaignForm()
	context = {'form':form,'Username':request.user.get_username()}
	print("Im Here")
	return render(request,"addcampaign.html",context)

def JoinCamp(request):
	if request.method == "POST":
		Form = SearchForm(request.POST)
		if Form.is_valid():
			name = Form.cleaned_data.get('Name')
			Camps = Campaigns.objects.all().filter(Name=name).values_list('Name',flat=True)
			Camp_l = list(Camps)
			Found = list()
			form = SearchForm()
			searched = True
			context = {'form':form,'Found':Camp_l,'Searched':searched}
			return render(request,'campaignsearch.html',context)
	form = SearchForm()
	searched = False
	context = {'form':form,'Searched':searched}
	return render(request,'campaignsearch.html',context)
def Campaign(request,CAMPAIGN):
  player = list()
  DM = Campaigns.objects.all().filter(Name=CAMPAIGN).values_list("DmName",flat=True)
  dm = list(DM)
  thedm = dm[0]
  #print(thedm)
  if request.user.get_username() == thedm:
    owner = True
  else:
    owner = False
  print(CAMPAIGN)
  print(owner)
  if request.method == "POST" and owner == False:
    print("HERE")
    Form = JoinCampaignForm(request.POST)
    if Form.is_valid():
      campaign = Campaigns.objects.get(Name=CAMPAIGN)
      if campaign.Password == Form.cleaned_data['Password']:
        Players.objects.create(Campaign=campaign,user = request.user.get_username())
        player = True
        DM = Campaigns.objects.all().filter(Name=CAMPAIGN).values_list("DmName",flat=True)
        dm = list(DM)
        thedm = dm[0]
        if request.user.get_username() == thedm:
          owner = True
        else:
          owner = False
        campaign = Campaigns.objects.get(Name = CAMPAIGN)
        players = Players.objects.all().filter(Campaign=campaign.Name).select_related().filter(Campaign=campaign.Name).values_list("user",flat=True)
        characters = Characters.objects.all().filter(user=request.user).select_related().values_list("Name",flat=True)
        Chars = list(characters)
        user = request.user.username
        form = AddPlayerForm() 
        info = {'Campaign':CAMPAIGN}
        Form = JoinCampaignForm(info) 
        chars = []
        for x in Chars:
          chars.append([x,x])
        charform = AddCharacterForm(choices = tuple(chars))
        context = {'players':players,'player':player,"Characters":charform,"Page":CAMPAIGN,"form":form,"Username":user,"Search":player,"Owner":owner,"Form":Form}
        return render(request,"Campaign.html",context)
      else:
        return redirect("/Campaign/" + CAMPAIGN + "/")
  if request.method == "POST" and owner == True:
    Form = AddPlayerForm(request.POST)
    if Form.is_valid():
      players = User.objects.all().filter(username = Form.cleaned_data['Name'] ).values_list("username",flat=True)
      Users=list(players)
      print(Users)
      form=AddPlayerForm()
      campaign = Campaigns.objects.get(Name = CAMPAIGN)
      players = Players.objects.all().filter(Campaign=campaign.Name).select_related().filter(Campaign=campaign.Name).values_list("user",flat=True)
      form = AddPlayerForm() 
      DM = Campaigns.objects.all().filter(DmName=request.user.get_username()).values_list("DmName",flat=True)
      dm = list(DM)
      thedm = dm[0]
      invite = Invitations.objects.create(Campaign = CAMPAIGN,DM = thedm,User = Form.cleaned_data['Name'])
      invite.save()
      print(thedm)
      if request.user.get_username() == thedm:
        owner = True
      else:
        owner = False
      context = {'players':players,"Page":CAMPAIGN,"form":form,"Search":Users,"Owner":owner}
      return render(request,"Campaign.html",context)
  DM = Campaigns.objects.all().filter(Name=CAMPAIGN).values_list("DmName",flat=True)
  dm = list(DM)
  thedm = dm[0]
  #print(thedm)
  if request.user.get_username() == thedm:
    owner = True
  else:
    owner = False
  campaign = Campaigns.objects.get(Name = CAMPAIGN)
  players = Players.objects.all().filter(Campaign=campaign.Name).select_related().filter(Campaign=campaign.Name).values_list("user",flat=True)
  charac = Players.objects.all().filter(Campaign=campaign.Name).select_related().values_list("Character",flat=True)

  characters = Characters.objects.all().filter(user=request.user).select_related().values_list("Name",flat=True)
  Chars = list(characters)
  for x in players:
    if x == request.user.get_username():
      Player = True
      break
    else:
      Player = False
  user = request.user.username
  form = AddPlayerForm() 
  info = {'Campaign':CAMPAIGN}
  Form = JoinCampaignForm(info) 
  chars = []
  for x in Chars:
    chars.append([x,x])
  values = {"Campaign":CAMPAIGN,"Name":tuple(chars)}
  charform = AddCharacterForm(user=request.user.get_username())#choices = tuple(chars))
  #charform.fields['Campaign']=CAMPAIGN
  #print(players)
  #print(player)
  #print(CAMPAIGN)
  #print(user)
  #print(player)
  #print(owner)
  print(charac)
  context = {'players':players,'player':Player,"chars":charac,"Characters":charform,"Page":CAMPAIGN,"form":form,"Username":user,"Search":player,"Owner":owner,"Form":Form}
  #print(context)
  return render(request,"Campaign.html",context)
def add_char(request,CAMPAIGN):
  if request.method == "POST":
    print("ASDASDASD")
    print(request.POST['Name'])
    champ = Campaigns.objects.get(Name=CAMPAIGN)
    play = Players.objects.all().filter(Campaign=champ.Name).select_related().get(user=request.user.get_username())
    play.Character = request.POST['Name']
    play.save()
    return redirect("/Campaign/"+CAMPAIGN+"/")
  return redirect("/Campaign/"+CAMPAIGN+"/")

def Logout(request):
  logout(request)
  return redirect("/")
# Create your views here.
