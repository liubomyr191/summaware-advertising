from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

from datetime import datetime
import json

from ..models.companies import Location, CurrentCompany
from ..models.rates import RateGLCode
from ..models.publications import Publication

from .... import views

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def list_location(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
        
    locations = Location.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "locations": locations,
        "advertising": "yes"
    }

    return render(request, "locations/list_locations.html", context)

def create_location(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - be able to have levels (2 letters/numbers, 3 letters/numbers, etc.)

    if request.method == "POST":
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            print('User does not exist')

        location = Location(location=reqData['location'], description=reqData['description'], pc=reqData['pc'], created_by=user)
        location.save()

        message = 'Location #' + str(location.id) + ' has been created by ' + request.user.username
        logging.info(message)
        print(message)

        return JsonResponse({ "message": "Success" }, status=201)

    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)

def edit_location(request, location_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
        
    try:
        location = Location.objects.get(id=location_id)
    except GLCode.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find GL code. Please try again." }, status=404)
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        location.location     = reqData['location']
        location.description  = reqData['description']
        location.pc           = reqData['pc']
        location.last_updated = datetime.now()

        location.save()

        message = 'GL Code #' + str(location.id) + ' has been updated by ' + request.user.username
        logging.info(message)
        print(message)

        return JsonResponse({ "message": "Success" }, status=200)

    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)
    
def location_details(request, location_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        try:
            location = Location.objects.get(pk=location_id)
        except Location.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find Location in our system. Please try again." }, status=404)
        
        res = {
            'location': location.location,
            'description': location.description,
            'pc': location.pc
        }
        
        return JsonResponse({ "message": "Success", "res": res }, status=200)
    
    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)
  
