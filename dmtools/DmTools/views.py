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
  #If a user is signed in get the campaigns that they are a part of
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
    #Get the input Username and password
    username = request.POST['username']
    password = request.POST['password']
    #Try to authenticate the user with their credentials
    user = authenticate(username=username,password=password)
    print(user)
    #If the right username and password log the user in and return to home page
    if user is not None:
      login(request,user)
      return redirect("/profile/"+user.get_username()+"/")
  #If it wasn't a post, just give the user a form to fill out
  else:
    form = LoginForm()
  context = {"SIform":form}
  return render(request,"signin.html",context)





def register(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    #If all parts of the form have been filled out save the form
    if form.is_valid():
    #Save the user and get the username and password to log in the user
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username,password=raw_password)
      login(request,user)
      return redirect("/profile/"+user.get_username()+"/")
   #If user just got to the page, give them an empty form to fill out
  else:
    form = UserCreationForm()
    form2 = LoginForm()    
  context = {"form":form,"SIform":form2}
  return render(request,"register.html",context)




def profile(request,USER):
  #If the user is responding to an invite
  if request.method == "POST":
    form = InviteForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
     #And they accepted the invitation
      if form.cleaned_data['accept'] == "Accept":
      #Add the user to the Campaign and remove the invitation
        camp = Campaigns.objects.get(Name=form.cleaned_data['Campaign'])
        player = Players.objects.create(Campaign=camp,user = USER)
        invites = Invitations.objects.filter(Campaign=form.cleaned_data['Campaign']).filter(User=USER).delete()

  
  form = CampaignForm()
  Dmfor = Campaigns.objects.all().filter(DmName=USER).values_list('Name',flat=True)
  playerfor = Players.objects.all().filter(user=USER).values_list('Campaign',flat=True)
  invites = Invitations.objects.all().filter(User=USER).values_list('Campaign',flat=True)
  user = User.objects.get(username=request.user.get_username())
  Chars = Characters.objects.all().filter(user=user).values_list('Name',flat=True)
  DmFor = list(Dmfor)
  Playerfor = list(playerfor)
  Invites = list(invites)
  print(invites)
  #If the user has an invite, Fill the campaign part of the form so User doesn't have to
  if len(Invites) !=  0:
    camp = {"Campaign":Invites[0]}
    Form = InviteForm(camp)
  else:
    Form = InviteForm()
  context = {"Username":USER,"Chars":Chars,"Form":Form,"form":form,"DmFor":DmFor,"Player":Playerfor,"Invites":Invites}
  return render(request,"profile.html",context)




def AddCamp(request):
  if request.method == "POST":
    form = CampaignForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data.get("Name")
      form.save()
      return redirect("/Campaign/"+name)
  values = {'DmName':request.user.get_username()}
  form = CampaignForm(values)
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
      context = {'form':form,'Found':Camp_l,'Searched':searched,'User':request.user.get_username()}
      return render(request,'campaignsearch.html',context)
  form = SearchForm()
  searched = False
  Use = request.user.get_username()
  Dmfor = Campaigns.objects.all().filter(DmName=Use).values_list('Name',flat=True)
  playerfor = Players.objects.all().filter(user=request.user.get_username()).values_list('Campaign',flat=True)
  DmFor = list(Dmfor)
  Playerfor = list(playerfor)
  context = {'form':form,'Searched':searched,'User':Use,'DM':DmFor,'Player':Playerfor}
  return render(request,'campaignsearch.html',context)





def Campaign(request,CAMPAIGN):
  player = list()
  DM = Campaigns.objects.all().filter(Name=CAMPAIGN).values_list("DmName",flat=True)
  dm = list(DM)
  thedm = dm[0]
  #If the logged in user is the DM he is the owner of the page
  if request.user.get_username() == thedm:
    owner = True
  else:
   #Otherwise he is not
    owner = False
    """  If the user has submitted a form
         and he is not the DM of the Campaign
         then he is trying to be added to the campaign
         So we get the password he input and see if it matches the 
         password set by the DM. If it is we add him to the Campaign
         Otherwise we don't and ask for the password again
    """
  if request.method == "POST" and owner == False:
    print("HERE")
    Form = JoinCampaignForm(request.POST)
    if Form.is_valid():
      campaign = Campaigns.objects.get(Name=CAMPAIGN)
      if campaign.Password == Form.cleaned_data['Password']:
        Players.objects.create(Campaign=campaign,user = request.user.get_username())
        Player = True
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
        charac = Players.objects.all().filter(Campaign=campaign.Name).select_related().values_list("Character",flat=True)
        Chars = list(characters)
        user = request.user.username
        form = AddPlayerForm() 
        info = {'Campaign':CAMPAIGN}
        Form = JoinCampaignForm(info) 
        CHARS = []
        for x in range(len(players)):
          CHARS.append([players[x],charac[x]])
        chars = []
        for x in Chars:
          chars.append([x,x])
        #charform = AddCharacterForm()
        charform = AddCharacterForm(campaign=CAMPAIGN,user=request.user.get_username())#choices = tuple(chars))
        context = {'players':tuple(CHARS),'player':player,"Characters":charform,"Page":CAMPAIGN,"form":form,"Username":user,"Search":Player,"Owner":owner,"Form":Form}
        return redirect("/Campaign/" + CAMPAIGN + "/")
        
        #return render(request,"Campaign.html",context)
      else:
        return redirect("/Campaign/" + CAMPAIGN + "/")
  """If a form has been submitted, and the user is the DM
     Then he is trying to add someone to the campaign, so we get the
     user from the form and if they exist, then we send them an invitation
  """
  if request.method == "POST" and owner == True:
    print("ITS A POST")
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
      characters = Characters.objects.all().filter(user=request.user).select_related().values_list("Name",flat=True)
      charac = Players.objects.all().filter(Campaign=campaign.Name).select_related().values_list("Character",flat=True)
      CHARS = []
      for x in range(len(players)):
        CHARS.append([players[x],charac[x]])
      context = {'players':tuple(CHARS),"Page":CAMPAIGN,"form":form,"Search":Users,"Owner":owner}
      return render(request,"Campaign.html",context)
  DM = Campaigns.objects.all().filter(Name=CAMPAIGN).values_list("DmName",flat=True)
  dm = list(DM)
  thedm = dm[0]
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
  try: 
    Player
  except:
    Player = False
  user = request.user.username
  form = AddPlayerForm() 
  info = {'Campaign':CAMPAIGN}
  Form = JoinCampaignForm(initial={'Campaign':CAMPAIGN}) 
  chars = []
  CHARS = []
  print("BEFORE RANGE")
  for x in range(len(players)):
    CHARS.append([players[x],charac[x]])
  for x in Chars:
    chars.append([x,x])
  values = {"Campaign":CAMPAIGN,'user':request.user.get_username()}
  charform = AddCharacterForm(campaign=CAMPAIGN,user=request.user.get_username())#choices = tuple(chars))
  charform.fields['Name'].choices = tuple(chars)
  Dmfor = Campaigns.objects.all().filter(DmName=user).values_list('Name',flat=True)
  playerfor = Players.objects.all().filter(user=request.user.get_username()).values_list('Campaign',flat=True)
  DmFor = list(Dmfor)
  Playerfor = list(playerfor)
  context = {'DM':DmFor,'Player':Playerfor,'players':tuple(CHARS),'player':Player,"Characters":charform,"Page":CAMPAIGN,"form":form,"Username":user,"Search":player,"Owner":owner,"Form":Form}
  print(context)
  return render(request,"Campaign.html",context)



