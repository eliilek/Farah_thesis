from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from models import *
import random
from django.utils.safestring import mark_safe
import json
import datetime
import csv

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

def download_results(request, user_id):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_' + str(user_id) + '_data.csv"'
    try:
        user = Subject.objects.get(subject_id=user_id)
        paired_data_set = PairedStimulusResultsBlock.objects.filter(subject=user).filter(completed=True)
        conjugate_data_set = ConjugateStimulusResultsBlock.objets.filter(subject=user).filter(completed=True)
    except Exception as e:
        print(e)

    #writer = csv.writer(response)
    #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])

    return response

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
    stimuli = sub.stimulus_set.filter(active=True).order_by('id')
    if len(stimuli)<4:
        return render(request, 'start-session.html', {'error':"Subject " + request.POST['id'] + " needs more active stimuli"})
    elif len(stimuli)>4:
        return render(request, 'start-session.html', {'error':"Subject " + request.POST['id'] + " has too many active stimuli"})

    if request.POST['assessment_type'] == "paired":
        results_block = PairedStimulusResultsBlock(subject=sub, session_number=request.POST['session_number'])
        results_block.save()
        request.session['active_response_block'] = results_block.id
        pairs = []
        pairs.append({'left':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id},
        'right':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id}})
        pairs.append({'left':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id},
        'right':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id}})
        pairs.append({'left':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id},
        'right':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id}})
        pairs.append({'left':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id},
        'right':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id}})
        pairs.append({'left':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id},
        'right':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id}})
        pairs.append({'left':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id},
        'right':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id}})
        pairs.append({'left':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id},
        'right':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id}})
        pairs.append({'left':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id},
        'right':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id}})
        pairs.append({'left':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id},
        'right':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id}})
        pairs.append({'left':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id},
        'right':{'video_id':stimuli[0].video_id, 'start_time':stimuli[0].start_time, 'id':stimuli[0].id}})
        pairs.append({'left':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id},
        'right':{'video_id':stimuli[1].video_id, 'start_time':stimuli[1].start_time, 'id':stimuli[1].id}})
        pairs.append({'left':{'video_id':stimuli[3].video_id, 'start_time':stimuli[3].start_time, 'id':stimuli[3].id},
        'right':{'video_id':stimuli[2].video_id, 'start_time':stimuli[2].start_time, 'id':stimuli[2].id}})
        random.shuffle(pairs)
        for pair in pairs:
            print pair['left']
            print pair['right']
        return render(request, 'paired-stimulus.html', {'pairs':mark_safe(json.dumps(pairs))})
    else:
        results_block = ConjugateStimulusResultsBlock(subject=sub, session_number=request.POST['session_number'])
        results_block.save()
        request.session['active_response_block'] = results_block.id
        videos = {}
        print request.POST['session_number']
        if request.POST['session_number'] == "1":
            print "one"
            videos['First'] = {'video_id':stimuli[0].video_id, 'id':stimuli[0].id, 'start_time':stimuli[0].start_time}
            videos['Second'] = {'video_id':stimuli[1].video_id, 'id':stimuli[1].id, 'start_time':stimuli[1].start_time}
            videos['Third'] = {'video_id':stimuli[2].video_id, 'id':stimuli[2].id, 'start_time':stimuli[2].start_time}
            videos['Fourth'] = {'video_id':stimuli[3].video_id, 'id':stimuli[3].id, 'start_time':stimuli[3].start_time}
        elif request.POST['session_number'] == 2:
            videos['First'] = {'video_id':stimuli[3].video_id, 'id':stimuli[3].id, 'start_time':stimuli[3].start_time}
            videos['Second'] = {'video_id':stimuli[2].video_id, 'id':stimuli[2].id, 'start_time':stimuli[2].start_time}
            videos['Third'] = {'video_id':stimuli[1].video_id, 'id':stimuli[1].id, 'start_time':stimuli[1].start_time}
            videos['Fourth'] = {'video_id':stimuli[0].video_id, 'id':stimuli[0].id, 'start_time':stimuli[0].start_time}
        elif request.POST['session_number'] == 3:
            videos['First'] = {'video_id':stimuli[1].video_id, 'id':stimuli[1].id, 'start_time':stimuli[1].start_time}
            videos['Second'] = {'video_id':stimuli[3].video_id, 'id':stimuli[3].id, 'start_time':stimuli[3].start_time}
            videos['Third'] = {'video_id':stimuli[0].video_id, 'id':stimuli[0].id, 'start_time':stimuli[0].start_time}
            videos['Fourth'] = {'video_id':stimuli[2].video_id, 'id':stimuli[2].id, 'start_time':stimuli[2].start_time}
        elif request.POST['session_number'] == 4:
            videos['First'] = {'video_id':stimuli[2].video_id, 'id':stimuli[2].id, 'start_time':stimuli[2].start_time}
            videos['Second'] = {'video_id':stimuli[0].video_id, 'id':stimuli[0].id, 'start_time':stimuli[0].start_time}
            videos['Third'] = {'video_id':stimuli[3].video_id, 'id':stimuli[3].id, 'start_time':stimuli[3].start_time}
            videos['Fourth'] = {'video_id':stimuli[1].video_id, 'id':stimuli[1].id, 'start_time':stimuli[1].start_time}
        print videos
        return render(request, 'conjugate-preference.html', {'videos':mark_safe(json.dumps(videos))})

    return HttpResponse("Something has gone horribly wrong if you're reading this")

def report_paired_results(request):
    if request.method != "POST" or not "active_response_block" in request.session.keys():
        return redirect("/")
    json_object = json.loads(request.body)
    for response in json_object:
        try:
            block = PairedStimulusResultsBlock.objects.get(id=request.session['active_response_block'])
            block.save()
            paired_response = PairedStimulusResult(
                block = block,
                video_left = Stimulus.objects.get(id=json_object[response]['video_left']),
                video_right = Stimulus.objects.get(id=json_object[response]['video_right'])
            )
            if 'video_selected' in json_object[response].keys():
                paired_response.video_selected = json_object[response]['video_selected']
            paired_response.save()
        except Exception as e:
            print(e)
    block.completed = True;
    block.save()
    request.session.pop('active_response_block')
    return HttpResponse("You shouldn't see this message")

def report_conjugate_results(request):
    if request.method != "POST" or not "active_response_block" in request.session.keys():
        return redirect("/")
    json_object = json.loads(request.body)
    for response in json_object:
        try:
            block = ConjugateStimulusResultsBlock.objects.get(id=request.session['active_response_block'])
            block.save()
            conjugate_response = ConjugateStimulusResult(
                block = block,
                video = Stimulus.objects.get(id=json_object[response]['video']),
                response_number = json_object[response]['response_number'],
                play_time = datetime.timedelta(seconds=json_object[response]['play_time'])
            )
            conjugate_response.save()
        except Exception as e:
            print(e)
    block.completed = True;
    block.save()
    request.session.pop('active_response_block')
    return HttpResponse("You shouldn't see this message")

def end_session(request):
    return render(request, 'end-of-session.html')
