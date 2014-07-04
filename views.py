from django.shortcuts import render
from django.http import HttpResponse

from submit.models import Developer, Game, GameForm, DeveloperForm
# Create your views here.
# OK, I'll do that, since you asked so nicely.

def main_page(request):
    if request.method == 'POST':
#TODO validation
        gameform = GameForm(request.POST)
        devform = DeveloperForm(request.POST)

        context = {
            'devform' : devform,
            'gameform' : gameform,
        }

        return render(request, 'submit/protoform.html', context)
    else:
        gameform = GameForm(auto_id = '%s', prefix='game')
        devform = DeveloperForm(auto_id = '%s', prefix='dev')
        return render(request, 'submit/protoform.html', {
            'gameform' : gameform, 
            'devform' : devform,
        })

#facilitate game name lookup with ajax
def name_lookup(request, name):
    present = False
    #case inensitive lookup. >0 means it presumably exists
    if Game.objects.filter(name__iexact = name).count() > 0:
        present = True        
    return HttpResponse(present)

###deprecated below

def main_page_1(request):
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
    if request.POST.get('dev-drop') != 'NotADev' and request.POST.get('dev-text') != None:
	halt = True
	testtext = 'Two developers'
    #lazy catch all error (it's not even real exception handling)
    if halt == True:
	testtext = 'Fuck your couch: ' + testtext
        print request.POST.get('dev-text')
	return render(request, 'submit/form.html', {
	    'developer': Developer.objects.all().order_by('name'),
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
