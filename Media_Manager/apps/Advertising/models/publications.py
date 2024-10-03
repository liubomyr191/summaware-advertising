from django.db import models
from django.forms import model_to_dict

from ..models.advertising import Adjustment
from ..models.companies import GLCode

from ..helpers import daysOfTheWeek, weekdayDict

# ------- MODEL DEFINITIONS -------
class Publication(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    spot_color = models.CharField(max_length=50)
    charge_tax = models.BooleanField(default=False)
    credit_memo = models.TextField(default=None)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_publication'

class PublicationRunDay(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, null=True)
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_publicationrunday'

class PublicationPageDimension(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    page_size = models.FloatField(default=0.0)
    columns_per_page = models.FloatField(default=0.0)
    column_width = models.FloatField(default=0.0)
    page_width = models.FloatField(default=0.0)
    page_height = models.FloatField(default=0.0)
    page_border = models.FloatField(default=0.0)
    gutter_size = models.FloatField(default=0.0)
    column_inches = models.FloatField(default=0.0)
    inches = models.FloatField(default=0.0)
    default_size = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'advertising_publicationpagedimension'

class PublicationDefaultStyle(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    font = models.CharField(max_length=100, default=None)
    font_size = models.FloatField(default=0.0)
    inset = models.FloatField(default=0.0)
    frame_width = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_publicationdefaultstyle'

class PublicationSection(models.Model):
    name = models.CharField(max_length=255)
    code=models.CharField(max_length=255)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE,null=True,blank=True)
    default_rates = models.FloatField(default=0.0)
    number_pages = models.FloatField(default=0.0)
    page_start = models.IntegerField(default=0)
    page_end = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_publicationsection'

# TODO - Version 2.0 --> PublicationSectionDeadline model


# ------- Method DEFINITIONS -------
def getPublicationRunDays(publication):
    """
        @param publication: a publication object

        returns an array of dictionary objects containing the run days of the publication 
    """

    runDays = PublicationRunDay.objects.filter(publication=publication)
    return [model_to_dict(day) for day in runDays]

def getRunDays(publication):
    """
        @param publication: a Publication object

        returns an array of strings containing the run days of the publication given
    """
    runDays = model_to_dict(PublicationRunDay.objects.get(publication=publication))

    runDayArray = [key for key in runDays if key in daysOfTheWeek and runDays[key]]
    return runDayArray
    
def getRunDaysByPublicationArray(publication_array):
    pass

def getPublicationSpotColors(publication_array):
    """
        @param publication_array: an array of publication ids

        returns an array of objects, each of which contains the name of the publication and the corresponding spot color 
    """
    colors = []
    for publication in publication_array:
        pubDetails = Publication.objects.get(id=publication)
        colors.append({ "publication_id": pubDetails.id, "publication_name": pubDetails.name, "color": pubDetails.spot_color })

    return colors

def getPublicationGLCodes(publication):
    """
        @param publication: a Publication object

        returns a list of GL Codes associated with the given publication
    """
    codes = GLCode.objects.filter(company=1)
    if len(codes):
        return [model_to_dict(code) for code in codes]
    else:
        return []

def getAdjustmentsByPublication(publication):
    """
        @param publication: a Publication object

        returns a list of Adjustments associated with the given publication
    """
    adjustments = Adjustment.objects.filter(publication=publication).select_related()
    if len(adjustments):
        return [model_to_dict(adjustment) for adjustment in adjustments]
    else:
        return []

def getAdjustmentsByPublicationArray(publication_array):
    """
        @param publication_array: an array of Publication ids

        returns an object containing Publication names as keys and its GL Codes in list format
    """

    publicationList = []
    for publicationId in publication_array:
        publication = Publication.objects.get(id=publicationId)  
        publicationList.append(publication)  

    adjustments = {}
    for publication in publicationList:
        if publication not in adjustments:
            adjustments[publication.name] = getAdjustmentsByPublication(publication)
    return adjustments