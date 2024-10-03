from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *

from .... import views
from ..models import AccountType
from ..forms import *

login_redirect = "/login/?next="

# TODO - make this a modal
def create_account_type(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == "POST":

        form = AccountTypesForm(request.POST)
        if form.is_valid():

            new_account_type = AccountType(code=(form.cleaned_data['code']).upper(), name=(form.cleaned_data['name']).capitalize())
            new_account_type.save()

            return HttpResponseRedirect('/advertising')

    else:
        form = AccountTypesForm()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "form": form
    }
    return render(request, "accounts/advertising_new_account_type.html", context)