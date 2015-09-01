from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from django.views.generic import View

from submit.models import *
# Create your views here.
# OK, I'll do that, since you asked so nicely.


###main view
#should I just switch it to a class based one? is it time?
def main_page(request):
    alert_message = ''
    success = ''
    if request.method == 'POST':
        #preprocess to seperate prefixes because I am a bad
        game_dict = game_process(request.POST)
        dev_dict = dev_process(request.POST)
        #bound forms for validation
        gform = GameForm(game_dict)
        dform = DeveloperForm(dev_dict)
        try:
            #gform might depend on dform, depending on whether the user selected
            #an existing dev or made a new one
            dtemp = Developer()
            gtemp = Game()
            dev_needs_saving = False
            if dform.is_valid():
                dtemp = dform.save()
                print 'dev testing'
                print dtemp.id
                gform.data['developer'] = dtemp.id
                print gform.data.get('developer')
                print '~~~~~'
                print gform.data
                print '~~~~~'
                dev_needs_saving = True
            elif 'developer' in gform.fields: 
                print gform.fields.get('developer')
                print gform.data.get('developer')
                print 'lololol'
            else:
                raise ValidationError('Developer fields are wrong, somehow!')

            #one way or another, the gform should be valid now
            #I hope
            print 'gform'
            print gform.data
            print gform.data.get('developer')
            print gform.is_valid()
            print gform.cleaned_data
            #reasons for failure:
            #duplicate dev will trigger invalid game, but only verify here
            #duplicate game will also trigger, but at least tell you why
            if gform.is_valid():
                gtemp = gform.save()
                if dev_needs_saving: dform.save()
                success = 'Success! ' + gtemp.name + ' by ' + gtemp.developer.name + ' has been added.'
            else:
                print 'gform failed'
                raise ValidationError('Something is wrong with your game fields.')
        except ValidationError as e:
            print e
            alert_message = [gform._errors, e]
    print alert_message

    #remember to include the custom id and prefix 
    gameform = GameForm(auto_id = '%s', prefix='game')
    devform = DeveloperForm(auto_id = '%s', prefix='dev')
    return render(request, 'submit/form.html', {
        'gameform' : gameform, 
        'devform' : devform,
        'success' : success,
        'alert' : alert_message,
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
#developer version of above
def dev_lookup(request, name):
    present = False
    #case inensitive lookup. >0 means it presumably exists
    if Developer.objects.filter(name__iexact = name).count() > 0:
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

'''
            if
            gtemp = Game(**gform.cleaned_data)
            #save dev entry(if one was not specified)
            if not 'developer' in gform.fields:
                dtemp = Developer(**dform.fields)
                #real validity check?
                print 'check dev valid'
                if not dform.is_valid():
                    raise ValidationError('something is wrong with the dev field!')
                
                print dtemp
                gtemp.developer = Developer(**dform.fields)
            #save game entry
            #gtemp = Game(**gform.cleaned_data)
            print 'check game valid'
            print gform.fields
            if not gform.is_valid():
                raise ValidationError('something is wrong with the game field!')
            print gtemp
            alert_message = 'Success! ' + gtemp.name + ' by ' + gtemp.developer.name + ' was successfully added.'
        #has something gone horribly wrong?
        except ValidationError as e:
            print e#
            alert_message = str(e)
'''

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

#holy fuckballs, what is all that gibberish above?
#did I write that?

#eh, fuck class based views for now

def tweet(request):
    form = TweetForm
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['gameselect'].id
            game = Game.objects.get(id = form.cleaned_data['gameselect'].id)
            print game
            game.tweet = form.cleaned_data['tweet']
            game.save()
    context = {
        'form' : form,
    }
    return render(request, 'submit/tweet.html', context)

def tweet_lookup(request, game_id):
    tweet = get_object_or_404(Game.objects.filter(id = game_id)).tweet
    return HttpResponse(tweet)

###tool for filling in missing e-mail
#now, this wouldn't actually need a purpose built too if it was on a spreadsheet
#fine, I'll admit it: I overengineered this thing. it's mostly unnecessary
#(not even mostly)
#((to be fair to myself, it's way more elegant than the above *everything*))
#
#scans for Developer entries with missing e-mail field, presents the whole thing
#to be reviewed/corrected
class MissingView(View):
    missing_form = DeveloperForm

    def get(self, request):
        missing_mail = Developer()
        try:
            missing_mail = Developer.objects.filter(email = '').order_by('?')[0]
            print "got missing"
        except:
            return HttpResponse('no more to fix')
        form = self.missing_form(instance = missing_mail)
        context = {
            'dev' : missing_mail.game_set.all(),
            'form' : form,
        }
        return render(request, 'submit/missing.html', context)

    def post(self, request):
        #try:
        if 'skippy' in request.POST:
            return redirect('/submit/missing/')
        mail = request.POST.get('email')
        post_name = request.POST.get('name')
        changed = Developer.objects.get(name = post_name)
        changed.email = mail
        changed.save()
        return redirect('/submit/missing/')
        #except:
            #return HttpResponse('ya done fucked up')

