from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

import json

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..models import Account, AccountType, SalesPerson
from ..forms import *

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def list_company_contacts(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    account = Account.objects.get(id=id)
    contacts = CompanyContact.objects.filter(account_id=account.id)
    for contact in contacts:
        contact.account = account

    numContacts = len(contacts)

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        reqData = reqData['formData']

        return JsonResponse({ "message": "Success" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "contacts": contacts,
        "active_contacts": contacts.filter(active=True),
        "inactive_contacts": contacts.filter(active=False),
        "numContacts": numContacts,
        "account_id": id
    }

    return render(request, "accounts/company_contacts/list_company_contacts.html", context)

def create_company_contact(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # TODO - refactor this to allow for AJAX requests 
    # should not be redirecting after it creates the account contact
    
    if request.method == "POST":
        reqData = json.loads(request.body.decode('utf-8'))
        reqData = reqData['formData']

        formData = {}
        for item in reqData:
            formData[item['name']] = item['value']

        isDefault = False if 'default' not in formData else True

        if isDefault:
            contacts = CompanyContact.objects.all()
            for c in contacts:
                if c.default:
                    c.default = False
                    c.save()
                    break
        
        contact = CompanyContact(first_name=formData['firstName'], last_name=formData['lastName'], email=formData['email'], 
                                    phone_number=formData['phone'], department=formData['department'])     
        account = Account.objects.get(id=id)
        contact.account = account
        contact.default = isDefault
        contact.save()

        return JsonResponse({ "message": "Success" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
    }
    return render(request, "accounts/company_contacts/new_company_contact.html", context)

def edit_company_contact(request, id=None, contact_id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find the account." }, status=200)
    
    contact = CompanyContact.objects.get(id=contact_id, account=account)
    
    if request.method == 'GET':            
        contact = CompanyContact.objects.get(id=contact_id)
        contacts = CompanyContact.objects.all()

        # check to see if there already is a default contact
        for c in contacts:
            if c.default:
                c.default = False
                c.save()
                break

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.email = request.POST.get('email')
        contact.phone_number = request.POST.get('phone_number')
        contact.department = request.POST.get('department')
        contact.active = False if request.POST.get('active') == None else True
        contact.default = False if request.POST.get('default') == None else True
        if not contact.active and contact.default:
            contact.default = False
        contact.save()

        formData = {}
        for item in reqData:
            formData[item['name']] = item['value']

        isDefault = False if 'default' not in formData else True

        if isDefault:
            contacts = CompanyContact.objects.all()
            for c in contacts:
                if c.default:
                    c.default = False
                    c.save()
                    break

        return JsonResponse({ "message": "Success" }, status=200)
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "contact": contact
    }

    return render(request, "accounts/company_contacts/edit_company_contact.html", context)

def account_contact_details(request, accountId, contactId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)

    try: 
        contact = CompanyContact.objects.get(pk=contactId, account=accountId)
    except CompanyContact.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find contact." }, status=200)

    if request.method =='GET':
        return JsonResponse({ "message": "Success", "contact": model_to_dict(contact) }, status=200)

    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        print(reqData)

        for c in CompanyContact.objects.filter(account=accountId):
            if c.default:
                c.default = False
                c.save()
                break
        
        contact.first_name = reqData['firstName']
        contact.last_name = reqData['lastName']
        contact.email = reqData['email']
        contact.phone_number = reqData['phone']
        contact.department = reqData['department']
        contact.active = reqData['active']
        contact.default = reqData['default']

        if not contact.active and contact.default:
            contact.default = False

        contact.save()

        return JsonResponse({ "message": "Success" }, status=200)
    else:
        return JsonResponse({ "message": "Error. Invalid request." }, status=400)
    
def account_contact_action(request, accountId, contactId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)
    
    try: 
        contact = CompanyContact.objects.get(pk=contactId, account=accountId)
    except CompanyContact.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find contact." }, status=200)
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        reqType = reqData['type']

        if reqType == 'delete':
            contact.active = False
            if contact.default:
                contact.default = False

            contact.save()

            message = 'Contact #' + str(contact.id) + ' (' + contact.first_name + ' ' + contact.last_name + ') is now active for account #' + str(contact.account.id)
            statusCode = 200
        
        elif reqType == 'active':
            contact.active = True
            contact.save()

            message = 'Contact #' + str(contact.id) + ' (' + contact.first_name + ' ' + contact.last_name + ') is now inactive for account #' + str(contact.account.id)
            statusCode = 200
        
        else: 

            message = 'Error. Unknown request. Please try again.'
            statusCode = 400
        
        print(message)
        logging.info(message)
        
        return JsonResponse({ "message": message }, status=statusCode)