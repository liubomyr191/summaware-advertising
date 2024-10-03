from django.db import models
from django.contrib.auth.models import User

from ..models.advertising import Account

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_role'

class UserRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_userrole'

class AccountAdmin(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accountadmin'

# TODO - there is a possibility to have more than one account manager, but for now only allow for one
class AccountManager(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accountmanager'

class AccountSalesperson(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accountsalesperson'

class AdAssistant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    salesperson = models.ForeignKey('SalesPerson', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_adassistant'

class CreditLimitManagerOverride(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    overridden = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_overridden = models.DateTimeField(null=True)

    class Meta:
        db_table = 'advertising_creditlimitmanageroverride'

class ManagerOverride(models.Model):
    name = models.CharField(max_length=200)
    overridden = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_user')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_overridden = models.DateTimeField(null=True)
    notes = models.TextField(default=None)

    class Meta:
        db_table = 'advertising_manageroverride'

class PublicationAccess(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_publicationaccess'

class CustomSizePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'advertising_customsizepermission'

class AccountAccess(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_accountaccess'

# TODO - permissions to be able to edit invoices, add/remove surcharges and/or service charges to an invoice (even after its been sent)
    

def getUserRoles(user, account):
    """
        @param username: an instance of the User model
        @param accountId: an instance of the Account model

        returns an array of role names assigned to a specific user
    """
    try:
        roles = UserRole.objects.filter(user=user, account=account)

    except UserRole.DoesNotExist:
        return []

    return [(Role.objects.get(id=role.role.id)).name for role in roles]

# TODO - refactor this to use the id instead of username 
# (some users may not have a username)
def isAdminOrManager(userId, accountId=None):
    """
        @param userId: an id of a user

        returns True if the user has a manager or admin role
    """
    
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return False

    if accountId is not None:
        try:
            account = Account.objects.get(pk=accountId)
        except Account.DoesNotExist:
            return False 

        try:
            accountAdminRole = AccountAdmin.objects.get(user=user, account=account)
            accountManagerRole = AccountManager.objects.get(user=user, account=account)
        except (AccountAdmin.DoesNotExist, AccountManager.DoesNotExist):
            return False

        return True if accountAdminRole or accountManagerRole else False     
    else :
        return True if user.is_superuser else False   


# Deprecated / Do Not Use
def isAdmin(user):
    """
        @param user: an instance of the User model
    """
    if isinstance(user, str):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return False

    return True if UserRole.objects.filter(user=user, role__in=[174, 175]) or user.is_superuser else False 

def getPublicationAccess(username):
    """
        @param username: the username of a user 

        returns an array of Publication objects that the given user has access to 
    """

    try: 
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return []

    return [row.publication for row in PublicationAccess.objects.filter(user=user)]
    
