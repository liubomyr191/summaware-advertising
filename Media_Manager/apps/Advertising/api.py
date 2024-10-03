from django.http import JsonResponse

from datetime import datetime

from .models.advertising import *
from .models.orders import *
from .models.rates import *
from .models.finance import *
from .models.publications import *

from .helpers import *

def calculateAdDimensions(height, width, size):
    if height is None or width is None or size is None:
        return ''

    if not isinstance(height, float):
        return None

    if not isinstance(width, float):
        return None

    if size == 'full':
        return (height, width)

    elif size == 'half': 
        return (height / 2, width)

    elif size == 'quarter':
        return (height / 2, width / 2) 

    else: 
        return None

def get_current_ads_running(request):
    dateFormat = '%Y-%m-%d'

    colorTypes = {
        "": "None",
        "full_color": "Full Color",
        "black_and_white": "Black and White",
        "solid_color": "Solid Color"
    }

    publication = request.headers.get('publication')
    inputDate = request.headers.get('date')

    if publication is None or inputDate is None:
        return JsonResponse({ "message": "Error. Invalid request." }, status=400)

    try:
        formattedDate = datetime.strptime(inputDate, dateFormat).date()
    except ValueError:
        return JsonResponse({ "message": "Error. Incorrect date format. It should be YYYY-MM-DD"})

    weekday = daysOfTheWeek[formattedDate.weekday()]
    
    try: 
        publication = Publication.objects.get(pk=publication)
    except Publication.DoesNotExist:
        return JsonResponse({ "message": "Cannot find publication." }, status=400)

    orderPublications = OrderPublication.objects.filter(publication=publication).order_by('order_id')
    publicationRunDays = PublicationRunDay.objects.get(publication=publication)
    runDaysDict = model_to_dict(publicationRunDays)

    pageDimensions = PublicationPageDimension.objects.get(publication=publication)

    currentAds = []
    for orderPub in orderPublications:
        order = orderPub.order
        publication = orderPub.publication

        try:
            orderPubSizes = OrderPublicationSize.objects.get(publication=publication, order=order)
        except OrderPublicationSize.DoesNotExist:
            continue

        if '00:00:00' not in order.start_date and '00:00:00' not in order.end_date:
            order.start_date = datetime.strptime(order.start_date, dateFormat).date()
            order.end_date = datetime.strptime(order.end_date, dateFormat).date()
        else:
            print('Start date and/or end date has extra values')
            continue

        if formattedDate >= order.start_date and formattedDate <= order.end_date and order.status == 'running':
            adDimensions = calculateAdDimensions(pageDimensions.page_height, pageDimensions.columns_per_page, orderPubSizes.size)
            if adDimensions is not None:
                height, width = adDimensions
            else:
                print('adDimensions is None')

            # ? How to handle missing page dimensions ?
            """
                - stop the api and return an error?
                - just skip over that ad and continue the loop?
                - create an errors array and append an error message to that array for that ad missing page dimensions
            """

            try:
                orderColors = OrderPublicationColor.objects.get(order=order, publication=publication)

                inColor = orderColors.color
            except OrderPublicationColor.DoesNotExist:
                inColor = False

            ad = {}
            if runDaysDict[weekday]:
                ad['date'] = inputDate

                ad['adName'] = order.name if order.name else ''
                ad['orderId'] = order.id
                ad['size'] = order.size 
                ad['adHeight'] = str(height) + ' inches'
                ad['adWidth'] = str(width) + ' cols'
                
                ad['color'] = inColor
                if inColor:
                    ad['colorType'] = orderColors.color_type

                ad['advertiser'] = order.account.name
                ad['version'] = order.version
                ad['notes'] = order.notes
                ad['cost'] = order.total_price
            else: 
                continue
            currentAds.append(ad)

    message = "No ads running" if len(currentAds) == 0 else "Success"
        
    return JsonResponse({ "message": message, "adsRunning": currentAds }, status=200)
