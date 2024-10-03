from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

import json
from datetime import timedelta, datetime, date

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..models import Account, AccountType, SalesPerson
from ..forms import *

from ..validate import validateZipCode, validateState, validateEmail

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def getRunDays(dict):
    days = []
    for day in daysOfTheWeek:
        if dict.get(day):
            days.append(day[0:3].title())
    return days

def list_ad_types(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    adTypes = AdType.objects.all().order_by('name')

    if request.method == "POST":
        data = request.POST.dict()

        if request.POST.get('type') == "edit":
            ad_type = AdType.objects.get(id=data['data[id]'])
            ad_type.name = data['data[name]']
            ad_type.code = data['data[code]']
            ad_type.save()

            return HttpResponseRedirect('/advertising/ad-types')
        
        elif request.POST.get('type') == "new":

            ad_type = AdType(name=data['data[name]'], code=data['data[code]'])
            ad_type.save()
            
            return HttpResponseRedirect('/advertising/ad-types')

        return HttpResponseRedirect('/advertising/ad-types')
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "adTypes": adTypes
    }

    return render(request, "advertising/ad_types/list_ad_types.html", context)

def delete_ad_type(request, ad_type_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if ad_type_id is None:
        return JsonResponse({"message": "No ad type provided!"})

    try:
        ad_type = AdType.objects.get(id=ad_type_id)
    except AdType.DoesNotExist:
        return JsonResponse({"message": "Ad type not found"})

    if ad_type:
        ad_type.delete()
    
    return HttpResponseRedirect('/advertising/ad-types')