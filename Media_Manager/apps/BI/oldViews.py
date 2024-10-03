"""
<!-- 
	To do:
		- Change so each page is a folder
		- Add 404
		- Quick access dashboards?
		- Change icon from pie chart to stat
		- Middle nav
			
	References:
		- https://partofthething.com/thoughts/authenticating-and-populating-users-in-django-using-a-windows-active-directory-and-sasl/
		- https://www.layoutit.com/build
		- https://d3js.org/
		- https://colorlib.com/wp/free-bootstrap-admin-dashboard-templates/
		- https://github.com/ColorlibHQ/AdminLTE
		- https://adminlte.io/themes/AdminLTE/index2.html#
		- http://192.241.131.173:8000/#
		- http://d3pie.org/#docs
		- https://github.com/d3/d3/wiki/Gallery
 -->
"""


'''
	- dropboxes look
	- dropboxes disabled when button not active
	- update centered
	- background grayed when button not active
	- set height/width, with scroll 


	- sort tables columns
	- multiple selects with ctrl
	- collapse filter section

	- breadcrumbs && filter/select breadcrumb

'''
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth import authenticate, login, logout

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

from .models import Chart
from .models import Chart_Group
from .models import Dashboard
from .models import Dashboard_Group
from .models import User_Chart
from .models import User_Dashboard

from ... import views

from .forms import DashboardPropertiesForm
from .forms import ChartPropertiesForm

#from markdownx.models import MarkdownxFields

#from django.http import JsonResponse
from django.http import HttpResponse
import json
from collections import OrderedDict 

import logging


url = "192.241.131.173:8000"
login_redirect = "/login/?next="

