from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

from datetime import datetime
import json

from ..models.companies import GLCode, CurrentCompany
from ..models.rates import RateGLCode
from ..models.publications import Publication

from .... import views

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def gl_code_dashboard(request):
    # Check if user is logged in, if not, redirect  to login screen
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + '/')
    return render(request, 'gl_codes/gl-dashboard.html')

def list_gl_codes(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
        
    gl_codes = GLCode.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "gl_codes": gl_codes,
        "advertising": "yes"
    }

    return render(request, "gl_codes/list_gl_codes.html", context)

def newGlCode(request):
    # Check if user is logged in, if not, redirect  to login screen
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + '/')
    return render(request, 'gl_codes/create-gl-code.html')

def create_gl_code(request):
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

        gl_code = GLCode(code=reqData['code'], description=reqData['description'], pl_type=reqData['pl_type'], created_by=user)
        gl_code.save()

        message = 'GL Code #' + str(gl_code.id) + ' has been created by ' + request.user.username
        logging.info(message)
        print(message)

        return JsonResponse({ "message": "Success" }, status=201)

    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)

def edit_gl_code(request, code_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
        
    try:
        gl_code = GLCode.objects.get(id=code_id)
    except GLCode.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find GL code. Please try again." }, status=404)
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        gl_code.code         = reqData['code']
        gl_code.description  = reqData['description']
        gl_code.pl_type      = reqData['pl_type']
        gl_code.last_updated = datetime.now()

        gl_code.save()

        message = 'GL Code #' + str(gl_code.id) + ' has been updated by ' + request.user.username
        logging.info(message)
        print(message)

        return JsonResponse({ "message": "Success" }, status=200)

    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)
    
def gl_code_details(request, code_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        try:
            glCode = GLCode.objects.get(pk=code_id)
        except GLCode.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find Gl Code in our system. Please try again." }, status=404)
        
        gl_code = {
            'code': glCode.code,
            'description': glCode.description,
            'pl_type': glCode.pl_type
        }
        
        return JsonResponse({ "message": "Success", "gl_code": gl_code }, status=200)
    
    else:
        return JsonResponse({ "message": "Error. Method not implemented" }, status=501)
    
def get_rate_gl_codes(request, rateId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        glCodeData = {}
        selectedCodes = {}

        pubList = request.GET.getlist('publications[]')
        for pub in pubList:
            try:
                publication = Publication.objects.get(pk=pub)
            except Publication.DoesNotExist:
                pass

            selectedCodes[publication.name] = []
            rateGLCode = RateGLCode.objects.filter(rate=rateId, publication=publication)
            for rateCode in rateGLCode:
                selectedCodes[rateCode.publication.name] = rateCode.gl_code.id
        
        if len(glCodeData):
            return JsonResponse({ "message": "Success", "gl_codes": glCodeData, "selectedCodes": selectedCodes }, status=200)
        else:
            return JsonResponse({ "message": "Error. Cannot find gl codes for rate. Please try again." }, status=404)