from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Developer(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    email = models.EmailField(max_length = 75, blank = True)
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


