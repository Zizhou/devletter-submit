from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class Developer(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    email = models.CharField(max_length = 200, blank = True)
    twitter = models.CharField(max_length = 140, blank = True)
    skype = models.CharField(max_length = 75, blank = True)
    url = models.CharField(max_length = 200, blank = True)
    notes = models.TextField(blank = True)
    mailing_address = models.CharField(max_length = 300, blank = True)

    def __unicode__(self):
	return self.name

class Game(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    developer = models.ForeignKey(Developer)
    lastyear = models.BooleanField()
    url = models.CharField(max_length = 200, blank = True)

    GENRE_CHOICES = (
        ('Spoopy', 'Spoopy'),
        ('Not-Spoopy', 'Not-Spoopy'),
    )

    genre = models.CharField(max_length = 100, choices =  GENRE_CHOICES, blank = True)

    def __unicode__(self):
	return self.name

#I wonder if it's bad form(hurr..) to put this here and not a forms.py file...?
#TODO: custom name fields


class GameForm(ModelForm):
    #override developer form for more customization
    developer = forms.ModelChoiceField(queryset  = Developer.objects.all().order_by('name' ), empty_label = 'Add new developer:')
    class Meta:
        model = Game
        fields = '__all__'

class DeveloperForm(ModelForm):
    # TODO: make notes smaller
    #notes = forms.TextField = 
    class Meta:
        model = Developer
        fields = '__all__'
