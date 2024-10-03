from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

from ..models.advertising import Account, IndustryCode
from .... import views

login_redirect = "/login/?next="

def list_industry_codes(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    industry_codes = IndustryCode.objects.filter(account=account_id, active=True).order_by('code')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account_id": account_id,
        "industry_codes": industry_codes
    }

    return render(request, "accounts/industry_codes/list_industry_codes.html", context)

def create_industry_code(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    # TODO - create primary and secondary codes for accounts
    if request.POST:
        exisitingIndustryCode = IndustryCode.objects.filter(code=request.POST.get('code')).exists()
        existingMarketDescription = IndustryCode.objects.filter(description=request.POST.get('description')).exists()

        if exisitingIndustryCode:
            context["message"] = "A industry code with that code already exists. Please try again."
            return render(request, "accounts/industry_codes/create_industry_code.html", context)
        elif existingMarketDescription:
            context["message"] = "A industry code with that description already exists. Please try again."
            return render(request, "accounts/industry_codes/create_industry_code.html", context)

        account = Account.objects.get(id=account_id)
        
        new_code = IndustryCode(code=request.POST.get('code'), description=request.POST.get('description'), account=account)
        new_code.save()

        return HttpResponseRedirect('/advertising/account/' + str(account_id) + '/industry-codes/')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
    }
    return render(request, "accounts/industry_codes/create_industry_code.html", context)

def edit_industry_code(request, account_id, code_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
    }

    industry_code = get_object_or_404(IndustryCode, pk=code_id)

    context["industry_code"] = industry_code

    if request.POST: 
        # if the industry code was marked as inactive
        if industry_code.active == True and request.POST.get('active') == None:
            industry_code.active = False
            industry_code.code = request.POST.get('code')
            industry_code.description = request.POST.get('description')
            industry_code.save()

            return HttpResponseRedirect('/advertising/account/' + str(account_id) + '/industry-codes/')

        # if the industry code was marked as active  
        elif industry_code.active == False and request.POST.get('active') == "on":
            industry_code.active = True
            industry_code.code = request.POST.get('code')
            industry_code.description = request.POST.get('description')
            industry_code.save()

            return HttpResponseRedirect('/advertising/account/' + str(account_id) + '/industry-codes/')
        # if the industry code was edited
        else: 
            existingIndustryCode = IndustryCode.objects.filter(code=request.POST.get('code')).exists()
            existingMarketDescription = IndustryCode.objects.filter(description=request.POST.get('description')).exists()

            # if the code is the same as the existing code
            # if existingIndustryCode:
            #     context["message"] = "A industry code with that code already exists. Please try again."
            #     return render(request, "accounts/industry_codes/edit_industry_code.html", context)
            # # if the description is the same as the existing description
            # elif existingMarketDescription:
            #     context["message"] = "A industry code with that description already exists. Please try again."
            #     return render(request, "accounts/industry_codes/edit_industry_code.html", context)
            # if the code and description are different
            # else:

            industry_code.code = request.POST.get('code')
            industry_code.description = request.POST.get('description')
            industry_code.active = False if request.POST.get('active') == None else True
            industry_code.save()

            return HttpResponseRedirect('/advertising/account/' + str(account_id) + '/industry-codes')
    return render(request, "accounts/industry_codes/edit_industry_code.html", context)