from django.shortcuts import render
from django.http import HttpResponse

from submit.models import Developer, Game
# Create your views here.

def main_page(request):
    developer = Developer.objects.all()
    
    context = {
	'developer' : developer
    }
    return render(request, 'submit/form.html', context)

def send(request):
    return HttpResponse('lol, butts')
