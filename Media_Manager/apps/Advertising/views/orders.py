from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages

import json
from datetime import timedelta, datetime, date
from decimal import Decimal

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.finance import *
from ..models.permissions import *
from ..models.publications import *

from ..helpers import daysOfTheWeek

from .... import views
from ..forms import *

login_redirect = "/login/?next="

def create_order(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
        
    # TODO - be able to select the number of insertions for a new order
    # TODO - handle what will happen if the override ad cost is set at creation and then removed after
    # TODO - when choosing a rate, if the rate end date is before the order end date, display a message saying that the rate will expire before the order is completed
    # TODO - set invoice frequency to account default as the default choice but still having the ability to change it and then process it on the back end 
    # TODO - if invoice frequency is set to every day, "sum up the invoices and then send them at the end of the accounting period"
    # TODO - some accounts may require a PO before the ad order will run 
    # TODO - have a "pending" status for new orders (in case they have to prepay beforehand) ("prepay required")

    context = {
        "access": "allow",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "ad_types": AdType.objects.all(),
        "ad_rates": AdvertisingRate.objects.all(),
        "user": request.user,
        "sales_people": SalesPerson.objects.filter(active=True),
        "publications": Publication.objects.all(),
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)],
        "canDefineCustomSize": CustomSizePermission.objects.filter(user=request.user.id).exists()
    }

    if id:
        account = Account.objects.get(id=id)
        context['selected_account'] = account
        try:
            context['account_salesperson'] = SalesPerson.objects.get(account=account)
        except SalesPerson.DoesNotExist:
            context['account_salesperson'] = None

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        topLevelDetails = reqData['topLevelDetails']
        publicationOrderData = reqData['publicationOrderData']

        try: 
            accountId = topLevelDetails['Account'].split(' ')[0]
            account = Account.objects.get(id=accountId)
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find account." }, status=200)
        
        try: 
            salespersonId = topLevelDetails['Salesperson'].split('-')[0]
            salesperson = SalesPerson.objects.get(id=salespersonId)
        except SalesPerson.DoesNotExist:
            salesperson = None

        tearsheets = True if topLevelDetails['Tearsheets'] == 'Yes' else False

        new_order = AdvertisingOrder(name=topLevelDetails['Name'], account=account, submitter=topLevelDetails['Ad Taker/Submitter'], salesperson=salesperson, notes=topLevelDetails['Notes'],
                                        tearsheets=tearsheets, invoice_frequency=topLevelDetails['Invoice Frequency'], total_price=topLevelDetails['Total Price'], 
                                        bill_date=datetime.today().strftime('%Y-%m-%d'))
        new_order.save()

        print('New order #' + str(new_order.id) + ' created')
        logging.info('New order #' + str(new_order.id) + ' created')

        dateArray = []
        
        for pub in publicationOrderData:
            publication = Publication.objects.get(name=pub)

            print(publicationOrderData[pub])

            orderPublication = OrderPublication(order=new_order, publication=publication)
            orderPublication.save()

            publicationRunDays = PublicationRunDay.objects.get(publication=publication)
            runDaysDict = model_to_dict(publicationRunDays)

            dateString = publicationOrderData[pub]['dates']['value']
            dates = dateString.split(',')

            # saving the individual dates to the database and creating insertions for the days the publication runs 
            totalInsertions = 0
            for date in dates:
                dateArray.append(date)
                date = datetime.strptime(date, '%Y-%m-%d').date()

                weekday = daysOfTheWeek[date.weekday()]

                if runDaysDict[weekday[0]]:
                    insertion = Insertion(publication=publication, date=date, weekday=weekday[0], status="Good", ad_order=new_order)
                    insertion.save()

                    totalInsertions += 1

                orderDate = OrderPublicationDate(order=new_order, publication=publication, date=date)
                orderDate.save()
            
            print('Total insertions created for publication: ' + publication.name + ': ' + str(totalInsertions))
            logging.info('Total insertions created for publication:' + publication.name + ': ' + str(totalInsertions))

            # getting the details of the adjustments from the database based on id given and linking them to the new order
            if len(publicationOrderData[pub]['adjustments']):
                for adjustId in publicationOrderData[pub]['adjustments']:
                    adjustment = Adjustment.objects.get(pk=adjustId)
                    
                    orderAdjustment = OrderAdjustment(order=new_order, adjustment=adjustment)
                    orderAdjustment.save()

            # getting the details of the rate from the database based on the id given and linking it to the new order 
            adRateData = publicationOrderData[pub]['adRate']
            adRate = AdvertisingRate.objects.get(pk=adRateData['value'])

            orderRate = OrderRate(order=new_order, rate=adRate, publication=publication, number_units=adRateData['units']['value'])
            orderRate.save()

            new_order.number_units = adRateData['units']['value']
            new_order.save()

            adTypeData = publicationOrderData[pub]['adType']
            adType = AdType.objects.get(code=adTypeData['value'])

            orderAdType = OrderPublicationAdType(order=new_order, adType=adType, publication=publication)
            orderAdType.save()

            orderSizeData = publicationOrderData[pub]['size']
            orderSize = OrderPublicationSize(order=new_order, publication=publication, size=orderSizeData['value'])
            orderSize.save()

            orderSectionData = publicationOrderData[pub]['section']
            if orderSectionData['value'] != '' and orderSectionData['name'] != '':
                publicationSection = PublicationSection.objects.get(pk=orderSectionData['value'])
                orderSection = OrderPublicationSection(order=new_order, publication=publication, section=publicationSection)
                orderSection.save()

            # TODO - save color (and color type) to the database and link it to the order 

        new_order.start_date = min(dateArray)
        new_order.end_date = max(dateArray)

        if topLevelDetails['Bill Date'] == 'Bill at Placement':
            bill_date = datetime.today().date()
        elif topLevelDetails['Bill Date'] == 'Bill at Start Date':
            bill_date = new_order.start_date
        elif topLevelDetails['Bill Date'] == 'Bill at End Date':
            bill_date = new_order.end_date
        elif topLevelDetails['Bill Date'] == 'Bill On Demand':
            bill_date = 'Billed on Demand'
        elif topLevelDetails['Bill Date'] == 'Bill at End of Accounting Period':
            # get the current accounting period for account selected and set to the last day of the accounting period
            pass

        new_order.bill_date = bill_date

        new_order.save()

        return JsonResponse({ "message": "Success! Order created!", "orderId": new_order.id }, status=200)
    
    #     if len(request.GET):
    #         result = {}
    #         adType = AdType.objects.get(pk=request.GET.get('ad_type'))
    #         publications = request.GET.getlist('publications[]')
    #         for pub in publications:
    #             deadline = AdDeadline.objects.filter(ad_type=int(adType.id), publication=int(pub))
    #             if deadline:
    #                 result['publication_' + pub] = deadline[0].days_prior
    #         return JsonResponse(result)

    return render(request, "orders/create_order.html", context)

