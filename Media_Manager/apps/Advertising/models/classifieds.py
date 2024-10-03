from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict

# ------- MODEL DEFINITIONS -------
class ClassifiedAd(models.Model):
    name = models.CharField(max_length=255)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    classification = models.ForeignKey('ClassifiedCampaignSummary', on_delete=models.CASCADE)
    #content = RichTextField(null=True, blank=True)
    content = models.TextField()
    recurring = models.BooleanField(default=False)
    recurring_amount = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    submitter = models.CharField(max_length=255, default=None)
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='on hold') # this will change once the ad is paid for 
    line_count = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=25, blank=True, null=True)  # Updated
    columns = models.IntegerField(default=0)
    column_length = models.IntegerField(default=0)
    unit = models.CharField(max_length=25, blank=True,null=True)
    words =models.CharField(max_length=25, blank=True,null=True)
    page_number = models.CharField(max_length=25, blank=True,null=True)
    overide_total=models.CharField(max_length=25, blank=True,null=True)
    custom_total = models.CharField(max_length=25, blank=True,null=True)
    layout_notes=models.TextField(blank=True,null=True)
    desgin_notes=models.TextField(blank=True,null=True)
    account_notes=models.TextField(blank=True,null=True)
    rate = models.CharField(max_length=250, blank=True, null=True)  # Updated

    # conversion_unit = models.CharField(max_length=20)
    ad_type = models.ForeignKey('AdminAdType', on_delete=models.CASCADE)
    # TODO - add a field for picture of the classified ad 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_classifiedad'

class ClassifiedStyling(models.Model):
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)
    frame_width = models.IntegerField(default=0)
    inset_amount = models.CharField(max_length=20)
    style_tag = models.TextField(default=None)

    class Meta:
        db_table = 'advertising_classifiedstyling'

class ClassifiedCampaignSummary(models.Model):
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    brief = models.CharField(max_length=255)
    advertiser_id = models.IntegerField(null=True)
    advertiser_name = models.CharField(max_length=50, null=True)
    contact_id = models.IntegerField(null=True)
    sales_contact = models.CharField(max_length=50, null=True)
    total_sub = models.IntegerField()
    total_adjustment = models.IntegerField()
    total_campaign = models.IntegerField()
    campaign_detail = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "advertising_campaign_summary"

class ClassifiedPublication(models.Model):
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)
    publication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_classifiedpublication'

class ClassifiedPublicationDate(models.Model):
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)
    publication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)
    date = models.CharField(max_length=25)

    class Meta:
        db_table = 'advertising_classifiedpublicationdate'


"""
    TODO - add a model for picture/logo of the classified ad
    # in case the customer just wants a picture instead of words as the content of the ad
"""

class ClassifiedGraphic(models.Model):
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'advertising_classifiedgraphic'


class Classification(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_classification'

    def __str__(self):
        return self.name

class UploadGraphic(models.Model):
    file_path = models.CharField(max_length=255, default=None)
    local_path = models.CharField(max_length=255, default=None)
    file = models.ImageField(upload_to="static/dist/img/advertising/")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_uploadgraphic'

class ClassifiedAdjustment(models.Model):
    code = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=255, default=None)
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    value_type = models.CharField(max_length=30, default=None) # ['amount', 'percentage']
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=100) # username
    apply_level = models.CharField(max_length=50) # ['order', 'insertion']
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    type = models.CharField(max_length=20) # ['credit', 'debit' ]
    active = models.BooleanField(default=True)
    prompt_for_value = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_classifiedadjustment'

    def __str__(self):
        return self.code

class ClassifiedAdAdjustment(models.Model):
    adjustment = models.ForeignKey('ClassifiedAdjustment', on_delete=models.CASCADE)
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_classifiedadadjustment'


class ClassifiedRate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    # ? All classified ads have the unit type of Liner? 
    # unit_type = models.CharField(max_length=100) 

    unit_price = models.FloatField(default=None)
    tax_category = models.CharField(max_length=100, default="No Tax")
    pricing = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100, blank=False)
    end_date = models.CharField(max_length=100, blank=False)
    hidden = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=100) # username

    class Meta:
        db_table = 'advertising_classifiedrate'

    def __str__(self):
        return self.name

class ClassifiedRatePublication(models.Model):
    rate = models.ForeignKey('ClassifiedRate', on_delete=models.CASCADE)
    publication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_classifiedratepublication'

class ClassifiedPublicationRate(models.Model):
    rate = models.ForeignKey('Rate', on_delete=models.CASCADE)
    publication = models.ForeignKey('AdminPublication', on_delete=models.CASCADE)
    classified = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE)

    class Meta:
        db_table = 'advertising_classifiedpublicationrate'

class ClassifiedAdType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_classifiedadtype'

class ClassifiedAdSize(models.Model):
    size = models.CharField(max_length=20)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_classifiedadsize'

class UploadGraphicsPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_upload_graphics = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_uploadgraphicspermission'

class DeleteGraphicsPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_deletegraphicspermission'

# ------- MODEL METHODS -------
def getClassifiedRates(publications):
    rateList = {}
    if (isinstance(publications, list)):
        for pubIndex in publications:
            publicationRates = ClassifiedRatePublication.objects.filter(publication=pubIndex)
            rateList[pubIndex] = []
            for pubRate in publicationRates:
                rate = pubRate.rate
                publication = pubRate.publication

                dict = {
                    'rate': model_to_dict(rate),
                    'publication': publication.name
                }

                rateList[pubIndex].append(dict)
    return rateList

def getAdDuration(classified):
    """
        @param classified: an instance of the ClassifiedAd model

        returns a string containing the amount of either days, weeks, or months the classified ad runs for 
    """
    pass
