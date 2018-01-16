from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from models import *

# return render(request, 'subject.html', {'sub': sub, 'response_list':response_list})

# Create your views here.
def index(request):
    #Should return selection of view data or start session
    return render(request, 'index.html')

def start(request):
    #Template for take user id, start session
    return render(request, 'start-session.html')

def select(request):
    #Pull participant id for each participant with data
    participants = Subject.objects.filter(Q(pairedStimulusResultsBlock)|Q(conjugateStimulusResultsBlock))
    return render(request, 'select-participant.html', {'participants':participants})
