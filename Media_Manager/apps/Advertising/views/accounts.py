from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

import json
import csv
from datetime import timedelta, datetime, date
from decimal import Decimal

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.permissions import *
from ..models.finance import *
from ..models.publications import *

from .... import views
from ..models import Account, AccountType, SalesPerson
from ..forms import *

from ..validate import validateZipCode, validateState, validateEmail

login_redirect = "/login/?next="

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def advertising_account(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # get account details
    account = get_object_or_404(Account, pk=id)
    user = get_object_or_404(User, pk=request.user.id)

    adminOrManager = isAdminOrManager(user.id, account.id)

    logger.info('/' + str(request.method) + ' - ' + str(request.user) + ' visited account #' + str(account.id) + '\'s page')

    if is_ajax(request):
        days = (date.today() - account.created_at.date()).days
        return JsonResponse({ "message": "Success", "days": days}, status=200)

    company_contacts = [contact for contact in CompanyContact.objects.all() if contact.account_id == account.id and not contact.active]

    try:
        billing_contact = CompanyContact.objects.get(account_id=account.id, active=True)
    except CompanyContact.DoesNotExist:
        billing_contact = None

    count = 0 
    advertising_orders = []
    for order in AdvertisingOrder.objects.filter(is_draft=False, status='running').order_by('-id'):
        if count < 5 and order.account_id == account.id:
            advertising_orders.append(order)
            count += 1
        # order.ad_type = AdType.objects.get(id=int(order.ad_type.id))

    history = [line for line in AccountHistory.objects.order_by('-timestamp') if int(line.account_id) == int(id)]

    salesRepNotes = None if account.sales_person is None else AccountSalesRepNote.objects.filter(sales_person=account.sales_person.id, account=account)

    today = date.today().strftime('%Y-%m-%d')

    if account and account.write_off_amount and account.write_off_period:
        if account.write_off_period == 'months':
            writeOffTime = account.write_off_amount * 30
        elif account.write_off_period == 'weeks':
            writeOffTime = account.write_off_amount * 7
        elif account.write_off_period == 'days':
            writeOffTime = account.write_off_amount
        
        writeOffDays = {}
        for invoice in Invoice.objects.filter(account=account, is_paid=False):
            writeOffDays[invoice.id] = invoice.bill_end + timedelta(days=writeOffTime)

    all_invoices = Invoice.objects.filter(account=account)
    open_invoices = [invoice for invoice in all_invoices if invoice.is_paid is False]
    paid_invoices = [invoice for invoice in all_invoices if invoice.is_paid is True]

    paid_invoices.sort(key=lambda x: x.date_paid, reverse=True)

    # if there's invoices linked to the account
    if len(all_invoices) > 0:

        # if there's only one invoice linked to the account
        if len(all_invoices) == 1:
            latest_invoice = open_invoices[0]
            oldest_invoice = open_invoices[0]

        # if there's more than one invoice linked to the account
        else:
            latest_invoice = open_invoices[len(open_invoices) - 1]
            oldest_invoice = open_invoices[0]
    
    # if there are no invoices linked to the account
    else:
        latest_invoice = None
        oldest_invoice = None

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        amount = str(float(reqData['amount']))
        
        if reqData['type'] == 'account_balance':
            goesTo = reqData['goesTo']
            if goesTo == 'account_balance':
                account.balance = account.balance - amount
                account.save()

                paymentNotes = 'Paid ' + amount + ' towards the account balance'
                payment = AccountPaymentHistory(account=account, amount=amount, payment_type='Default', payment_method='dev', payment_notes=paymentNotes)
                payment.save() 

                logging.info(request.user.username + ' paid '  + amount  + ' towards the account ' +  account.id + '\'s balance')

                return JsonResponse({ "message": "Success! Account balance is now " + account.balance }, status=200)
            elif goesTo == 'latest_invoice':
                latest_invoice.amount = latest_invoice.amount - amount

                if latest_invoice.amount == 0:
                    latest_invoice.is_paid = True
                    latest_invoice.date_paid = datetime.now()

                    message = "Success! Invoice #" + latest_invoice.id + " is now paid completely"
                
                else:
                    latest_invoice.amount = latest_invoice.amount - amount
                    message = "Success! Invoice #" + latest_invoice.id + " now has a balance of $" + latest_invoice.amount
                
                latest_invoice.save()

                return JsonResponse({ "message": message }, status=200)

            elif goesTo ==  'oldest_invoice':
                oldest_invoice.amount = oldest_invoice.amount - amount

                if oldest_invoice.amount == 0:
                    oldest_invoice.is_paid = True
                    oldest_invoice.date_paid = datetime.now()

                    message = "Success! Invoice #" + oldest_invoice.id + " is now paid completely"
                
                else:
                    oldest_invoice.amount = oldest_invoice.amount - amount
                    message = "Success! Invoice #" + oldest_invoice.id + " now has a balance of $" + oldest_invoice.amount
                
                oldest_invoice.save()

                return JsonResponse({ "message": message }, status=200)

            elif goesTo ==  'split_oldest_latest':
                latestInvoiceAmount = float("{:.2f}".format(amount/2))
                oldestInvoiceAmount = float("{:.2f}".format(amount - latestInvoiceAmount))

                oldest_invoice.amount -= oldestInvoiceAmount
                oldest_invoice.save()

                latest_invoice.amount -= latestInvoiceAmount
                latest_invoice.save()

                if oldest_invoice.amount <= 0:
                    oldest_invoice.is_paid = True
                    oldest_invoice.date_paid = datetime.now()

                if latest_invoice.amount <= 0:
                    latest_invoice.is_paid = True
                    latest_invoice.date_paid = datetime.now()

                message = 'Payment successful'

                return JsonResponse({ "message": message }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account": account,
        "sales_person": account.sales_person,
        "company_contacts": company_contacts,
        "advertising_orders": advertising_orders,
        "history": history,
        "account_notes": AccountNote.objects.filter(account=account),
        "salesRepNotes": salesRepNotes,
        "today": today,
        "billing_contact": billing_contact,
        "open_invoices": open_invoices,
        "paid_invoices": paid_invoices,
        "adminOrManager": adminOrManager
    }

    return render(request, 'accounts/advertising_account.html', context)

def edit_advertising_account(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - when editing the account, have a dropdown for the billing contact (from the Company Contacts table)
    # this will work just like the default contact does (only 1 per account)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account_types": AccountType.objects.all(),
        "sales_people": SalesPerson.objects.all(),
        "industry_codes": IndustryCode.objects.all(),
        "publications": Publication.objects.all(),
    }

    if id:
        account = Account.objects.get(id=id)
        context['adminOrManager'] = isAdminOrManager(request.user.id, account.id)

        context['account'] = account
        context['industry_codes'] = IndustryCode.objects.filter(account_id=account.id)

        sort_order = [overflow.name for overflow in OverflowBalance.objects.filter(account=account).order_by('sort_order')]

        context['overflow_account_balance'] = sort_order.index('account_balance') if 'account_balance' in sort_order else None
        context['overflow_oldest_invoice'] = sort_order.index('oldest_invoice') if 'oldest_invoice' in sort_order else None
        context['overflow_floating_credit'] = sort_order.index('floating_credit') if 'floating_credit' in sort_order else None

    if request.method == 'POST':

        account.archived = True if request.POST.get('archived') == "on" else False
        account.submitter = request.user.username

        account.name = request.POST.get('name')
        account.contact_name = request.POST.get('contact_name')
        account.address = request.POST.get('address')
        account.city = request.POST.get('city')
        account.state = request.POST.get('state')
        account.zip_code = request.POST.get('zip_code')
        account.phone = request.POST.get('phone')
        account.email = request.POST.get('email')
        account.website = request.POST.get('website')
        account.legacy_id = request.POST.get('legacy_id')
        account.billing_email = request.POST.get('billing_email')
        account.invoice_frequency = request.POST.get('invoice_frequency')
        account.mail_invoice_charge = request.POST.get('mail_invoice_charge') if request.POST.get('mail_invoice_charge') else 0.0

        account.write_off_amount = request.POST.get('writeOffAmount') if request.POST.get('writeOffAmount') else 0
        account.write_off_period = request.POST.get('writeOffPeriod')

        isPrintChargeActive = True if account.mail_invoice_charge != 0.0 or '' else False
        # TODO - make sure this isnt creating a lot of unnecessary AccountPrintInvoiceCharges in the database 
        printCharge = AccountPrintInvoiceCharge(account=account, amount=Decimal(account.mail_invoice_charge), active=isPrintChargeActive)
        printCharge.save()

        account.account_type = AccountType.objects.get(id=request.POST.get('account_type')) if request.POST.get('account_type') else None
        account.sales_person = SalesPerson.objects.get(id=request.POST.get('sales_person')) if request.POST.get('sales_person') else None
        account.industry_code = IndustryCode.objects.get(id=request.POST.get('industry_code')) if request.POST.get('industry_code') else None

        account.credit_limit = request.POST.get('credit_limit')
        account.invoice_type = request.POST.get('invoice_type')

        account.can_accept_checks = True if request.POST.get('can_accept_checks') == 'on' else False
        account.tax_exempt = True if request.POST.get('tax_exempt') == 'on' else False
        # account.use_credit_first = True if request.POST.get('use_credit_first') == 'on' else False
        account.prepay_required = True if request.POST.get('prepay_required') == 'on' else False

        account.default_publication = Publication.objects.get(id=request.POST.get('default_publication')) if request.POST.get('default_publication') else None

        # get the previous overflow balance order from the database 
        prevOverflowBalances = OverflowBalance.objects.filter(account=account)
        for balance in prevOverflowBalances:
            balance.delete()

        for i in range(3):
            name = request.POST.get('overflow_' + str(i+1))
            accepted_names = ['account_balance', 'oldest_invoice', 'floating_credit']
            if (name != '') and name in accepted_names:
                overflow_balance = OverflowBalance(account=account, name=request.POST.get('overflow_' + i+1), sort_order=(i+1))
                overflow_balance.save()

        account.save()

        # TODO - add entry to show changes made to account (old vs. new)
        detail = request.user.username + " updated the ad account"
        submitter = request.user.first_name + " " + request.user.last_name
        history = AccountHistory(detail=detail, account=account, submitter=submitter)
        history.save()

        return HttpResponseRedirect("/advertising/account/" + str(account.id))

    return render(request, 'accounts/advertising_edit.html', context)

def create_account(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - when the user fills out the contact portion of the form, use the information to create a company contact 
    # TODO - if a sales rep is creating the account, it should default the sales rep field to be their sales rep account
    # TODO - submitter/ad taker field should be a dropdown of all sales reps, admins, etc. (anybody with the correct permissions to create an order)

    if request.method == "POST":
        isValidEmail = validateEmail(request.POST.get('email'))
        if not isValidEmail:
            print('Error. ' + request.POST.get('email') + ' is not a valid email')

        isValidState = validateState(request.POST.get('state'))
        if not isValidState:
            print('Error. ' + request.POST.get('state') + ' is not a valid state')

        isValidZip = validateZipCode(request.POST.get('zip_code'))
        if not isValidZip:
            print('Error. ' + request.POST.get('zip_code') + ' is not a valid zip')

        if request.POST.get('accountType') != '':
            try:
                accountType = AccountType.objects.get(pk=request.POST.get('accountType'))
            except AccountType.DoesNotExist:
                accountType = None
                print('Error. ' + request.POST.get('accountType') + ' is not a valid account type')
        else:
            accountType = None
        
        if request.POST.get('sales_person') != '':
            try:
                salesperson = SalesPerson.objects.get(pk=request.POST.get('sales_person'))
            except SalesPerson.DoesNotExist:
                salesperson = None
                print('Error. ' + request.POST.get('sales_person') + ' is not a valid salesperson id')

        else:
            salesperson = None

        if request.POST.get('industry_code') != '':
            try:
                industry_code = IndustryCode.objects.get(pk=request.POST.get('industry_code'))
            except IndustryCode.DoesNotExist:
                industry_code = None
                print('Error. ' + request.POST.get('industry_code') + ' is not a valid industry code id')
        else:
            industry_code = None

        contactName = request.POST.get('first_name')+' '+request.POST.get('last_name')
        account = Account(name=request.POST.get('name'), contact_name=contactName, contact_name_first=request.POST.get('first_name'), contact_name_last=request.POST.get('last_name'), company_name_1=request.POST.get('company_name_1'), company_name_2=request.POST.get('company_name_2'), address=request.POST.get('address'), address_2=request.POST.get('address2'), country=request.POST.get('country'), city=request.POST.get('city'), state=request.POST.get('state'),
                            zip_code=request.POST.get('zip_code'), tearsheets=request.POST.get('tearsheets'), phone=request.POST.get('phone'), email=request.POST.get('email'), billing_email=request.POST.get('billingEmail'), tax_id=request.POST.get('tax_id'), prepay_required=request.POST.get('prepay_required'),
                            website=request.POST.get('website'), legacy_id=request.POST.get('legacy_id'), submitter=request.user.username, account_type=accountType,
                            sales_person=salesperson, industry_code=industry_code)
        account.save()

        mainAddress = AccountAddress(account=account, address1=request.POST.get('address'), city=request.POST.get('city'), state=request.POST.get('state'),
                                        zip_code=request.POST.get('zip_code'), primary=True)
        mainAddress.save()

        contact = CompanyContact(account=account, first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'), default=True, active=True)
        contact.save()

        if request.POST.get('use-billing-address'):
            if request.POST.get('use-billing-address') ==  'different':
                address = AccountAddress(account=account, address1=request.POST.get('billing-address'), city=request.POST.get('billing-city'), billing=True)

                if not validateState(request.POST.get('billing-state')):
                    print('Error. ' + request.POST.get('billing-state') + ' is not a valid state')
                    address.state = None
                else:
                    address.state = request.POST.get('billing-state')

                if not validateZipCode(request.POST.get('billing-zip-code')):
                    print('Error. ' + request.POST.get('billing-zip-code') + ' is not a valid zip code')
                    address.zip_code = None
                else:
                    address.zip_code = request.POST.get('billing-zip-code')

                address.save()
            elif request.POST.get('use-billing-address') ==  'same':
                address = AccountAddress(account=account, address1=request.POST.get('address'), city=request.POST.get('city'), state=request.POST.get('state'),
                                            zip_code=request.POST.get('zip_code'), billing=True)
                
                address.save()

        message = 'Account #' + str(account.id) + ': ' + account.name + 'created by ' + request.user.username
        logging.info(message)
        print(message)

        return HttpResponseRedirect("/advertising/account/" + str(account.id))

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "accountTypes": AccountType.objects.all(),
        "industryCodes": IndustryCode.objects.all().order_by('code'),
        "salespersonList": SalesPerson.objects.all()

    }
    return render(request, "accounts/advertising_new.html", context)

def merge_account(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - show the two accounts side by side and select what merges over Account A
    # orders, payments, notes, everything, etc.

    if request.method == "POST":
        form = MergeAccountForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["account1"] == form.cleaned_data["account2"]:
                print("Two accounts cannot be the same")
            else:
                account1 = Account.objects.get(id=int(form.cleaned_data['account1']))
                account2 = Account.objects.get(id=int(form.cleaned_data['account2']))

                account2.archived = True
                account2.save()

                return HttpResponseRedirect('/advertising')

    else:
        form = MergeAccountForm()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "form": form
    }
    return render(request, "accounts/merge_account.html", context)

def import_account_data(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        file = request.FILES.get('csv_file')
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        import_data = []
        for row in reader: 
            import_data.append(row)

        data = json.dumps(import_data, indent=4)
                
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
    }
    return render(request, "accounts/import_account_data.html", context)

# TODO - create a view function for importing account data
    # when importing account data, assume the user is starting from scratch
    # if it comes across a salesperson not already in the system, create and save that salesperson 

def get_account_names(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        if request.GET.get('name'):
            accountName = request.GET.get('name')
            try:
                account = Account.objects.get(name=accountName)
            except Account.DoesNotExist:
                account = None

            print(request.GET.get('name'))

            return JsonResponse({ "message": "Success", "id": account.id }, status=200)
        elif request.GET.get('id'):
            accountId = request.GET.get('id')
            try:
                account = Account.objects.get(id=accountId)
            except Account.DoesNotExist:
                account = None

            return JsonResponse({ "message": "Success", "id": account.id }, status=200)
        else:
            return JsonResponse({ "message": "Error. An error has occurred." }, status=200)
    
    else:
        return JsonResponse({ "message": "Error. Method not implemented." }, status=405)