def list_orders(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # TODO - refactor this to be faster (currently takes a long time to load)

    for order in AdvertisingOrder.objects.filter(active=True):
        if datetime.strptime(order.end_date, '%Y-%m-%d').date() < date.today():
            order.active = False
            order.status = 'inactive'

            if order.override_ad_cost == '':
                order.override_ad_cost = 0

            order.save()


    orders = AdvertisingOrder.objects.filter(is_draft=False, date_created__lt=(datetime.today() + timedelta(days=-30))).order_by('-id')
    today = datetime.today().strftime('%Y-%m-%d')

    active_orders = []
    inactive_orders = []

    for order in orders:
        account = Account.objects.get(id=order.account.id)
        order.account_name = account.name
        order.ad_type = AdType.objects.get(id=order.ad_type.id)

        if order.start_date >= today:
            order.status = "Upcoming"
            active_orders.append(order)
        elif today >= order.start_date and today <= order.end_date:
            order.status = "Active"
            active_orders.append(order)
        else:
            order.status = "Inactive"
            inactive_orders.append(order)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "orders": orders,
        "active_orders": active_orders,
        "inactive_orders": inactive_orders,
    }
    return render(request, "orders/list_orders.html", context)

def view_order(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    order = get_object_or_404(AdvertisingOrder, pk=id)

    order.start_date = datetime.strptime(order.start_date, '%Y-%m-%d').date()

    # if the end date has already passed, mark the order as inactive
    order.end_date = datetime.strptime(order.end_date, '%Y-%m-%d').date()
    if order.end_date < date.today():
        order.active = False
        order.save()

    order.bill_date = datetime.strptime(order.bill_date, '%Y-%m-%d').date()

    orderPublicationData = {}
    orderPubAdType = OrderPublicationAdType.objects.filter(order=order)

    for orderPub in OrderPublication.objects.filter(order=order):
        orderPublicationData[orderPub.publication.name] = {}

    for orderAdType in OrderPublicationAdType.objects.filter(order=order):
        orderPublicationData[orderAdType.publication.name]['ad_type'] = orderAdType.adType.name

    sizes = {
        "quarter": "Quarter Page",
        "half": "Half Page",
        "full": "Full Page",
        "custom": "Custom",
    }
    for orderPubSize in OrderPublicationSize.objects.filter(order=order):
        orderPublicationData[orderAdType.publication.name]['size'] = sizes[orderPubSize.size]

    orderDates = []
    for orderDate in OrderPublicationDate.objects.filter(order=order):
        orderPublicationData[orderDate.publication.name]
        orderDates.append(orderDate.date)

    # minDate = min(orderDates)
    # maxDate = max(orderDates)

    publicationRateList = []
    orderRates = OrderRate.objects.filter(order=order)
    for row in orderRates:
        pubRate = {}
        pubRate['publication'] = row.publication
        pubRate['rate'] = row.rate
        publicationRateList.append(pubRate)
    
    salesperson = order.salesperson

    if order.status == 'running':
        order.status = 'active'

    colorTypes = {
        "": "None",
        "full_color": "Full Color",
        "black_and_white": "Black and White",
        "solid_color": "Solid Color"
    }

    orderColorList = []
    orderColors = OrderPublicationColor.objects.filter(order=order)
    for row in orderColors:
        orderColor = {}
        orderColor['publication'] = row.publication
        orderColor['inColor'] = row.color

        if row.color_type in colorTypes:
            orderColor['colorType'] = colorTypes[row.color_type]
        else:
            orderColor['colorType'] = row.color_type

        orderColorList.append(orderColor)
    
    order.total_price = '${:,.2f}'.format(order.total_price)

    insertions = Insertion.objects.filter(ad_order=order)

    detail = 'Viewed the ad order'
    submitter = request.user.first_name + ' ' + request.user.last_name
    history = OrderHistory(detail=detail, order_number=id, account=order.account, submitter=submitter)
    history.save()

    history = OrderHistory.objects.filter(order_number=id).order_by('-timestamp')[:15] 

    logging.info(request.user.username + ' visited order #' + str(order.id))

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "order": order,
        "salesperson": salesperson,
        "history": history,
        "insertions": insertions,
        "isCustomSize": order.size == "custom",
        "publicationRateList": publicationRateList,
        "orderColorList": orderColorList,
        "isAdminOrManager": isAdminOrManager(request.user.id, order.account.id),
        "today": date.today(),
        "orderPublicationData": orderPublicationData
    }

    return render(request, "orders/view_advertising_order.html", context)

