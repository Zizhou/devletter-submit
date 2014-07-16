from django.shortcuts import render
from django.http import HttpResponse

from submit.models import Developer, Game, GameForm, DeveloperForm
# Create your views here.
# OK, I'll do that, since you asked so nicely.


###main view
#should I just switch it to a class based one? is it time?
def main_page(request):
    if request.method == 'POST':
        #preprocess to seperate prefixes because I am a bad
        game_dict = game_process(request.POST)
        dev_dict = dev_process(request.POST)
        #bound forms for validation
        gform = GameForm(game_dict)
        dform = DeveloperForm(dev_dict)
        try:
            #check validity of form data for duplicates
            gform.is_valid()
            dform.is_valid()
            print gform.cleaned_data
            print dform.cleaned_data
            #save dev entry(if one was not specified 
            if not gform.cleaned_data['developer']
                dtemp 
            #save game entry
            #gtemp = Game(gform.
            return HttpResponse('hai')
        except e:
            print e#
            return HttpResponse(str(e))
    #remember to include the custom id and prefix 
    gameform = GameForm(auto_id = '%s', prefix='game')
    devform = DeveloperForm(auto_id = '%s', prefix='dev')
    return render(request, 'submit/protoform.html', {
        'gameform' : gameform, 
        'devform' : devform,
    })

###handles game name lookup in conjunction with ajax in template
#quasi-api thing
#takes string of game title (case insensitive)
#returns False if game not present, True if it is
def name_lookup(request, name):
    present = False
    #case inensitive lookup. >0 means it presumably exists
    if Game.objects.filter(name__iexact = name).count() > 0:
        present = True        
    return HttpResponse(present)

###ugly hack to seperate out game and dev data from POST data because prefixes 
###my db field names are bad and I should feel bad
#POST goes in, all data from fields relevant to Game form come out
def game_process(POST):
    game_dict = {}

    for data in POST:
        if str(data)[:4] == 'game':
            game_dict[str(data)[5:]] = POST.get(data)
    return game_dict

#so, a more flexible function where I pass in prefix as a param would be more
#flexible, and definitely better DRY, but at this point, it's like bailing
#out the Titanic

def dev_process(POST):
    dev_dict = {}

    for data in POST:
        if str(data)[:3] == 'dev':
            dev_dict[str(data)[4:]] = POST.get(data)
    return dev_dict



###deprecated below
###apparently all of this was just *wrong*, anyway


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
