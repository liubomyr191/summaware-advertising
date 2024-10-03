from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..forms import *

from .orders import create_order

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def getRunDays(dict):
    days = []
    for day in daysOfTheWeek:
        if dict.get(day):
            days.append(day[0:3].title())
    return days


def list_drafts(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - be able to show drafts from the last 30 days, 60 days, 90 days, etc.
    # TODO - managers should be able to see their sales reps' drafts

    if request.user.is_superuser:
        drafts = AdvertisingOrder.objects.filter(is_draft=True).order_by('-date_created')
    else:
        try:
            salesperson = SalesPerson.objects.get(email=request.user.email)
            drafts = AdvertisingOrder.objects.filter(salesperson=salesperson, is_draft=True).order_by('-date_created')
        except SalesPerson.DoesNotExist:
            salesperson = None
            drafts = []

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "drafts": drafts
    }

    return render(request, "drafts/list_drafts.html", context)

def list_account_drafts(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    drafts = AdvertisingOrder.objects.filter(account=id, is_draft=True).order_by('-date_created')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account_id": id,
        "drafts": drafts
    }

    return render(request, "drafts/list_account_drafts.html", context)

def load_draft(request, account_id, draft_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "accounts": Account.objects.filter(archived=False),
        "publications": Publication.objects.all(),
        "industry_codes": IndustryCode.objects.all(),
        "sales_people": SalesPerson.objects.filter(active=True),
        "ad_types": AdType.objects.all(),
        "adjustments": Adjustment.objects.all()
    }

    if not draft_id:
        return HttpResponseRedirect('/advertising/account/' + account_id + '/drafts/')

    draft = get_object_or_404(AdvertisingOrder, pk=draft_id)
    draftPublications = OrderPublication.objects.filter(order=draft)
    draftAdjustments = OrderAdjustment.objects.filter(order=draft)

    if request.method == 'POST':
        create_order(request, account_id)
    
    context["account_id"] = account_id
    context["draft"] = draft
    context["draftDict"] = model_to_dict(draft)
    context["draftPublications"] = [pub.publication.id for pub in draftPublications]
    context["draftAdjustments"] = [adjustment.adjustment.id for adjustment in draftAdjustments]

    context['draftId'] = draft_id
    context['draftBillDate'] = draft.bill_date
    context['draftStartDate'] = draft.start_date
    context['draftEndDate'] = draft.end_date
    # context['draftAdRateId'] = draft.ad_rate.id 
    
    return render(request, "drafts/load_draft.html", context)

def delete_draft(request, id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if not id:
        return HttpResponseRedirect('/advertising/drafts/')

    try:
        draft = AdvertisingOrder.objects.get(id=id)

        orderPublicationList = OrderPublication.objects.filter(order=draft)
        if len(orderPublicationList) > 0:
            for publication in orderPublicationList:
                publication.delete()

        orderAdjustmentList = OrderAdjustment.objects.filter(order=draft)
        if len(orderAdjustmentList) > 0:
            for adjustment in orderAdjustmentList:
                adjustment.delete()

        insertionList = Insertion.objects.filter(ad_order=draft)
        if len(insertionList) > 0:
            for insertion in insertionList:
                insertion.delete()

        draft.delete()

        return HttpResponseRedirect('/advertising/drafts/')

    except AdvertisingOrder.DoesNotExist:
        return HttpResponseRedirect(('/advertising/drafts/'))

def delete_account_draft(request, account_id, draft_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if not draft_id:
        return HttpResponseRedirect('/advertising/account/' + {account_id} + '/drafts/')

    draft = get_object_or_404(AdvertisingOrder, pk=draft_id)
    try:
        orderPublicationList = OrderPublication.objects.filter(order=draft)
        if len(orderPublicationList) > 0:
            for publication in orderPublicationList:
                publication.delete()

        orderAdjustmentList = OrderAdjustment.objects.filter(order=draft)
        if len(orderAdjustmentList) > 0:
            for adjustment in orderAdjustmentList:
                adjustment.delete()

        insertionList = Insertion.objects.filter(ad_order=draft)
        if len(insertionList) > 0:
            for insertion in insertionList:
                insertion.delete()

        draft.delete()
    except Exception as e:
        print(e)
        logging.error(e)

    uri = request.build_absolute_uri()
    if 'account' in uri:
        return HttpResponseRedirect('/advertising/account/' + {account_id} + '/drafts/')
    else:
        return HttpResponseRedirect('/advertising/drafts/')