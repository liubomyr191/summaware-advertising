from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.forms import model_to_dict

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    type = models.CharField(max_length=75)
    active = models.BooleanField(default=True)
    agency_id = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_company'

class CompanyAccount(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_companyaccount'

class CompanyGLCode(models.Model):
    code = models.CharField(max_length=4, unique=True)
    description = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_companyglcode'

class GLCode(models.Model):
    code = models.CharField(max_length=4, unique=True)
    description = models.CharField(max_length=100)
    # company = models.ForeignKey('Company', on_delete=models.CASCADE)
    pl_type = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        permissions = (
            ('can_create_gl_codes', 'Can create GL Codes'),
            ('can_edit_gl_codes', 'Can edit GL Codes'),
            ('can_import_gl_codes', 'Can import GL Codes'),
            ('can_export_gl_codes', 'Can export GL Codes'),
        )

    class Meta:
        db_table = 'advertising_glcode'

class ProfitCode(models.Model):
    description = models.CharField(max_length=100)
    profit_code = models.CharField(max_length=4, unique=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'advertising_profitcode'

class Location(models.Model):
    location = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=100)
    pc = models.CharField(max_length=3)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        permissions = (
            ('can_create_location', 'Can create Location'),
            ('can_edit_locations', 'Can edit Location'),
            ('can_import_location', 'Can import Location'),
            ('can_export_location', 'Can export Location'),
        )

    class Meta:
        db_table = 'advertising_location'

class CurrentCompany(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advertising_currentcompany'

class UserCompany(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_access = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'advertising_usercompany'


def isChildAccount(company, account):
    """
        determines if the account given is a child account under the company given
    """

    isChild = CompanyAccount.objects.filter(company=company, account=account)
    return len(isChild) > 0 


def getChildAccounts(company, includeAll=False):
    """
        returns a list of Account objects that are child accounts of the company given
    """
    companyAccountList = CompanyAccount.objects.filter(company=company)

    allAccountList = []
    activeAccountList = []

    for companyAccount in companyAccountList:
        currAccount = companyAccount.account
        if includeAll:
            allAccountList.append(currAccount)
        else:
            if not currAccount.archived:
                activeAccountList.append(currAccount)

    return allAccountList if includeAll else activeAccountList