def edit_order(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # TODO - If setting an override ad cost, change the overall price of the order 
    # ask if we should keep the previous price of the order in case it needs to be changed back

    # TODO - if only one publication is selected during initial creation and then is edited to add more publications, handle this situation
    # TODO - color and color type are not being selected onload

    order = AdvertisingOrder.objects.get(id=id)
    order.account = Account.objects.get(id=order.account.id)

    charges = [{"id": charge.id, "name": charge.name} for charge in ServiceCharge.objects.all()]
    orderPublications = [pub.publication.id for pub in OrderPublication.objects.filter(order=order)]

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        topLevelDetails = reqData['topLevelDetails']
        publicationOrderData = reqData['publicationOrderData']

        try:
            order = AdvertisingOrder.objects.get(pk=id)
        except AdvertisingOrder.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find the order in our system. Please try again." }, status=404)
        
        order.name = topLevelDetails['Name']
        
        try: 
            order.account = Account.objects.get(name=topLevelDetails['Account'])
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find the account in our system. Please try again." }, status=404)
        
        order.submitter = topLevelDetails['Ad Taker/Submitter']

        try: 
            salespersonId = topLevelDetails['Salesperson'].split('-')[0]
            salesperson = SalesPerson.objects.get(id=salespersonId)
            order.salesperson = salesperson
        except SalesPerson.DoesNotExist:
            order.salesperson = None

        if topLevelDetails['Bill Date'] == 'Bill at Placement':
            order.bill_date = datetime.today().date()
        elif topLevelDetails['Bill Date'] == 'Bill at Start Date':
            order.bill_date = order.start_date
        elif topLevelDetails['Bill Date'] == 'Bill at End Date':
            order.bill_date = order.end_date
        elif topLevelDetails['Bill Date'] == 'Bill On Demand':
            order.bill_date = 'Billed on Demand'

        order.invoice_frequency = topLevelDetails['Invoice Frequency']
        order.notes = topLevelDetails['Notes']
        order.total_price = topLevelDetails['Total Price']
        order.tearsheets = True if topLevelDetails['Tearsheets'] == 'Yes' else False

        order.save()

        # get the list of publications associated with the order 
        orderPublications = OrderPublication.objects.filter(order=order)
        
        for reqPub in publicationOrderData:
            try:
                publication = Publication.objects.get(name=reqPub)
            except Publication.DoesNotExist:
                return JsonResponse({ "error": "Error. Cannot find " + reqPub + " in our system." }, status=404)
            
            # loop through the order publications from the database
            for orderPub in orderPublications:

                # check and make sure an OrderPublication exists in the database for the publication name from the req data
                # if it exists but is not in the reqPublications list, delete the record 
                if (reqPub != orderPub.publication.name):
                    orderPub.delete()

                # if it does not exist, create a record
                if reqPub != orderPub.publication.name:
                    newOrderPub = OrderPublication(order=order, publication=publication)
                    newOrderPub.save()

            reqDates = publicationOrderData[reqPub]['dates']['value']
            reqDates = [datetime.strptime(dateString, '%Y-%m-%d').date() for dateString in reqDates]

            # get the run days for the publication and convert to a dictionary
            publicationRunDays = PublicationRunDay.objects.get(publication=publication)
            runDaysDict = model_to_dict(publicationRunDays)

            # get the insertions for the order from the database (filtered by publication and order)
            orderInsertions = Insertion.objects.filter(ad_order=order, publication=publication)
            orderInsertionDates = [insertion.date for insertion in orderInsertions]

            # loop through the insertions in the database and make sure there is a record for each one from the request
            for insertion in orderInsertions:

                # if there are any from the order but does not match the list from the request, delete it
                if insertion.date not in reqDates:
                    insertion.delete()
                
            # if there are any in the request that are not in the database, create them
            for reqDate in reqDates:
                weekday = daysOfTheWeek[reqDate.weekday()]
                if runDaysDict[weekday[0]] and reqDate not in orderInsertionDates:
                    Insertion.objects.create(ad_order=order, publication=publication, date=reqDate, weekday=daysOfTheWeek[reqDate.weekday()][0])

            # get the order's adjustments from the database 
            # orderAdjustments = OrderAdjustment.objects.filter(order=order)
            
            # for adjustment in orderAdjustments:
            #     if adjustment not in publicationOrderData[reqPub]['adjustments']:
            #         adjustment.delete()

            # for adjustment in publicationOrderData[reqPub]['adjustments']:
            #     if adjustment not in orderAdjustments:
            #         OrderAdjustment.objects.create(order=order, adjustment=Adjustment.objects.get())

            # get the order's rates from the database
            orderRate = OrderRate.objects.filter(order=order, publication=publication)
            reqRateName = publicationOrderData[reqPub]['adRate']['name'].split(' - ')[0]

            if orderRate.exists():
                orderRate = orderRate.first()
                if orderRate.rate.name != reqRateName:
                    orderRate.delete()

            else:
                newOrderRate = OrderRate(order=order, publication=publication, rate=AdvertisingRate.objects.get(name=reqRateName))
                newOrderRate.number_units = publicationOrderData[reqPub]['adRate']['units']['value']
                newOrderRate.save()
                
            # get the order's ad types from the database 
            orderAdType = OrderPublicationAdType.objects.filter(order=order, publication=publication)
            reqAdType = publicationOrderData[reqPub]['adType']['value']

            if orderAdType.exists():
                orderAdType = orderAdType.first()
                if orderAdType.adType.code != reqAdType:
                    orderAdType.delete()

            else:
                newOrderAdType = OrderPublicationAdType(order=order, publication=publication, adType=AdType.objects.get(code=reqAdType))
                newOrderAdType.save()

            # get the order's sizes from the database 
            orderSize = OrderPublicationSize.objects.filter(order=order, publication=publication)
            reqSize = publicationOrderData[reqPub]['size']['value']

            if orderSize.exists():
                orderSize = orderSize.first()
                if orderSize.size != reqSize:
                    orderSize.delete()

            else:
                newOrderSize = OrderPublicationSize(order=order, publication=publication, size=reqSize)
                newOrderSize.save()

            # get the order's publication's sections from the database 
            orderPubSection = OrderPublicationSection.objects.filter(order=order, publication=publication)
            if 'section' in publicationOrderData[reqPub]:
                reqSection = publicationOrderData[reqPub]['section']['value']

                if orderPubSection.exists():
                    orderPubSection = orderPubSection.first()
                    if orderPubSection.section.name != reqSection:
                        orderPubSection.delete()

                else:
                    newOrderPubSection = OrderPublicationSize(order=order, publication=publication, size=reqSection)
                    newOrderPubSection.save()
            else:
                if orderPubSection.exists():
                    orderPubSection.first().delete()


        # TODO - refactor this to use the updated OrderPublicationColor model to store colors for an order 
        # if request.user.has_perm('can_make_ad_color'):
        #     order.color = False if 'color' not in reqData.keys() else True
        #     if order.color is not False:
        #         order.color_type = reqData['color_type']
            
        detail = 'Edited the ad order'
        submitter = request.user.first_name + ' ' + request.user.last_name
        history = OrderHistory(detail=detail, order_number=order.id, account=order.account, submitter=submitter)
        history.save()

        return JsonResponse({ "message": "Success" }, status=200)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "order": order,
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)],
        "id": id,
        "charges": charges,
        "ad_types": AdType.objects.all(),
        "publications": Publication.objects.all(),
        "sales_people": SalesPerson.objects.all(),
        "orderPublications": orderPublications,
    }

    return render(request, "orders/edit_order.html", context)

