from django.contrib import admin

from submit.models import Game, Developer, ThemeBlock, PointOfContact
# Register your models here.

class GameInline(admin.StackedInline):
    model = Game

class POCInline(admin.StackedInline):
    model = PointOfContact

class DeveloperAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created']

    fields = ['name', 'email', 'prior_contact', 'twitter', 'skype', 'url', 'notes', 'mailing_address', 'date_created']

    inlines = [POCInline, GameInline]

class GameAdmin(admin.ModelAdmin):
    fields = ['name', 'developer', 'lastyear', 'url','genre', 'notes', 'date_created']
    readonly_fields = ['date_created']
class ThemeBlockAdmin(admin.ModelAdmin):
    fields = ['name']

class PointOfContactAdmin(admin.ModelAdmin):
    fields = ['name', 'developer', 'email', 'notes']

admin.site.register(Game, GameAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(ThemeBlock, ThemeBlockAdmin)
admin.site.register(PointOfContact, PointOfContactAdmin)
