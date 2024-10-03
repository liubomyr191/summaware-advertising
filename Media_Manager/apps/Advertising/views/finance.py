from django.shortcuts import get_object_or_404, render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse

from decimal import Decimal

from datetime import datetime, date
import json

import logging
logger = logging.getLogger(__name__)

from ..models import *

from .... import views

from ..helpers import generateRandomNumber

login_redirect = "/login/?next="

def view_account_invoices(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    account = get_object_or_404(Account, pk=account_id)

    all_invoices = Invoice.objects.filter(account=account)
    open_invoices = [invoice for invoice in all_invoices if invoice.is_paid is False and invoice.date_sent is None]
    paid_invoices = [invoice for invoice in all_invoices if invoice.is_paid is True]

    paid_invoices.sort(key=lambda x: x.date_paid, reverse=True)

    logger.info('/' + request.method + ' - User #' + str(request.user.id) + ' visited account #' + str(account.id) + '\'s invoices')
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "open_invoices": open_invoices, 
        "paid_invoices": paid_invoices,
    }

    return render(request, "finance/invoicing/AccountInvoices.html", context)

def account_ledger(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    account = get_object_or_404(Account, pk=account_id)
    ledgerItems = AccountLedger.objects.filter(account=account).select_related()

    logger.info('/' + request.method + ' - User #' + str(request.user.id) + ' visited account #' + str(account.id) + '\'s ledger')
    
    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "ledgerItems": ledgerItems
    }

    return render(request, "finance/invoicing/AccountLedger.html", context)

def list_all_invoices(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    # TODO - managers and admins can go back and edit an invoice until the end of the period
    # TODO - be able to automatically run invoices daily 

    invoices = Invoice.objects.all().order_by('is_paid')

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            invoice = Invoice.objects.get(pk=reqData['id'])
        except Invoice.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find invoice"}, status=400)

        invoice.bill_end = reqData['bill_end']
        invoice.memo = reqData['memo']

        invoice.save()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "invoices": invoices,
        "isAdmin": isAdminOrManager(request.user.id)
    }

    return render(request, "finance/InvoiceList.html", context)

def view_aging_report(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if not isAdminOrManager(request.user.id):
        return HttpResponseRedirect('/advertising')

    today = date.today()

    overdueInvoices = [model_to_dict(invoice) for invoice in Invoice.objects.filter(is_paid=False, bill_end__lt=today)]
    for invoice in overdueInvoices:
        invoice['days_overdue'] = (today - invoice['bill_end']).days

    overdueInvoices = sorted(overdueInvoices, key=lambda invoice: invoice['days_overdue']) 

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "overdueInvoices": overdueInvoices,
        "isAdmin": isAdminOrManager(request.user.id)
    }

    return render(request, "finance/aging/GeneralAgingReport.html", context)

def view_account_aging_report(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if account_id is None:
        return HttpResponseRedirect('/advertising')

    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return HttpResponseRedirect('/advertising')

    # checking the user's roles to see if they have access to the aging report
    adminManager = isAdminOrManager(request.user.id, account_id)

    if not adminManager:
        return HttpResponseRedirect('/advertising/' + str(account_id))

    today = date.today()

    less_than_30 = 0
    between_31_60 = 0
    between_61_90 = 0
    more_than_90 = 0

    overdueInvoices = [model_to_dict(invoice) for invoice in Invoice.objects.filter(is_paid=False, bill_end__lt=today, account=account)]
    for invoice in overdueInvoices:
        daysOverdue = (today - invoice['bill_end']).days
        if daysOverdue <= 30:
            less_than_30 += invoice['amount']
        elif daysOverdue >= 31 and daysOverdue <= 60:
            between_31_60 += invoice['amount']
        elif daysOverdue >= 61 and daysOverdue <= 90:
            between_61_90 += invoice['amount']
        else:
            more_than_90 += invoice['amount']

        invoice['days_overdue'] = daysOverdue

    overdueInvoices = sorted(overdueInvoices, key=lambda invoice: invoice['days_overdue']) 

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "isAdminOrManager": adminManager,
        "overdueInvoices": overdueInvoices,
        
        "less_than_30": less_than_30, 
        "between_31_60": between_31_60,
        "between_61_90": between_61_90,
        "more_than_90": more_than_90
    }

    return render(request, "finance/aging/AccountInvoiceAging.html", context)