def list_account_orders(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    orders = AdvertisingOrder.objects.filter(account_id=id, is_draft=False).order_by('-id')

    today = datetime.today().strftime('%Y-%m-%d')

    active_orders = []
    inactive_orders = []

    for order in orders:
        account = Account.objects.get(id=order.account.id)
        order.account = account
        order.ad_type = AdType.objects.get(id=order.ad_type.id)

        if order.start_date >= today and order.active and order.active is True:
            order.status = "Upcoming"
            active_orders.append(order)
        elif today >= order.start_date and today <= order.end_date and order.active is True:
            order.status = "Active"
            active_orders.append(order)
        else:
            order.status = "Inactive"
            inactive_orders.append(order)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "orders": orders,
        "active_orders": active_orders,
        "inactive_orders": inactive_orders,
    }
    return render(request, "orders/list_orders.html", context)

def list_publication_orders(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    publication = get_object_or_404(Publication, pk=id)
    orderPublications = OrderPublication.objects.filter(publication=publication)
    
    orderList = []

    for orderPub in orderPublications:
        order = orderPub.order

        # get all orders that started less than 30 days ago 
        if datetime.strptime(order.start_date, "%Y-%m-%d") < (datetime.now() - timedelta(days=-30)):
            
            try:
                orderRate = OrderRate.objects.get(order=order.id, publication=publication)
                rateName = orderRate.rate.name
            except OrderRate.DoesNotExist as dne:
                rateName = None

            order.rate = rateName
            orderList.append(order)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "publication": publication,
        "orderList": orderList
    }
    return render(request, "orders/PublicationOrderList.html", context)

