from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

import json
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *
from ..models.permissions import AccountAccess

from .... import views
from ..forms import *

from ..validate import validateZipCode, validateState, validateEmail

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def getRunDays(dict):
    days = []
    for day in daysOfTheWeek:
        if dict.get(day):
            days.append(day[0:3].title())
    return days

def pubDashboard(request):
    # Check if user is logged in, if not, redirect  to login screen
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + '/')
    return render(request, 'publications/publication-dashboard.html')

def create_publication(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "ad_types": AdType.objects.all()
        }

    if request.method == 'POST': 
        reqDict = request.POST.dict()

        reqData = {}
        runDays = []
        formData = json.loads(reqDict['formData'])
        for key in formData:
            pair = formData[key]
            if pair['name'] == 'runDays':
                runDays.append(pair['value'])

            reqData[pair['name']] = pair['value']


        if validateZipCode(reqData['zip_code']):
            zip_code = reqData['zip_code']
        else:
            print("Error. Invalid zip code. Please try again.")
            return JsonResponse({ "message": "Error. Invalid zip code. Please try again."}, status=500)

        if validateState(reqData['state']):
            state = reqData['state']
        else:
            print("Error. Invalid zip code. Please try again.")
            return JsonResponse({ "message": "Error. Invalid zip code. Please try again."}, status=500)
        
        publication = Publication(name=reqData['name'], address=reqData['address'], city=reqData['city'], state=state, zip_code=zip_code, 
                                    spot_color=reqData['spot_color'], credit_memo=reqData['credit_memo'])
        
        if 'charge_tax' in reqData:
            publication.charge_tax = True 
        
        publication.save()

        message = 'New publication #' + str(publication.id) + ': ' + publication.name + ' created by: ' + request.user.username
        logging.info(message)
        print(message)

        weekdays = { 'sunday': False, 'monday': False, 'tuesday': False, 'wednesday': False, 'thursday': False, 'friday': False, 'saturday': False }
        
        for day in weekdays:
            weekdays[day] = True if day in runDays else False
        weekdays['publication_id'] = publication.id

        run_days = PublicationRunDay(sunday=weekdays['sunday'], monday=weekdays['monday'],  tuesday=weekdays['tuesday'],wednesday=weekdays['wednesday'], thursday=weekdays['thursday'],
                                        friday=weekdays['friday'],saturday=weekdays['saturday'], publication_id=weekdays['publication_id'])
        run_days.save()

        message = 'New publication run days created for publication #' + str(publication.id)
        logging.info(message)
        print(message)

        page_dimensions = PublicationPageDimension(publication=publication, page_size=reqData['page_size'], columns_per_page=reqData['columns_per_page'], column_width=reqData['column_width'],
                                                    page_width=reqData['page_width'], page_height=reqData['page_height'], page_border=reqData['page_border'], gutter_size=reqData['gutter_size'], 
                                                    column_inches=reqData['column_inches'], inches=reqData['inches'], default_size=reqData['default_size'])

        page_dimensions.save()

        message = 'New publication page dimensions created for publication #' + str(publication.id)
        logging.info(message)
        print(message)

        if 'deadlines[]' in reqDict:
            deadlineDict = json.loads(reqDict['deadlines[]'])

            for deadline in deadlineDict:
                try:
                    adType = AdType.objects.get(id=int(deadline['ad_type']['value']))
                    adDeadline = AdDeadline(publication=publication, publication_day=deadline['publication_day'], time=deadline['time'], 
                                            days_prior=deadline['days_prior'], priority_level=deadline['deadline_priority'], ad_type=adType)
                    adDeadline.save()
                except AdType.DoesNotExist:
                    print('Cannot find ad type with id: ', deadline['ad_type']['value'])

        return JsonResponse({ "message": "Success", "pubId": publication.id }, status=200)

    return render(request, "publications/new_publication.html", context)

