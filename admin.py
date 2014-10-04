from django.contrib import admin

from submit.models import Game, Developer, ThemeBlock, PointOfContact
# Register your models here.

class GameInline(admin.StackedInline):
    model = Game

class POCInline(admin.StackedInline):
    model = PointOfContact

class DeveloperAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'prior_contact', 'twitter', 'skype', 'url', 'notes', 'mailing_address']

    inlines = [POCInline, GameInline]

class GameAdmin(admin.ModelAdmin):
    fields = ['name', 'developer', 'lastyear', 'url','genre', 'notes']

class ThemeBlockAdmin(admin.ModelAdmin):
    fields = ['name']

class PointOfContactAdmin(admin.ModelAdmin):
    fields = ['name', 'developer', 'email', 'notes']

admin.site.register(Game, GameAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(ThemeBlock, ThemeBlockAdmin)
admin.site.register(PointOfContact, PointOfContactAdmin)
