from django.contrib import admin

from submit.models import Game, Developer
# Register your models here.

class GameInline(admin.StackedInline):
    model = Game

class DeveloperAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'twitter', 'skype', 'url', 'notes', 'mailing_address']

    inlines = [GameInline]

class GameAdmin(admin.ModelAdmin):
    fields = ['name', 'developer', 'lastyear', 'url','genre', 'notes']


admin.site.register(Game, GameAdmin)
admin.site.register(Developer, DeveloperAdmin)