def view_account_fiscal_years(request, account_id):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if account_id is None or account_id == '':
        return HttpResponseRedirect('/advertising')

    account = get_object_or_404(Account,pk=account_id)
    fiscalYears = FiscalYear.objects.filter(account=account).order_by('-startDate').select_related()

    # TODO - when creating invoice periods, allow for upload, download via csv file
    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        try:
            account = Account.objects.get(pk=reqData['accountId'])
        except Account.DoesNotExist:
            return JsonResponse({ "message": "Error. Cannot find an account with that id. Please try again." }, status=500)
        
        if reqData['type'] == 'fiscal_year': 
            fiscalYear = FiscalYear(description=reqData['description'], startDate=reqData['startDate'], endDate=reqData['endDate'], account=account)
            fiscalYear.save()

            logging.info(request.user.username + ' created fiscal year #' + str(fiscalYear.id))

            return JsonResponse({ "message": 'Success!', "fiscalYear": model_to_dict(fiscalYear)}, status=200)
        elif reqData['type'] == 'accounting_period':

            try: 
                fiscalYear = FiscalYear.objects.get(description=reqData['fiscalYear'])
            except FiscalYear.DoesNotExist:
                return JsonResponse({ "message": "Error. Cannot find a fiscal year with that name."}, status=500)

            # TODO - add functionality to open and edit a closed accounting period (if within the current period)
            accountingPeriod = AccountingPeriod(code=reqData['code'], period=reqData['name'], start_date=reqData['startDate'], end_date=reqData['endDate'], account=account, fiscal_year=fiscalYear)
            accountingPeriod.save()

            logging.info(request.user.username + ' created accounting period #' + str(accountingPeriod.id))

            return JsonResponse({ "message": "Success!", "accountingPeriod": model_to_dict(accountingPeriod) }, status=200)

        return HttpResponseRedirect('/advertising/account/' + str(account.id) + '/fiscal-years')

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "account": account, 
        "fiscalYears": fiscalYears,
    }

    return render(request, "finance/FiscalYears.html", context)

