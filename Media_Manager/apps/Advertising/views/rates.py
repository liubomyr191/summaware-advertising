from operator import mod
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse

from datetime import timedelta, datetime
import json

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..models import *
from ..forms import *


login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def getRunDays(dict):
    days = []
    for day in daysOfTheWeek:
        if dict.get(day):
            days.append(day[0:3].title())
    return days

def create_rate(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':

        rateExists = AdvertisingRate.objects.filter(name=request.POST.get('name')).exists()
        if rateExists:
            return JsonResponse({ "message": "Error. A rate with that name already exists. Please try again." }, status=400)

        new_rate = AdvertisingRate(name=request.POST.get('name'), description=request.POST.get('description'), unit_type=request.POST.get('unit_type'), unit_price=request.POST.get('unit_price'), 
                                    tax_category=request.POST.get('tax_category'), ad_type=AdType.objects.get(id=request.POST.get('ad_type')), start_date=request.POST.get('start_date'), 
                                    end_date=request.POST.get('end_date'),  location=request.POST.get('location'), pricing=request.POST.get('pricing'), price=request.POST.get('rate_price'))
        
        try:
            gl_code = GLCode.objects.get(pk=request.POST.get('default_gl_code'))
        except GLCode.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find that GL Code in our system. Please try again" }, status=404)
        
        new_rate.default_gl_code = gl_code

        new_rate.save()

        # hasCurrentCompany = CurrentCompany.objects.filter(user=request.user.id)
        # if len(hasCurrentCompany):
        #     currentCompany = hasCurrentCompany.first()

        #     companyRate = CompanyRate(company=currentCompany.company.id, rate=new_rate)
        #     companyRate.save()
        # else:
        #     # TODO - how should it be handled if there is no current company?
        #     pass

        publicationList = []
        reqPublications = request.POST.getlist('publication')
        for publication in reqPublications:
            try:
                pub = Publication.objects.get(id=publication)
            except Publication.DoesNotExist:
                continue
            publicationList.append(pub)
        
        # pubGLCodes = {}
        # for index in request.POST:
        #     if index.startswith('pub-') and index not in pubGLCodes:
        #             publicationId = index.split("-")[1]
        #             pubGLCodes[publicationId] = request.POST.get('pub-' + str(publicationId) + '-gl-code')
        #     else:
        #         continue

        # for publication in publicationList:
        #     if pubGLCodes:
        #         try:
        #             gl_code = GLCode.objects.get(pk=pubGLCodes[str(publication.id)])

        #             publication_glcode = RateGLCode(rate=new_rate, gl_code=gl_code)
        #             publication_glcode.save()
        #         except GLCode.DoesNotExist:
        #             continue

            rate_publication = RatePublication(publication=publication, rate=new_rate)
            rate_publication.save()

        isLocked = False if request.POST.get('account') == '' else True
        if isLocked:
            new_rate.locked = True
            new_rate.account = Account.objects.get(id=request.POST.get('account'))
            new_rate.save()

        else:
            new_rate.locked = False
            new_rate.save()
        
        return JsonResponse({ "message": "Rate created!", "rateId": new_rate.id }, status=200)
                
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "gl_codes": GLCode.objects.all(),
        "publications": Publication.objects.all(),
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)],
        "ad_types": AdType.objects.all(),
    }
    return render(request, "rates/create_rate.html", context)

def list_rates(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    rates = AdvertisingRate.objects.all().order_by('-id')
    activeRates = []
    inactiveRates = []
    hiddenRates = []
    for rate in rates:
        if rate.end_date:
            rate.end_date = datetime.strptime(rate.end_date, '%Y-%m-%d')
            rate.notice_date = rate.end_date - timedelta(days=3)
            rate.notice_date = rate.notice_date.date()
            rate.end_date = rate.end_date.strftime('%Y-%m-%d')

        if rate.active == True:
            activeRates.append(rate)
        else:
            inactiveRates.append(rate)
        
        if rate.hidden == True:
            hiddenRates.append(rate)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "activeRates": activeRates,
        "inactiveRates": inactiveRates,
        "hiddenRates": hiddenRates,
        "now": datetime.now().date()
    }
    return render(request, "rates/list_rates.html", context)

