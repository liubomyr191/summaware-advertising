from datetime import datetime, timedelta, date
import json

from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User

from ... import views

from .models.advertising import *
from .models.publications import *
from .models.orders import *
from .models.permissions import *
from .models.finance import *

import logging
logger = logging.getLogger(__name__)

login_redirect = "/login/?next="

def view_admin_panel(request):
    # ? Should groups have roles too?

    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')

    logging.info(request.user.username + ' accessed the admin page')

    today = datetime.today()
    month_ago = today - timedelta(days=30)

    today = str(today)[:10]
    month_ago = str(month_ago)[:10]

    orderIds = [order.id for order in AdvertisingOrder.objects.filter(bill_date__gte=month_ago).exclude(bill_date='bill_on_demand')]
    orderInvoiceIds = [orderInvoice.order.id for orderInvoice in OrderInvoice.objects.all()]

    ordersToBeInvoiced = [AdvertisingOrder.objects.get(pk=id) for id in orderIds if id not in orderInvoiceIds]

    insertionInvoices = InsertionInvoice.objects.filter(date__lte=date.today(), is_paid=False, date_sent=None)

    """
        somehow get the 'bill_on_demand' insertion bills to be listed alongside the other regular invoices in the table
        and mark when the invoice gets paid, somehow mark the corresponding insertion bill paid as well 

        Thoughts/Notes
        ------------------
        - maybe tag the invoices in such a way that we can mark the orderinsertion bill table row as paid when its paid off?
        - or just change the price of the order so that the correct invoice price is shown (from the orderinsertion bill table)?

    """

    sentInvoices = Invoice.objects.exclude(date_sent__isnull=True).order_by('-date_sent')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "isAdmin": isAdminOrManager(request.user.id),
        "users": User.objects.all(),
        "roles": Role.objects.all().order_by('description'),
        "accounts": Account.objects.all(),
        "salesreps": SalesPerson.objects.all(),
        "ordersToBeInvoiced": ordersToBeInvoiced,
        "sentInvoices": sentInvoices,
        "insertionInvoices": insertionInvoices
    }

    return render(request, 'auth/adminPanel.html', context)

def get_user_roles(request, userId):

    accountId = request.GET.get('account')

    try:
        user = User.objects.get(id=userId)
        account = Account.objects.get(id=accountId)

    except (User.DoesNotExist, Account.DoesNotExist):
        return JsonResponse({ "message": "Invalid parameters. Please try again." }, status=200)

    roleDetails = getUserRoles(user, account)

    return JsonResponse({ "errors": [], "roles": roleDetails }, status=200)

def save_user_roles(request, userId):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user.username)
            role = Role.objects.get(name=request.POST.get('role'))
            account = Account.objects.get(id=request.POST.get('account'))
        except (User.DoesNotExist, Role.DoesNotExist, Account.DoesNotExist):
            return JsonResponse({ "message": "Error. Invalid request."}, status=400)

        hasRole = request.POST.get('hasRole') if request.POST.get('hasRole') else False

        if role.name ==  'admin':
            if hasRole == 'true':
                adminRole = AccountAdmin(account=account, user=user, date_updated=datetime.now())
                adminRole.save()

                logging.info(request.user.username + ' added the role of Admin on account #' + str(account.id) + ' to user ' + user.first_name + ' ' + user.last_name)
            else: 
                try:
                    adminRole = AccountAdmin.objects.get(account=account, user=user)
                    adminRole.delete()

                    logging.info(request.user.username + ' removed the role of Admin on account #' + str(account.id) + ' from user ' + user.first_name + ' ' + user.last_name)
                except AccountAdmin.DoesNotExist:
                    pass
        elif role.name == 'manager':
            if hasRole == 'true':
                adManager = AccountManager(user=user, account=account)
                adManager.save()

                logging.info(request.user.username + ' added the role of Account Manager on account #' + str(account.id) + ' to user ' + user.first_name + ' ' + user.last_name)
            else: 
                try:
                    adManager = AccountManager.objects.get(account=account, user=user)
                    adManager.delete()

                    logging.info(request.user.username + ' removed the role of Account Manager on account #' + str(account.id) + ' from user ' + user.first_name + ' ' + user.last_name)
                except AccountManager.DoesNotExist:
                    pass
        elif role.name == 'ad_assistant':
            if hasRole == 'true':
                adAssistant = AdAssistant(user=user, account=account)
                adAssistant.save()

                logging.info(request.user.username + ' added the role of Ad Assistant on account #' + str(account.id) + ' to user ' + user.first_name + ' ' + user.last_name)
            else: 
                try:
                    adAssistant = AdAssistant.objects.get(account=account, user=user)
                    adAssistant.delete()

                    logging.info(request.user.username + ' removed the role of Ad Assistant on account #' + str(account.id) + ' from user ' + user.first_name + ' ' + user.last_name)
                except AdAssistant.DoesNotExist:
                    pass
        elif role.name == 'salesperson':
            if hasRole == 'true':
                salesperson = AccountSalesperson(user=user, account=account)
                salesperson.save()

                logging.info(request.user.username + ' added the role of Account Salesperson on account #' + str(account.id) + ' to user ' + user.first_name + ' ' + user.last_name)
            else:
                try:
                    salesperson = AccountSalesperson.objects.get(user=user, account=account)
                    salesperson.delete()
                
                    logging.info(request.user.username + ' removed the role of Account Salesperson on account #' + str(account.id) + ' from user ' + user.first_name + ' ' + user.last_name)
                except AccountSalesperson.DoesNotExist:
                    pass

        try:
            userRole = UserRole.objects.get(user=user, role=role, account=account)
            if hasRole != 'true':
                userRole.delete()
                return JsonResponse({ "message": role.description + ' role successfully removed!'})
        except UserRole.DoesNotExist:
            newUserRole = UserRole(user=user, role=role, account=account)
            newUserRole.save()
            return JsonResponse({ "message": role.description + ' role added', "role": model_to_dict(newUserRole)}, status=200)

