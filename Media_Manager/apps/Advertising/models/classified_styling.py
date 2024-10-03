from django.db import models
from django_jsonfield_backport.models import JSONField

class ClassifiedStyle(models.Model):
    name = models.CharField(max_length=255)

    self_service_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'advertising_classified_styles'


class ClassifiedPublicationStyle(models.Model):
    publication_id = models.IntegerField()
    style_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Publication ID: {} - Style ID: {}".format(self.publication_id, self.style_id)
    
    class Meta:
        db_table = 'advertising_classified_publication_styles'


class ClassifiedStyleFontColor(models.Model):
    style_id = models.IntegerField()
    font = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Style ID: {} - Font: {} - Color: {}".format(self.style_id, self.font, self.color)
    
    class Meta:
        db_table = 'advertising_classified_styles_font_color'

class ClassifiedStyleFontSpec(models.Model):
    style_id = models.IntegerField()
    specs = JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Style ID: {} - Specs: {}".format(self.style_id, self.specs)
    
    class Meta:
        db_table = 'advertising_classified_styles_font_spec'