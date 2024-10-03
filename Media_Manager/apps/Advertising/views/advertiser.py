from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)

import json
from django.shortcuts import render
from ..models.advertising import *
from ..models.classifieds import *
from ..models.advertising import Account, SalesPerson, AccountType, MarketCode, IndustryCode, CompanyContact, AdvertiserTaskList
from .... import views
from ..forms import *
from django.core import serializers
from django.db.models import Q

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def advertiser_dashboard(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    advertiserId = request.GET.get('advertiserId')
    newAccount = Account.objects.filter(id=advertiserId).first()
    accountTypes = AccountType.objects.all()
    accountTypeList = serializers.serialize('json', accountTypes)
    department = CompanyDepartment.objects.all()
    accountInfo = Account.objects.filter(id=advertiserId).first()
    contacts = CompanyContact.objects.filter(account__id=newAccount.id).all()

    # Filter parameters
    date_filter = request.GET.get('date')
    creator_filter = request.GET.get('creator')
    format_filter = request.GET.get('format')
    pricing_filter = request.GET.get('pricing')
    search_query = request.GET.get('search')

    adCampaign = ClassifiedCampaignSummary.objects.filter(advertiser_id=advertiserId)

    # Apply filters
    if date_filter:
        if date_filter == 'Most Recent':
            adCampaign = adCampaign.order_by('-created_date')
        elif date_filter == 'Oldest':
            adCampaign = adCampaign.order_by('created_date')

    if creator_filter and creator_filter != 'Select':
        adCampaign = adCampaign.filter(sales_contact__icontains=creator_filter)

    if format_filter and format_filter != 'Select':
        adCampaign = adCampaign.filter(campaign_detail__icontains=format_filter)  # Assuming 'campaign_detail' contains format info

    if pricing_filter and pricing_filter != 'Select':
        if pricing_filter == 'Most Expensive':
            adCampaign = adCampaign.order_by('-total_campaign')
        elif pricing_filter == 'Least Expensive':
            adCampaign = adCampaign.order_by('total_campaign')

    if search_query:
        adCampaign = adCampaign.filter(
            Q(campaign_name__icontains=search_query) |
            Q(advertiser_name__icontains=search_query) |
            Q(campaign_detail__icontains=search_query)
        )

    if newAccount.website and not newAccount.website.startswith(('http://', 'https://')):
        newAccount.website = 'http://' + newAccount.website

    context = {
        "id": advertiserId,
        "newAccount": newAccount,
        "accountTypes": accountTypes,
        "accountTypeList": accountTypeList,
        "department": department,
        "accountInfo": accountInfo,
        "adCampaigns": adCampaign,
        "contacts": contacts,
        "date_filter": date_filter,
        "creator_filter": creator_filter,
        "format_filter": format_filter,
        "pricing_filter": pricing_filter,
        "search_query": search_query,
    }

    return render(request, "dashboard.html", context)

def all_advertisers(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    AccountList = Account.objects.select_related('account_type').all().order_by('id')
    context = {
        "accountList" : AccountList,
    }
    return render(request, "advertising/advertisers_all.html",context)

def advertiser_home(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if request.method == 'GET':
        account_type_list= AccountType.objects.all()
        AccountList = Account.objects.all().order_by('-id')
        context = {
            "accountList" : AccountList,
            "account_type_list":account_type_list
        }
        return render(request, "HomeAdvertiser.html", context)

def edit_new_advertiser(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'GET':
        advertiserId = request.GET.get('advertiserId',None)
        if advertiserId:
            accountTypeQuery = AccountType.objects.all()
            accountTypeList = serializers.serialize('json', accountTypeQuery)

            marketCodeQuery = MarketCode.objects.all()
            marketCodeList = serializers.serialize('json', marketCodeQuery)

            salesPersonQuery = SalesPerson.objects.all()
            salesPersonList = serializers.serialize('json', salesPersonQuery)
            states = AllStates.objects.all()
            current_account = Account.objects.filter(id=advertiserId).first()
            current_account_market_code = MarketCode.objects.filter(account__id=current_account.id).first()
            context = {
                "accountTypes": accountTypeQuery,
                "accountTypeList": accountTypeList,
                "marketCodes": marketCodeQuery,
                "marketCodeList": marketCodeList,
                "salesPersons": salesPersonQuery,
                "salesPersonList": salesPersonList,
                "states": states,
                "advertising" : "yes",
                "current_account":current_account,
                "current_account_market_code":current_account_market_code
            }
            return render(request, "EditNewAdvertiser.html", context)

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        advertiser_id = request.GET.get('advertiserId',None)
        # Check if an advertiserId is provided to update an existing advertiser
        if advertiser_id:
            try:
                modal = Account.objects.get(pk=advertiser_id)
            except Account.DoesNotExist:
                return JsonResponse({"message": "Advertiser not found."}, status=404)
        else:
            modal = Account()

        try:
            accountId = data['accountType']
            account = AccountType.objects.get(pk=accountId)
        except AccountType.DoesNotExist:
            account = None

        try:
            marketCodeId = data['marketCode']
            marketCode = MarketCode.objects.get(pk=marketCodeId)
        except MarketCode.DoesNotExist:
            marketCode = None

        try:
            salesPersonId = data['salesPerson']
            salesPerson = SalesPerson.objects.get(pk=salesPersonId)
        except SalesPerson.DoesNotExist:
            salesPerson = None

        modal.account_type = account
        modal.contact_name = data['firstName']
        modal.contact_name_first = data['firstName']
        modal.contact_name_last = data['lastName']
        modal.name = data['businessName']
        modal.company_name_1 = data['businessName']  
        modal.address = data['address']
        modal.city = data['city']
        modal.state = data['state']
        modal.zip_code = data['zipCode']
        modal.phone = data['phoneNumber']
        modal.email = data['email']
        modal.website = data['website']
        modal.market_code = marketCode
        modal.sales_person = salesPerson
        modal.submitter = data['submitter']
        modal.legacy_id = data['legacyId']
        modal.billing_email = data['bilEmail']
        modal.billing_address = data['bilAddress']
        modal.billing_city = data['bilCity']
        modal.billing_state = data['bilState']
        modal.billing_zip_code = data['bilZipCode']
        modal.status = 0  

        modal.save()

        return JsonResponse({'success': "Successful!", 'id': modal.id})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def taskSetActivity(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        row = AdvertiserTaskList.objects.get(id=data['id'])
        row.complete = 1
        row.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def create_task (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        if data['id'] == 0:
            task = AdvertiserTaskList(
                title=data['title'],
                due_date=data['due_date'],
                priority=data['priority'],
                content=data['content'],
                account_id=data['account_id'],
                note=data['note'],
                complete=0,
                status=1
            )

            task.save()

        if data['id'] != 0:
            row = AdvertiserTaskList.objects.get(id=data['id'])

            row.title = data['title']
            row.due_date = data['due_date']
            row.priority = data['priority']
            row.account_id = data['account_id']
            row.content = data['content']
            row.note = data['note']

            row.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def delete_id_contact (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        obj_to_delete = CompanyContact.objects.get(id=data['id'])

        obj_to_delete.active = 0
        obj_to_delete.save()
        active_contacts = CompanyContact.objects.filter(active=1)
        ac_con = list(active_contacts.values())

        inactive_contacts = CompanyContact.objects.filter(active=0)
        inac_con = list(inactive_contacts.values())

        contacts = {
            'active': ac_con,
            'inactive': inac_con,
        }

        return JsonResponse(contacts)
def taskRemove (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        obj_to_delete = AdvertiserTaskList.objects.get(id=data['id'])

        obj_to_delete.status = 0
        obj_to_delete.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def create_contact (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        if data['id'] == 0:
            contact = CompanyContact(
                account_id=data['account'],
                first_name=data['firstname'],
                last_name=data['lastname'],
                full_name=data['firstname'] + " " + data['lastname'],
                email=data['email'],
                department_id=data['department'],
                phone_number=data['phone'],
                default=data['default'],
                active=1
            )
            contact.save()

        if data['id'] != 0:
            print("==============update=================")
            contact = CompanyContact.objects.get(id=data['id'])

            contact.account_id = data['account']
            contact.first_name = data['firstname']
            contact.last_name = data['lastname']
            contact.email = data['email']
            contact.department_id = data['department']
            contact.phone_number = data['phone']
            contact.full_name = data['firstname'] + " " + data['lastname']
            contact.default = data['default']

            contact.save()

        active_contacts = CompanyContact.objects.filter(active=1)
        ac_con = list(active_contacts.values())

        inactive_contacts = CompanyContact.objects.filter(active=0)
        inac_con = list(inactive_contacts.values())

        contacts = {
            'active': ac_con,
            'inactive': inac_con,
        }

        return JsonResponse(contacts)
def get_id_contact (request) :
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        search_contacts = Account.objects.filter(id=data['id'])
        contacts = list(search_contacts.values())
        return JsonResponse(contacts)

def getTaskList (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        if data['status'] == 'active':
            active_Tasks = AdvertiserTaskList.objects.filter(status=1)
            ac_con = list(active_Tasks.values())

            contacts = {
                'active': ac_con,
            }

            return JsonResponse(contacts)
        if data['status'] == 'complete':
            active_Tasks = AdvertiserTaskList.objects.filter(complete=1)
            ac_con = list(active_Tasks.values())

            contacts = {
                'active': ac_con,
            }

            return JsonResponse(contacts)

def search_filter_contacts (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        if data['param'] == 'all':
            active_contacts = CompanyContact.objects.filter(active=1)
            ac_con = list(active_contacts.values())

            inactive_contacts = CompanyContact.objects.filter(active=0)
            inac_con = list(inactive_contacts.values())

            contacts = {
                'active': ac_con,
                'inactive': inac_con,
            }

            return JsonResponse(contacts)
        if data['param'] == 'search':
            active_contacts = CompanyContact.objects.filter(full_name__contains=data['search_val'], active=1)
            ac_con = list(active_contacts.values())

            inactive_contacts = CompanyContact.objects.filter(full_name__contains=data['search_val'],active=0)
            inac_con = list(inactive_contacts.values())

            contacts = {
                'active': ac_con,
                'inactive': inac_con,
            }
            return JsonResponse(contacts)
        if data['param'] == 'filter':

            if data['status'] == 2:
                if data['dept'] == 0:
                    active_contacts = CompanyContact.objects.filter(active=1)
                    ac_con = list(active_contacts.values())

                    inactive_contacts = CompanyContact.objects.filter(active=0)
                    inac_con = list(inactive_contacts.values())

                elif data['dept'] != 0:
                    active_contacts = CompanyContact.objects.filter(department_id=data['dept'],active=1)
                    ac_con = list(active_contacts.values())

                    inactive_contacts = CompanyContact.objects.filter(department_id=data['dept'], active=0)
                    inac_con = list(inactive_contacts.values())
                contacts = {
                    'active': ac_con,
                    'inactive': inac_con,
                }

                return JsonResponse(contacts)
            elif data['status'] != 2:
                if data['status'] == 1:
                    if data['dept'] == 0:
                        active_contacts = CompanyContact.objects.filter(active=1)
                        ac_con = list(active_contacts.values())
                    elif data['dept'] != 0:
                        active_contacts = CompanyContact.objects.filter(department_id=data['dept'],active=1)
                        ac_con = list(active_contacts.values())
                    contacts = {
                        'active': ac_con,
                        'inactive': ''
                    }
                    return JsonResponse(contacts)
                elif data['status'] == 0:
                    if data['dept'] == 0:
                        inactive_contacts = CompanyContact.objects.filter(active=0)
                        inac_con = list(inactive_contacts.values())
                    elif data['dept'] != 0:
                        inactive_contacts = CompanyContact.objects.filter(department_id=data['dept'], active=0)
                        inac_con = list(inactive_contacts.values())
                    contacts = {
                        'active': '',
                        'inactive': inac_con
                    }
                    return JsonResponse(contacts)
                
 