from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User


from datetime import datetime, timedelta

from django.http import JsonResponse
from .advertising import Account
from .orders import AdvertisingOrder

# -------------- Model Definitions ------------------
class AccountLedger(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=20)
    transaction_number = models.IntegerField()
    description = models.TextField(max_length=100)
    batch_number = models.IntegerField()
    amount = models.FloatField(max_length=10)
    balance = models.FloatField(max_length=10)
    due_date = models.DateField()
    period = models.ForeignKey('AccountingPeriod', on_delete=CASCADE)
    account = models.ForeignKey('Account', on_delete=CASCADE)

    class Meta:
        db_table = 'advertising_accountledger'

class AccountingPeriod(models.Model):
    code = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    account = models.ForeignKey('Account', on_delete=CASCADE)
    status = models.BooleanField(default=True)
    fiscal_year = models.ForeignKey('FiscalYear', on_delete=CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_accountingperiod'

# class ServiceCharge(models.Model):
#     pass

# TODO - include the fields: batch #, description, batch date, period, status, notes
class ServiceChargeHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    service_charge = models.ForeignKey('ServiceCharge', on_delete=CASCADE)
    submitter = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_servicechargehistory'

class Transaction(models.Model):
    date = models.DateField()
    invoice = models.ForeignKey('Invoice', on_delete=CASCADE)
    description = models.TextField()
    amount = models.FloatField()
    transaction_number = models.IntegerField(default=None)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'advertising_transaction'

class Invoice(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE, default=None)
    bill_end = models.DateField()
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    memo = models.TextField(default=None, null=True)
    date_sent = models.DateTimeField(null=True)
    date_paid = models.DateTimeField(null=True)
    original_amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'advertising_invoice'

class OrderInvoice(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=CASCADE)
    is_paid = models.BooleanField(default=False)
    # date_to_send = models.DateField()
    date_sent = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_orderinvoice'

class FiscalYear(models.Model):
    description = models.CharField(max_length=100, default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    account = models.ForeignKey('Account', on_delete=CASCADE)

    class Meta:
        db_table = 'advertising_fiscalyear'

class TransactionCode(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    subtype = models.CharField(max_length=100)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    balance_manually = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_transactioncode'

class ServiceCharge(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=None)
    apply_level = models.CharField(max_length=50)
    enabled = models.BooleanField(default=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_servicecharge'

# class AccountServiceCharge(models.Model):
#     charge = models.ForeignKey(ServiceCharge, on_delete=models.CASCADE)
#     account = models.ForeignKey('Account', on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)

class InvoiceServiceCharge(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    service_charge = models.ForeignKey('ServiceCharge', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_invoiceservicecharge'

class InvoicePaymentHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount = models.FloatField()
    notes = models.CharField(max_length=200)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_invoicepaymenthistory'

class OverflowBalance(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, default=None)
    sort_order = models.IntegerField(default=None)

    class Meta:
        db_table = 'advertising_overflowbalance'

class AccountPrintInvoiceCharge(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_accountprintinvoicecharge'

class InvoicePrintCharge(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_invoiceprintcharge'

class AccountingPeriodInvoice(models.Model):
    accounting_period = models.ForeignKey('AccountingPeriod', on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_accountingperiodinvoice'

class AccountBalanceHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    balance = models.DecimalField(decimal_places=2, max_digits=19, default=None)
    type = models.CharField(max_length=20) # [debit (-), credit (+)]
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accountbalancehistory'

class InvoiceWriteOff(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, default=None)
    written_off_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date_written_off = models.DateTimeField(default=None)

    class Meta:
        db_table = 'advertising_invoicewriteoff'

class BadDebt(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_baddebt'

class InvoiceAging(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=19, decimal_places=2)
    days_overdue = models.IntegerField(default=0)

    class Meta:
        db_table = 'advertising_invoiceaging'


# -------------- Model Methods ------------------
def getAccountingPeriodsFromFiscalYear(fiscal_year):
    """
        @param fiscal_period: a model instance of a fiscal year

        returns a list containing instances of AccountingPeriod linked to the fiscal year parameter
    """
    accountingPeriods = AccountingPeriod.objects.filter(fiscal_year=fiscal_year)
    return accountingPeriods

def getInvoiceAmountPerDay(startDate, endDate):
    startDateObj = datetime.strptime(startDate, '%Y-%m-%d')
    endDateObj = datetime.strptime(endDate, '%Y-%m-%d')

    delta = endDateObj - startDateObj
    return delta.days

def getInvoiceAmountPerWeek(startDate, endDate):
    numDays = getInvoiceAmountPerDay(startDate, endDate)

    return numDays // 7

def getInvoiceAmountPerMonth(startDate, endDate):
    startDateObj = datetime.strptime(startDate, '%Y-%m-%d')
    endDateObj = datetime.strptime(endDate, '%Y-%m-%d')

    num_months = (endDateObj.year - startDateObj.year) * 12 + (endDateObj.month - startDateObj.month)

    return num_months

def writeOffInvoice(invoiceId, username):
    """
        @param invoiceId: an id of an invoice
        @param username: the username of the user writing off the invoice 
    """

    try:
        # get the invoice to be written off 
        invoice = Invoice.objects.get(id=invoiceId)

    # if its not found, return a message saying it cant be found
    except Invoice.DoesNotExist:
        return JsonResponse({ "message": "Error. Invoice not found" }, status=200)

    # validate that the user doing this is an actual user in the system
    try:
        user = user.objects.get(username=username)

    # if not found, send a message saying the user could not be found 
    except User.DoesNotExist:
        return JsonResponse({ "message": "Error. Cannot find user." }, status=200)

    # mark the invoice as paid and add a credit memo saying its been written off
    invoice.is_paid = True
    if invoice.memo == '':
        invoice.memo = 'Written off at ' + datetime.now()
    else:
        invoice.memo = '\nInvoice written off at ' + datetime.now()

    invoice.save()

    # save a record of the bad debt in the database with the invoice number for our records 
    badDebt = BadDebt(account=invoice.account, invoice=invoice, amount=invoice.amount)
    badDebt.save()


    # save a record of the invoice write off in the database for our records 
    invoiceWriteOff = InvoiceWriteOff(account=invoice.account, invoice=invoice, amount=invoice.amount, written_off_by=user)
    invoiceWriteOff.save()

    return JsonResponse({ "message": "Invoice successfully written off" }, status=200)