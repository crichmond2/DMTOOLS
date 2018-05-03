from django import forms
from .models import *
from django.core.validators import validate_unicode_slug
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import PasswordInput

ACCEPT=(
  ('Accept','Accept'),
  ('Decline','Decline'))
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
class NewCharacterForm(forms.Form):
  user = forms.CharField(required = True)
  Name = forms.CharField(required = True)
  ClassLevel = forms.CharField(label="Class and Level",required = False,initial="none")
  BackGround = forms.CharField(required = False,initial="none")
  Race = forms.CharField(required = False,initial="none")
  Alignment = forms.CharField(required = False,initial="none")
  ExperiencePoints = forms.IntegerField(required = False,initial=0)
  ArmorClass = forms.IntegerField(required = False,initial=0)
  Inititative = forms.IntegerField(required = False,initial=0)
  Speed = forms.IntegerField(required = False,initial=0)
  ProficiencyBonus = forms.IntegerField(required = False,initial=0)
  Strength = forms.IntegerField(required = False,initial=0)
  Dexterity = forms.IntegerField(required = False,initial=0)
  Constitution = forms.IntegerField(required = False,initial=0)
  Intelligence = forms.IntegerField(required = False,initial=0)
  Wisdom = forms.IntegerField(required = False,initial=0)
  Charisma = forms.IntegerField(required = False,initial=0)
  Acrobatics = forms.IntegerField(required = False,initial=0)
  AnimalHandling = forms.IntegerField(required = False,initial=0)
  Arcana = forms.IntegerField(required = False,initial=0)
  Athletics = forms.IntegerField(required = False,initial=0)
  Deception = forms.IntegerField(required = False,initial=0)
  History = forms.IntegerField(required = False,initial=0)
  Insight = forms.IntegerField(required = False,initial=0)
  Intimidation = forms.IntegerField(required = False,initial=0)
  Investigation = forms.IntegerField(required = False,initial=0)
  Medicine = forms.IntegerField(required = False,initial=0)
  Nature = forms.IntegerField(required = False,initial=0)
  Perception = forms.IntegerField(required = False,initial=0)
  Performance = forms.IntegerField(required = False,initial=0)
  Persuasion = forms.IntegerField(required = False,initial=0)
  Religion = forms.IntegerField(required = False,initial=0)
  SleightOfHand = forms.IntegerField(required = False,initial=0)
  Stealth = forms.IntegerField(required = False,initial=0)
  Survival = forms.IntegerField(required = False,initial=0)
  PassiveWisdom = forms.IntegerField(required = False,initial=0)
  Proficiencies = forms.IntegerField(required = False,initial=0)
  Languages = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  HitPointMaximum = forms.IntegerField(required = False,initial=0)
  Cantrips = forms.CharField(required = False,initial="none")
  SpellSlots = forms.CharField(required = False,initial="none")
  PreparedSpells = forms.CharField(required = False,initial="none")
  Spellbook = forms.CharField(required = False,initial="none")
  Equipment  = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  PersonalityTraits = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  Ideals = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  Bonds = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  Flaws = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  SpellcastingAbility = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  ArcaneRecovery = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  Darkvision = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  FeyAncestry = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  Trance = forms.CharField(widget = forms.Textarea,required = False,initial="none")
  ShelterOfTheFaithful = forms.CharField(widget = forms.Textarea,required = False,initial="none")

  class Meta:
    model = Characters
    fields = ("user","Name")
  def save(self,commit=True):
    Char = Characters()
    user = User.objects.get(username=self.cleaned_data['user'])
    Char.user = user
    Char.Name = self.cleaned_data['Name']
    Char.ClassLevel = self.cleaned_data['ClassLevel']
    Char.Background = self.cleaned_data['BackGround']
    Char.Race = self.cleaned_data['Race']
    Char.Alignment = self.cleaned_data['Alignment']
    Char.ExpierincePoints = self.cleaned_data['ExperiencePoints']
    Char.ArmorClass = self.cleaned_data['ArmorClass']
    Char.Initiative = self.cleaned_data['Inititative']
    Char.Speed = self.cleaned_data['Speed']
    Char.ProficencyBonus = self.cleaned_data['ProficiencyBonus']
    Char.Strength = self.cleaned_data['Strength']
    Char.Dexterity = self.cleaned_data['Dexterity']
    Char.Constituion = self.cleaned_data['Constitution']
    Char.Inteligence = self.cleaned_data['Intelligence']
    Char.Wisdom = self.cleaned_data['Wisdom']
    Char.Charisma = self.cleaned_data['Charisma']
    Char.Acrobatics = self.cleaned_data['Acrobatics']
    Char.AnimalHandling = self.cleaned_data['AnimalHandling']
    Char.Arcana = self.cleaned_data['Arcana']
    Char.Athletics = self.cleaned_data['Athletics']
    Char.Deception = self.cleaned_data['Deception']
    Char.History = self.cleaned_data['History']
    Char.Insight = self.cleaned_data['Insight']
    Char.Intimidation = self.cleaned_data['Intimidation']
    Char.Investigation = self.cleaned_data['Investigation']
    Char.Medicine = self.cleaned_data['Medicine']
    Char.Nature = self.cleaned_data['Nature']
    Char.Perception = self.cleaned_data['Perception']
    Char.Performance = self.cleaned_data['Performance']
    Char.Persuasion = self.cleaned_data['Persuasion']
    Char.Religion = self.cleaned_data['Religion']
    Char.SleightOfHand = self.cleaned_data['SleightOfHand']
    Char.Stealth = self.cleaned_data['Stealth']
    Char.Survival = self.cleaned_data['Survival']
    Char.PassiveWisom = self.cleaned_data['PassiveWisdom']
    Char.Proficiencies = self.cleaned_data['Proficiencies']
    Char.Languages = self.cleaned_data['Languages']
    Char.HitPointMaximum = self.cleaned_data['HitPointMaximum']
    Char.Cantrips = self.cleaned_data['Cantrips']
    Char.SpellSlots = self.cleaned_data['SpellSlots']
    Char.PreparedSpells = self.cleaned_data['PreparedSpells']
    Char.Spellbook = self.cleaned_data['Spellbook']
    Char.Equipment = self.cleaned_data['Equipment']
    Char.PersonalityTraits = self.cleaned_data['PersonalityTraits']
    Char.Ideals = self.cleaned_data['Ideals']
    Char.Bonds = self.cleaned_data['Bonds']
    Char.Flaws = self.cleaned_data['Flaws']
    Char.SpellcastingAbility = self.cleaned_data['SpellcastingAbility']
    Char.ArcaneRecovery = self.cleaned_data['ArcaneRecovery']
    Char.Darkvision = self.cleaned_data['Darkvision']
    Char.FeyAncestry = self.cleaned_data['FeyAncestry']
    Char.Trance = self.cleaned_data['Trance']
    Char.ShelterOfTheFaithful = self.cleaned_data['ShelterOfTheFaithful']
    if commit:
      Char.save()
    return Char