def ajax_dashboard(request):
	cache = False

	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	chart_id = request.POST.get("chart_id", -1)
	dashboard_id = request.POST.get("dashboard_id", -1)
	new_field_id = request.POST.get("new_field_id", -1)
	old_field = request.POST.get("old_field", -1)
	old_field_value = request.POST.get("old_field_value", -1)
	select_position = request.POST.get("select_position", -1)

	drilldown_breadcrumb = request.POST.get("drilldown_breadcrumb", -1)

	response_data = {}

	if chart_id is None or chart_id == -1:
		return HttpResponse(json.dumps({"access": "allow", "message": "No chart id supplied!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

	try:
		usergroups = []
		for group in request.user.groups.all():
			usergroups.append(group.id)

		dashboard_access_check = Dashboard.objects.filter(id=dashboard_id, dashboard_group__usergroup_id__in=usergroups)
	
		chart_access_check = Chart.objects.filter(id=chart_id, chart_group__usergroup_id__in=usergroups)

		if len(chart_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No chart found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		if len(dashboard_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")


		dashboard = User_Dashboard.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id)
		if not dashboard:
			dashboard = Dashboard.objects.filter(id=dashboard_id, dashboard_group__usergroup_id__in=usergroups)
			
		if drilldown_breadcrumb != -1:
			if not remove_drilldowns(chart_access_check[0].id, request.user.id, drilldown_breadcrumb):
				return HttpResponse(json.dumps({"access": "allow", "message": "Error while changing drilldown!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		if new_field_id != -1 and old_field != -1 and old_field_value != -1 and select_position != -1:
			if not add_drilldowns(chart_access_check[0].id, request.user.id, json.loads(chart_access_check[0].drilldown_options, object_pairs_hook=OrderedDict), new_field_id, old_field, old_field_value, select_position):
				return HttpResponse(json.dumps({"access": "allow", "message": "Error while drilling down!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		chart = User_Chart.objects.filter(chart_id=chart_access_check[0].id, user_id=request.user.id)
		if not chart:
			chart = Chart.objects.filter(id=chart_id, chart_group__usergroup_id__in=usergroups)

		if cache:
			midtc_conn = connections["default"]
		else:
			midtc_conn = connections["midtc"]

		if chart[0].query == "":
			return HttpResponse(json.dumps({"access": "allow", "message": "No frontend query supplied!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		#response_data = {"access": "allow", "data": replace_reg(chart[0].query, json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict),json.loads(chart[0].wheres, object_pairs_hook=OrderedDict)), "message": "false", "title": chart[0].title, "chart_type": chart[0].chart_type, "headers": ""}
		
		try:
			with midtc_conn.cursor() as cursor:
				query, values = replace_reg(chart[0].query, 
					json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].selects, object_pairs_hook=OrderedDict), 
					select_position,json.loads(chart[0].wheres, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].group_bys, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].order_bys, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].drilldown_options, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)
				)

				if cache:
					query = query.replace('amp_raw.','')

				if len(values) > 0:
					#print(query)
					#print(values)
					cursor.execute(query, values)
				else:
					#print("===============")
					#print(query)
					#print("===============")
					cursor.execute(query)
				#print(vars(chart[1]))
				response_data = {"access": "allow", "data": cursor.fetchall(), "attributes": chart[0].attributes, "message": "false", "chart_id": chart[0].id, "title": chart[0].title, "chart_type": chart[0].chart_type, "drilldowns": json.loads(chart[0].drilldown_options, object_pairs_hook=OrderedDict), "headers": cursor.description, "drilldown_breadcrumb":get_breadcrumb(json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)), "query":query}
		#except ProgrammingError:
		#	response_data["message"] = query
		except OperationalError as e:
			response_data["message"] = query
			response_data["message"] = "Error connecting to database!"

	except Chart.DoesNotExist:
		response_data["message"] = "No such chart exists!"

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def remove_drilldowns(chart_id, user_id, drilldown_breadcrumb):
	if drilldown_breadcrumb != -1:

		if drilldown_breadcrumb == 'clear':
			drilldowns = OrderedDict()
		else:
			drilldown_level = -1
			chart = User_Chart.objects.filter(chart_id=chart_id, user_id=user_id)
			drilldowns = json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)
			if not chart:
				return False

			if drilldowns:
				for drilldown_key, drilldown_values in drilldowns.items():
					if 'value' in drilldown_values.keys() and drilldown_values['value'] == drilldown_breadcrumb and 'level' in drilldown_values.keys():
						drilldown_level = drilldown_values['level']

				copy = drilldowns.copy()

				for drilldown_key2, drilldown_values2 in drilldowns.items():
					if drilldown_level != -1:
						if drilldown_values2['level'] > drilldown_level:
							del copy[drilldown_key2]
						elif drilldown_values2['level'] == drilldown_level:
							copy['current'] = drilldown_values2
							del copy[drilldown_key2]

				drilldowns = copy

			else:
				drilldowns = OrderedDict()

		User_Chart.objects.filter(user_id=user_id, chart_id=chart_id).update(drilldowns=json.dumps(drilldowns))

		return True

	return False

	# Convert from json to OrderedDict
	drilldowns = json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)

def add_drilldowns(chart_id, user_id, drilldown_options, new_field_id, old_field, old_field_value, select_position):
	chart = User_Chart.objects.filter(chart_id=chart_id, user_id=user_id)
	if not chart:
		default_chart = Chart.objects.filter(id=chart_id)
		if not default_chart:
			return False
		User_Chart.objects.create(chart_id=default_chart[0].id, user_id=user_id, title=default_chart[0].title, query=default_chart[0].query, attributes=default_chart[0].attributes, time=default_chart[0].time, chart_type=default_chart[0].chart_type, drilldowns=default_chart[0].drilldowns, selects=default_chart[0].selects, wheres=default_chart[0].wheres, group_bys=default_chart[0].group_bys, order_bys=default_chart[0].order_bys, limits=default_chart[0].limits)
		chart = User_Chart.objects.filter(chart_id=chart_id, user_id=user_id)


	# Convert from json to OrderedDict
	drilldowns = json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)

	# List of drilldown options
	drilldown_list = {}
	for drill_key, drill_array in drilldown_options.items():
		for drill_key, drill in drill_array.items():
			drilldown_list.update({drill_key:drill})

	if new_field_id in drilldown_list.keys() and old_field in drilldown_list.values():
		if drilldowns:
			# Set the current drilldown level to the last
			drilldown_lowest_position = -1
			for drilldown_key, drilldown_values in drilldowns.items():
				if drilldown_key != 'default' and drilldown_key != 'current':
					if int(drilldown_values['level']) > int(drilldown_lowest_position):
						drilldown_lowest_position = int(drilldown_values['level'])
			if drilldown_lowest_position != -1:
				drilldown_lowest_position += 1
				dkey = 'level' + str(drilldown_lowest_position)
			else:
				dkey = 'level1'
				drilldown_lowest_position = 1

			drilldowns[dkey] = OrderedDict()
			drilldowns[dkey]['name'] = old_field
			drilldowns[dkey]['level'] = str(drilldown_lowest_position) 
			drilldowns[dkey]['field'] = old_field
			drilldowns[dkey]['value'] = old_field_value

			drilldowns['current']['name'] = drilldown_list.get(new_field_id, -1)
			drilldowns['current']['level'] = str(drilldown_lowest_position + 1) 
			drilldowns['current']['field'] = drilldown_list.get(new_field_id, -1)
			# Update the current drilldown to the one being input
		else:
			# Insert json drilldown
			drilldowns = OrderedDict()
			drilldowns['default'] = OrderedDict()
			drilldowns['default']['field'] = old_field
			drilldowns['default']['value'] = old_field_value
			drilldowns['default']['position'] = select_position
			drilldowns['default']['level'] = '0'
			drilldowns['current'] = OrderedDict()
			drilldowns['current']['name'] = drilldown_list.get(new_field_id, -1)
			drilldowns['current']['level'] = '1'
			drilldowns['current']['field'] = drilldown_list.get(new_field_id, -1)

		# Update database with new drilldowns
		User_Chart.objects.filter(user_id=user_id, chart_id=chart_id).update(drilldowns=json.dumps(drilldowns))

		return True
	else:
		return False

def get_breadcrumb(drilldowns):
	if drilldowns:
		results = '<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item active" aria-current="page"><a href="#" class="drilldown_breadcrumb" value="clear">Clear</a></li>'

		for drilldown_key, drilldown_values in drilldowns.items():
			if drilldown_key != 'current':
				results += '<li class="breadcrumb-item active" aria-current="page"><a href="#" class="drilldown_breadcrumb" value="' + drilldown_values['value'] + '">' + drilldown_values['field'] + ' (' + drilldown_values['value'] + ')</a/></li>'

		if 'current' in drilldowns.keys():
			results += '<li class="breadcrumb-item" aria-current="page">' + drilldowns['current']['field'] + '</li>'

		results += '</ol></nav>'

		return results

	else:
		return ''


def replace_reg(query, filters, selects, position, wheres, group_bys, order_bys, drilldowns_options, drilldowns):
	values = []
	new_query = query
		
	if drilldowns:
		new_query = new_query.replace('%', '%%')

	if drilldowns:
		drilldown_term = ''
		drilldown_where = ''
		drilldown_position = -1
		drilldown_values = []
		for drilldown_key, drilldown_value in drilldowns.items():
			if drilldown_key == 'current':
				drilldown_term = drilldown_value['field']
				drilldown_level = drilldown_value['level']

			elif drilldown_key == 'default':
				drilldown_position = drilldown_value['position']

			if drilldown_key != 'current':
				drilldown_where += drilldown_value['field'] + '=%s AND '
				drilldown_values.append(drilldown_value['value'])

	for select_group_key, select_group in selects.items():
		count = 0
		select_line = ''
		for select_key, select in select_group.items():	
			#if new_field_id != -1 and old_field != -1 and old_field_value != -1 and int(position) == int(count) and position != -1 and old_field in drilldown_list.values(): #~!@
			
			if select['prefix'] != '':
				select_line += select['prefix'] + '.'

			if drilldowns and drilldown_term != '' and drilldown_position != '-1' and int(drilldown_position) == int(count):
				select_line += drilldown_term + ','
			else:
				select_line += select['value'] + ','

			count += 1

		if select_line != '':
			new_query = new_query.replace('$' + select_group_key, select_line[:-1])
			
	for where_group_key, where_group in wheres.items():
		line = ''

		for where_key, where in where_group.items():
			if where != "false" and where_key != "hardcodes" and filters['layout'][where['value_id']]['status'] == 'on':
				if line == '':
					line += 'WHERE '
				
				line += where['field'] + ' ' + where['operator_start']
				
				for option_key, option in filters['layout'][where['value_id']]['options'].items():
					if option['checked'] == "true":
						if where['type'] == "string":
							line += '"'

						line += option['title']

						if where['modifier'] != "false":
							line += where['modifier']

						if where['type'] == "string":
							line += '"'
						line += ','

				if line.endswith(','):
					line = line[:-1] 

				line += where['operator_end'] + ' AND '

		#if new_field_id != -1 and old_field != -1 and old_field_value != -1 and old_field in drilldown_list.values(): #~!@
		if drilldowns and drilldown_where != '':
			line += drilldown_where
			values.extend(drilldown_values)


		if where_group['hardcodes'] != 'false':
			for hardcode_key, hardcode in where_group['hardcodes'].items():
				if line == '':
					line = 'WHERE '
				line += hardcode['value'] + ' AND '

		if line.endswith(' AND '):
			line = line[:-5]

		if line != '':
			new_query = new_query.replace('$' + where_group_key, line)
	
	for parent_group_key, parent_group in group_bys.items():
		for group_key, group in parent_group.items():
			group_line = ''
		
			#if new_field_id != -1 and old_field != -1 and old_field_value != -1 and old_field in drilldown_list.values(): #~!@
			if group['prefix'] != '':
				group_line += group['prefix'] + '.'

			if drilldowns and drilldown_term != '':
				group_line += drilldown_term
			else:
				group_line += group['value']

			if group_line != '':
				new_query = new_query.replace('$' + group_key, group_line)

	
	for parent_order_key, order_group in order_bys.items():
		for order_key, order in order_group.items():
			order_line = ''

			if 'prefix' in order.keys() and order['prefix'] != '':
				order_line += order['prefix'] + '.'

			if 'value' in order.keys() and order['value'] != '':
				order_line += order['value']
			elif 'field' in order.keys() and order['field'] != '':
				order_line += '"' + order['value'] + '"'

			if 'order' in order.keys() and order['order'] != '':
				order_line += ' ' + order['order']

			if order_line != '':
				new_query = new_query.replace('$' + order_key, order_line)

	
	
	new_query += ' LIMIT 15'
	
	return new_query, values

def bi_view(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	usergroups = []
	for group in request.user.groups.all():
		usergroups.append(group.id)

	#if request.POST.get('id', '') == '':
	dashboard = Dashboard.objects.filter(dashboard_group__usergroup_id__in=usergroups).order_by('id')[:10].values()

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "dashboards": dashboard, "menu": views.get_sidebar(request)}
	return render(request, "bi.html", context)

def view_dashboard_view(request, id=0):
	#update_cache()

	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi/viewdashboard")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	if id == 0 or id == '':
		return render(request, "viewdashboard.html", {"message":"No dashboard specified!", "menu": views.get_sidebar(request)})

	usergroups = []
	for group in request.user.groups.all():
		usergroups.append(group.id)

	dashboard_access_check = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)

	if len(dashboard_access_check) < 1:
		return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

	usergroups = []
	for group in request.user.groups.all():
		usergroups.append(group.id)

	if 'update' in request.POST:
		update = request.POST.get('update', -1)
		if update != -1:
			dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)

			if not dashboard:
				default_dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)
				User_Dashboard.objects.create(dashboard_id=id,user_id=request.user.id, name=default_dashboard[0].name, time=default_dashboard[0].time, charts=default_dashboard[0].charts, filters=default_dashboard[0].filters, description=default_dashboard[0].description, status=default_dashboard[0].status)
				dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)

			filters = json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict)
			if update != 'Update All':
				for option_key, option in filters['layout'][update]['options'].items():
					value = request.POST.getlist('values[' + update + ']', -1)
					if value != -1 and option['title'] in value:
						option['checked'] = "true"
					else:
						option['checked'] = "false"
			else:
				for filter_key, filter_value in filters['layout'].items():
					for option_key, option in filter_value['options'].items():
						value = request.POST.getlist('values[' + filter_key + ']', -1)
						if value != -1 and option['title'] in value:
							option['checked'] = "true"
						else:
							option['checked'] = "false"

			User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id).update(filters=json.dumps(filters))

	dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)
	if not dashboard:
		dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups).annotate(dashboard_id=F('id'))	

	#dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)

	if len(dashboard) > 0:
		context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "dashboard": dashboard[0], "charts":json.loads(dashboard[0].charts, object_pairs_hook=OrderedDict), "filters":json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict), "menu": views.get_sidebar(request)}
	else:
		context = {"access": "allow", "message": "No such dashboard exists!", "menu": views.get_sidebar(request)}

	return render(request, "viewdashboard.html", context)

