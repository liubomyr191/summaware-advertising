from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

import json

from ... import views
from .models import Account, AccountType, SalesPerson
from .forms import AdvertisingAccountForm, AccountTypesForm, SalesPersonForm
from Media_Manager.apps.Advertising import forms

url = "192.241.131.173:8000"
login_redirect = "/login/?next="


def advertising_view(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/coming_soon.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    accounts = Account.objects.all()

    context = {
     "access": "allow",
     "message": "",
     "groups": ', '.join(views.get_groups(request)),
     "menu": views.get_sidebar(request),
     "accounts": accounts
    }

    return render(request, "advertising/coming_soon.html", context)


def advertising_new(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # check if this is a POST request
    if request.method == "POST":

        # create an instance of the form and populate the request data into the form
        form = AdvertisingAccountForm(request.POST)

        # sales_person_id = request.POST['sales_person']
        person = SalesPerson.objects.get(id=int(request.POST['sales_person']))

        # check that it is a valid form
        if request.POST:

            # process the form data
            new_account = Account(
                publication=request.POST['publication'],
                submitter=request.POST['submitter'],
                account_type=request.POST['account_type'],
                market_code=request.POST['market_code'],
                business_name=request.POST['business_name'],
                contact_name=request.POST['contact_name'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                city=request.POST['city'],
                state=request.POST['state'],
                zip_code=request.POST['zip_code'],
                website=request.POST['website']
            )

            # save the form data to the database
            id = int(request.POST['sales_person'])
            new_account.sales_person = SalesPerson.objects.get(id=id)
            new_account.save()

            # redirect to the main advertising page
            return HttpResponseRedirect("/advertising/account/" + new_account.id)

    # if it is a GET request
    else: 

        # create a new instance of the form
        form = AdvertisingAccountForm(initial={'submitter': request.user})

    context = {
     "access": "allow", 
     "message":"", 
     "groups": ', '.join(views.get_groups(request)), 
     "menu": views.get_sidebar(request),
     "form": form
    }
    return render(request, "advertising/advertising_new.html", context)

def advertising_account(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # retrieve account information from database 
    # if it does not exist, return a 404 error 
    account = get_object_or_404(Account, pk=id)

    context = {
        "access": "allow", 
        "message":"", 
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account": account
    }

    return render(request, 'advertising/advertising_account.html', context)

def edit_advertising_account(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if id: 
        # get the corresponding account data given the id parameter
        account = Account.objects.get(id=id)

    form = AdvertisingAccountForm(request.POST or None, instance=account)
    
    if request.POST:
        account.publication = request.POST['publication']
        account.submitter = request.POST['submitter']
        account.account_type = request.POST['account_type']

        id = int(request.POST['sales_person'])
        account.sales_person = SalesPerson.objects.get(id=id)

        account.market_code = request.POST['market_code']
        account.business_name = request.POST['business_name']
        account.contact_name = request.POST['contact_name']
        account.address = request.POST['address']
        account.city = request.POST['city']
        account.state = request.POST['state']
        account.zip_code = request.POST['zip_code']
        account.phone = request.POST['phone']
        account.email = request.POST['email']
        account.website = request.POST['website']

        account.save()
        return HttpResponseRedirect("/advertising/account/" + {account.id})

    context = {
        "access": "allow", 
        "message":"", 
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account": account,
        "form": form
    }

    return render(request, 'advertising/advertising_edit.html', context)

def create_account_type(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # check if this is a POST request
    if request.method == "POST":

        # create an instance of the form and populate the request data into the form 
        form = AccountTypesForm(request.POST)

        # check that it is a valid form
        if form.is_valid():

            # process the form data
            new_account_type = AccountType(
                code=(form.cleaned_data['code']).upper(),
                description=(form.cleaned_data['description']).capitalize()
            )

            # save the form data to the database
            new_account_type.save()

            # redirect to the main advertising page
            return HttpResponseRedirect('/advertising')

    # if it is a GET request
    else: 
        # create a new instance of the form
        form = AccountTypesForm()

    context = {
     "access": "allow", 
     "message":"", 
     "groups": ', '.join(views.get_groups(request)), 
     "menu": views.get_sidebar(request),
     "form": form
    }
    return render(request, "advertising/advertising_new_account_type.html", context)

def create_salesperson(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising/advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # check if this is a POST request
    if request.method == "POST":
        
        # create an instance of the form and populate the request data into the form 
        form = SalesPersonForm(request.POST)

        # check that it is a valid form
        if form.is_valid():
            # process the form data
            new_salesperson = SalesPerson(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                company=form.cleaned_data['company'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number']
            )

            # save the form data to the database
            new_salesperson.save()

            # redirect to the main advertising page
            return HttpResponseRedirect('/advertising')

    # if it is a GET request
    else: 
        # create a new instance of the form
        form = SalesPersonForm()

    context = {
     "access": "allow", 
     "message":"", 
     "groups": ', '.join(views.get_groups(request)), 
     "menu": views.get_sidebar(request),
     "form": form
    }
    return render(request, "advertising/advertising_salesperson_new.html", context)


def all_advertisers(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    return render(request, "advertising/advertisers_all.html") 