class CampaignForm(forms.Form):
  Name = forms.CharField(label="Campaign Name")
  NumPlayer = forms.IntegerField()
  DmName = forms.CharField(label="Dm Name")
  Password = forms.CharField(widget=PasswordInput())
  class Meta:
    model = Campaigns
    fields = ("Name","Num_Players","DmName","Password")
  def save(self,commit=True):
    Camp = Campaigns()
    Camp.Name = self.cleaned_data['Name']
    Camp.Num_Players = self.cleaned_data['NumPlayer']
    Camp.DmName = self.cleaned_data['DmName']
    Camp.Password = self.cleaned_data['Password']
    if(commit==True):
      Camp.save()
    return Camp
#class PlayerForm(forms.Form):
#	Campaign
class SearchForm(forms.Form):
	Name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Search for Campaign'}),required=True)
class AddPlayerForm(forms.Form):
  Name = forms.CharField(label="Name",
                         widget=forms.TextInput(attrs={'placeholder':'Player Name'}),required=True)
class InviteForm(forms.Form):
  Campaign = forms.CharField()
  accept = forms.ChoiceField(choices=ACCEPT)
class JoinCampaignForm(forms.Form):
  Campaign = forms.CharField(label="Campaign Name")
  Password = forms.CharField(label="Password",
                             widget=PasswordInput())
def get_choices(user):
  print(user)
  m_User = User.objects.all().filter(username = user)
  print(m_User)
  characters = Characters.objects.all().filter(user=m_User).select_related().values_list("Name",flat=True)
  Chars = list(characters)
  chars = []
  for x in Chars:
    chars.append([x,x])
  print("GET CHOICES" + str(tuple(chars)))
  return tuple(chars) 
class AddCharacterForm(forms.Form):

  #def __init__(self,campaign,user,*args,**kwargs):
  #  super(AddCharacterForm,self).__init__(*args,**kwargs)
  #  self.fields['Campaign'] = campaign
  #  self.valid=False
  #  m_user = user
  #  if(m_user != "None"):
  #    self.fields['Name'] = forms.ChoiceField(choices=get_choices(m_user))
  Campaign = forms.CharField(label="Campaign Name")
  #characters = Characters.objects.all().filter(user=user).select_related().values_list("Name",flat=True)
  #Characters = list(characters)
  Name = forms.ChoiceField(label = ": Add a Character",choices = ACCEPT)