def view_manager_overrides(request):
    # if not isAdminOrManager(request.user.username):
    #     return HttpResponseRedirect('/advertising')

    managerOverrides = CreditLimitManagerOverride.objects.filter(overridden=False)

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            user = User.objects.get(username=request.user.username)
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find user" }, status=200)

        managerOverride = ManagerOverride(name=reqData['name'], created_by=user, manager=user, notes=reqData['notes'] if 'notes' in reqData else None)
        managerOverride.save()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "managerOverrides": managerOverrides
    }

    return render(request, 'auth/ManagerOverrides.html', context)

def view_publication_access(request):
    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')

    users = User.objects.all()
    publications = Publication.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "users": users,
        "publications": publications
    }

    return render(request, 'auth/PublicationAccess.html', context)

# TODO - add logging messages and document this section thoroughly 
def user_publication_access(request, userId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not isAdminOrManager(request.user.id):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    try:
        user = User.objects.get(pk=userId)
    except User.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find user" }, status=200)

    if request.method == 'GET':
        publicationAccessList = [pub.publication.id for pub in PublicationAccess.objects.filter(user=user)]

        return JsonResponse({ "message": "Success", "publication_access": publicationAccessList }, status=200)

    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            publicationId = reqData['publication'].split('-')[1]
            publication = Publication.objects.get(pk=publicationId)
        except Publication.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find publication. Please try again." }, status=200)

        grantAccess = reqData['isChecked']
        hasPublicationAccess = PublicationAccess.objects.filter(user=userId, publication=publication).exists()

        message = ''

        if hasPublicationAccess and not grantAccess:
            usrPubAccess = PublicationAccess.objects.get(user=userId, publication=publication)
            usrPubAccess.delete()

            message = 'Successfully removed access to ' + publication.name
        
        if not hasPublicationAccess and grantAccess:
            usrPubAccess = PublicationAccess(user=user, publication=publication)
            usrPubAccess.save()

            message = 'Successfully granted access to ' + publication.name

        publicationAccess = [pub.publication.id for pub in PublicationAccess.objects.filter(user=user)]
        
        return JsonResponse({ "message": message, "publication_access": publicationAccess }, status=200)

    else:
        return JsonResponse({ "message": "Error. Invalid request." }, status=400)
    
def view_user_account_access(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')
    
    if request.method == 'GET':
        accountList = Account.objects.all()
        userList = User.objects.all()

        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "accountList": accountList,
            "userList": userList
        }

        return render(request, "auth/UserAccountAccess.html", context)
    
def user_account_access(request, userId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not isAdminOrManager(request.user.id):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        user = User.objects.get(pk=userId)
    except User.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find user" }, status=200)

    if request.method == 'GET':
        accountAccessList = [row.account.id for row in AccountAccess.objects.filter(user=user)]

        return JsonResponse({ "message": "Success", "account_access": accountAccessList }, status=200)


    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        accountId = reqData['accountId'].split('-')[1]
        isChecked = reqData['isChecked']
        
        try:
            account = Account.objects.get(pk=accountId)
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find account" }, status=404)
        
        if isChecked:
            access = AccountAccess(user=user, account=account)
            access.save()
            
            message = "User #" + str(user.id) + " now has access to account #" + str(account.id)
            logging.info(message)
            print(message)

            return JsonResponse({ "message": message }, status=200)
        else:
            try:
                access = AccountAccess.objects.get(user=user, account=account)
                access.delete()

                message = "User #" + str(user.id) + " no longer has access to account #" + str(account.id)
                logging.info(message)
                print(message)

                return JsonResponse({ "message": message }, status=200)
            except AccountAccess.DoesNotExist:
                message = "Cannot find user's account access in the database"
                logging.warning(message)

                return JsonResponse({ "message": message }, status=404)
    else:
        return JsonResponse({ "message": "Error. Invalid request." }, status=400)