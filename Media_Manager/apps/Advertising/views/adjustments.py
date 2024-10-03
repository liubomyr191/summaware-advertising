from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

import json

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..forms import *

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

# TODO - rename adjustments to "add-ons"
def list_adjustments(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    adjustments = Adjustment.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "adjustments": adjustments
    }

    return render(request, "advertising/adjustments/list_adjustments.html", context)

def create_adjustment(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        publication = Publication.objects.get(pk=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find publication."}, status=404)

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        print(reqData)

        adjustment = Adjustment(code=reqData['code'], description=reqData['description'], apply_level=reqData['apply_level'], 
                                    value_type=reqData['value_type'], amount=reqData['amount'], type=reqData['type'], publication=publication, gross_net=reqData['grossNet'])
        
        if 'section' in reqData and reqData['section']:
            adjustment.section = reqData['section']

        adjustment.save()

        return JsonResponse({ "message": "Success"}, status=201)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "gl_codes": gl_codes
    }

    return render(request, "advertising/adjustments/new_adjustment.html", context)

def edit_adjustment(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    gl_codes = GLCode.objects.all()

    adjustment_types = [('flat', 'Flat'), ('percent', 'Percent'), ('none', 'None')]
    apply_levels = [('order', 'Order'), ('publication','Publication'), ('insertion', 'Insertion')]

    if id:
        adjustment = Adjustment.objects.get(id=id)

        if request.method == 'POST':
            adjustment.code = request.POST.get('code')
            adjustment.description = request.POST.get('description')
            adjustment.apply_level = request.POST.get('apply_level')
            adjustment.start_date = request.POST.get('start_date')
            adjustment.end_date = request.POST.get('end_date')
            adjustment.value_type = request.POST.get('type')
            adjustment.tax_category = request.POST.get('tax_category')
            adjustment.gross_net = request.POST.get('grossNet')

            adjustment.save()

            return HttpResponseRedirect('/advertising/adjustments')
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "gl_codes": gl_codes,
        "adjustment_types": adjustment_types,
        "apply_levels": apply_levels,
        "adjustment": adjustment
    }

    return render(request, "advertising/adjustments/edit_adjustment.html", context)

def adjustment_details(request, publication_id, adjustment_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        adjustment = Adjustment.objects.get(pk=adjustment_id, publication=publication_id)
    except Adjustment.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find adjustment"}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({ "message": "Success", "adjustment": model_to_dict(adjustment)}, status=200)

    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        adjustment.code = reqData['code']
        adjustment.description = reqData['description']
        adjustment.apply_level = reqData['apply_level']
        adjustment.value_type = reqData['value_type']
        adjustment.amount = reqData['amount']
        adjustment.type = reqData['type']
        adjustment.gross_net = reqData['grossNet']

        if reqData['section']:
            try:
                section = PublicationSection.objects.get(pk=reqData['section'])
            except PublicationSection.DoesNotExist:
                section = None

            adjustment.section = section

        else:
            adjustment.section = None

        adjustment.prompt_for_value = reqData['prompt_for_value']
        adjustment.active = reqData['active']

        adjustment.save()

        return JsonResponse({ "message": "Success" }, status=200)

    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)