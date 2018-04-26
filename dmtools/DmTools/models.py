from django.db import models

class Campaigns(models.Model):
  Name = models.CharField(max_length=500)
  Number_Player = models.IntegerField()
  DmName = models.CharField(max_length=150)
  def save(self,commit = True, *args, **kwargs):
    if(commit==True):
      super(Campaigns,self).save(*args,**kwargs)
class Players(models.Model):
  Campaign = models.ForeignKey(Campaigns,on_delete=models.CASCADE,related_name="players")
  user = models.CharField(max_length=150)
  def save(self,*args,**kwargs):
    super(Players,self).save(*args,**kwargs)

# Create your models here.
