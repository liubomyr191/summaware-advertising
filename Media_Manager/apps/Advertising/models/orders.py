from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

from ..models.advertising import Adjustment, SalesPerson

# ------- MODEL DEFINITIONS -------
class AdvertisingOrder(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    ad_type = models.ForeignKey('AdType', on_delete=models.CASCADE, null=True)
    ad_rate = models.ForeignKey('AdvertisingRate', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    submitter = models.CharField(max_length=100)
    salesperson = models.ForeignKey(SalesPerson, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    custom_min_height = models.IntegerField(default=0, null=True, blank=True)
    custom_min_width = models.IntegerField(default=0, null=True, blank=True)
    custom_max_height = models.IntegerField(default=0, null=True, blank=True)
    custom_max_width = models.IntegerField(default=0, null=True, blank=True)
    number_units = models.IntegerField(default=0)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    override_ad_cost = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    tearsheets = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    bill_date = models.CharField(max_length=100, default=None)
    notes = models.TextField(null=True)
    total_price = models.DecimalField(max_digits=19, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    # color = models.BooleanField(default=False)
    # color_type = models.CharField(max_length=100, default=None, null=True)
    is_draft = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    invoice_frequency = models.CharField(max_length=20, default=None)
    version = models.IntegerField(default=1)
    version_notes = models.TextField()
    status = models.CharField(max_length=30, default='running') # ['running', 'paused', 'cancelled']

    class Meta:
        permissions = (
            ("can_override_pricing", "Can override pricing"),
            ("can_override_deadline", "Can override deadline"),
            ("can_access_ad", "Can access ad"),
            ("can_edit_ad", "Can edit ad"),
            ("can_lock_ad", "Can lock ad"),
            ("can_make_ad_color", "Can make ad color"),
            ("can_define_custom_size", "Can define custom size"),
        )

        db_table = 'advertising_advertisingorder'

class OrderPublication(models.Model):
    order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.publication.name

    def was_recently_created(self):
        return self.date_created >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        db_table = 'advertising_orderpublication'

class OrderRate(models.Model):
    order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    rate = models.ForeignKey('AdvertisingRate', on_delete=models.CASCADE)
    number_units = models.IntegerField(default=0)

    class Meta:
        db_table = 'advertising_orderrate'

class OrderPublicationColor(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE, default=None)
    publication = models.ForeignKey('publication', on_delete=models.CASCADE, default=None)
    color = models.BooleanField(default=False)
    color_type = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = 'advertising_orderpublicationcolor'

class OrderPublicationSize(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    custom_min_height = models.IntegerField(default=0, null=True, blank=True)
    custom_min_width = models.IntegerField(default=0, null=True, blank=True)
    custom_max_height = models.IntegerField(default=0, null=True, blank=True)
    custom_max_width = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'advertising_orderpublicationsize'

class OrderPublicationDate(models.Model):
    date = models.DateField(default=None)
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_orderpublicationdate'

class AdType(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_adtype'

class OrderHistory(models.Model):
    detail = models.CharField(max_length=250)
    order_number = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    submitter = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_orderhistory'

class AdDeadline(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, default=None)
    publication_day = models.CharField(max_length=100)
    time = models.TimeField(default='00:13:00')
    ad_type = models.ForeignKey(AdType, on_delete=models.CASCADE)
    days_prior = models.IntegerField()
    priority_level = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("can_edit_deadline", "Can edit deadline"),
            ("can_view_deadline", "Can view deadline"),
            ("can_delete_deadline", "Can delete deadline"),
        )

        db_table = 'advertising_addeadline'

class Insertion(models.Model):
    ad_order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, default=None)
    date = models.DateField(default=None)
    weekday = models.CharField(max_length=25, default=None)
    status = models.CharField(max_length=100, default='Good')
    late = models.BooleanField(default=False)
    color = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("can_change_rate_mid_run", "Can change rate mid-run"),
        )

        db_table = 'advertising_insertion'

class LateAdApproval(models.Model):
    ad_order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    manager_email = models.CharField(max_length=100)
    manager_approval = models.BooleanField(default=False)
    publication_email = models.CharField(max_length=100)
    publication_approval = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_lateadapproval'

class RateLocation(models.Model):
    location = models.CharField(max_length=100)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'advertising_ratelocation'

class OrderAdjustment(models.Model):
    order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    adjustment = models.ForeignKey(Adjustment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_orderadjustment'

#
class InsertionInvoice(models.Model):
    order = models.ForeignKey(AdvertisingOrder, on_delete=models.CASCADE)
    insertion = models.ForeignKey(Insertion, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(null=True)
    date_paid = models.DateTimeField(null=True)

    class Meta:
        db_table = 'advertising_insertioninvoice'

class OrderCancellation(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE, default=None)
    date_cancelled = models.DateTimeField(default=None)
    cancelled_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_ordercancellation'

class OrderPublicationAdType(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    adType = models.ForeignKey('AdType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_orderpublicationadtype'

class OrderPublicationNote(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    notes = models.TextField(default=None)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderPublicationSection(models.Model):
    order = models.ForeignKey('AdvertisingOrder', on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    section = models.ForeignKey('PublicationSection', on_delete=models.CASCADE)

# ------- MODEL METHODS -------
def getOrderRates(order, publication):
    """
        @param order: an AdvertisingOrder model instance
        @param publication: an AdvertisingRate model instance

        returns a list of AdvertisingRate objects in a list
    """
    return OrderRate.objects.filter(order=order,publication=publication)
    
def getOrderRatesByPublicationArray(order, publication_array):
    """
    """
    if not isinstance(publication_array, list):
        return { "message": "Invalid list of publications given. Please try again." }

    results = {}
    for publication in publication_array:
        if publication not in results:
            results[publication.name] = getOrderRates(order, publication)
    return results