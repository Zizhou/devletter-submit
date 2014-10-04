#custom validators
#I should probably learn how this *really* works at some point

from django.core.exceptions import ValidationError

#raise validation error if duplicate game name exists
def validate_game_name(value):
    if Game.objects.filter(name__iexact = value).count > 0:
        msg  = 'Game aleady exists!'
        raise ValidationError(msg)
    return value
