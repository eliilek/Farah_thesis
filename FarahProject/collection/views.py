from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from models import *
import random
from django.utils.safestring import mark_safe
import json

# Create your views here.
def index(request):
    #Should return selection of view data or start session
    return render(request, 'index.html')

def start(request):
    #Template for take user id, start session
    return render(request, 'start-session.html')

def select(request):
    #Pull participant id for each participant with data
    participants = Subject.objects.filter(Q(pairedstimulusresultsblock__completed=True)|Q(conjugatestimulusresultsblock__completed=True))
    return render(request, 'select-participant.html', {'participants':participants})

def select_type(request):
    if request.method != "POST" or not 'id' in request.POST.keys():
        return redirect("/")
    try:
        sub = Subject.objects.get(subject_id=request.POST['id'])
        return render(request, 'select-assessment-session.html', {'id':sub.subject_id})
    except:
        return render(request, 'start-session.html', {'error':"No subject with ID " + request.POST['id'] + " exists"})

def selection_redirect(request):
    if request.method != "POST" or not 'assessment_type' in request.POST.keys() or not 'session_number' in request.POST.keys():
        return redirect("/")
    try:
        sub = Subject.objects.get(subject_id=request.POST['id'])
    except:
        return render(request, 'start-session.html', {'error':"No subject with ID " + request.POST['id'] + " exists"})
    print sub.stimulus_set.all()
    stimuli = sub.stimulus_set.filter(active=True)
    if len(stimuli)<4:
        return render(request, 'start-session.html', {'error':"Subject " + request.POST['id'] + " needs more active stimuli"})
    elif len(stimuli)>4:
        return render(request, 'start-session.html', {'error':"Subject " + request.POST['id'] + " has too many active stimuli"})

    if request.POST['assessment_type'] == "paired":
        request.session['active_response_block'] = PairedStimulusResultsBlock(subject=sub, session_number=request.POST['session_number'])
        request.session['active_response_block'].save()
        pairs = []
        pairs.append({'left':model_to_dict(stimuli[0]), 'right':model_to_dict(stimuli[1])})
        pairs.append({'left':model_to_dict(stimuli[0]), 'right':model_to_dict(stimuli[2])})
        pairs.append({'left':model_to_dict(stimuli[0]), 'right':model_to_dict(stimuli[3])})
        pairs.append({'left':model_to_dict(stimuli[1]), 'right':model_to_dict(stimuli[0])})
        pairs.append({'left':model_to_dict(stimuli[1]), 'right':model_to_dict(stimuli[2])})
        pairs.append({'left':model_to_dict(stimuli[1]), 'right':model_to_dict(stimuli[3])})
        pairs.append({'left':model_to_dict(stimuli[2]), 'right':model_to_dict(stimuli[0])})
        pairs.append({'left':model_to_dict(stimuli[2]), 'right':model_to_dict(stimuli[1])})
        pairs.append({'left':model_to_dict(stimuli[2]), 'right':model_to_dict(stimuli[3])})
        pairs.append({'left':model_to_dict(stimuli[3]), 'right':model_to_dict(stimuli[0])})
        pairs.append({'left':model_to_dict(stimuli[3]), 'right':model_to_dict(stimuli[1])})
        pairs.append({'left':model_to_dict(stimuli[3]), 'right':model_to_dict(stimuli[2])})
        random.shuffle(pairs)
        return render(request, 'paired-stimulus.html', {'pairs':mark_safe(json.dumps(pairs)})
    else:
        pass
    return HttpResponse("Placeholder")

def report_paired_results(request):
    if request.method != "POST" or not "active_response_block" in request.session.keys():
        return redirect("/")
    json_object = json.loads(request.body)
    for response in json_object:
        print response.keys()
        try:
            block = request.session['active_response_block']
            block.save()
            paired_response = PairedStimulusResult(
                block = block,
                video_left = response['video_left']
                video_right = response['video_right']
            )
            if 'video_selected' in response.keys():
                paired_response.video_selected = response['video_selected']
            paired_response.save()
        except:
            pass
    return HttpResponse("You shouldn't see this message")
