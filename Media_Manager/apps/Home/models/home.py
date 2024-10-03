from django.db import models
from django.contrib.auth.models import User


class Confirmation_Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TextField()
    code = models.TextField()
    status = models.TextField()

    class Meta:
        db_table = 'mm_code_confirmations'


class Org_Meta(models.Model):
    meta_key = models.CharField(max_length=255, default='')
    meta_value = models.TextField()

    class Meta:
        db_table = 'mm_org_info'


class User_Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.CharField(max_length=255, default='')
    ip_address = models.TextField()
    dashboard_name = models.TextField()
    dashboard_charts = models.TextField()
    dashboard_filters = models.TextField()

    chart_title = models.TextField()
    chart_table_name = models.CharField(max_length=50, default='')
    chart_query = models.TextField()
    chart_attributes = models.TextField()
    chart_chart_type = models.CharField(max_length=11)
    chart_drilldowns = models.TextField()
    chart_selects = models.TextField()
    chart_wheres = models.TextField()
    chart_group_bys = models.TextField()
    chart_order_bys = models.TextField()
    chart_limits = models.TextField()

    class Meta:
        db_table = 'mm_user_logs'


class Error_Logs(models.Model):
    dashboard_id = models.CharField(max_length=10, default='')
    chart_id = models.CharField(max_length=10, default='')
    user_dashboard_id = models.CharField(max_length=10, default='')
    user_chart_id = models.CharField(max_length=10, default='')
    error = models.TextField()
    query = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard_name = models.TextField()
    dashboard_charts = models.TextField()
    dashboard_filters = models.TextField()

    chart_title = models.TextField()
    chart_table_name = models.CharField(max_length=50, default='')
    chart_query = models.TextField()
    chart_attributes = models.TextField()
    chart_chart_type = models.CharField(max_length=11)
    chart_drilldowns = models.TextField()
    chart_selects = models.TextField()
    chart_wheres = models.TextField()
    chart_group_bys = models.TextField()
    chart_order_bys = models.TextField()
    chart_limits = models.TextField()

    class Meta:
        db_table = 'mm_user_error_logs'