def update_cache():
	default_conn = connections["default"]
	midtc_conn = connections["midtc"]

	try:
		with default_conn.cursor() as cursor0:
			with midtc_conn.cursor() as cursor1:
				'''
				cursor1.execute('SHOW CREATE TABLE amp_raw.champ_new_inserted_amp_data_pull')
				create_table = cursor1.fetchone()[1]
				cursor0.execute('DROP TABLE IF EXISTS champ_new_inserted_amp_data_pull')
				cursor0.execute(create_table)
				'''

				batch = 500
				current = 0

				cursor1.execute('SELECT * FROM amp_raw.champ_new_inserted_amp_data_pull WHERE period_year IN ("2020", "2019", "2018") AND period_month IN ("P01")') #' AND Row_ID = "567741"')
				results1 = cursor1.fetchall()
				query = 'INSERT INTO champ_new_inserted_amp_data_pull VALUES '
				for row1 in results1:
					query += '('
					for values in row1:
						query += '"' + str(values).replace('\"', '\\"') + '",'

					query = query[0:-1] + '),'
					current += 1

					if current > batch:
						cursor0.execute(query[0:-1])
						current = 0
						query = 'INSERT INTO champ_new_inserted_amp_data_pull VALUES '

				if current is not 0:
					cursor0.execute(query[0:-1])
				

	except Exception as e:
		print(e)

