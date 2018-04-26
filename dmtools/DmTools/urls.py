from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$',views.home,name='home'),
  url(r'^Signin/$',views.signin,name="Signin"),
  url(r'^Signin/Signin/$',views.signin,name='SigninHelp'),
  url(r'^register/$',views.register,name='Register'),
  url(r'^logout/$',views.Logout,name='logout'),
]
