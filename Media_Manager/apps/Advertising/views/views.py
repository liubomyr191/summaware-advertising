from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.templatetags.static import static

import json

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *
from ..models.companies import CompanyAccount, CurrentCompany, getChildAccounts
from ..models.permissions import AccountAccess

from .... import views
from ..forms import *
from datetime import datetime as dt

login_redirect = "/login/?next="

def advertising_view(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    currentUser = User.objects.get(id=request.user.id)

    hasCurrentCompany = CurrentCompany.objects.filter(user=currentUser)

    currentCompany = None

    if len(hasCurrentCompany):
        currentCompanyAccounts = getChildAccounts(hasCurrentCompany[0].company)
        currentCompany = hasCurrentCompany[0].company
    else:
        currentCompanyAccounts = []

    # company_accounts = [row.account for row in CompanyAccount.objects.filter(company=1).select_related()]

    publications = Publication.objects.all()

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    current_datetime = dt.now()

    if current_datetime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= current_datetime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'

    try:
        salesperson = SalesPerson.objects.get(email=request.user.email)
        salesperson_id = salesperson.id
        salesperson_accounts = Account.objects.filter(sales_person=salesperson_id)
        salesperson_tasks = SalesPersonTask.objects.filter(salesperson=salesperson_id, completed=False, date=today)

        overdue_tasks = getOverdueSalesPersonTasks(salesrep=salesperson)
        
    except SalesPerson.DoesNotExist:
        salesperson_accounts = None
        salesperson_id = None
        salesperson_tasks = []
        overdue_tasks = []

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "accountList": currentCompanyAccounts,
        "publications": publications,
        "salesperson_id": salesperson_id,
        "salesperson_accounts": salesperson_accounts,
        "salesperson_tasks": salesperson_tasks,
        "overdue_tasks": overdue_tasks, 
        "currentCompany": currentCompany,
        "advertising":True,
        "greeting": greeting
    }

    return render(request, "advertising.html", context)

def list_service_charges(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - service charges page (apply as of <date>, apply to period <period dropdown>, comment, notes, multiselect to choose businesses this applies to)
    serviceCharges = ServiceCharge.objects.all()

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        service_charge = ServiceCharge.objects.get(id=data["charge_id"])
        service_charge.enabled = data["enabled"]
        service_charge.save()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "serviceCharges": serviceCharges,
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)]
    }
    return render(request, "finance/service_charges/list_service_charges.html", context)

def create_service_charge(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        print(reqData)

        account = None
        if 'account' in reqData and reqData is not None:
            try: 
                account = Account.objects.get(pk=reqData['account'])
            except Account.DoesNotExist:
                account = None

        newServiceCharge = ServiceCharge(name=reqData['name'], amount=reqData['amount'], apply_level=reqData['applyLevel'], enabled=True, account=account)
        newServiceCharge.save()

        return JsonResponse({ "message": "New service charge created" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
    }
    return render(request, "finance/service_charges/new_service_charge.html", context)

def edit_service_charge(request, charge_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            serviceCharge = ServiceCharge.objects.get(pk=charge_id)
        except ServiceCharge.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find service charge" }, status=400)

        serviceCharge.name = reqData['name']
        serviceCharge.amount = reqData['amount']
        serviceCharge.apply_level = reqData['applyLevel']
        serviceCharge.enabled = reqData['enabled']

        if 'account' in reqData and reqData['account'] is not None:
            try: 
                account = Account.objects.get(pk=reqData['account'])
                serviceCharge.account = account
            except Account.DoesNotExist:
                serviceCharge.account = None
        else:
            serviceCharge.account = None

        serviceCharge.save()

        return JsonResponse({ "message": "Service charge saved" }, status=200)

def create_account_service_charge(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # form = AccountServiceChargeForm(initial={'order_number': id})

    if request.method == "POST":

        serviceCharge = ServiceCharge.objects.get(id=int(request.POST.get('charge')))
        account = Account.objects.get(id=int(request.POST.get('account')))
        orderNumber = AdvertisingOrder.objects.get(id=request.POST.get('order_number'))

        # charge = AccountServiceCharge(charge=serviceCharge, account=account, order_number=orderNumber)
        # charge.save()

        return HttpResponseRedirect('/advertising/order/' + id)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        # "form": form
    }

    return render(request, "finance/service_charges/new_account_service_charge.html", context)