def view_insertion(request, id=None):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    insertion = get_object_or_404(Insertion, pk=id)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "insertion": insertion
    }

    return render(request, "orders/view_insertion.html", context)

def edit_insertion(request, orderId, insertionId):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    try:
        order = AdvertisingOrder.objects.get(pk=orderId)
        insertion = Insertion.objects.get(pk=insertionId, ad_order=order)
    except (AdvertisingOrder.DoesNotExist, Insertion.DoesNotExist):
        return HttpResponseRedirect('/advertising/order/' + str(orderId))

    format = '%Y-%m-%d'    

    insertion.date = datetime.strftime(insertion.date, format)

    if request.POST:

        try:
            insertion.publication = Publication.objects.get(id=request.POST.get('publication'))

        except Publication.DoesNotExist:
            return HttpResponseRedirect('/advertising/order/' + str(order.id) + '/insertion/' + str(insertion.id) + '/edit')

        insertion.date = datetime.strptime(request.POST.get('date'), format)
        insertion.status = request.POST.get('status')
        insertion.save()

        return HttpResponseRedirect('/advertising/order/' + str(insertion.ad_order.id))
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "insertion": insertion,
        "publications": Publication.objects.all()
    }

    return render(request, "orders/edit_insertion.html", context)

def cancel_order(request, orderId):

    # TODO - make the cancellation process into its own function and the message it returns should be displayed on the screen
    # TODO - add a conmfirmation box to confirm they want to cancel the order 
    # TODO - Handle refunds 

    try:
        order = AdvertisingOrder.objects.get(pk=orderId)
    except AdvertisingOrder.DoesNotExist:
        return HttpResponseRedirect('/advertising')

    # TODO - add a try/except block to check if the start/end dates have values 
    # skip the date check if the order doesnt have start/end date values

    order.start_date = datetime.strptime(order.start_date, '%Y-%m-%d')
    order.end_date = datetime.strptime(order.end_date, '%Y-%m-%d')

    if order.end_date.date() < date.today():
        print('cannot cancel an order that has already ended')
        return HttpResponseRedirect('/advertising/order/' + str(order.id))

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist as ude:
        print(ude)
        return HttpResponseRedirect('/advertising')

    try:
        orderCancellation = OrderCancellation(order=order, date_cancelled=datetime.now(), cancelled_by=user)
        orderCancellation.save()
    except ValueError as ve:
        print(ve)
        return HttpResponseRedirect('/advertising/order/' + str(order.id))

    account = order.account

    # if the order has been cancelled but ads have already started running
    if order.start_date.date() < date.today():
        print('the order has already started')

        # get the amount of insertions not run yet
        insertionsNotRun = Insertion.objects.filter(ad_order=order, date__lte=date.today())
        numberInsertionsNotRun = insertionsNotRun.count()
        
        # if its billed on demand, theres gonna be multiple invoices
        if order.bill_date == 'bill_on_demand':
            print('the order\'s bill date is set to on demand')

            # gets the number of insertions not yet run and divide the total price of that order by that number of insertions
            totalInsertions = Insertion.objects.filter(ad_order=order).count()

            # calculate the price per insertion and times that by the amount of insertions not run yet
            refundAmount = (order.total_price / totalInsertions) * numberInsertionsNotRun
            refundAmount = round(refundAmount, 2)

            # refund the amount for the insertions not ran yet
            account.credit = round(account.credit + refundAmount, 2)
            account.save()

            # loop through each invoice and essentially write them off
            for insertion in insertionsNotRun:
                orderInvoices = OrderInvoice.objects.filter(order=insertion.ad_order)

                for inv in orderInvoices:

                    inv.is_paid = True
                    inv.amount = 0
                    if inv.invoice.memo == '':
                        inv.invoice.memo = 'Order #' + str(order.id) + ' cancelled. Invoice written off at {datetime.now()}'
                    else:
                        inv.invoice.memo = '\nOrder #' + str(order.id) + ' cancelled. Invoice written off at {datetime.now()}'
                    
                    inv.invoice.save()
                    inv.save()

                    print('Invoice #' + inv.invoice.id + ' has been written off due to order #' + str(order.id) + ' being cancelled')
                    logging.info('Invoice #' + inv.invoice.id + ' has been written off due to order #' + str(order.id) + ' being cancelled')

                # ? should we add a record of the invoice write off in the InvoiceWriteOff table?
            
        else:
            # if its not billed on demand, theres gonna only be one single invoice
            try:
                invoice = Invoice.objects.get(order=order)
            except Invoice.DoesNotExist:
                print('invoice not found')

            print('the bill date is a set date')

            order.bill_date = datetime.strptime(order.bill_date, '%Y-%m-%d')

            # if the bill date has not passed (they placed the order, but haven't paid for it yet)
            if order.bill_date.date() > date.today():
                print('the bill date has not passed yet. marking the order as inactive')

                # mark the order as inactive 
                order.active = False
                order.save()

            # if the bill date has not passed (they placed the order, and have paid for it)
            else:
                print('the bill date has passed. will process a refund')

                # if they paid in full, refund the entire amount
                if invoice.amount == 0:
                    print('user has paid all of invoice. refunding the entire amount')

                    account.credit = account.credit + invoice.original_amount
                    account.save()
                else:
                    # if the have been making payments and still have an amount left to pay
                    print('amount still left on invoice to pay. refunding that amount to the account')
                    creditAmount = 0
                    creditAmount = creditAmount + invoice.amount

                    transactionList = Transaction.objects.filter(invoice=invoice)
                    if len(transactionList):
                        for transaction in transactionList:
                            creditAmount = creditAmount + transaction.amount

                    account.credit = Decimal(account.credit) + creditAmount
                    account.save()        

            invoice.is_paid = True
            invoice.amount = 0
            if invoice.memo == '':
                invoice.memo = 'Order #' + str(order.id) + ' cancelled. Invoice written off at ' + datetime.now()
            else:
                invoice.memo = '\nOrder #' + str(order.id) + ' cancelled. Invoice written off at ' + datetime.now()
            
            logging.info('Invoice #' + str(invoice.id) + ' has been written off due to order #' + str(order.id) + ' being cancelled')
        
    # if the order is cancelled before the ads have started running
    else:
        print('the order has not already started')

        # refund the total amount of the order and add the refund amount back to the original account
        account.credit = round(account.credit + order.total_price, 2)
        account.save()

        print('amount refunded: $', str(order.total_price))

    # loop through the insertions and mark each as 'killed'
    insertionList = Insertion.objects.filter(ad_order=order)
    if len(insertionList):
        for insertion in insertionList:
            insertion.status = 'Killed'
            insertion.save()
    else:
        print('no insertions found for order #' + str(order.id))

    order.active = False
    order.status = 'cancelled'
    order.save()

    detail = request.user.username + ' cancelled the ad order'
    submitter = request.user.first_name + ' ' + request.user.last_name
    history = OrderHistory(detail=detail, order_number=order.id, account=order.account, submitter=submitter)
    history.save()

    print('order #' + str(order.id) + ' has been cancelled')
    logging.info('Order #' + str(order.id) + ' has been cancelled by User #' + request.user.id)

    return HttpResponseRedirect('/advertising/order/' + str(order.id))


