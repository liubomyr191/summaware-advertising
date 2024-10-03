from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

import json

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *
from ..models.permissions import AdAssistant

from .... import views
from ..forms import *

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def list_salesperson(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    salespersonList = SalesPerson.objects.all()
    numReps = len(salespersonList)
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "salespersonList": salespersonList,
        "numReps": numReps,
        "advertising": "yes"
    }
    if request.method == "GET":

        return render(request, "accounts/salesperson/list_salesperson.html", context)
    
    salesperson = SalesPerson(first_name=request.POST['firstName'], last_name=request.POST['lastName'], company=request.POST['company'], address=request.POST['address'], 
                                    city=request.POST['city'], state=request.POST['state'], zip_code=request.POST['zip_code'], email=request.POST['email'], 
                                    phone_number=request.POST['phone'], commission_percentage=request.POST['commissionPercentage'])

    salesperson.save()

    return HttpResponseRedirect('/advertising/salesperson/all/')
    

def create_salesperson(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "POST":
        # reqData = json.loads(request.body.decode('utf-8'))
        print(request.POST)
        salesperson = SalesPerson(first_name=request.POST['firstName'], last_name=request.POST['lastName'], company=request.POST['company'], address=request.POST['address'], 
                                    city=request.POST['city'], state=request.POST['state'], zip_code=request.POST['zip_code'], email=request.POST['email'], 
                                    phone_number=request.POST['phone'], commission_percentage=request.POST['commissionPercentage'])

        salesperson.save()

        # TODO - verify that it is a unique number and email address
        # return JsonResponse({ "message": "Success" }, status=200)
        salespersonList = SalesPerson.objects.all()
        numReps = len(salespersonList)

        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "salespersonList": salespersonList,
            "numReps": numReps
        }
        return HttpResponseRedirect('/advertising/salesperson/success/')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "advertising": "yes"
    }
    return render(request, "accounts/salesperson/create_salesperson.html", context)

def view_salesperson(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    salesperson = SalesPerson.objects.get(id=id)
    drafts = AdvertisingOrder.objects.filter(salesperson_id=salesperson.id, is_draft=True)

    userList = User.objects.values('id', 'username', 'first_name', 'last_name', 'email')

    adAssistants = AdAssistant.objects.filter(salesperson=salesperson)
    for assistant in AdAssistant.objects.all():
        print(model_to_dict(assistant))

    # TODO - be able to add/change the avatar/profile picture for the salesperson 
    # TODO - add an active flag for a salesperson
    # this would add a log entry for the account: "<user> marked <salesperson> inactive"

    # TODO - ability to have a bulk removal of salespeople from accounts (ask nate/nick about this?)
    if request.method == 'POST':
        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "salesperson": salesperson
        }

        if len(request.POST.get('zip_code')) > 5:
            context['message'] = "Zip code must be 5 digits or less."
            return render(request, "accounts/salesperson/view_salesperson.html", context)
        
        if len(request.POST.get('state')) > 2:
            context["message"] = "State must be 2 characters or less."
            return render(request, "accounts/salesperson/view_salesperson.html", context)

        salesperson.first_name = request.POST.get('first_name')
        salesperson.last_name = request.POST.get('last_name')
        salesperson.company = request.POST.get('company')
        salesperson.address = request.POST.get('address')
        salesperson.city = request.POST.get('city')
        salesperson.state = request.POST.get('state')
        salesperson.zip_code = request.POST.get('zip_code')
        salesperson.email = request.POST.get('email')
        salesperson.phone_number = request.POST.get('phone_number')
        salesperson.commission_percentage = request.POST.get('commission_percentage')
        salesperson.active = True if request.POST.get('active') == 'on' else False
        salesperson.save()

        return render(request, "accounts/salesperson/view_salesperson.html", context)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "salesperson": salesperson,
        "drafts": drafts,
        "userList": userList,
        "adAssistants": adAssistants,
        "advertising": "yes"
    }
    return render(request, "accounts/salesperson/view_salesperson.html", context)

def success_salesperson(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if request.method == 'GET':
        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
        }
        return render(request, "accounts/salesperson/success_salesperson.html", context)


def get_account_salesperson_details(request, id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return JsonResponse({ "message": "Error. Account not found."}, status=200)

    if account.sales_person:
        try:
            salesperson = SalesPerson.objects.get(id=account.sales_person.id)
        except SalesPerson.DoesNotExist:
            return JsonResponse({ "message": "Cannot find salesperson associated with that account" }, status=200)

        salespersonDetails = model_to_dict(salesperson)

        return JsonResponse({ "message": "Success", "salesperson_details": salespersonDetails }, status=200)

    else:
        return JsonResponse({ "message": "No salesperson associated with that account" }, status=200)
    
def salesperson_ad_assistants(request, id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        salesperson = SalesPerson.objects.get(pk=id)
    except SalesPerson.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find your user account." }, status=404)
    
    if request.method == 'GET':
        adAssistants = [model_to_dict(assistant) for assistant in AdAssistant.objects.filter(salesperson=salesperson)]

        return JsonResponse({ "message": "Success", "ad_assistants": adAssistants }, status=200)
    
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        print(reqData)

        # # get all of the accounts for the sales rep
        salespersonAccounts = Account.objects.filter(sales_person=salesperson)

        if len(reqData['adAssistants']) > 0:
            for userId in reqData['adAssistants']:
                try:
                    user = User.objects.get(pk=userId)
                except User.DoesNotExist:
                    return JsonResponse({ "message": "Error. Cannot find your user account." }, status=404)

                # check to make sure that they're not already an ad assistant for the sales rep
                prevAdAssistant = AdAssistant.objects.filter(salesperson=salesperson, user=user)
                alreadyAssistant = prevAdAssistant.exists()

                print(alreadyAssistant)
                # if they're not already an ad assistant, create them as one in the database for each account the salesperson is associated with
                # ? maybe in the future, refactor this to be able to choose which accounts an ad assistant can be associated with? (v2?)
                if not alreadyAssistant:
                    for account in salespersonAccounts:
                        adAssistant = AdAssistant(salesperson=salesperson, user=user, account=account)
                        adAssistant.save() # TODO - not showing in database
                
                # remove any ad assistants not selected from the list
                adAssistants = AdAssistant.objects.filter(salesperson=salesperson)
                for assistant in adAssistants:
                    if assistant.user.id not in reqData['adAssistants']:
                        assistant.delete()

            return JsonResponse({ "message": "Success" }, status=200)
        
        # if none were selected, remove all ad assistants associated with the selected salesperson
        else:
            adAssistants = AdAssistant.objects.filter(salesperson=salesperson)
            for assistant in adAssistants:
                if assistant.user.id not in reqData['adAssistants']:
                    assistant.delete()
                        

        return JsonResponse({ "message": "Success" }, status=201)

    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)