def add_char(request,CAMPAIGN):
  if request.method == "POST":
    champ = Campaigns.objects.get(Name=CAMPAIGN)
    play = Players.objects.all().filter(Campaign=champ.Name).select_related().get(user=request.user.get_username())
    play.Character = request.POST['Name']
    play.save()
    return redirect("/Campaign/"+CAMPAIGN+"/")
  return redirect("/Campaign/"+CAMPAIGN+"/")



def change_char(request,CAMPAIGN):
  camp = Campaigns.objects.get(Name=CAMPAIGN)
  play = Players.objects.all().filter(Campaign=camp.Name).select_related().get(user=request.user.get_username())
  play.Character = "None"
  play.save()
  return redirect("/Campaign/"+CAMPAIGN+"/")


def new_character(request):
  if request.method=="POST":
    form = NewCharacterForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/profile/'+request.user.get_username()+'/')
  values = {'user':request.user.get_username(),
            'ClassLevel':"none",
            'BackGround':"none",
            'Race':"none",
            'Alignment':"none",
            'ExperiencePoints':0,
            'ArmorClass':0,
            'Inititative':0,
            'Speed':0,
            'ProficiencyBonus':0,
            'Strength':0,
            'Dexterity':0,
            'Constitution':0,
            'Intelligence':0,
            'Wisdom':0,
            'Charisma':0,
            'Acrobatics':0,
            'AnimalHandling':0,
            'Arcana':0,
            'Athletics':0,
            'Deception':0,
            'History':0,
            'Insight':0,
            'Intimidation':0,
            'Investigation':0,
            'Medicine':0,
            'Nature':0,
            'Perception':0,
            'Performance':0,
            'Persuasion':0,
            'Religion':0,
            'SleightOfHand':0,
            'Stealth':0,
            'Survival':0,
            'PassiveWisdom':0,
            'Proficiencies':0,
            'Languages':"none",
            'HitPointMaximum':0,
            'Cantrips':"none",
            'SpellSlots':'none',
            'PreparedSpells':'none',
            'Spellbook':'none',
            'Equipment':'none',
            'PersonalityTraits':'none',
            'Ideals':'none',
            'Bonds':'none',
            'Flaws':'none',
            'SpellcastingAbility':'none',
            'ArcaneRecovery':'none',
            'Darkvision':'none',
            'FeyAncestry':'none',
            'Trance':'none',
            'ShelterOfTheFaithful':'none'
           }
  form = NewCharacterForm(values)
  context = {"CharacterForm":form}
  #return redirect('/profile/'+request.user.get_username()+'/')
  return render(request,"character.html",context)

def char_page(request,CHARACTER):
  user = User.objects.get(username=request.user.get_username())
  character = Characters.objects.filter(user=user).get(Name = CHARACTER)
  values = character.__dict__
  val = []
  for x in values:
    val.append([x,str(values.get(x,""))])
    if x == 'user_id':
      user_id = values.get(x,"")
      user_name = User.objects.get(pk=user_id)
      val.append(['user',user_name])
      print(user_name)
  print(dict(val))
  form = NewCharacterForm(dict(val))
  #form.user = "BITCH"#request.user.get_username()
  form.fields['user'].initial = "BITCH"
  context = {"Username":request.user.get_username(),"CharForm":form}
  return render(request,"Character.html",context)

def TownGen(request):
  user = request.user.get_username()
  context = {'Username':user}
  return render(request,"towngen.html",context)

def Logout(request):
  logout(request)
  return redirect("/")
# Create your views here.