def view_publication(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if id is None:
        return HttpResponseRedirect('/advertising')

    publication = get_object_or_404(Publication, pk=id)
    
    try:
        runDays = PublicationRunDay.objects.get(publication_id=id)
        runDays = getRunDays(model_to_dict(runDays))
        runDays = ', '.join(runDays)
    except PublicationRunDay.DoesNotExist:
        runDays = None

    deadlineList = [deadline for deadline in AdDeadline.objects.all() if int(deadline.publication.id) == int(publication.id)]
    for deadline in deadlineList:
        deadline.time = datetime.datetime.strptime(deadline.time, '%H:%M:%S').time()
        deadline.ad_type = AdType.objects.get(id=deadline.ad_type.id)
        deadline.publication = Publication.objects.get(id=deadline.publication.id)

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    count = 0 
    advertising_orders = []
    for row in OrderPublication.objects.filter(publication_id=id).order_by('-date_created').select_related():
        rowDict = model_to_dict(row)
        rowDict['order'] = AdvertisingOrder.objects.get(id=row.order.id)
        rowDict['publication'] = Publication.objects.get(id=row.publication.id)
        if count < 5 :
            advertising_orders.append(rowDict)
            count += 1

    try:
        pageDimensions = PublicationPageDimension.objects.get(publication_id=id)
    except PublicationPageDimension.DoesNotExist:
        pageDimensions = None

    adjustments = Adjustment.objects.filter(publication=id)

    querySet = PublicationDefaultStyle.objects.filter(publication=publication)

    hasDefaultStyles = querySet.exists()
    defaultStyles = querySet.first() if hasDefaultStyles else None

    sectionList = PublicationSection.objects.filter(publication=publication)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "ad_types": AdType.objects.all(),
        "publication": publication,
        "runDays": runDays, 
        "advertising_orders": advertising_orders,
        "todays_date": today,
        "deadlines": deadlineList,
        "pageDimensions": pageDimensions,
        "adjustments": adjustments,
        "defaultStyles": defaultStyles,
        "sectionList": sectionList
    }
    return render(request, "publications/view_publication.html", context)

def edit_publication(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    weekdays = {
        'sunday': False,
        'monday': False,
        'tuesday': False,
        'wednesday': False,
        'thursday': False,
        'friday': False,
        'saturday': False,
    }

    publication = Publication.objects.get(id=id)
    try:
        pubRunDays = PublicationRunDay.objects.get(publication=publication)
    except PublicationRunDay.DoesNotExist:
        pubRunDays = None

    if request.method == 'POST':
        context = {
            "publication": publication,
            "access": "allow",
            "groups": ', '.join(views.get_groups(request)),
            "menu": views.get_sidebar(request),
            "publication": publication,
            "pubRunDays": pubRunDays,
            "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)]
        }
        if len(request.POST.get('zip_code')) > 5:
            context['message'] = "Zip code must be 5 digits or less."
            return render(request, "publications/edit_publication.html", context)
        
        if len(request.POST.get('state')) > 2:
            context["message"] = "State must be 2 characters or less."
            return render(request, "publications/edit_publication.html", context)

        publication.name = request.POST.get('name')
        publication.address = request.POST.get('address')
        publication.city = request.POST.get('city')
        publication.state = request.POST.get('state')
        publication.zip_code = request.POST.get('zip_code')
        publication.spot_color = request.POST.get('spot_color')
        publication.credit_memo = request.POST.get('credit_memo')
        publication.charge_tax = True if request.POST.get('charge_tax') else False
        publication.save()

        runDays = request.POST.getlist('runDays')

        for i in runDays:
            weekdays[i] = True
        
        pubRunDays.sunday = weekdays['sunday']
        pubRunDays.monday = weekdays['monday']
        pubRunDays.tuesday = weekdays['tuesday']
        pubRunDays.wednesday = weekdays['wednesday']
        pubRunDays.thursday = weekdays['thursday']
        pubRunDays.friday = weekdays['friday']
        pubRunDays.saturday = weekdays['saturday']

        pubRunDays.save()

        return HttpResponseRedirect('/advertising/publication/' + str(publication.id))
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "publication": publication,
        "pubRunDays": pubRunDays,
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)]
    }

    return render(request, "publications/edit_publication.html", context)

def new_page_dimensions(request,publication_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    publication = Publication.objects.get(id=publication_id)

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        pageSize = reqData['page_size']
        columnsPerPage = reqData['columns_per_page']
        columnWidth = reqData['column_width']
        pageWidth = reqData['page_width']
        pageHeight = reqData['page_height']
        pageBorder = reqData['page_border']
        gutterSize = reqData['gutter_size']
        columnInches = reqData['column_inches']
        inches = reqData['inches']
        default_size = reqData['default_size']
    
        newPageDimension = PublicationPageDimension(page_size=pageSize, columns_per_page=columnsPerPage, column_width=columnWidth, page_width=pageWidth, 
                                                    page_height=pageHeight, page_border=pageBorder, gutter_size=gutterSize, column_inches=columnInches, inches=inches, 
                                                    default_size=default_size, publication=publication)
        
        newPageDimension.save()

        return JsonResponse({ "message": "Success" }, status=200)
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)

