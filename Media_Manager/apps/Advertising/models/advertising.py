from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.forms import model_to_dict

from datetime import datetime, date

from django.http import JsonResponse

# ------- MODEL DEFINITIONS -------
class SalesPerson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None,null=True,blank=True)
    city = models.CharField(max_length=100, default=None,null=True,blank=True)
    state = models.CharField(max_length=100, default=None,null=True,blank=True)
    zip_code = models.CharField(max_length=100, default=None,null=True,blank=True)
    email = models.CharField(max_length=100, default=None,null=True,blank=True)
    phone_number = models.CharField(max_length=100, null=True, default=None)
    active = models.BooleanField(default=True)
    commission_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'advertising_salesperson'

class IndustryCode(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    account = models.ForeignKey('Account', on_delete=CASCADE,null=True,blank=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_industrycode'

class CompanyDepartment(models.Model):
    name = models.CharField(max_length=30, unique=True)

    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_department'



class Account(models.Model):
    # Old fields
    submitter = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.ForeignKey('AccountType', null=True, on_delete=SET_NULL)
    sales_person = models.ForeignKey('SalesPerson', null=True, on_delete=SET_NULL, default=None)
    industry_code = models.ForeignKey('IndustryCode', null=True, on_delete=SET_NULL, default=None, related_name='account_industry_code')
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_name_first = models.CharField(max_length=100, null=True, blank=True)
    contact_name_last = models.CharField(max_length=100, null=True, blank=True)
    company_name_1 = models.CharField(max_length=255, null=True, blank=True)
    company_name_2 = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    legacy_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2, null=True, blank=True)
    total_spent = models.FloatField(default=0.00, null=True, blank=True)
    last_activity = models.CharField(max_length=100, null=True, blank=True)
    last_ad_run = models.DateField(default=None, null=True, blank=True)
    can_run_ads = models.BooleanField(default=True, null=True, blank=True)
    default_publication = models.ForeignKey('Publication', on_delete=SET_NULL, null=True, default=None)
    can_accept_checks = models.BooleanField(default=True, null=True, blank=True)
    tax_exempt = models.BooleanField(default=False, null=True, blank=True)
    last_payment_date = models.CharField(max_length=100, null=True, blank=True)
    invoice_frequency = models.CharField(default='period', max_length=45, null=True, blank=True)
    invoice_type = models.CharField(default='email', max_length=45, null=True, blank=True)
    mail_invoice_charge = models.FloatField(default=0.00, null=True, blank=True)
    credit = models.DecimalField(default=0, max_digits=19, decimal_places=2, null=True, blank=True)
    credit_limit = models.DecimalField(default=1000.0, max_digits=19, decimal_places=2, null=True, blank=True)
    write_off_amount = models.IntegerField(default=0, null=True, blank=True)
    write_off_period = models.CharField(max_length=30, default=None, null=True, blank=True)
    prepay_required = models.BooleanField(default=False, null=True, blank=True)
    billing_email = models.EmailField(max_length=100, null=True, blank=True)
    billing_address = models.EmailField(max_length=100, null=True, blank=True)
    billing_city = models.EmailField(max_length=100, null=True, blank=True)
    billing_state = models.EmailField(max_length=100, null=True, blank=True)
    billing_zip_code = models.EmailField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=0, null=True, blank=True)

    # New fields from the Excel sheet
    sort_2 = models.CharField(max_length=100, null=True, blank=True)
    customer_number = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    alt_account_number = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    account_type_code = models.CharField(max_length=100, null=True, blank=True)
    account_type_descr = models.CharField(max_length=255, null=True, blank=True)
    business_unit = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    export_ar = models.BooleanField(default=False)
    subscriber = models.BooleanField(default=False)
    in_collection = models.BooleanField(default=False)
    notify_manager = models.BooleanField(default=False)
    do_not_publish = models.BooleanField(default=False)
    no_new_ads = models.BooleanField(default=False)
    setaside_new_ads_code = models.CharField(max_length=100, null=True, blank=True)
    setaside_new_ads_descr = models.CharField(max_length=255, null=True, blank=True)
    prepay_cash_required = models.BooleanField(default=False)
    po_required = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    stop_date = models.DateField(null=True, blank=True)
    run_date = models.DateField(null=True, blank=True)
    label_line_1 = models.CharField(max_length=255, null=True, blank=True)
    label_line_2 = models.CharField(max_length=255, null=True, blank=True)
    label_line_3 = models.CharField(max_length=255, null=True, blank=True)
    label_line_4 = models.CharField(max_length=255, null=True, blank=True)
    label_line_5 = models.CharField(max_length=255, null=True, blank=True)
    label_line_6 = models.CharField(max_length=255, null=True, blank=True)

    # def __str__(self):
    #     return self.name

    class Meta:
        permissions = (
            ('view_account_notes', 'Can view account notes'),
            ('can_view_sales_rep_notes', 'Can view sales rep notes'),
            ('can_add_sales_rep_notes', 'Can add sales rep notes'),
            # TODO - add permission to restrict access to changing sales rep field
        )
        db_table = 'advertising_account'