def clone_order(request, orderId):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    try:
        order = AdvertisingOrder.objects.get(pk=orderId)
    except AdvertisingOrder.DoesNotExist:
        message = 'Error. Cannot find order with id #' + orderId + '. Redirecting to homepage.'

        logging.info(message)
        print(message)

        return HttpResponseRedirect('/advertisting')

    print(model_to_dict(order))

    """
        Steps to clone an order
        --------------------------

        1) clicks a button and sends the orderId here so the system can get all of the info
        2) populates a template order form (except for the start and end dates)
        3) once the template form populates, the same steps would then be followed when creating a new order (subtotal modal, drafts, etc.)

        # TODO - create an order form template that can be populated with given values 
            - can already be used in the draft system and now the cloning system 

    """

    return JsonResponse({ "message": "Order successfully cloned" }, status=200)

def create_order_form(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    """
        - This will serve as a template form so any valid values can be passed to it and only those values will be shown in the form.
        - Will serve same function as create_order page but have templating function.
        - When the form submits, it will be passed directly to the create_order route to be processed 
    """

def create_order_dev(request):

    context = {
        "access": "allow",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "adTypes": AdType.objects.all(),
        "adRates": AdvertisingRate.objects.all(),
        "user": request.user,
        "sales_people": SalesPerson.objects.filter(active=True),
        "publications": Publication.objects.all(),
        "accounts": [row.account for row in AccountAccess.objects.filter(user=request.user.id)],
    }

    return render(request, "orders/create_order_dev.html", context)

def search_order_details(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if request.method != 'GET':
        return JsonResponse({ "message": "Error. Invalid request method." }, status=200)

    orderId = request.GET.get('orderId')

    try:
        order = AdvertisingOrder.objects.get(pk=orderId)
    except AdvertisingOrder.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find order with that id." }, status=200)

    orderPublications = OrderPublication.objects.filter(order=order)
    pubList = [model_to_dict(orderPub) for orderPub in orderPublications]

    return JsonResponse({ "message": "Success", "order_publications": pubList }, status=200)

def search_order_publication(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    publicationId = request.GET.get('id')
    orderId = request.GET.get('orderId')

    try:
        publication = Publication.objects.get(pk=publicationId)
    except Publication.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find publication" }, status=200)

    rateList = []
    for row in RatePublication.objects.filter(publication=publication):
        currRate = {}
        if row.rate.active:
            currRate['id'] = row.rate.id
            currRate['name'] = row.rate.name
            currRate['price'] = row.rate.unit_price
            currRate['unit_type'] = row.rate.unit_type

            rateList.append(currRate)

    adjustmentList = [model_to_dict(adjustment) for adjustment in Adjustment.objects.filter(publication=publication)] 

    sectionList = [{ "name": section.name, "value": section.id } for section in PublicationSection.objects.filter(publication=publication, active=True)]

    selectedData = {}

    if orderId:
        try:
            order = AdvertisingOrder.objects.get(pk=orderId)
        except AdvertisingOrder.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find that order in our system. Please try again." }, status=200)

        try:
            orderAdType = OrderPublicationAdType.objects.get(order=order, publication=publication)
            selectedData['ad_type'] = model_to_dict(orderAdType.adType)
        except OrderPublicationAdType.DoesNotExist:
            selectedData['ad_type'] = {}

        try:
            orderRate = OrderRate.objects.get(order=order, publication=publication)
            selectedData['ad_rate'] = model_to_dict(orderRate.rate)
            selectedData['number_units'] = order.number_units
        except OrderRate.DoesNotExist:
            selectedData['ad_rate'] = {}

        try:
            orderPubSize = OrderPublicationSize.objects.get(order=order, publication=publication)
            if orderPubSize.size != 'custom':
                selectedData['size'] = orderPubSize.size
            else:
                selectedData['size'] = orderPubSize.size

                selectedData['size']['custom_min_width'] = orderPubSize.custom_min_width
                selectedData['size']['custom_min_height'] = orderPubSize.custom_min_height

                selectedData['size']['custom_max_width'] = orderPubSize.custom_max_width
                selectedData['size']['custom_max_height'] = orderPubSize.custom_max_height
        except OrderPublicationSize.DoesNotExist:
            selectedData['size'] = {}

        try:
            runDates = OrderPublicationDate.objects.filter(publication=publication, order=order)
            
            dateArray = [date.date for date in runDates]
            for date in dateArray:
                date = date.strftime('%Y-%m-%d') + ','

            selectedData['dates'] = dateArray
        except OrderPublicationDate.DoesNotExist:
            selectedData['dates'] = []

    return JsonResponse({ 
        "message": "Success", 
        "rates": rateList, 
        "adjustments": adjustmentList, 
        "color": publication.spot_color, 
        "sectionList": sectionList,
        "selectedData": selectedData
    }, status=200)

def order_subtotal(request):
    if request is None or not request.user.is_authenticated:
        return JsonResponse({ "message": "Error. Access forbidden." }, status=403)

    if not request.user.has_perm('BI.advertising_access'):
        return JsonResponse({ "message": "Error. Access forbidden" }, status=403)

    reqData = json.loads(request.body.decode('utf-8'))

def custom_size_permission(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')
    
    permissionList = [permission.user.id for permission in CustomSizePermission.objects.all()]
    
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            user = User.objects.get(pk=reqData['userId'])
        except User.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find that user in our system. Please try again." }, status=404)
        
        permission = CustomSizePermission.objects.filter(user=user)
        hasPermission = permission.exists()

        # if the user is granted the permission
        if reqData['hasPermission']:
            if not hasPermission and reqData['hasPermission']:
                permission = CustomSizePermission(user=user)
                permission.save()

                message = 'User #' + str(user.id) + ' now has the permission: Custom Size'
                print(message)
                logging.info(message)

                return JsonResponse({ "message": "Sucess" }, status=201)

        # if the permission is being revoked/removed
        else:
            if hasPermission:
                permission.delete()

                message = 'User #' + str(user.id) + ' no longer has the permission: Custom Size'
                print(message)
                logging.info(message)
            else: 
                return JsonResponse({ "message": "Error. Cannot find permission in our system. Please try again" }, status=404)

        return JsonResponse({ "message": "Success" }, status=200)
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "userList": User.objects.all(),
        "permissionList": permissionList
    }

    return render(request, 'orders/CustomSizePermission.html', context)