def view_rate(request, rate_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    rate = get_object_or_404(AdvertisingRate, pk=rate_id)

    ratePublications = RatePublication.objects.filter(rate=rate)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "rate": rate,
        "ratePublications": ratePublications
    }
    return render(request, "rates/view_rate.html", context)

def edit_rate(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    rate = AdvertisingRate.objects.get(id=int(id))
    # rate.gl_code = GLCode.objects.get(id=rate.gl_code.id)

    hasCurrentCompany = CurrentCompany.objects.filter(user=request.user.id)
    if hasCurrentCompany.exists():
        currentCompany = hasCurrentCompany.first()
    else:
        currentCompany = None

    ratePublications = [ratePub.publication.id for ratePub in RatePublication.objects.filter(rate=rate)]
    # rateGLCodes = [rateCode.gl_code.id for rateCode in RateGLCode.objects.filter(rate=rate)]

    # gl_codes = CompanyGLCode.objects.filter(company=currentCompany.company.id)    

    locations = [("static", "Static"),("prem_insideCover", "Inside Cover (Premium)"),("prem_backCover", "Back Cover (Premium)"),("prem_center", "Center (Premium)")]

    if request.method == "POST":
        data = request.POST.dict()

        rate.name = data['name']
        rate.description = data['description']
        rate.unit_type = data['unit_type']
        rate.unit_price = data['unit_price']
        # rate.gl_code = GLCode.objects.get(id=data['gl_code'])
        rate.tax_category = data['tax_category']
        rate.ad_type = AdType.objects.get(id=data['ad_type'])
        rate.start_date = data['start_date']
        rate.end_date = data['end_date']
        rate.location = data['location']
        rate.pricing = data['pricing']

        try:
            gl_code = GLCode.objects.get(pk=data['default_gl_code'])
            rate.default_gl_code = gl_code
        except GLCode.DoesNotExist:
            gl_code = None
        
        if 'hidden' in data:
            rate.hidden = True
        else:
            rate.hidden = False

        if request.POST.get('locked'):
            if request.POST.get('account') == '':
                rate.locked = False
                rate.account = None
            else:
                rate.locked = True
                try:
                    rate.account = Account.objects.get(id=request.POST.get('account'))
                except Account.DoesNotExist:
                    rate.locked = False
                    rate.account = None
        else:
            rate.locked = False
            rate.account = None

        rate.save()

        logging.info(request.user.username + ' made edits to rate #' + str(rate.id))

        data['publications'] = request.POST.getlist('publication')
        ratePublications = RatePublication.objects.filter(rate=rate)

        for ratePub in ratePublications:
            if ratePub.publication.id not in data['publications']:
                publication = Publication.objects.get(id=ratePub.publication.id)
                RatePublication.objects.filter(rate=rate, publication=publication).delete()

        for pub in data['publications']:
            if pub not in ratePublications:
                RatePublication.objects.create(rate=rate, publication=Publication.objects.get(id=pub))

        return HttpResponseRedirect('/advertising/rate/' + str(rate.id))

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "rate": rate,
        "publications": Publication.objects.all(),
        "ad_types": AdType.objects.all(),
        "gl_codes": GLCode.objects.all(),
        "locations": locations,
        "ratePublications": ratePublications,
        "accounts": Account.objects.filter(archived=False)
    }
    return render(request, "rates/edit_rate.html", context)

def list_account_rates(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    account_rates = AdvertisingRate.objects.filter(account=Account.objects.get(id=account_id))
    unlocked_rates = AdvertisingRate.objects.filter(locked=False)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account_rates": account_rates,
        "unlocked_rates": unlocked_rates,
    }
    return render(request, "rates/list_account_rates.html", context)