class AccountAddress(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    address1 = models.CharField(max_length=255, default=None)
    address2 = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=255, default=None)
    state = models.CharField(max_length=50, default=None)
    zip_code = models.CharField(max_length=50)
    primary = models.BooleanField(default=False)
    billing = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_accountaddress'
    
class AccountType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_accounttype'

class MarketCode(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    active = models.IntegerField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        db_table = "advertising_marketcode"

class CompanyContact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=CASCADE)
    department = models.ForeignKey('CompanyDepartment', on_delete=CASCADE)
    default = models.IntegerField()
    active = models.IntegerField()
    class Meta:
        db_table = 'advertising_companycontact'

class AdvertiserTaskList(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    due_date = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    note = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=CASCADE)
    status = models.IntegerField()
    complete = models.IntegerField()
    class Meta:
        db_table = 'advertising_tasks'

class AccountHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    detail = models.CharField(max_length=100)
    submitter = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accounthistory'

class AccountPaymentHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    amount = models.FloatField()
    payment_type = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)
    payment_method = models.CharField(max_length=100)
    payment_notes = models.TextField(null=True)

    class Meta:
        db_table = 'advertising_accountpaymenthistory'

# TODO - Add a model for company contacts history
class AdminPublication(models.Model):
    parent_id = models.IntegerField()
    name = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.ForeignKey('AllStates', on_delete=models.CASCADE, default=None)
    zip_code = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    calendar_type = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    gl_override = models.CharField(max_length=255)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE, default=None)
    repeat = models.IntegerField(default=0)
    schedule_type = models.IntegerField(default=1)
    run_days = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    created_by = models.CharField(max_length=255)

    class Meta:
        db_table = 'advertising_adminpublication'

class AdminPublicationSchedule(models.Model):
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    gl_override = models.CharField(max_length=255)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE, default=None)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'advertising_adminpublication_schedule'

class PubAdjustment(models.Model):
    adminadjustment = models.ForeignKey('AdminAdjustment', on_delete=CASCADE)
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_pub_adjustment'

class PubRategroup(models.Model):
    rategroup = models.ForeignKey('RateGroup', on_delete=CASCADE)
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_pub_rategroup'

class PubSection(models.Model):
    adminsection = models.ForeignKey('PublicationSection', on_delete=CASCADE)
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_pub_section'

class PubRegion(models.Model):
    region = models.ForeignKey('Region', on_delete=CASCADE)
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_pub_region'

class AdminAdjustment(models.Model):
    code = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=255, default=None)
    apply_level = models.CharField(max_length=50) # ['order', 'insertion']
    value_type = models.CharField(max_length=50) # ['amount', 'percentage']
    value = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=100) # username
    type = models.CharField(max_length=20) # ['credit', 'debit']
    # type = models.CharField(max_length=20) # ['gross', 'net']
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    prompt_for_value = models.BooleanField(default=False)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE, default=None)
    section = models.ForeignKey('PublicationSection', on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = 'advertising_adminadjustment'

    def __str__(self):
        return self.code
class PubAdType(models.Model):
    adminadtype = models.ForeignKey('AdminAdType', on_delete=CASCADE)
    adminpublication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_pub_adtype'
class AdminAdType(models.Model):
    code = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=255, default=None)
    default_rate = models.ForeignKey('Rate', on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'advertising_adminadtype'

    def __str__(self):
        return self.code
class AdminMarketCode(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "advertising_adminmarketcode"
class Adjustment(models.Model):
    code = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=255, default=None)
    apply_level = models.CharField(max_length=50) # ['order', 'insertion']
    value_type = models.CharField(max_length=50) # ['amount', 'percentage']
    amount = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=100) # username
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    type = models.CharField(max_length=20) # ['credit', 'debit']
    # type = models.CharField(max_length=20) # ['gross', 'net']
    active = models.BooleanField(default=True)    
    prompt_for_value = models.BooleanField(default=False)
    section = models.ForeignKey('PublicationSection', on_delete=models.CASCADE, default=None)
    gross_net = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'advertising_adjustment'

    def __str__(self):
        return self.code
