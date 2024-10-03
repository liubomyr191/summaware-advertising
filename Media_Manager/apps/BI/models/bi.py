from django.db import models
from django.contrib.auth.models import User, Group, Permission

class Dashboard(models.Model):
	name = models.TextField()
	time = models.TextField()
	last_modified = models.TextField(default='')
	charts = models.TextField()
	filters = models.TextField()
	description = models.TextField()
	status = models.CharField(max_length=25)
	order_id = models.IntegerField(default='0')
	allowed_user_groups = models.TextField(default='')
	allowed_role_groups = models.TextField(default='')
	allowed_individuals = models.TextField(default='')
	group_owner = models.ForeignKey(Group, on_delete=models.CASCADE)
	section = models.TextField(default='')

	class Meta:
		app_label = 'BI'
		db_table = 'mm_dashboards'
		permissions = [
			("accounting_access", "Can access Accounting section"),
			("advertising_access", "Can access Advertising section"),
			("bi_access", "Can access Business Intelligence section"),
			("circulation_access", "Can access Circulation section"),
			("editorial_access", "Can access Editorial section"),
			("production_access", "Can access Production section")
		]

class Chart(models.Model):
	title = models.TextField()
	status = models.CharField(max_length=25)
	query = models.TextField()
	table_name = models.CharField(max_length=50, default='')
	attributes = models.TextField()
	time = models.TextField()
	chart_type = models.CharField(max_length=11)
	drilldowns = models.TextField()
	selects = models.TextField()
	wheres = models.TextField()
	group_bys = models.TextField()
	order_bys = models.TextField()
	limits = models.TextField()
	aliases = models.TextField(default='{}')
	drilldown_status = models.BooleanField(default=True)
	drilldown_options = models.TextField(default='')
	source_id = models.CharField(max_length=5, default='')
	allowed_user_groups = models.TextField(default='')
	allowed_role_groups = models.TextField(default='')
	allowed_individuals = models.TextField(default='')
	group_owner = models.ForeignKey(Group, on_delete=models.CASCADE)
	assigned_dashboards = models.TextField()

	class Meta:
		db_table = 'mm_charts'

class Tag(models.Model):
	tagname = models.CharField(max_length=20)
	time = models.CharField(max_length=11)
	created_by = models.CharField(max_length=20)

	class Meta:
		db_table = 'mm_tags'

class Mail(models.Model):
	userid = models.IntegerField()
	fromid = models.IntegerField()
	time = models.IntegerField()
	subject = models.TextField()
	message = models.TextField()

	class Meta:
		db_table = 'mm_user_mail'

class Notification(models.Model):
	userid = models.IntegerField()
	time = models.IntegerField()
	message = models.TextField()

	class Meta:
		db_table = 'mm_user_notifications'

class Task(models.Model):
	userid = models.IntegerField()
	time = models.IntegerField()
	subject = models.TextField()
	status = models.CharField(max_length=15)

	class Meta:
		db_table = 'mm_user_tasks'

class User_Chart(models.Model):
	chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.TextField()
	status = models.CharField(max_length=25)
	table_name = models.CharField(max_length=50, default='')
	query = models.TextField()
	attributes = models.TextField()
	time = models.TextField()
	chart_type = models.CharField(max_length=11)
	drilldowns = models.TextField()
	selects = models.TextField()
	wheres = models.TextField()
	group_bys = models.TextField()
	order_bys = models.TextField()
	limits = models.TextField()
	aliases = models.TextField(default='{}')
	drilldown_status = models.BooleanField(default=True)
	drilldown_options = models.TextField(default='')
	source_id = models.CharField(max_length=5, default='')
	allowed_user_groups = models.TextField(default='')
	allowed_role_groups = models.TextField(default='')
	allowed_individuals = models.TextField(default='')
	group_owner = models.ForeignKey(Group, on_delete=models.CASCADE)
	assigned_dashboards = models.TextField()

	class Meta:
		db_table = 'mm_user_charts'

class User_Dashboard(models.Model):
	dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.TextField()
	time = models.TextField()
	charts = models.TextField()
	filters = models.TextField()
	description = models.TextField()
	status = models.CharField(max_length=25)
	allowed_user_groups = models.TextField(default='')
	allowed_role_groups = models.TextField(default='')
	allowed_individuals = models.TextField(default='')
	order_id = models.IntegerField(default='0')
	group_owner = models.ForeignKey(Group, on_delete=models.CASCADE)

	class Meta:
		db_table = 'mm_user_dashboards'
		permissions = [
			("accounting_access", "Can access Accounting section"),
			("advertising_access", "Can access Advertising section"),
			("bi_access", "Can access Business Intelligence section"),
			("circulation_access", "Can access Circulation section"),
			("editorial_access", "Can access Editorial section"),
			("production_access", "Can access Production section")
		]
class Source(models.Model):
	engine = models.TextField()
	name = models.TextField()
	user = models.TextField()
	password = models.TextField()
	host = models.TextField()
	port = models.CharField(max_length=15)
	class Meta:
		db_table = 'mm_source'

class Source_Group(models.Model):
	source = models.ForeignKey(Source, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

	class Meta:
		db_table = 'mm_source_group'

class Role(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	name = models.TextField()
	class Meta:
		db_table = 'mm_role'

class User_Roles(models.Model):
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	class Meta:
		db_table = 'mm_user_roles'