def edit_page_dimensions(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    page_dimensions = PublicationPageDimension.objects.get(publication=publication_id)

    if request.method != 'POST':
        return JsonResponse({ "message": "Error. Access Forbidden." }, status=403)

    reqData = json.loads(request.body.decode('utf-8'))

    page_dimensions.page_size = reqData['page_size']
    page_dimensions.columns_per_page = reqData['columns_per_page']
    page_dimensions.column_width = reqData['column_width']
    page_dimensions.page_width = reqData['page_width']
    page_dimensions.page_height = reqData['page_height']
    page_dimensions.page_border = reqData['page_border']
    page_dimensions.gutter_size = reqData['gutter_size']
    page_dimensions.column_inches = float(reqData['column_inches'])
    page_dimensions.inches = float(reqData['inches'])
    page_dimensions.default_size = reqData['default_size']

    page_dimensions.save()

    return JsonResponse({ "message": "Success. Page dimensions saved." }, status=200)
    

def get_publication_page_dimensions(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)

    if publication_id is None:
        return JsonResponse({ "message": "Error. Cannot find publication." }, status=200)

    if request.method == 'GET':
        dimensions = PublicationPageDimension.objects.get(publication=publication_id)

        return JsonResponse({ "message": "Page dimensions found.", "dimensions": model_to_dict(dimensions) }, status=200)

    else:
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)
    
def get_publication_run_days(request, id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)
    
    try:
        runDays = PublicationRunDay.objects.get(publication=id)

        runDaysDict = model_to_dict(runDays)
        runDaysArray = [day for day in runDaysDict if day in daysOfTheWeek and runDaysDict[day]]

        return JsonResponse({ "message": "Success", "run_days": runDaysArray }, status=200)
    except PublicationRunDay.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find any run days for that publication" }, status=404)

def get_spot_colors(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)

    publications = request.GET.getlist('publications[]')

    colors = getPublicationSpotColors(publications)
    
    return JsonResponse({ "errors": [], "colors": colors }, status=200)

def get_publication_list(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    publicationList = [model_to_dict(pub) for pub in Publication.objects.all()]

    return JsonResponse({ "message": "Success", "publications": publicationList }, status=200)

def create_default_styles(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        # print(reqData)

        try:
            publication = Publication.objects.get(pk=publication_id)
        except Publication.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find publication" }, status=200)
        
        defaultStyles = PublicationDefaultStyle(publication=publication, font=reqData['font'], font_size=reqData['font_size'], 
                                                    inset=reqData['inset'], frame_width=reqData['frame_width'])
        defaultStyles.save()

        return JsonResponse({ "message": "Success! Default styles have been created!" }, status=200)
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)
    
def default_styles_details(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        publication = Publication.objects.get(pk=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find publication." }, status=200)
    
    querySet = PublicationDefaultStyle.objects.filter(publication=publication)

    hasDefaultStyles = querySet.exists()
    
    if request.method == 'GET':
        if not hasDefaultStyles:
            message = 'Error. Cannot find a default styling with for that publication. Please try again.'

            logging.info(message)
            print(message)
            return JsonResponse({ "message": message }, status=200)
        else:
            return JsonResponse({ "message": "Success", "details": model_to_dict(querySet.first()) }, status=200)
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))
        print(reqData)

        if not hasDefaultStyles:
            message = 'Error. Cannot find a default styling with for that publication. Please try again.'

            logging.info(message)
            print(message)
            return JsonResponse({ "message": message }, status=200)
        else:
            defaultStyles = querySet.first()
            defaultStyles.font = reqData['font']
            defaultStyles.font_size = reqData['font_size']
            defaultStyles.inset = reqData['inset']
            defaultStyles.frame_width = reqData['frame_width']

            defaultStyles.save()

            return JsonResponse({ "message": "Success! Default styles have been updated." }, status=200)
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)
    
def create_publication_section(request, publication_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        publication = Publication.objects.get(pk=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find publication. Please try again"}, status=404)
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        section = PublicationSection(name=reqData['name'], number_pages=reqData['number_pages'], publication=publication)
        
        try:
            section.save()
            return JsonResponse({ "message": "Success" }, status=201)
        except Exception as ex:
            print(ex)
            return JsonResponse({ "message": "Error Cannot create new publication section" }, status=500)
    
def publication_section_details(request, publication_id, section_id):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)
    
    try:
        section = PublicationSection.objects.get(pk=section_id)
    except PublicationSection.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find publication section" }, status=200)
    
    if request.method == 'GET':
        return JsonResponse({ "message": "Success", "section": model_to_dict(section)}, status=200)
    
    elif request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        section.name = reqData['name']
        section.number_pages = reqData['number_pages']

        section.active = reqData['active']

        section.save()

        return JsonResponse({ "message": "Success" }, status=200)
    
    else:
        return JsonResponse({ "message": "Error. Method not allowed." }, status=405)