class DigitalSize(models.Model):
    product = models.ForeignKey('DigitalProduct', on_delete=models.CASCADE)
    size = models.ForeignKey('StandardSize', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_digital_size'

class MagazineSize(models.Model):
    product = models.ForeignKey('MagazineProduct', on_delete=models.CASCADE)
    size = models.ForeignKey('StandardSize', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_magazine_size'
        
class NewspaperSize(models.Model):
    product = models.ForeignKey('NewspaperProduct', on_delete=models.CASCADE)
    size = models.ForeignKey('StandardSize', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_newspaper_size'
class MagazineProduct(models.Model):
    product_mag = models.TextField(null=True)
    measurement_type = models.TextField(null=True)
    fold_orientation = models.TextField(null=True)
    height = models.IntegerField()
    width = models.IntegerField()
    columns = models.IntegerField()
    column_width = models.IntegerField()
    page_width = models.IntegerField()
    page_height = models.IntegerField()
    page_border = models.IntegerField()
    gutter_size = models.IntegerField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'advertising_magazine_products'

    def __str__(self):
        return self.code
    
class NewspaperProduct(models.Model):
    product_mag = models.TextField(null=True)
    measurement_type = models.TextField(null=True)
    fold_orientation = models.TextField(null=True)
    height = models.IntegerField()
    width = models.IntegerField()
    columns = models.IntegerField()
    column_width = models.IntegerField()
    page_width = models.IntegerField()
    page_height = models.IntegerField()
    page_border = models.IntegerField()
    gutter_size = models.IntegerField()
    top_border = models.FloatField(default=0.0)
    bottom_border = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'advertising_newspaper_products'

    def __str__(self):
        return self.product_mag

class DigitalProduct(models.Model):
    product_mag = models.TextField(null=True)
    format = models.TextField(null=True)
    adminadtype = models.ForeignKey('AdminAdType', on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'advertising_digital_products'

    def __str__(self):
        return self.code
class StandardSize(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField() # type == 1 == newspaper, type == 2 == magazine , type == 3 == digital
    description = models.TextField(null=True)
    columns = models.IntegerField()
    height = models.FloatField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'advertising_standardsize'
    @property
    def total_columns_in(self):
        return self.columns * self.height
    def __str__(self):
        return self.description
    
class AccountNote(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    note = models.TextField(null=True)
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_accountnote'

class AccountSalesRepNote(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    sales_person = models.ForeignKey(SalesPerson, on_delete=CASCADE)
    note = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_accountsalesrepnote'

class SalesPersonTask(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(null=True, default=datetime.today().strftime('%Y/%m/%d'))
    salesperson = models.ForeignKey('SalesPerson', on_delete=CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'advertising_salespersontask'

class SalesPersonLedger(models.Model):
    salesperson = models.ForeignKey('SalesPerson', on_delete=CASCADE)
    order = models.ForeignKey('AdvertisingOrder', on_delete=CASCADE)
    money_spent = models.FloatField(default=0.0)
    date_spent = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_salespersonledger'

class SubCompany(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Example --> region, subsection, dept., etc.

    class Meta:
        db_table = 'advertising_subcompany'

class AllStates(models.Model):
	name = models.TextField()
	abbreviation = models.TextField()

	class Meta:
		db_table = 'all_states'

class Region(models.Model):
    name = models.TextField()
    code = models.TextField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    class Meta:
        db_table = 'advertising_region'

class AdminTax(models.Model):
    name = models.TextField()
    description = models.TextField(null=True)
    format = models.CharField(max_length=255)
    assigned_gl = models.CharField(max_length=255)
    amount = models.FloatField(default=0)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE, default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    class Meta:
        db_table = 'advertising_tax'

    def __str__(self):
        return self.description
    
class AdminFiscalYear(models.Model):
    name = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    class Meta:
        db_table = 'advertising_adminfiscalyear'

    def __str__(self):
        return self.name
# ------- MODEL METHODS -------
def getSalesPersonFullName(salesrep_id):
    """
        @param salesrep_id: the id of a salesperson

        returns the full name of a salesperson
    """

    try:
        salesrep = SalesPerson.objects.get(id=salesrep_id)
    except SalesPerson.DoesNotExist:
        return ""
    
    return str(salesrep.first_name + " " + salesrep.last_name)

def getActiveSalesPersonTasks(salesrep):
    """
        @param salesrep: a SalesPerson object

        returns an array of dictionaries containing the salesperson's active tasks
    """
    return [model_to_dict(task) for task in SalesPersonTask.objects.filter(salesperson=salesrep, completed=False)]

def getOverdueSalesPersonTasks(salesrep):
    """
        @param salesrep: a SalesPerson object

        returns an array of dictionaries containing the salesperson's overdue tasks
    """
    overdue_tasks = []
    try:
        taskList = SalesPersonTask.objects.filter(salesperson=salesrep)
        if taskList:
            for task in taskList:
                if task.date < datetime.date(datetime.today()) and not task.completed:
                    overdue_tasks.append(model_to_dict(task))

        else:
            return []
        return overdue_tasks
    except SalesPersonTask.DoesNotExist:
        return []

def wasCreatedRecently(account):
    """
        @param account: an instance of the Account model

        returns True if account.created_at was less than a month ago and False if otherwise
    """

    return (date.today() - account.created_at.date()).days < 30
   