def dashboard(request, id=0):
	#send_mail('', 'test', '', ['9194826920@verizon.net'])
	
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi")
	
	# Check if user has access to the BI
	if not request.user.has_perm('BI.bi_access'):
		return render(request, "chart.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	charts = ''

	# Insert new dashboard if submitted
	if request.method == 'POST':
		if request.POST.get('submit', 'else') == 'dashboardProperties':
			form = DashboardPropertiesForm(request.POST)
			if form.is_valid():
				if id == 0 or id == '' or id == None:
					d = Dashboard.objects.create(name=form.cleaned_data['dashboardName'],time='1',charts='{}',filters='{}',description=form.cleaned_data['dashboardDescription'],status=form.cleaned_data['dashboardStatus'])
					d.save()
					id = d.id

					for group in request.user.groups.all():
						g = Dashboard_Group.objects.create(dashboard=d, usergroup_id=group.id)
						g.save()

					return redirect('/bi/dashboard/' + str(id) + '/')
				else:
					Dashboard.objects.filter(id=id).update(name=form.cleaned_data['dashboardName'], description=form.cleaned_data['dashboardDescription'], status=form.cleaned_data['dashboardStatus'])
		#elif request.POST.get('submit', 'else') == 'dashboardProperties':

	# Check whether to create or edit dashboard
	if id == 0 or id == '' or id == None:
		id = -1

		# User doesn't have appropriate permissions to add dashboard
		if not request.user.has_perm('BI.can_add_dash'):
			return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

		dashboard = None
	else:
		# Get required usergroups for this dashboard
		usergroups = []
		for group in request.user.groups.all():
			usergroups.append(group.id)
		
		 # Check if user has access to see chart
		dashboard_access_check = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)
		if len(dashboard_access_check) < 1:
			return render(request, "bi.html", {"access": "deny", "message": "No dashboard exists with that id!", "menu": views.get_sidebar(request)})
		
		# User doesn't have appropriate permissions to edit chart
		if not request.user.has_perm('BI.can_change_dash'):
			return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

		dashboard = Dashboard.objects.filter(id=id)
		dashboard = dashboard[0]

		if 'layout' in str(dashboard.charts):
			dashboard.charts = dashboard.charts.replace('row', '').replace('cell', '')

			dashboard_charts = json.loads(dashboard.charts, object_pairs_hook=OrderedDict)
			chart_names = {}
			ids_list = []
			for row, cell in dashboard_charts['layout'].items():
				for cell_id, cell_attributes in cell.items():
					ids_list.append(cell_attributes['id'])

			charts_data = Chart.objects.filter(id__in=ids_list)
			for row in charts_data:
				chart_names[str(row.id)] = row.title

			previous_id = ''
			for row2, cell2 in dashboard_charts['layout'].items():
				for cell_id2, cell_attributes2 in  cell2.items():
					charts += '<div class="grid-stack-item" data-gs-x="' + str(cell_id2) + '" data-gs-y="' 
					if previous_id == str(row2):
						str(int(row2) + int(cell_attributes2['width']))
					else:
						charts += str(row2)
					charts += '" data-gs-width="' + str(cell_attributes2['width']) + '" data-gs-height="1">'
					charts += '<div class="grid-stack-item-content" id="' + str(cell_attributes2['id']) + '">' + str(chart_names[cell_attributes2['id']]) + '</div>'
					charts += '</div>'
					previous_id = str(row2)
		else:
			charts = '<div class="grid-stack-item" data-gs-x="0" data-gs-y="0" data-gs-width="6" data-gs-height="1"></div>'

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "menu": views.get_sidebar(request), "dashboard": dashboard, "id": str(id), "charts": charts}
	return render(request, "dashboard.html", context)

