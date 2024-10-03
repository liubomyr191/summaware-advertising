from datetime import datetime, timedelta
from getpass import getuser
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Permission, User

# from Media_Manager.apps.Advertising.models.advertising import SalesPerson

from ... import views

from .models.advertising import *
from .models.orders import *
from .models.permissions import *
from .models.finance import *

def view_admin_panel(request):
    # ? Should groups have roles too?

    if not isAdminOrManager(request.user.username):
        return HttpResponseRedirect('/advertising')

    today = datetime.today()
    month_ago = today - timedelta(days=30)

    today = str(today)[:10]
    month_ago = str(month_ago)[:10]

    orderIds = [order.id for order in AdvertisingOrder.objects.filter(bill_date__gte=month_ago)]
    orderInvoiceIds = [orderInvoice.order.id for orderInvoice in OrderInvoice.objects.all()]

    ordersToBeInvoiced = [AdvertisingOrder.objects.get(pk=id) for id in orderIds if id not in orderInvoiceIds]

    sentInvoices = Invoice.objects.exclude(date_sent__isnull=True).order_by('-date_sent')

    # sentInvoicesDict = {}
    # for invoice in sentInvoices:
    #     accountName = invoice.account.name
    #     if accountName not in sentInvoicesDict:
    #         sentInvoicesDict[accountName] = []
    #     sentInvoicesDict[accountName].append(invoice)
    # sentInvoices = enumrate(sentInvoicesDict)

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "users": User.objects.all(),
        "roles": Role.objects.all().order_by('description'),
        "salesreps": SalesPerson.objects.all(),
        "ordersToBeInvoiced": ordersToBeInvoiced,
        "sentInvoices": sentInvoices
    }

    return render(request, 'auth/AdminPanel.html', context)

def get_user_roles(request, userId):

    try:
        user = User.objects.get(id=userId)

    except User.DoesNotExist:
        return JsonResponse({ "message": "User does not exist" }, status=404)

    roleDetails = getUserRoles(user.username)

    return JsonResponse({ "errors": [], "roles": roleDetails }, status=200)

def save_user_roles(request, userId):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        role = Role.objects.get(name=request.POST.get('role'))
        hasRole = request.POST.get('hasRole')

        try:
            userRole = UserRole.objects.get(user=user, role=role)
            if hasRole != 'true':
                userRole.delete()
                return JsonResponse({ "message": f'{role.description} role successfully removed!'})
                
        except UserRole.DoesNotExist:
            newUserRole = UserRole(user=user, role=role)
            newUserRole.save()
            return JsonResponse({ "message": f'{role.description} role added', "role": model_to_dict(newUserRole)}, status=200)
