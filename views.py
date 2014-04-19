from django.shortcuts import render
from django.http import HttpResponse

from submit.models import Developer, Game
# Create your views here.

def main_page(request):
    developer = Developer.objects.all().order_by('name')
    message = 'Enter info here:'
    context = {
	'developer' : developer,
	'systemmessage' : message
    }

    return render(request, 'submit/form.html', context)

#this is the ugliest shit ever
#like, seriously, wtf
def send(request):
    testtext = 'There is no error.'
    games = Game.objects.all()
    devs = Developer.objects.all()
    halt = False

    for g in games:
	if request.POST.get('game') == g.name:
	    halt = True
	    testtext = 'duplicate game'
	    continue
    #could these have been done more elegantly? probably (definitely)
    for d in devs:
	if request.POST.get('dev-text') == d.name:
 	    halt = True
	    testtext = 'duplicate dev'
	    continue
    if request.POST.get('dev-drop') == 'NotADev' and request.POST.get('dev-text') == '':
	halt = True
	testtext = 'No dev selected'
    if request.POST.get('dev-drop') != 'NotADev' and request.POST.get('dev-text') != '':
	halt = True
	testtext = 'Two developers'
    #lazy catch all error (it's not even real exception handling)
    if halt == True:
	testtext = 'Fuck your couch: ' + testtext
	return render(request, 'submit/form.html', {
	    'developer': Developer.objects.all(),
	    'systemmessage' : testtext})
    else:
	#create and save the new record
	r = request.POST #lazy shorthand
	devname = 'There are FOUR lights'
	#create new dev record if info entered
	if request.POST.get('dev-drop') == 'NotADev':
	    devtemp = Developer(name = r.get('dev-text'), email = r.get('dev-email'), twitter = r.get('dev-twitter'))
	    devtemp.save()
	    devname = r.get('dev-text')
	else:
	    devname = r.get('dev-drop')
	#sloppy function to change POST data to boolean
	lytemp = True if r.get('lastyear') == 'True'  else False
	#the actual saving is here
	gametemp =  Game(name = r.get('game'), developer = Developer.objects.get(name = devname), lastyear = lytemp)
	gametemp.save()
	successtext = 'Success! ' + r.get('game') + ' by ' + devname + ' added!'
	return render(request, 'submit/form.html', {
	    'developer': Developer.objects.all(),
	    'systemmessage' : successtext})
