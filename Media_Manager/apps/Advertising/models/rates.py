from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import model_to_dict

from Media_Manager.apps.Advertising.models.orders import AdType

from .advertising import Account
from .orders import AdType
from .companies import GLCode
from .publications import Publication

# ------- MODEL DEFINITIONS -------
class RateGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_deactivate_rate", "Can deactivate rate"),
            ("can_reactivate_rate", "Can reactivate rate"),
            ("can_view_hidden_rates", "Can view hidden rates"),
            ("can_lock_rates", "Can lock rates"),
            ('can_create_rates', "Can create rates")
        )

        db_table = 'advertising_rategroup'

class Rate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pricing = models.BooleanField(default=False)
    measurement_type = models.CharField(max_length=100)
    tax_category = models.CharField(max_length=100, default="No Tax")
    override_privileges= models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    assigned_groups = models.BooleanField(default=True)
    ad_type = models.ForeignKey(AdType, on_delete=CASCADE)
    # ad_type = models.IntegerField(max_length = 14)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    insertion_min = models.CharField(max_length=255)
    insertion_max = models.CharField(max_length=255)
    line_for_ad_min = models.CharField(max_length=255)
    line_for_ad_max = models.CharField(max_length=255)
    insertion_count = models.IntegerField()
    base_cost = models.CharField(max_length=100)
    base_count = models.CharField(max_length=100)
    additional_cost = models.CharField(max_length=100)
    additional_count = models.CharField(max_length=100)
    charge_for = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    default_gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_deactivate_rate", "Can deactivate rate"),
            ("can_reactivate_rate", "Can reactivate rate"),
            ("can_view_hidden_rates", "Can view hidden rates"),
            ("can_lock_rates", "Can lock rates"),
            ('can_create_rates', "Can create rates")
        )

        db_table = 'advertising_rate'

class ExtraRateGroup(models.Model):
    rate = models.ForeignKey(Rate, on_delete=CASCADE)
    rategroup = models.ForeignKey(RateGroup, on_delete=CASCADE)

    class Meta:
        permissions = (
            ("can_deactivate_rate", "Can deactivate rate"),
            ("can_reactivate_rate", "Can reactivate rate"),
            ("can_view_hidden_rates", "Can view hidden rates"),
            ("can_lock_rates", "Can lock rates"),
            ('can_create_rates', "Can create rates")
        )

        db_table = 'advertising_extra_rategroup'
class AdvertisingRate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    unit_type = models.CharField(max_length=100)
    unit_price = models.FloatField(default=None)
    tax_category = models.CharField(max_length=100, default="No Tax")
    pricing = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    ad_type = models.ForeignKey(AdType, on_delete=CASCADE)
    # ad_type = models.IntegerField(max_length = 14)
    start_date = models.CharField(max_length=100, blank=False)
    end_date = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Static") # TODO - move location from ad rate to order
    hidden = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    default_gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE)
    publication_id = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_deactivate_rate", "Can deactivate rate"),
            ("can_reactivate_rate", "Can reactivate rate"),
            ("can_view_hidden_rates", "Can view hidden rates"),
            ("can_lock_rates", "Can lock rates"),
            ('can_create_rates', "Can create rates")
        )

        db_table = 'advertising_advertisingrate'

class SpecialRate(models.Model):
    numTimes = models.IntegerField(null=True, default=0)
    required_cost = models.FloatField(null=True)
    price = models.FloatField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_specialrate'

class RatePublication(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    rate = models.ForeignKey(AdvertisingRate, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advertising_ratepublication'

class RateGLCode(models.Model):
    rate = models.ForeignKey(AdvertisingRate, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE)
    # company = models.ForeignKey('Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_rateglcode'

# class CompanyRateGLCode(models.Model):
#     company = models.ForeignKey('Company', on_delete=models.CASCADE)
#     rate = models.ForeignKey('AdvertisingRate', on_delete=models.CASCADE)
#     publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
#     gl_code = models.ForeignKey('CompanyGLCode', on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)

#     class Meta:
#         db_table = 'advertising_companyrateglcode'


# ------- MODEL METHODS -------
def getActiveRates():
    """
        returns a list of all active rates 
    """
    return AdvertisingRate.objects.filter(active=True)

def getActiveRatesByAccount(account):
    """
        @param account: an Account model instance
        
        returns a list of all active rates for a given account
    """
    return getActiveRates().filter(account=account)

def getActiveRatesByPublication(publication, ad_type):
    """
        @param publication_id: a Publication model instance
        @param ad_type: an Ad Type model instance

        returns a list of all active rates for a given publication
    """
    publicationRates = RatePublication.objects.filter(publication=publication)
    if len(publicationRates):
        rates = []
        for pubRate in publicationRates:
            try:
                rate = AdvertisingRate.objects.get(id=pubRate.rate.id, ad_type=ad_type, active=True)
                rates.append(model_to_dict(rate))
            except AdvertisingRate.DoesNotExist as error:
                print(error)
                continue
        return rates
    else:
        return []

def getActiveRatesByPublicationArray(publication_array, ad_type):
    """
        @param publication_array: an array of Publication model instances
        @param ad_type: an Ad Type model

        returns an object containing Publication names as keys and its rates in list format
    """
    if not isinstance(publication_array, list):
        return { "message": "Invalid list of publications given. Please try again." }

    results = {}
    for publication in publication_array:
        if publication not in results:
            results[publication.name] = getActiveRatesByPublication(publication, ad_type)
    return results

def getRatePublications(rateId):
    if isinstance(rateId, str):
        try:
            rate = AdvertisingRate.objects.get(pk=rateId)
        except Publication.DoesNotExist:
            return "Error. Cannot find rateId"
    
    return RatePublication.objects.filter(rate=rate)