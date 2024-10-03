from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

from datetime import datetime
import json

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..forms import *

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def getRunDays(dict):
    days = []
    for day in daysOfTheWeek:
        if dict.get(day):
            days.append(day[0:3].title())
    return days

def view_ad_deadlines(request, publication_id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    deadlineList = [deadline for deadline in AdDeadline.objects.all() if int(deadline.publication.id) == int(publication_id)]
    for deadline in deadlineList:
        deadline.time = datetime.strptime(deadline.time, '%H:%M:%S').time()
        deadline.ad_type = AdType.objects.get(id=deadline.ad_type.id)
        deadline.publication = Publication.objects.get(id=deadline.publication.id)

    context = {
        "access": "allow",

        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "deadlineList": deadlineList,
        "publication_id": publication_id
    }

    return render(request, "publications/ad_deadlines/view_ad_deadlines.html", context)

def new_ad_deadline(request, publication_id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    daysOfTheWeek = {
        'sunday': 'Sunday',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday'
    }
    publication = Publication.objects.get(id=publication_id)

    if request.method == "POST":
        pub_days = request.POST.getlist('publication_day')
        ad_type = AdType.objects.get(id=request.POST.get('ad_type'))
        days_prior = int(request.POST.get('days_prior'))
        time = request.POST.get('time')
        priority_level = request.POST.get('deadline_priority')

        for day in pub_days:
            deadline = AdDeadline(publication=publication,publication_day=daysOfTheWeek[day],time=time,ad_type=ad_type,days_prior=days_prior, 
                                    priority_level=priority_level)
            deadline.save()
        return HttpResponseRedirect('/advertising/publication/' + str(publication.id))

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "daysoftheweek": daysOfTheWeek,
        "ad_types": AdType.objects.all(),
        "publication_id": publication.id
    }

    return render(request, "publications/ad_deadlines/new_ad_deadline.html", context)

def ad_deadlines_details(request, publication_id, deadline_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        adDeadline = AdDeadline.objects.get(pk=deadline_id, publication=publication_id)

        runDayList = []
        try:
            runDayList = PublicationRunDay.objects.get(publication=publication_id)
            runDayList = model_to_dict(runDayList)
        except PublicationRunDay.DoesNotExist:
            runDayList = None
    except AdDeadline.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find ad deadline. Please try again." }, status=404)
    
    if request.method == 'GET':
        return JsonResponse({ "message": "Success", "deadline": model_to_dict(adDeadline), "runDayList": runDayList }, status=200)
    
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        adDeadline.publication_day = reqData['publication_day']
        adDeadline.time = reqData['time']
        adDeadline.days_prior = int(reqData['days_prior'])
        adDeadline.priority_level = reqData['priority_level']

        try:
            adDeadline.ad_type = AdType.objects.get(id=reqData['ad_type'])
        except AdType.DoesNotExist:
            adDeadline.ad_type = None

        adDeadline.save()

        return JsonResponse({ "message": "Success" }, status=200)

    else:
        return JsonResponse({ "message": "Error. Method not implemented." }, status=405)

# def edit_ad_deadlines(request, publication_id, deadline_id):
#     if request is None or not request.user.is_authenticated:
#         return redirect(login_redirect + "advertising")

#     if not request.user.has_perm('BI.advertising_access'):
#         return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

#     deadline = AdDeadline.objects.get(id=deadline_id, publication_id=publication_id)

#     if request.method == "POST":
#         deadline.publication_day = request.POST.get('publication_day')
#         deadline.time = request.POST.get('time')
#         deadline.ad_type = AdType.objects.get(id=request.POST.get('ad_type'))
#         deadline.days_prior = int(request.POST.get('days_prior'))
#         deadline.save()

#         return HttpResponseRedirect('/advertising/publication/' + str(publication_id))

#     context = {
#         "access": "allow",
#         "message": "",
#         "groups": ', '.join(views.get_groups(request)),
#         "menu": views.get_sidebar(request),
#         "ad_types": AdType.objects.all(),
#         "deadline": deadline,
#         "deadlineJSON": model_to_dict(deadline),
#         "publication_id": publication_id
#     }

#     return render(request, "publications/ad_deadlines/edit_ad_deadlines.html", context)