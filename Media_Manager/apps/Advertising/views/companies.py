from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.permissions import *
from ..models.finance import *
from ..models.publications import *
from ..models.companies import Company, CompanyAccount, CurrentCompany, UserCompany, CompanyGLCode

from .... import views

login_redirect = "/login/?next="

def list_companies(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    companies = Company.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "companies": companies
    }

    return render(request, "company/CompanyList.html", context)

def create_company(request):
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

        return render(request, "company/CreateCompany.html", context)
    elif request.method == 'POST':
        reqData = request.POST.dict()

        reqData.pop('csrfmiddlewaretoken', None)

        new_company = Company(**reqData)
        new_company.save()

        return HttpResponseRedirect('/advertising/companies/')

def view_company_details(request, company_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    company = get_object_or_404(Company, pk=company_id)
    user = get_object_or_404(User, pk=request.user.id)

    # get the accounts associated with the company
    company_accounts = CompanyAccount.objects.filter(company=company_id).select_related()

    # showing the default contact info (if set) for each account associated with the company
    for row in company_accounts:
        contacts = CompanyContact.objects.filter(account=row.account)
        for contact in contacts:
            if contact.default:
                row.contact_name = contact.first_name + ' ' + contact.last_name
                row.contact_email = contact.email

    # determine if the company shown is the current company selected
    userCompany = UserCompany.objects.filter(user=user, company=company)
    if not userCompany.exists():
        hasAccess = False
        isCurrentCompany = False
    else:
        hasAccess = True if (userCompany.first()).has_access else False
        isCurrentCompany = CurrentCompany.objects.filter(user=user, company=company).exists()

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            account = Account.objects.get(pk=reqData['account_id'])
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find that account." }, status=400)

        company_account = CompanyAccount.objects.filter(company=company, account=account)
        company_account.delete()

        return JsonResponse({ "message": "Account removed" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "company": company,
        "company_accounts": company_accounts, 
        "isCurrentCompany": isCurrentCompany,
        "hasAccess": hasAccess, 
    }

    return render(request, "company/CompanyDetail.html", context)

def edit_company_details(request, company_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        reqData = request.POST.dict()

        company.name = reqData['name']
        company.address = reqData['address']
        company.city = reqData['city']
        company.state = reqData['state']
        company.zipcode = reqData['zipcode']
        company.email = reqData['email']
        company.phone = reqData['phone']
        company.type = reqData['type']
        company.agency_id = reqData['agency_id'] if 'agency_id' in reqData else ''
        company.name = reqData['name']

        company.save()

        return HttpResponseRedirect('/advertising/company/' + str(company.id))

def view_company_credit_limits(request, company_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    company = get_object_or_404(Company, pk=company_id)
    company_accounts = [row.account for row in CompanyAccount.objects.filter(company=company)]

    if request.method == 'POST':
        reqData = request.POST.dict()

        for key in reqData.keys():
            creditLimit = reqData[key]
            accountId = key[20:21]
            
            try:
                account = Account.objects.get(id=accountId)
                account.credit_limit = Decimal(creditLimit)

                account.save()
            except Account.DoesNotExist:
                continue;

        return JsonResponse({ "message": "Success! Credit limits saved!" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "company": company,
        "company_accounts": company_accounts, 
    }

    return render(request, "company/CompanyCreditLimits.html", context)

def user_current_company(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':
        companyList = Company.objects.all()

        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "companyList": companyList,
        }

        return render(request, "company/CurrentCompany.html", context)

    elif request.method == 'POST':
        # TODO - this is throwing an error -> may have to change this back to `json.loads(request.body)`
        reqData = json.loads(request.body.decode('utf-8'))
        
        companyId = reqData['companyId']
        isChecked = reqData['isChecked']

        # TODO --> make sure the user has access to that company before marking it as their current company

        try:
            company = Company.objects.get(id=companyId)
        except Company.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find company. Please try again." }, status=200)
        
        # does the user currently have a company listed?
        anyCurrentCompany = CurrentCompany.objects.filter(user=user).exists()

        # if the user wants this company as their current viewing company
        if isChecked:
            # does the user already have a current company listed?
            if anyCurrentCompany:
                # get the currentCompany entry from the database and remove it 
                currentCompany = CurrentCompany.objects.filter(user=user).first()
                currentCompany.delete()
            
            # create a record in the database
            currentCompany = CurrentCompany(company=company, user=user)
            currentCompany.save()

            message = 'User #' + str(user.id) + ' is now using company #' + str(company.id) + ' ('+ company.name +')'
        
        # if the user wants to remove this as their current company
        else:
            # get the currentCompany entry from the database and remove it 
            currentCompany = CurrentCompany.objects.filter(user=user).first()
            currentCompany.delete()

            message = 'User #' + str(user.id) + ' is no longer using company #' + str(company.id) + ' ('+ company.name +')'
        
        logging.info(message)
        print(message)

        return JsonResponse({ "message": message }, status=200)
    
# managers/admins should be able to grant/revoke certain user's access to different companies
def view_user_company_access(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')
    
    if request.method == 'GET':
        companyList = Company.objects.all()
        userList = User.objects.all()

        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "companyList": companyList,
            "userList": userList
        }

        return render(request, "company/UserCompanyAccess.html", context)

    else: 
        return JsonResponse({ "message": "Error. Method not implemented" }, status=405)
    
def get_user_company_access(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if not isAdminOrManager(request.user.id):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        companyId = request.GET.get('companyId')
        companyList = []

        if companyId != '':
            try:
                company = Company.objects.get(id=companyId)
                companyList = [row.user.id for row in UserCompany.objects.filter(company=company) if row.has_access]
            except Company.DoesNotExist:
                return JsonResponse({ "message": "Error. Cannot find company access details" }, status=200)
    
        return JsonResponse({ "message": "Success", "user_list": companyList }, status=200)
    
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        userId = reqData['userId']
        companyId = reqData['companyId']

        # verify that it is a valid user
        try:
            user = User.objects.get(pk=userId)
        except Exception as ex:
            print(ex)
            logging.info(ex)
            return JsonResponse({ "message": "Error. Cannot find the user.", "error": ex }, status=200)
        
        # verify that it is a valid company
        try:
            company = Company.objects.get(pk=companyId)
        except Exception as ex:
            print(ex)
            logging.info(ex)
            return JsonResponse({ "message": "Error. Cannot find the company.", "error": ex }, status=200)
        
        # check to see if the user had previous access to company
        previousAccess = UserCompany.objects.filter(user=user, company=company)

        # if the user never had access before 
        if not previousAccess.exists() and reqData['hasAccess']:
            userCompany = UserCompany(user=user, company=company, has_access=True)
            userCompany.save()
            
            message = 'User' + str(user.id) + ' now has access to company #' + str(company.id)
            
        # if the user had access, and now does not 
        elif previousAccess.exists() and not reqData['hasAccess']:
            prevAccess = previousAccess.first()
            if not prevAccess:
                return JsonResponse({ "message": "Error. Cannot find current record of access." }, status=2000)
            else:
                prevAccess.has_access = False
                prevAccess.save()

                isCurrentCompany = CurrentCompany.objects.filter(user=user, company=company)
                if isCurrentCompany.exists():
                    currentCompany = isCurrentCompany.first()
                    currentCompany.delete()

                message = 'User #' + str(user.id) + ' no longer has access to ' + company.name

        # if the user had access, then did not, and now has 
        else:
            prevAccess = previousAccess.first()
            prevAccess.has_access = True
            prevAccess.save()

            message = 'User #' + str(user.id) + ' has regained access to ' + company.name

        print(message)
        logging.info(message)
            
        return JsonResponse({ "message": message }, status=200)
        
    else: 
        return JsonResponse({ "message": "Error. Method not implemented" }, status=405)