from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import datetime

# Create your models here.

class Developer(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    email = models.CharField(max_length = 200, blank = True)
    twitter = models.CharField(max_length = 140, blank = True)
    skype = models.CharField(max_length = 75, blank = True)
    url = models.CharField(max_length = 200, blank = True)
    notes = models.TextField(blank = True)
    mailing_address = models.CharField(max_length = 300, blank = True)
    prior_contact = models.BooleanField(default = False)
    date_created = models.DateTimeField(default = datetime.datetime.now)

    def __unicode__(self):
	return self.name

    class Meta:
        ordering = ['name']

class PointOfContact(models.Model):
    name = models.CharField(max_length = 200)
    developer = models.ForeignKey(Developer)
    email = models.EmailField()
    notes = models.TextField(blank = True)

    def __unicode__(self):
        contact = unicode(self.developer.name) +" "+ self.name 
        return contact
    class Meta:
        ordering = ['developer']


class Game(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    developer = models.ForeignKey(Developer)
    lastyear = models.BooleanField()
    url = models.CharField(max_length = 200, blank = True)
    notes = models.TextField(blank = True)
    genre = models.ForeignKey('ThemeBlock', blank = True, null = True)
    date_created = models.DateTimeField(default = datetime.datetime.now)

    def __unicode__(self):
	return self.name
    class Meta:
        ordering = ['name']


class ThemeBlock(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']


class GameForm(ModelForm):
    #override developer form for more customization
    developer = forms.ModelChoiceField(queryset  = Developer.objects.all().order_by('name' ), empty_label = 'Add new developer:')
    class Meta:
        model = Game
        fields = '__all__'

    def clean_name(self):
        if Game.objects.filter(name__iexact = self.cleaned_data.get('name')).count() > 0:
            raise ValidationError('Duplicate game!')
        return self.cleaned_data.get('name')

#this one probably needs work
#in fact, I'm sure it's missing some important validation
    '''
    def clean_developer(self):
        try:
            if not self.developer:
                raise ValidationError('Duplicate dev and/or you fucked up the form in a non-standard way.')
            return self.cleaned_data.get('developer')
        except AttributeError as e:
            return ValidationError('Something *really* fucked up*')
    '''
#helper function to try to insert missing developer
#it doesn't really work
    def get_developer(self, dev):
        try:
            self.developer.data = dev
            return True
        except:
            return False

class DeveloperForm(ModelForm):
    # TODO: make notes smaller
    #notes = forms.TextField = 
    class Meta:
        model = Developer
        fields = '__all__'
    def clean_name(self):
        if Developer.objects.filter(name__iexact = self.cleaned_data.get('name')).count() > 0:
            raise ValidationError('Duplicate dev!')
        return self.cleaned_data.get('name')

