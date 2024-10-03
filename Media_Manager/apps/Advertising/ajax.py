from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

import json
from datetime import datetime, timedelta
from random import randint
from decimal import Decimal

from Media_Manager.apps.Advertising.models.permissions import CreditLimitManagerOverride

from .models.advertising import *
from .models.orders import *
from .models.rates import *
from .models.finance import *
from .models.publications import *
from .models.companies import Company, CompanyAccount, CompanyGLCode, CurrentCompany

from ... import views
from .helpers import is_ajax

login_redirect = "/login/?next="

import logging
logger = logging.getLogger(__name__)

def getValueFromJSON(data, name):
    if isinstance(data, str):
        data = json.loads(data)

    for item in data:
        if item['name'] == name:
            return item['value']
        else:
            continue

def generateRandomNumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def late_order(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    data = json.loads(request.body.decode('utf-8'))
    formData = json.loads(data['jsonFormData'])
    confirmFormData = json.loads(data['confirmFormData'])

    publicationId = int(getValueFromJSON(formData, "publication"))
    publication = Publication.objects.get(id=publicationId)

    managerEmail = getValueFromJSON(confirmFormData, "managerEmail")
    publicationEmail = getValueFromJSON(confirmFormData, "publicationEmail")

    approval = LateAdApproval(manager_email=managerEmail, publication_email=publicationEmail)

    return JsonResponse({"errors": []}, status=200)

def get_rate_location(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    data = json.loads(request.body.decode('utf-8'))

    try:
        rateLocation = RateLocation.objects.get(location=data['location'], publication_id=data['publication'])
    except RateLocation.DoesNotExist:
        rateLocation = None

    if rateLocation is None:
        return JsonResponse({"errors": ["Rate location not found!"]}, status=200)

    return JsonResponse({"errors": [], "rate": model_to_dict(rateLocation)}, status=200)

def search_account(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        value = request.GET.get('value')
        if value is None:
            return JsonResponse({"errors": ["No value provided!"]}, status=200)
        else:
            value = value.strip()
            accounts = Account.objects.filter(name__icontains=value)
            # get publications for each account found 
            for account in accounts:
                account.publications = Publication.objects.filter(account=account)

            data = []
            for account in accounts:
                account_dict = model_to_dict(account)
                account_dict['sales_person'] = model_to_dict(SalesPerson.objects.get(id=account_dict['sales_person']))
                account_dict['account_type'] = model_to_dict(AccountType.objects.get(id=account_dict['account_type']))
                account_dict['publications'] = []
                for publication in account.publications:
                    if publication.account_id == account.id:
                        account_dict['publications'].append(model_to_dict(publication))
                data.append(account_dict)

            return JsonResponse({ "errors": [], "results": data }, status=200)

def order_search_account(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        value = request.GET.get('value')
        if value is None:
            return JsonResponse({"errors": ["No value provided!"]}, status=200)
        else:
            value = value.strip()
            accounts = Account.objects.filter(business_name__icontains=value).values()

            results = []
            for account in accounts:
                results.append(account)
            return JsonResponse({ "errors": [], "results": results}, status=200)

def order_search_rates(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        publications = request.GET.getlist('publications[]')
        adType = request.GET.get('ad_type')
        startDate = request.GET.get('start_date')
        endDate = request.GET.get('end_date')

        try:
            adType = AdType.objects.get(pk=adType)
        except AdType.DoesNotExist:
            return JsonResponse({ "message": "Invalid Ad Type. Please try again." }, status=404)

        publicationList = []
        for publication in publications:
            try:
                publication = Publication.objects.get(id=publication)
            except Publication.DoesNotExist:
                continue

            publicationList.append(publication)

        rateList = getActiveRatesByPublicationArray(publicationList, adType)

    return JsonResponse({ "errors": [], "rates": rateList }, status=200)

def order_search_rate_details(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        rate_id = request.GET.get('ad_rate') 
        if rate_id != '':
            try:
                rate = AdvertisingRate.objects.get(id=rate_id)
            except AdvertisingRate.DoesNotExist:
                return JsonResponse({"message": "No rate found. Please try again." }, status=404)
            
            return JsonResponse({ "rate": model_to_dict(rate) }, status=200)
        else:
            return JsonResponse({ "message": "Invalid rate id. Please try again. "}, status=404)

def order_search_adjustments(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        requestData = request.GET.get('value')
        if requestData is None:
            return JsonResponse({"errors": ["No value provided!"]}, status=200)
        else:
            requestData = requestData.split(',')
            adjustmentList = []
            for publication_id in requestData:
                adjustments = Adjustment.objects.filter(publication_id=publication_id)
                for adjustment in adjustments:
                    adjustmentList.append(model_to_dict(adjustment))

            return JsonResponse({ "errors": [], "results": [adjustmentList]}, status=200)

def order_subtotal(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

        data = json.loads(request.body.decode('utf-8'))

        account = Account.objects.get(pk=data['accountId'])

        if data['ad_type'] == '':
            return JsonResponse({"errors": ["Ad type is required!"]}, status=400)
                
        ad_type = AdType.objects.get(id=data['ad_type'])

        publicationNames = []
        for publication in data['publications']:
            publicationNames.append(Publication.objects.get(id=publication).name)

        ad_rate_details = {}
        ad_rates = data['ad_rate']
        # publications = ad_rates.keys()
        for index, rate in enumerate(ad_rates):
            pubName = publicationNames[index]
            try:
                rate_details = AdvertisingRate.objects.get(pk=ad_rates[rate]['rate_id']) 

                numberUnits = int(ad_rates[rate]['number_units'])
                unitPrice = float(rate_details.unit_price)
                subtotal = str(numberUnits * unitPrice)

                ad_rate_details[pubName] = {
                    "rate_details": model_to_dict(rate_details),
                    "subtotal": subtotal
                }
                
            except AdvertisingRate.DoesNotExist:
                continue

        adjustment_list = []
        if len(data['adjustments']) > 0:
            for adjustment in data['adjustments']:
                adjustments = adjustment.split('-')
                adjustment_list.append(model_to_dict(Adjustment.objects.get(id=int(adjustments[1]))))

        sales_person = SalesPerson.objects.get(id=data['salesperson'])

        insertion_list = {}
        totalInsertions = 0
        for pubName in publicationNames:
            publication = Publication.objects.get(name=pubName)
            runDays = PublicationRunDay.objects.get(publication=publication)

            runDaysDict = model_to_dict(runDays)

            startDate = datetime.strptime(data['start_date'], '%Y-%m-%d')
            endDate = datetime.strptime(data['end_date'], '%Y-%m-%d')

            numDaysBetween = (endDate - startDate).days

            insertion_list[pubName] = []

            currentDate = startDate
            while numDaysBetween >= 0:
                weekday = daysOfTheWeek[currentDate.weekday()]
                if runDaysDict[weekday]:
                    insertion = {
                        "weekday": weekday,
                        "date": currentDate.strftime('%Y-%m-%d')
                    }
                    insertion_list[pubName].append(insertion)
                    totalInsertions += 1
                currentDate += timedelta(days=1)
                numDaysBetween -= 1

        return JsonResponse({
            "errors": [], 
            "creditLimit": account.credit_limit,
            "ad_type": model_to_dict(ad_type), 
            "ad_rates": ad_rate_details,
            "publications": publicationNames,
            "adjustments": adjustment_list,
            "sales_person": model_to_dict(sales_person),
            "insertion_list": insertion_list,
            "totalInsertions": totalInsertions
        }, status=200)

def edit_order_rates(request):
    if request.method == 'GET':
        orderId = request.GET.get('order')
        publicationList = request.GET.getlist('publications[]')

        try:
            order = AdvertisingOrder.get(pk=orderId)
        except AdvertisingOrder.DoesNotExist:
            return JsonResponse({ "message: Error. Order cannot be found. "}, status=400)

        rateList = getOrderRatesByPublicationArray(order, publicationList)

    return JsonResponse({ "message": 'Success', "rateList": rateList})

def company_account_list(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'GET':
        company_id = request.GET.get("id")

        accounts = [model_to_dict(account) for account in Account.objects.all()]
        company_accounts = [model_to_dict(company_account) for company_account in CompanyAccount.objects.filter(company=company_id)]
        
        return JsonResponse({ "message": "Success", "accounts": accounts, "company_accounts": company_accounts }, status=200)
    
    if request.method =='POST':
        reqData = json.loads(request.body.decode('utf-8'))

        account_id = int(reqData['account_id']) if "account_id" in reqData else None
        company_id = reqData['company_id']

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return JsonResponse({ "message": "Error. Company with that id does not exist. Please try again."}, status=404)

        if account_id is not None:
            account = Account.objects.get(pk=account_id)
            
            if reqData["checked"]:
                company_account = CompanyAccount(company=company, account=account)
                company_account.save()

                return JsonResponse({ "message": "Account added" }, status=200)
            elif reqData["checked"] == False:
                try:
                    company_account = CompanyAccount.objects.get(company=company, account=account)
                    company_account.delete()
                except CompanyAccount.DoesNotExist:
                    pass
                return JsonResponse({ "message": "Account removed" }, status=200)
            
        # TODO - what should be done if the account id is None?
        else:
            pass

def account_details(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        try:
            account = Account.objects.get(id=account_id)
            return JsonResponse({ "errors": [], "account": model_to_dict(account) }, status=200)
        except Account.DoesNotExist:
            return JsonResponse({"errors": ["Account not found."]}, status=200)

def get_account_notes(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        if id is None:
            return JsonResponse({"errors": ["No account id provided!"]}, status=200)
        else:
            account = Account.objects.get(id=id)
            account_notes = AccountNote.objects.filter(account=account)
            data = []
            for account_note in account_notes:
                timestamp = account_note.timestamp.strftime("%m/%d/%Y %H:%M:%S")
                note = model_to_dict(account_note)
                note['timestamp'] = timestamp
                data.append(note)
            return JsonResponse({ "errors": [], "results": data }, status=200)


    else:
        if request.body is None:
            return JsonResponse({"errors": ["No note provided!"]}, status=200)

        data = json.loads(request.body.decode('utf-8'))
        if data:
            note = data['notes']
            accountId = data['account_id']
            if note == '':
                return JsonResponse({"errors": ["No note provided!"]}, status=200)
            account = Account.objects.get(id=accountId)

            new_note = AccountNote(account=account, note=note, user=request.user.username)
            new_note.save()

            detail = request.user.username + ' added a note'
            submitter = request.user.first_name + ' ' + request.user.last_name
            history = AccountHistory(account=account, submitter=submitter, detail=detail)
            history.save()

            return JsonResponse({ "errors": [], "results": model_to_dict(new_note) }, status=200)
        else:
            return JsonResponse({"errors": ["Unable to create note"]}, status=200)

def edit_account_note(request, account_id, note_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        if account_id is None:
            return JsonResponse({"errors": ["No account id provided!"]}, status=200)

        if note_id is None:
            return JsonResponse({"errors": ["No note id provided!"]}, status=200)

        account = Account.objects.get(id=account_id)
        accountNote = AccountNote.objects.get(id=note_id)

        note = {
            "account_note": model_to_dict(accountNote),
            "account_id": account.id,
            "timestamp": accountNote.timestamp.strftime("%m/%d/%Y %H:%M:%S")
        }

        return JsonResponse({ "errors": [], "results": note }, status=200)

    else:
        if request.body is None:
            return JsonResponse({"errors": ["No note provided!"]}, status=200)

        data = json.loads(request.body.decode('utf-8'))
        if data:
            note = data['note']
            accountId = data['account_id']
            if note == '':
                return JsonResponse({"errors": ["No note provided!"]}, status=200)
            account = Account.objects.get(id=accountId)
            accountNote = AccountNote.objects.get(id=data['note_id'])
            accountNote.note = note
            accountNote.save()
            return JsonResponse({ "errors": [], "results": model_to_dict(accountNote) }, status=200)
        else:
            return JsonResponse({"errors": ["Unable to save note"]}, status=200)

def get_salesrep_notes(request, id, sales_rep_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        if id is None:
            return JsonResponse({"errors": ["No account id provided!"]}, status=200)
        
        if sales_rep_id is None:
            return JsonResponse({"errors": ["No sales rep id provided!"]}, status=200)
        
        account = Account.objects.get(id=id)
        sales_rep = SalesPerson.objects.get(id=sales_rep_id)
        accountSalesrepNotes = AccountSalesRepNote.objects.filter(account=account, sales_person_id=sales_rep)
        data = []
        for accountSalesrepNote in accountSalesrepNotes:
            timestamp = accountSalesrepNote.timestamp.strftime("%m/%d/%Y %H:%M:%S")
            note = model_to_dict(accountSalesrepNote)
            note['timestamp'] = timestamp
            note['sales_person'] = model_to_dict(accountSalesrepNote.sales_person)
            data.append(note)
        return JsonResponse({ "errors": [], "results": data }, status=200)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        if data['sales_rep_id'] == '':
            return JsonResponse({"errors": ["Sales rep id is required!"]}, status=200)

        if data['note'] == '':
            return JsonResponse({"errors": ["No note provided!"]}, status=200)

        if request.user.is_superuser:
            pass

        sales_rep = SalesPerson.objects.get(id=data['sales_rep_id'])
        account = Account.objects.get(id=data['account_id'])
        note = data['note']

        new_note = AccountSalesRepNote(account=account, sales_person=sales_rep, note=note)
        new_note.save()

        return JsonResponse({ "errors": [], "results": model_to_dict(new_note) }, status=200)

def edit_salesrep_note(request, account_id, sales_rep_id, note_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "GET":
        if account_id is None:
            return JsonResponse({"errors": ["No account id provided!"]}, status=200)

        if sales_rep_id is None:
            return JsonResponse({"errors": ["No sales rep id provided!"]}, status=200)

        if note_id is None:
            return JsonResponse({"errors": ["No note id provided!"]}, status=200)

        account = Account.objects.get(id=account_id)
        sales_rep = SalesPerson.objects.get(id=sales_rep_id)
        accountSalesRepNote = AccountSalesRepNote.objects.get(id=note_id)

        note = {
            "id": accountSalesRepNote.id,
            "account_id": account.id,
            "sales_person": model_to_dict(sales_rep),
            "note": accountSalesRepNote.note,
            "timestamp": accountSalesRepNote.timestamp.strftime("%m/%d/%Y %H:%M:%S")
        }

        return JsonResponse({ "errors": [], "results": note }, status=200)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data['note'] == '':
            return JsonResponse({"errors": ["No note provided!"]}, status=200)

        if request.user.is_superuser:
            pass

        sales_rep = SalesPerson.objects.get(id=data['sales_rep_id'])
        account = Account.objects.get(id=data['account_id'])
        note = data['note']

        accountSalesrepNote = AccountSalesRepNote.objects.get(id=data['note_id'])
        accountSalesrepNote.note = note
        accountSalesrepNote.save()

        return JsonResponse({ "errors": [], "results": model_to_dict(accountSalesrepNote) }, status=200)

def get_publication_run_days(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if publication_id is None:
        return JsonResponse({"errors": ["No publication id provided!"]}, status=200)

    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({"error": "Publication does not exist with the id provided."}, status=404)
    
    data = getPublicationRunDays(publication)

    return JsonResponse({ "errors": [], "results": data }, status=200)

def import_gl_codes(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

    return HttpResponseRedirect('/advertising/company/' + id)

def get_salesreps_tasks(request, salesrep_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    try:
        salesrep = SalesPerson.objects.get(id=salesrep_id)
    except SalesPerson.DoesNotExist:
        return JsonResponse({ "message": "Sales Person not found." }, status=404)

    tasks = getActiveSalesPersonTasks(salesrep)
    name = str(salesrep.first_name + " " + salesrep.last_name)

    if len(tasks) > 0:
        return JsonResponse({ "message": "Tasks found.", "taskList": tasks, "name": name }, status=200)
    else:
        return JsonResponse({ "message": "No tasks found.", "name": name }, status=200)

def new_salesrep_task(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        try:
            salesperson = SalesPerson.objects.get(id=data['salesrep_id'])
        except SalesPerson.DoesNotExist:
            return JsonResponse({"message": "Sales Person not found. Please try again. "}, status=404)

        new_task = SalesPersonTask(text=data['text'], salesperson=salesperson)

        if 'date' in data:
            new_task.date = data['date']
        else:
            new_task.date = datetime.today().strftime('%Y-%m-%d')

        new_task.save()
        
        return JsonResponse({"message": "Task created!", "task": model_to_dict(new_task)}, status=200)

def mark_task_complete(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    data = json.loads(request.body.decode('utf-8'))

    taskId = data['task']
    salesrep_id = data['salesrep_id']

    try:
        salesperson = SalesPerson.objects.get(id=salesrep_id)
        task = SalesPersonTask.objects.get(id=taskId, salesperson=salesperson)
    except (SalesPersonTask.DoesNotExist,SalesPerson.DoesNotExist):
        return JsonResponse({"message": "An error occurred. Please try again." }, status=404)

    task.completed = True
    task.date_completed = datetime.now()
    task.save()

    logging.info('Task #%s marked as complete by: %s' % (task.id, request.user.username))

    return JsonResponse({"message": "Task completed!" }, status=200)

def delete_salesrep_task(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    data = json.loads(request.body.decode('utf-8'))

    taskId = data['task']
    salesrep_id = data['salesrep_id']

    try:
        salesperson = SalesPerson.objects.get(id=salesrep_id)
    except SalesPerson.DoesNotExist:
        return JsonResponse({"message": "The Sales Rep does not exist. Please try again." }, status=404)

    try:
        task = SalesPersonTask.objects.get(id=taskId, salesperson=salesperson)
        task.delete()
    except SalesPersonTask.DoesNotExist:
        return JsonResponse({"message": "The task does not exist. Please try again." }, status=404)

    return JsonResponse({"message": "Task deleted!" }, status=200)

def get_gl_codes(request):
    if request.method == 'GET':
        glCodes = []

        currentCompany = CurrentCompany.objects.get(user=request.user.id)
        if currentCompany:
            reqPublications = request.GET.getlist('publications[]')
            codeList = [model_to_dict(code) for code in CompanyGLCode.objects.filter(company=currentCompany.company.id)]

            glCodes = {}

            for reqPubId in reqPublications:
                try:
                    publication = Publication.objects.get(pk=reqPubId)
                except Publication.DoesNotExist:
                    continue

                glCodes[publication.name] = codeList

        return JsonResponse({ "message": "", "gl_codes": glCodes}, status=200)
    else:
        return JsonResponse({ "message": "Invalid request" }, status=400)

def get_publication_adjustments(request):

    if request.method == 'GET':
        publications = request.GET.getlist('publications[]')
    
        adjustments = getAdjustmentsByPublicationArray(publications)

        return JsonResponse({ "message": "Success", "adjustments": adjustments})
    else:
        return JsonResponse({ "message": "Invalid request"}, status=400)

def new_invoice(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # TODO - figure out a way to split an order balance/amount based on invoice frequency selected at the time of order creation
    
    if request.method == 'POST':
        reqData = request.body.decode('utf8').replace("'", '"')
        reqData = json.loads(reqData)

        memo = reqData['memo'] if 'memo' in reqData else ''
        serviceCharges = reqData['serviceChargeList']
        invoiceCost = Decimal(reqData['invoiceCost'])
        account = Account.objects.get(id=reqData['accountId'])

        today = datetime.today()
        month_from_now = today + timedelta(days=30)

        period = AccountingPeriod.objects.filter(account=account, start_date__lte=today, end_date__gte=today)

        if len(period) == 0:
            return JsonResponse({ "message": "Error. No accounting period set up. Please try again."}, status=200)

        isInsertionInvoice = False
        if 'isInsertionInvoice' in reqData and reqData['insertionId'] != 0:
            isInsertionInvoice = True
            try:
                insertionInvoice = InsertionInvoice.objects.get(insertion=reqData['insertionId'])
            except InsertionInvoice.DoesNotExist:
                pass

            insertionInvoice.date_sent = datetime.now()
            insertionInvoice.save()

        else:
            try:
                order = AdvertisingOrder.objects.get(id=reqData['orderId'])
            except AdvertisingOrder.DoesNotExist:
                return JsonResponse({ "message": "Error. Invalid parameters."}, status=200)

            new_invoice = Invoice(account=account, amount=round(invoiceCost,2), bill_end=month_from_now, order=order, memo=memo, original_amount=invoiceCost)
            new_invoice.save()

            orderInvoice = OrderInvoice(order=order,invoice=new_invoice)
            orderInvoice.save()

            logging.info('Invoice #' + new_invoice.id + ' has now been linked to order #' + order.id)

            errorList = []
            for charge in serviceCharges:
                try:
                    service_charge = ServiceCharge.objects.get(pk=int(charge))

                    new_invoice.amount = new_invoice.amount + Decimal(service_charge.amount)
                    new_invoice.save()

                    invoiceCharge = InvoiceServiceCharge(service_charge=service_charge, invoice=new_invoice)
                    invoiceCharge.save()
                except ServiceCharge.DoesNotExist:
                    errorList.push('Service Charge #' + charge + ' could not be added.')

            if 'printInvoiceCharge' in reqData:
                invoicePrintCharge = InvoicePrintCharge(amount=Decimal(reqData['printInvoiceCharge']), invoice=new_invoice)
                invoicePrintCharge.save()

            # accountingPeriodInvoice = AccountingPeriodInvoice(accounting_period=period[0], invoice=new_invoice)
            # accountingPeriodInvoice.save()

        today = datetime.date(today)
        transactionNumber = generateRandomNumber(5)
        batchNumber = generateRandomNumber(7)

        if isInsertionInvoice:
            description = 'Insertion ' + insertionInvoice.insertion.id + '\'s invoice #' + insertionInvoice.id
            ledger_item = AccountLedger(date=today, type='inv', transaction_number=transactionNumber, description=description, batch_number=batchNumber, amount=insertionInvoice.price, 
                                    balance=0.00, due_date=month_from_now, period=period[0], account=account)
            ledger_item.save()

            logging.info('Invoice #' + insertionInvoice.id + ' has been created and assigned to account #' + account.id)

            return JsonResponse({ "message": "Success", "insertionInvoice": model_to_dict(insertionInvoice) }, status=200)

        else:
            description = 'Order ' + order.id + '\'s invoice #' + new_invoice.id
            ledger_item = AccountLedger(date=today, type='inv', transaction_number=transactionNumber, description=description, batch_number=batchNumber, amount=new_invoice.amount, 
                                    balance=0.00, due_date=month_from_now, period=period[0], account=account)
            ledger_item.save()

            logging.info('Invoice #' + new_invoice.id + ' has been created and assigned to account #' + account.id)

            return JsonResponse({ "message": "Success", "new_invoice": model_to_dict(new_invoice) }, status=200)

def get_accounting_periods(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            account = Account.objects.get(pk=reqData['accountId'])
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find an account with that id" }, status=500)

        try: 
            fiscalYear = FiscalYear.objects.get(account=account, description=reqData['fiscalYear'])
        except FiscalYear.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find fiscal year with that description." }, status=500)

        periodList = []
        accountingPeriods = getAccountingPeriodsFromFiscalYear(fiscalYear)
        for i in accountingPeriods:
            periodList.append(model_to_dict(i))

        return JsonResponse({ "message": "Success!", "accountingPeriods": periodList }, status=200)
    else:
        return JsonResponse({ "message": "Error. Invalid request." }, status=400)

def set_accounting_period_action(request, accounting_period_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if accounting_period_id is None or accounting_period_id == '':
        return JsonResponse({ "message": "Error. Missing accounting period id. Please try again."}, status=400)

    reqData = json.loads(request.body.decode('utf-8'))

    status = True if reqData['status'] == 'true' else False

    try: 
        accounting_period = AccountingPeriod.objects.get(id=accounting_period_id)
    except AccountingPeriod.DoesNotExist:
        return JsonResponse({ "message": "Cannot find an accounting period with that id. Please try again."}, status=400)

    accounting_period.status = not status
    accounting_period.save()

    if status:
        logging.info(request.user.username + ' closed accounting period {accounting_period.code}')
    else: 
        logging.info(request.user.username + ' opened accounting period {accounting_period.code}')

    return JsonResponse({ "message": "Success!" }, status=200)

def get_invoice_payment(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        if not reqData['invoiceId']:
            return JsonResponse({ "message": "No invoice id provided. Please try again."}, status=400)

        try:
            invoice = Invoice.objects.get(pk=reqData['invoiceId'])
        except Invoice.DoesNotExist:
            return JsonResponse({ "message": "Failure. Cannot find an invoice with that id. Please try again." }, status=400)

        return JsonResponse({ "message": "Success", "invoice": model_to_dict(invoice) }, status=200)

    elif request.method == 'GET':
        reqType = request.GET.get('reqType')
        account_id = request.GET.get('account')

        reqType = reqType.replace('\'', '')

        if reqType == 'account_balance':
            try:
                account = Account.objects.get(pk=account_id)
            except Account.DoesNotExist:
                return JsonResponse({ "message":"Error. Cannot find account." }, status=400)

            open_invoices = Invoice.objects.filter(account=account, is_paid=False, amount__gt=0)
            
            latest_invoice = open_invoices.order_by('-date_sent').first()
            oldest_invoice = open_invoices.order_by('date_sent').first()

            return JsonResponse({ "message": "Success", "latestAmount": latest_invoice.amount, "oldestAmount": oldest_invoice.amount }, status=200)

        else:
            return JsonResponse({ "message": "Error. Invalid request." }, status=400)

def get_invoice_details(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'GET':
        invoiceId = request.GET.get('invoiceId')

    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        invoiceId = reqData['invoiceId']

    try:
        invoice = Invoice.objects.get(id=invoiceId)
    except Invoice.DoesNotExist:
        return JsonResponse({ "message": "Cannot find invoice with that number. Please try again." }, status=200)

    invoiceServiceCharges = InvoiceServiceCharge.objects.filter(invoice=invoice)
    account = invoice.account

    invoiceChargeList = []
    if len(invoiceServiceCharges):
        for row in invoiceServiceCharges:
            try:
                service_charge = ServiceCharge.objects.get(id=row.service_charge.id)
                invoiceChargeList.append({
                    "name": service_charge.name,
                    "amount": service_charge.amount,
                })
            except ServiceCharge.DoesNotExist:
                continue
    if account.invoice_type == 'print' or account.invoice_type == 'both':
        invoiceChargeList.append({
            "name": "Mailed Invoice Service Charge",
            "amount": account.mail_invoice_charge
        })

    return JsonResponse({ "message": "Success. Invoice found.", "invoice": model_to_dict(invoice), "service_charges": invoiceChargeList }, status=200)

def get_service_charges(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'GET' and request.GET.get('account') != '':
        try:
            accountId = request.GET.get('account')
            account = Account.objects.get(pk=accountId)
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find account." }, status=400)

        serviceChargeList = [model_to_dict(charge) for charge in ServiceCharge.objects.filter(enabled=True, account__isnull=True)]
        accountServiceCharges = ServiceCharge.objects.filter(account=account)
        if accountServiceCharges:
            for serviceCharge in accountServiceCharges:
                serviceChargeList.append(model_to_dict(serviceCharge))

        if (account.invoice_type == 'print' or account.invoice_type == 'both') and account.mail_invoice_charge > 0:
            serviceChargeList.append({
                "name": "Mail Invoice Service Charge",
                "amount": Decimal(account.mail_invoice_charge),
                "apply_level": 'order'
            })
    

    return JsonResponse({ "message": "Success", "service_charges": serviceChargeList }, status=200)

def get_service_charge_details(request, charge_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    try:
        serviceCharge = ServiceCharge.objects.get(pk=charge_id)
    except ServiceCharge.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find service charge" }, status=400)

    return JsonResponse({ "message": "Success! Service charge found", "serviceCharge": model_to_dict(serviceCharge) }, status=200)

def get_accounting_period_invoices(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'GET':

        periodId = request.GET.get('periodId')
        accountId = request.GET.get('accountId')

        try:
            period = AccountingPeriod.objects.get(pk=periodId)

        except AccountingPeriod.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find accounting period." }, status=400)

        invoices = Invoice.objects.filter(account=accountId)
        
        invoiceList = []
        for invoice in invoices:
            print(invoice.created_at.date(), period.start_date, period.end_date)
            if invoice.created_at.date() >= period.start_date and invoice.created_at.date() <= period.end_date:
                invoice = serializers.serialize('json', [invoice])
                invoice = json.loads(invoice)[0]['fields']
                invoiceList.append(invoice)

        return JsonResponse({ "message": "Success", "invoices": invoiceList }, status=200)

def override_credit_limit(request):
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            account = Account.objects.get(pk=reqData['accountId'])
            order = AdvertisingOrder.objects.get(pk=reqData['orderId'])
            manager = User.objects.get(pk=reqData['managerId'])
        except (Account.DoesNotExist, AdvertisingOrder.DoesNotExist, User.DoesNotExist):
            return JsonResponse({ "message": "Error. Invalid parameters. Please try again." }, status=200)

        try:
            override = CreditLimitManagerOverride.objects.get(account=account,order=order)
        except CreditLimitManagerOverride.DoesNotExist:
            return JsonResponse({ "message": "Cannot find override request. Please try again." }, status=200)

        override.overridden = True
        override.date_overridden = datetime.now()
        override.save()

        order.active = True
        order.is_draft = False
        order.save()

        account.balance += Decimal(order.total_price)
        account.save()

        return HttpResponseRedirect('/advertising/order/' + order.id + '/')