def chart(request, id=0):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi")

	# Check if user has access to the BI
	if not request.user.has_perm('BI.bi_access'):
		return render(request, "chart.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	# Insert new chart if submitted
	if request.method == 'POST':
		if request.POST.get('submit', 'else') == 'chartProperties':
			form = ChartPropertiesForm(request.POST)
			if form.is_valid():
				if id == 0 or id == '' or id == None:
					c = Chart.objects.create(title=form.cleaned_data['chartName'], query='', attributes='{}', time='1', chart_type=form.cleaned_data['chartType'], drilldowns='{}', selects='{}', wheres='{}', group_bys='{}', order_bys='{}', limits='{}')
					c.save()
					id = c.id

					for group in request.user.groups.all():
						g = Chart_Group.objects.create(chart=c, usergroup_id=group.id)
						g.save()

					return redirect('/bi/chart/' + str(id) + '/')
				else:
					Chart.objects.filter(id=id).update(title=form.cleaned_data['chartName'], chart_type=form.cleaned_data['chartType'])
		#elif request.POST.get('submit', 'else') == 'dashboardProperties':

	# Check whether to create or edit chart
	if id == 0 or id == '' or id == None:
		id = -1

		# User doesn't have appropriate permissions to add chart
		if not request.user.has_perm('BI.can_add_chart'):
			return render(request, "chart.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

		chart = None
	else:
		# Get required usergroups for this chart
		usergroups = []
		for group in request.user.groups.all():
			usergroups.append(group.id)

		 # Check if user has access to see chart
		chart_access_check = Chart.objects.filter(id=id, chart_group__usergroup_id__in=usergroups)
		if len(chart_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")
		
		# User doesn't have appropriate permissions to edit chart
		if not request.user.has_perm('BI.can_add_chart'):
			return render(request, "chart.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

		chart = Chart.objects.filter(id=id)
		chart = chart[0]

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "chart": chart, "id": str(id), "menu": views.get_sidebar(request)}
	return render(request, "chart.html", context)

"""
def error_404_view(request, exception):
	data = {"name": ""}
	return render(request, 'admin/error_404.html', data)
"""