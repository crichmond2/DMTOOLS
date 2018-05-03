from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$',views.home,name='home'),
  url(r'^Signin/$',views.signin,name="Signin"),
  url(r'^Signin/Signin/$',views.signin,name='SigninHelp'),
  url(r'^register/$',views.register,name='Register'),
  url(r'^profile/(?P<USER>.*)/$',views.profile,name='profile'),
	url(r'^add_campaign/$',views.AddCamp,name='AddCampaign'),
	url(r'^Campaign/(?P<CAMPAIGN>.+)/$',views.Campaign,name='Campaign'),
  url(r'^add_char/(?P<CAMPAIGN>.+)/$',views.add_char,name='Add Character'),
  url(r'^town_gen/$',views.TownGen,name="Town Generator"),
  url(r'^new_character/$',views.new_character,name = 'new Character'),
  url(r'^change_char/(?P<CAMPAIGN>.+)/$',views.change_char,name='Change Character'),
  url(r'^Character/(?P<CHARACTER>.+)/$',views.char_page,name="Edit Char"),
	url(r'^join_campaign/$',views.JoinCamp,name='JoinCampaign'),
  url(r'^logout/$',views.Logout,name='logout'),
]