def list_rate_locations(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    locations = RateLocation.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "locations": locations
    }

    return render(request, "orders/list_rate_locations.html", context)

def add_rate_location(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    form = RateLocationForm()

    if request.method == "POST":
        publication = Publication.objects.get(id=request.POST.get('publication'))
        location = RateLocation(publication=publication, location=request.POST.get('location'), price=request.POST.get('price'))
        location.save()
        return HttpResponseRedirect('/advertising/rates/locations')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "form": form
    }

    return render(request, "orders/new_rate_location.html", context)

def list_special_rates(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    special_rates = SpecialRate.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "special_rates": special_rates
    }

    return render(request, "orders/list_special_rates.html", context)

def list_company_rates(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if not isAdminOrManager(request.user.id):
        return redirect('/advertising')
    
    rates = AdvertisingRate.objects.filter(active=True, locked=False)
    companies = Company.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "rates": rates,
        "companies": companies
    }

    return render(request, "rates/list_company_rates.html", context)

def get_rate_publications(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        ratePubs = getRatePublications(publication_id)

        return JsonResponse({ "message": "Success", "rate_publications": ratePubs }, status=200)
    
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)
    
def get_rate_details(request, rate_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        try:
            rateDetails = AdvertisingRate.objects.get(pk=rate_id)
            rateDict = model_to_dict(rateDetails)
            if 'default_gl_code' in rateDict and rateDict['default_gl_code'] is not None:
                glCode = GLCode.objects.get(pk=rateDetails.default_gl_code.id)
                rateDict['default_gl_code'] = model_to_dict(glCode)
            return JsonResponse({ "message": "Success", "rate_details": rateDict }, status=200)
        except AdvertisingRate.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find advertising rate." }, status=404)
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)
    
def get_rate_publication_gl_codes(request, rateId):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'GET':
        glCodeList = []
        gl_codes = GLCode.objects.all()
        for row in gl_codes:
            glCodeList.append(model_to_dict(row))

        ratePubList = []
        ratePublications = RatePublication.objects.filter(rate=rateId)
        for ratePub in ratePublications:
            ratePubList.append(model_to_dict(ratePub.publication))

        selectedCodes = []
        selectedCodes = [model_to_dict(rateGLCode) for rateGLCode in RateGLCode.objects.filter(rate=rateId)]

        return JsonResponse({ "message": "Success", "gl_codes": glCodeList, "rate_publications": ratePubList, "selected_codes": selectedCodes }, status=200)
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            gl_code = GLCode.objects.get(pk=reqData['glCodeId'])
            publication = Publication.objects.get(pk=reqData['publicationId'])
            rate = AdvertisingRate.objects.get(pk=rateId)
        except (Publication.DoesNotExist, AdvertisingRate.DoesNotExist):
            return JsonResponse({ "message": "Error. Cannot find the gl code in our system" }, status=404)
        
        try:
            rateGLCode = RateGLCode.objects.get(rate=rate, publication=publication)
            rateGLCode.gl_code = gl_code
            rateGLCode.save()

            return JsonResponse({ "message": "Success" }, status=200)
        except RateGLCode.DoesNotExist:
            rateGLCode = RateGLCode(gl_code=gl_code, rate=rate, publication=publication)
            rateGLCode.save()
        
        return JsonResponse({ "message": "Success" }, status=200)
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)
    
def view_rate_gl_codes(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if request.method == 'GET':

        companyList = Company.objects.all()
        rateList = AdvertisingRate.objects.all()

        context = {
            "access": "allow",
            "message": "",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "companyList": companyList,
            "rateList": rateList,
        }

        return render(request, "rates/rate_gl_codes.html", context)
    
# TODO - Ability to save a draft of the rate for a certain amount of days --> admins should be able to change the amount of days
# TODO - Add a quotes page -> similar to the new ad rate page, but with no save/create button,
# TODO - GL Code select should be typeable (maybe use a "datalist" element)