def list_transaction_codes(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    transaction_codes = TransactionCode.objects.all()

    context = {
        "access": "allow",
        "message": "",
        "groups": ', '.join(views.get_groups(request)),
        "menu": views.get_sidebar(request),
        "transaction_codes": transaction_codes
    }

    return render(request, "finance/TransactionCodesList.html", context)

def pay_invoice(request, invoiceId):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")
    
    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    invoice = get_object_or_404(Invoice, pk=invoiceId)

    account = invoice.account

    if request.method == 'POST':
        reqData = json.loads(request.body.decode('utf-8'))

        today_date = datetime.today()
        date_str = today_date.isoformat()

        if reqData['amount'] == 'full':

            invoice.is_paid = True 
            invoice.date_paid = date_str
            invoice.save()

            logger.info('/' + request.method + ' - User #' + str(request.user.id) + ' paid invoice #' + str(invoice.id) + ' in full')

            date_str = date_str[0:10]
            description = 'Invoice #' + str(invoice.id) + ' payment in full'
            transaction = Transaction(date=date_str, invoice=invoice, description=description, amount=invoice.amount, transaction_number=generateRandomNumber(5))
            transaction.save()

            return JsonResponse({ "message": "Invoice paid" }, status=200)
        elif reqData['amount'] == 'use_credit':
            creditBalance = round(Decimal(account.credit),2)
            difference = invoice.amount - creditBalance
            creditUsed = abs(invoice.amount - creditBalance)

            if difference < 0:
                creditBalance = abs(difference)

                invoice.is_paid = True
                invoice.date_paid = date_str
                invoice.amount = 0
                invoice.save()

                date_str = date_str[0:10]
                description = 'Invoice #' + str(invoice.id) + ' was paid off using credit amount of $' + str(creditBalance)
                transaction = Transaction(date=date_str, invoice=invoice, description=description, amount=creditUsed, transaction_number=generateRandomNumber(5))
                transaction.save()

                account.credit = creditBalance - creditUsed
                account.save()

                logging.info(request.user.username + ' paid off invoice #' + str(invoice.id) + ' using ' + str(account.id) + '}\'s credit balance of $' + str(invoice.amount + difference))

                return JsonResponse({ "message": "Invoice paid" }, status=200)
            else:
                invoice.amount = invoice.amount - creditBalance
                invoice.save()

                account.credit = 0
                account.save()

                date_str = date_str[0:10]
                description = 'Invoice #' + str(invoice.id) + ' amount was reduced by $' + str(creditBalance) + ' using credit balance'
                transaction = Transaction(date=date_str, invoice=invoice, description=description, amount=creditUsed, transaction_number=generateRandomNumber(5))
                transaction.save()

                return JsonResponse({ "message": "Invoice paid" }, status=200)

        else:
            reqAmount = Decimal(reqData['amount'])
            invoice.amount = invoice.amount - reqAmount

            if invoice.amount < 0:
                difference = abs(0 - invoice.amount)

                invoice.amount = 0
                invoice.is_paid = True
                invoice.date_paid = datetime.now()

                invoice.save()

                logger.info('/' + request.method + ' - User #' + str(request.user.id) + ' paid $' + str(reqAmount) + ' on invoice #' + str(invoice.id))

                date_str = date_str[0:10]
                description = 'Invoice #' + str(invoice.id) + ' payment of $' + str(reqAmount)
                transaction = Transaction(date=date_str, invoice=invoice, description=description, amount=reqAmount, transaction_number=generateRandomNumber(5))
                transaction.save()
                
                overflowSortOrder = [overflow.name for overflow in OverflowBalance.objects.filter(account=invoice.account).order_by('sort_order')]

                done = False
                while difference > 0 and not done and len(overflowSortOrder) > 0:
                    overflow_location = overflowSortOrder[0]

                    account = invoice.account

                    if overflow_location == 'account_balance':
                        if account.balance > 0:
                            if account.balance - difference > 0:
                                account.balance = account.balance - difference
                                account.save()

                                paymentNotes = 'Paid ' + str(difference) + ' towards the account balance'
                                payment = AccountPaymentHistory(account=account, amount=difference, payment_type='Default', payment_method='dev', payment_notes=paymentNotes)
                                payment.save() 

                                logging.info(request.user.username + ' paid ' + str(difference) + ' towards account #' + str(account.id) + '\'s balance')

                                difference = 0
                                done = True
                            else:
                                difference = abs(account.balance - difference)

                                paymentNotes = request.user.username + ' paid account #' + str(account.id) + '\'s remaining balance'
                                payment = AccountPaymentHistory(account=account, amount=account.balance, payment_type='Default', payment_method='dev', payment_notes=paymentNotes)
                                payment.save() 

                                account.balance = 0
                                account.save()

                                logging.info(request.user.username + ' paid account #' + str(account.id) + '}\'s remaining balance')

                    elif overflow_location == 'oldest_invoice':
                        oldest_invoice = Invoice.objects.filter(account=account, is_paid=False, amount__gt=0).order_by('date_sent').first()

                        if oldest_invoice.amount - difference > 0:
                            oldest_invoice.amount = oldest_invoice.amount - difference
                            oldest_invoice.save()

                            paymentNotes = request.user.username + ' paid ' + str(difference) + ' towards invoice #' + str(oldest_invoice.id)
                            payment = AccountPaymentHistory(account=account, amount=difference, payment_type='Default', payment_method='dev', payment_notes=paymentNotes)
                            payment.save() 

                            logging.info(request.user.username + ' paid ' + str(difference) + ' towards invoice #' + str(oldest_invoice.id))

                            difference = 0
                            done = True
                        else:
                            difference = abs(oldest_invoice.amount - difference) 

                            paymentNotes = request.user.username + ' paid ' + str(difference) + ' paid invoice #' + str(oldest_invoice.id) + '\'s remaining amount'
                            payment = AccountPaymentHistory(account=account, amount=difference, payment_type='Default', payment_method='dev', payment_notes=paymentNotes)
                            payment.save() 

                            logging.info(request.user.username + ' paid ' + str(difference) + ' paid invoice #' + str(oldest_invoice.id) + '\' remaining amount')

                            oldest_invoice.amount = 0
                            oldest_invoice.is_paid = True
                            oldest_invoice.date_paid = datetime.now()
                    
                    elif overflow_location == 'floating_credit':
                        account.credit = Decimal(account.credit) + difference
                        account.save()

                        logging.info('$' + str(difference) + ' was added to account #' + str(account.id)  + '\'s floating credit')

                        difference = 0
                        done = True

                    overflowSortOrder.pop(0)
            else:
                # since the amount was already taken out of the invoice's remaining balance, we just save the invoice
                invoice.save()

                date_str = date_str[0:10]
                description = 'Invoice #' + str(invoice.id)  + 'amount was reduced by $' + str(reqAmount)
                transaction = Transaction(date=date_str, invoice=invoice, description=description, amount=reqAmount, transaction_number=generateRandomNumber(5))
                transaction.save()

                logging.info(request.user.username + ' paid $' + str(reqAmount) + ' on invoice #' + str(invoice.id))

                return JsonResponse({ "message": 'Invoice payment sent. Remaining invoice amount: $' + str(invoice.amount) }, status=200)