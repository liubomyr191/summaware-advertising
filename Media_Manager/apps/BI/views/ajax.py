from django.shortcuts import render, redirect
#from cryptography.fernet import Fernet
import base64
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth import authenticate, login, logout

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

from ..models import Chart
from ..models import Dashboard
from ..models import User_Chart
from ..models import User_Dashboard
from ..models import Source

from ...Home.models import Org_Meta
from ...Home.models import User_Logs
from ...Home.models import Error_Logs

from ..models import Role
from ..models import User_Roles

from .... import views

from django.http import HttpResponse
import json, csv
from collections import OrderedDict 
from django.core.mail import send_mail

import logging


url = "192.241.131.173:8000"
login_redirect = "/login/?next="

key = b'bDCiiSwQiPw5M7qVJ2vbsEoZYht3q-suI5JrXaTbnco='

def ajax_dashboard(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	user_dash = 'null'
	user_chart = 'null'

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
		user_groups_query = []
		user_groups_string = ''
		for group in request.user.groups.all():
			usergroups.append(group.id)
			user_groups_string += 'FIND_IN_SET(' + str(group.id) + ', allowed_user_groups) OR '

		user_roles = User_Roles.objects.filter(user_id=request.user.id)
		for role in user_roles.values():
			user_groups_string += 'FIND_IN_SET(' + str(role['role_id']) + ', allowed_role_groups) OR '
		user_groups_string += 'FIND_IN_SET(' + str(request.user.id) + ', allowed_individuals) OR '
		user_groups_query = [user_groups_string[:-4]]

		#dashboard_access_check = Dashboard.objects.filter(id=dashboard_id, dashboard_group__usergroup_id__in=usergroups)
		dashboard_access_check = Dashboard.objects.filter(id=dashboard_id).extra(where=user_groups_query)

	
		#chart_access_check = Chart.objects.filter(id=chart_id, chart_group__usergroup_id__in=usergroups)
		chart_access_check = Chart.objects.filter(id=chart_id).extra(where=user_groups_query)

		if len(chart_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No chart found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		if len(dashboard_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")


		dashboard = User_Dashboard.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id)
		if not dashboard:
			#dashboard = Dashboard.objects.filter(id=dashboard_id, dashboard_group__usergroup_id__in=usergroups)
			dashboard = Dashboard.objects.filter(id=dashboard_id).extra(where=user_groups_query)
		else:
			user_dash = dashboard_id

		if drilldown_breadcrumb != -1:
			dd_response, dd_status = remove_drilldowns(chart_access_check[0].id, request.user.id, drilldown_breadcrumb)
			if not dd_status:
				Error_Logs.objects.create(dashboard_id=dashboard_id, chart_id=chart_id, user_dashboard_id=user_dash, user_chart_id=user_chart, error='cannot drill down lower', query=dd_response, user=request.user, dashboard_name=dashboard[0].name, dashboard_charts=dashboard[0].charts, dashboard_filters=dashboard[0].filters, chart_title=chart_access_check[0].title, chart_table_name=chart_access_check[0].table_name, chart_query=chart_access_check[0].query, chart_attributes=chart_access_check[0].attributes, chart_chart_type=chart_access_check[0].chart_type, chart_drilldowns=chart_access_check[0].drilldowns, chart_selects=chart_access_check[0].selects, chart_wheres=chart_access_check[0].wheres, chart_group_bys=chart_access_check[0].group_bys, chart_order_bys=chart_access_check[0].order_bys, chart_limits=chart_access_check[0].limits)
				return HttpResponse(json.dumps({"access": "allow", "message": "Error while changing drilldown!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		if new_field_id != -1 and old_field != -1 and old_field_value != -1 and select_position != -1:
			dd2_response, dd2_status = add_drilldowns(chart_access_check[0].id, request.user.id, json.loads(chart_access_check[0].drilldown_options, object_pairs_hook=OrderedDict), new_field_id, old_field, old_field_value, select_position)
			if not dd2_status:
				Error_Logs.objects.create(dashboard_id=dashboard_id, chart_id=chart_id, user_dashboard_id=user_dash, user_chart_id=user_chart, error='error adding drilldown', query=dd2_response, user=request.user, dashboard_name=dashboard[0].name, dashboard_charts=dashboard[0].charts, dashboard_filters=dashboard[0].filters, chart_title=chart_access_check[0].title, chart_table_name=chart_access_check[0].table_name, chart_query=chart_access_check[0].query, chart_attributes=chart_access_check[0].attributes, chart_chart_type=chart_access_check[0].chart_type, chart_drilldowns=chart_access_check[0].drilldowns, chart_selects=chart_access_check[0].selects, chart_wheres=chart_access_check[0].wheres, chart_group_bys=chart_access_check[0].group_bys, chart_order_bys=chart_access_check[0].order_bys, chart_limits=chart_access_check[0].limits)
				return HttpResponse(json.dumps({"access": "allow", "message": "Error while drilling down!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		chart = User_Chart.objects.filter(chart_id=chart_access_check[0].id, user_id=request.user.id)
		if not chart:
			#chart = Chart.objects.filter(id=chart_id, chart_group__usergroup_id__in=usergroups)
			chart = Chart.objects.filter(id=chart_id).extra(where=user_groups_query)
			chart_id = chart[0].id
		else:
			chart_id = chart[0].chart_id
			user_chart = chart[0].chart_id

		cache = False
		cache_check = Org_Meta.objects.filter(meta_key= 'cache_enabled')
		if cache_check.count() > 0 and cache_check[0].meta_value == 'true':
			filters = json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict)
			if filters['layout']['filter0']['status'] == 'on':
				if filters['layout']['filter0']['options']:
					for option_key, option_value in filters['layout']['filter0']['options'].items():
						if option_value['title'] in ['2021', '2020', '2019']:
							if option_value['checked'] == 'true':
								cache = True
						else:
							if option_value['checked'] == 'true':
								cache = False

		if cache:
			midtc_conn = connections["default"]
		else:
			#midtc_conn = connections["midtc"]
			
			source = Source.objects.filter(id=chart[0].source_id)
			if chart[0].source_id == '2':
				midtc_conn = connections["default"]
			else:
				if chart[0].source_id not in connections:
					source = source[0]
					newDB = {}
					newDB['ENGINE'] = source.engine
					newDB['NAME'] = source.name #decrypt(source.name)
					newDB['USER'] = source.user #decrypt(source.user)
					newDB['PASSWORD'] = source.password #decrypt(source.password)
					newDB['HOST'] = source.host #decrypt(source.host)
					newDB['PORT'] = source.port
					connections.databases[chart[0].source_id] = newDB

					#if newDB['NAME'] is None or newDB['USER'] is None or newDB['PASSWORD'] is None or newDB['HOST'] is None:
					#return HttpResponse(json.dumps({"access": "allow", "message": "Error getting source for chart!", "newDB": newDB, "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

				midtc_conn = connections[chart[0].source_id]
			

		if chart[0].query == "":
			return HttpResponse(json.dumps({"access": "allow", "message": "No frontend query supplied!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

		#response_data = {"access": "allow", "data": replace_reg(chart[0].query, json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict),json.loads(chart[0].wheres, object_pairs_hook=OrderedDict), request.user), "message": "false", "title": chart[0].title, "chart_type": chart[0].chart_type, "headers": ""}
		
		try:
			with midtc_conn.cursor() as cursor:
				query, values = replace_reg(chart[0].query, 
					json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].selects, object_pairs_hook=OrderedDict), 
					select_position,json.loads(chart[0].wheres, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].group_bys, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].order_bys, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].limits, object_pairs_hook=OrderedDict),
					json.loads(chart[0].drilldown_options, object_pairs_hook=OrderedDict), 
					json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict),
					request.user
				)

				if cache:
					query = query.replace('amp_raw.','')

				if len(values) > 0:
					#print(query)
					#print(values)
					#response_data["query"] = query
					response_data["values"] = values
					cursor.execute(query, values)
				else:
					#print("===============")
					#print(query)
					#print("===============")
					query = query.replace('%%', '%')
					cursor.execute(query)
				#print(vars(chart[1]))

				order_by_info = json.loads(chart[0].order_bys, object_pairs_hook=OrderedDict)
				#aliases = json.loads(chart[0].aliases, object_pairs_hook=OrderedDict)
				
				#if 'groups' in order_by_info and 'order_group0' in order_by_info['groups'] and 'value' in order_by_info['groups']['order_group0']:
				#	if order_by_info['groups']['order_group0']['value'] in aliases:
				#		sort = aliases[str(order_by_info['groups']['order_group0']['value'])]
				#	else:
				#		sort = ''
				#else:
				#	sort = ''
				
				if 'groups' in order_by_info and 'order_group0' in order_by_info['groups'] and 'order' in order_by_info['groups']['order_group0']:
					order = order_by_info['groups']['order_group0']['order']
				else:
					order = 'asc'
					
				if 'groups' in order_by_info and 'order_group0' in order_by_info['groups'] and 'sort' in order_by_info['groups']['order_group0']:
					sort = order_by_info['groups']['order_group0']['sort']
				else:
					sort = ''

				response_data = {"cache":cache, "access": "allow", "data": cursor.fetchall(), "attributes": chart[0].attributes, "message": "false", "chart_id": chart_id, "title": chart[0].title, "chart_type": chart[0].chart_type, "drilldowns": json.loads(chart[0].drilldown_options, object_pairs_hook=OrderedDict), "headers": cursor.description, "drilldown_breadcrumb":get_breadcrumb(json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)), "sort": sort, "order": order}
				#response_data['query'] = query
		except ProgrammingError as e:
			Error_Logs.objects.create(dashboard_id=dashboard_id, chart_id=chart_id, user_dashboard_id=user_dash, user_chart_id=user_chart, error='ProgrammingError: ' + str(e), query=query, user=request.user, dashboard_name=dashboard[0].name, dashboard_charts=dashboard[0].charts, dashboard_filters=dashboard[0].filters, chart_title=chart[0].title, chart_table_name=chart[0].table_name, chart_query=chart[0].query, chart_attributes=chart[0].attributes, chart_chart_type=chart[0].chart_type, chart_drilldowns=chart[0].drilldowns, chart_selects=chart[0].selects, chart_wheres=chart[0].wheres, chart_group_bys=chart[0].group_bys, chart_order_bys=chart[0].order_bys, chart_limits=chart[0].limits)
			response_data["message"] = "Error querying chart. If you just added a filter, try setting one of the filter options. Otherwise try resetting the chart to default (using the gear on the chart). If all else fails file a ticket."
			response_data["drilldown_breadcrumb"] = get_breadcrumb(json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict))
			#response_data['query'] = query
		except OperationalError as e:
			Error_Logs.objects.create(dashboard_id=dashboard_id, chart_id=chart_id, user_dashboard_id=user_dash, user_chart_id=user_chart, error='OperationalError: ' + str(e), query=query, user=request.user, dashboard_name=dashboard[0].name, dashboard_charts=dashboard[0].charts, dashboard_filters=dashboard[0].filters, chart_title=chart[0].title, chart_table_name=chart[0].table_name, chart_query=chart[0].query, chart_attributes=chart[0].attributes, chart_chart_type=chart[0].chart_type, chart_drilldowns=chart[0].drilldowns, chart_selects=chart[0].selects, chart_wheres=chart[0].wheres, chart_group_bys=chart[0].group_bys, chart_order_bys=chart[0].order_bys, chart_limits=chart[0].limits)
			response_data["message"] = "Error querying chart. If you just added a filter, try setting one of the filter options. Otherwise try resetting the chart to default (using the gear on the chart). If all else fails file a ticket."#query
			response_data["drilldown_breadcrumb"] = get_breadcrumb(json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict))
			#response_data['query'] = query
		#except ValueError as e2:
		#	print('asdf')

	except Chart.DoesNotExist:
		response_data["message"] = "No such chart exists!"

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def export(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	cache = False
	dashboard_id = request.GET.get('dashboard_id', -1)
	chart_id = request.GET.get('chart_id', -1)

	if dashboard_id != -1 and chart_id != -1:
		try:
			usergroups = []
			user_groups_query = []
			user_groups_string = ''
			for group in request.user.groups.all():
				usergroups.append(group.id)
				user_groups_string += 'FIND_IN_SET(' + str(group.id) + ', allowed_user_groups) OR '

			user_roles = User_Roles.objects.filter(user_id=request.user.id)
			for role in user_roles.values():
				user_groups_string += 'FIND_IN_SET(' + str(role['role_id']) + ', allowed_role_groups) OR '
			user_groups_string += 'FIND_IN_SET(' + str(request.user.id) + ', allowed_individuals) OR '
			user_groups_query = [user_groups_string[:-4]]

			dashboard_access_check = Dashboard.objects.filter(id=dashboard_id).extra(where=user_groups_query)
			chart_access_check = Chart.objects.filter(id=chart_id).extra(where=user_groups_query)

			if len(chart_access_check) < 1:
				return HttpResponse(json.dumps({"access": "allow", "message": "No chart found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")

			if len(dashboard_access_check) < 1:
				return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")


			# Create the HttpResponse object with the appropriate CSV header.
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="export.csv"'

			chart = User_Chart.objects.filter(chart_id=int(chart_id), user_id=int(request.user.id)).extra(where=user_groups_query)

			if not chart:
				chart = Chart.objects.filter(id=int(chart_id)).extra(where=user_groups_query)

			dashboard = User_Dashboard.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id)
			if not dashboard:
				dashboard = Dashboard.objects.filter(id=dashboard_id).extra(where=user_groups_query)

			if cache:
				midtc_conn = connections["default"]
			else:
				#midtc_conn = connections["midtc"]
				
				source = Source.objects.filter(id=chart[0].source_id)
				if chart[0].source_id not in connections:
					source = source[0]
					newDB = {}
					newDB['ENGINE'] = source.engine
					newDB['NAME'] = source.name #decrypt(source.name)
					newDB['USER'] = source.user #decrypt(source.user)
					newDB['PASSWORD'] = source.password #decrypt(source.password)
					newDB['HOST'] = source.host #decrypt(source.host)
					newDB['PORT'] = source.port
					connections.databases[chart[0].source_id] = newDB
				midtc_conn = connections[chart[0].source_id]

			try:
				with midtc_conn.cursor() as cursor:
					query, values = replace_reg(chart[0].query, 
						json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict), 
						json.loads(chart[0].selects, object_pairs_hook=OrderedDict), 
						-1,
						json.loads(chart[0].wheres, object_pairs_hook=OrderedDict), 
						json.loads(chart[0].group_bys, object_pairs_hook=OrderedDict), 
						json.loads(chart[0].order_bys, object_pairs_hook=OrderedDict), 
						json.loads(chart[0].limits, object_pairs_hook=OrderedDict),
						json.loads(chart[0].drilldown_options, object_pairs_hook=OrderedDict), 
						json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict),
						request.user
					)

					if cache:
						query = query.replace('amp_raw.','')

					if len(values) > 0:
						cursor.execute(query, values)
					else:
						cursor.execute(query)

					writer = csv.writer(response)

					column_names = [i[0] for i in cursor.description]
					writer.writerow(column_names)
					for row in cursor.fetchall():
						writer.writerow(row)

					return response

			except OperationalError as e:
				return HttpResponse('{"message":"Error connecting to database!"}', content_type="application/json")

		except Chart.DoesNotExist:
			return HttpResponse('{"message":"No such chart exists!"}', content_type="application/json")
	else:
		return HttpResponse('{"message":"An error has occurred!"}', content_type="application/json")

def reset(request):
	response = '{"message":"failed"}'
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	if 'reset_id' in request.GET:
		reset_id = request.GET.get('reset_id', -1)
		reset_type = request.GET.get('reset_type', -1)
		if reset_id != -1 and reset_type != -1:
			if reset_type == 'dashboard':
				User_Dashboard.objects.filter(dashboard_id=reset_id, user_id=request.user.id).delete()
			elif reset_type == 'chart':
				User_Chart.objects.filter(chart_id=reset_id, user_id=request.user.id).delete()

			response = '{"message":"success"}'
		else:
			response = '{"message":"invalid id or type"}'
	else:
		response = '{"message":"invalid parameters"}'

	return HttpResponse(response, content_type="application/json")

def resort(request):
	response = '{"message":"failed"}'
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	dashboard_id = request.GET.get('dashboard_id', -1)
	chart_id = request.GET.get('chart_id', -1)
	sort = request.GET.get('sort', -1)
	order = request.GET.get('order', -1)
	if dashboard_id != -1 and chart_id != -1 and chart_id != 'undefined' and sort != -1 and order != -1 and order.lower() in ['asc', 'desc']:
		chart = User_Chart.objects.filter(chart_id=chart_id, user_id=request.user.id)
		if not chart:
			default_chart = Chart.objects.filter(id=chart_id)
			if not default_chart:
				return HttpResponse('{"message":"failed"}', content_type="application/json")

			User_Chart.objects.create(chart_id=default_chart[0].id, user_id=request.user.id, title=default_chart[0].title, query=default_chart[0].query, attributes=default_chart[0].attributes, time=default_chart[0].time, chart_type=default_chart[0].chart_type, drilldowns=default_chart[0].drilldowns, selects=default_chart[0].selects, wheres=default_chart[0].wheres, group_bys=default_chart[0].group_bys, order_bys=default_chart[0].order_bys, limits=default_chart[0].limits, source_id=default_chart[0].source_id, table_name=default_chart[0].source_id, status=default_chart[0].status, drilldown_options=default_chart[0].drilldown_options, allowed_user_groups=default_chart[0].allowed_user_groups, allowed_role_groups=default_chart[0].allowed_role_groups, allowed_individuals=default_chart[0].allowed_individuals, assigned_dashboards=default_chart[0].assigned_dashboards, group_owner_id=default_chart[0].group_owner_id, aliases=default_chart[0].aliases)
			chart = User_Chart.objects.filter(chart_id=chart_id, user_id=request.user.id)
		
		aliases = json.loads(chart[0].aliases, object_pairs_hook=OrderedDict)
		order_bys = json.loads(chart[0].order_bys, object_pairs_hook=OrderedDict)
		changed = False
		if 'groups' in order_bys:
			for key, value in order_bys['groups'].items():
				response = '{"value":"' + str(value['value']) + '", "checking":{'
				if str(value['value']) in aliases:
					for key2, value2 in aliases.items():
						response = response + '"' + str(value2.lower()) + '":"' + str(sort.lower()) + '",'
						if value2.lower() == sort.lower():
							value['value'] = str(key2)
							value['order'] = order
							changed = True
			if response != '{"checking":{':
				response = response[0:-1]
			response = response + '}}'
			if changed:
				chart.update(order_bys=json.dumps(order_bys))
				response = '{"message":"success"}'
		else:
			response = '{"message":"No Groups"}'

	else:
		response = '{"message":"invalid parameters"}'

	return HttpResponse(response, content_type="application/json")

def toggle_filter(request):
	response = '{"message":"failed"}'
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "ajax")

	dashboard_id = request.POST.get('dashboard_id', -1)
	filter_key = request.POST.get('filter_key', -1)
	filter_status = request.POST.get('filter_status', -1)
	if dashboard_id != -1 and filter_key != -1 and filter_status != -1:
		d = User_Dashboard.objects.filter(dashboard_id=int(dashboard_id), user_id=request.user.id)
		
		if not d:
			default_dashboard = Dashboard.objects.filter(id=int(dashboard_id))

			User_Dashboard.objects.create(dashboard_id=int(dashboard_id),user_id=request.user.id, name=default_dashboard[0].name, time=default_dashboard[0].time, charts=default_dashboard[0].charts, filters=default_dashboard[0].filters, description=default_dashboard[0].description, status=default_dashboard[0].status, allowed_user_groups= default_dashboard[0].allowed_user_groups, allowed_role_groups=default_dashboard[0].allowed_role_groups, allowed_individuals=default_dashboard[0].allowed_individuals, group_owner_id=default_dashboard[0].group_owner_id)
			d = User_Dashboard.objects.filter(dashboard_id=int(dashboard_id), user_id=request.user.id)

		filters = json.loads(d[0].filters, object_pairs_hook=OrderedDict)
		for key, f in filters['layout'].items():
			if str(key) == str(filter_key).lower():
				f['status'] = filter_status
				User_Dashboard.objects.filter(dashboard_id=int(dashboard_id), user_id=request.user.id).update(filters=json.dumps(filters, cls=DjangoJSONEncoder))
				response = '{"message":"success", "url": "/bi/viewdashboard/' + dashboard_id + '/"}'
				break
	else:
		response = '{"message":"invalid parameters"}'

	return HttpResponse(response, content_type="application/json")

'''
def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(key) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        #logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        #logging.getLogger("error_logger").error(traceback.format_exc())
        return None
'''

def remove_drilldowns(chart_id, user_id, drilldown_breadcrumb):
	if drilldown_breadcrumb != -1:

		if drilldown_breadcrumb == 'clear':
			drilldowns = OrderedDict()
		else:
			drilldown_level = -1
			chart = User_Chart.objects.filter(chart_id=chart_id, user_id=user_id)
			drilldowns = json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)
			if not chart:
				return 'No Chart found', False

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

		return 'Success', True

	return 'Cannot drill down lower', False

	# Convert from json to OrderedDict
	drilldowns = json.loads(chart[0].drilldowns, object_pairs_hook=OrderedDict)

def add_drilldowns(chart_id, user_id, drilldown_options, new_field_id, old_field, old_field_value, select_position):
	chart = User_Chart.objects.filter(chart_id=chart_id, user_id=user_id)
	if not chart:
		default_chart = Chart.objects.filter(id=chart_id)
		if not default_chart:
			return 'Cannot find default chart', False
		User_Chart.objects.create(chart_id=default_chart[0].id, user_id=user_id, title=default_chart[0].title, query=default_chart[0].query, attributes=default_chart[0].attributes, time=default_chart[0].time, chart_type=default_chart[0].chart_type, drilldowns=default_chart[0].drilldowns, selects=default_chart[0].selects, wheres=default_chart[0].wheres, group_bys=default_chart[0].group_bys, order_bys=default_chart[0].order_bys, limits=default_chart[0].limits, source_id=default_chart[0].source_id, table_name=default_chart[0].source_id, status=default_chart[0].status, drilldown_options=default_chart[0].drilldown_options, allowed_user_groups=default_chart[0].allowed_user_groups, allowed_role_groups=default_chart[0].allowed_role_groups, allowed_individuals=default_chart[0].allowed_individuals, assigned_dashboards=default_chart[0].assigned_dashboards, group_owner_id=default_chart[0].group_owner_id, aliases=default_chart[0].aliases)
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
					if int(float(drilldown_values['level'])) > int(float(drilldown_lowest_position)):
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

		return 'Success', True
	else:
		return 'New field not in drilldown list', False

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


def replace_reg(query, filters, selects, position, wheres, group_bys, order_bys, limits, drilldowns_options, drilldowns, user):
	values = []
	new_query = query
		
	if drilldowns:
		new_query = new_query.replace('%', '%%')

	if drilldowns:
		drilldown_term = ''
		drilldown_where = ''
		drilldown_position = -1
		drilldown_values = []
		drilldown_previous_field = ''
		drilldown_order_by = ''
		for drilldown_key, drilldown_value in drilldowns.items():
			if drilldown_key == 'current':
				drilldown_term = drilldown_value['field']
				drilldown_level = drilldown_value['level']
				drilldown_order_by = drilldown_value['field']

			elif drilldown_key == 'default':
				drilldown_position = drilldown_value['position']
				drilldown_previous_field = drilldown_value['field']

			if drilldown_key != 'current':
				drilldown_where += drilldown_value['field'] + '=%s AND '
				drilldown_values.append(drilldown_value['value'])

	for select_group_key, select_group in selects.items():
		count = 0
		select_line = ''
		for select_key, select in select_group.items():	
			if 'is_case' in select and select['is_case'] != '':
				select_line += select['start'] + wheres[select['where_group']][select['where']]['field'] + select['inbetween'] + '' + select['after'] + select['end']

			#if new_field_id != -1 and old_field != -1 and old_field_value != -1 and int(position) == int(count) and position != -1 and old_field in drilldown_list.values(): #~!@
			
			if select['prefix'] != '':
				select_line += select['prefix'] + '.'

			if drilldowns and drilldown_term != '' and drilldown_position != '-1' and int(float(drilldown_position)) == int(float(count)):
				select_line += drilldown_term + ','
			else:
				select_line += select['value'] + ','

			count += 1

		if select_line != '':
			new_query = new_query.replace('$' + select_group_key, select_line[:-1])
			
	for where_group_key, where_group in wheres.items():
		line = ''
		
		field_grouping_format = ''
		field_grouping = ''

		if 'field_grouping' in where_group and where_group['field_grouping'] != 'false':
			for fk0, fv0 in filters['layout'][where_group['field_grouping']['filter_option0']]['options'].items():
				if fv0['checked'] == 'true':
					field_grouping_format = where_group['field_grouping']['value'].replace('$' + where_group['field_grouping']['filter_option0'],fv0['title'])
					if 'filter_option1' in where_group['field_grouping']:
						for fk1, fv1 in filters['layout'][where_group['field_grouping']['filter_option1']]['options'].items():
							if where_group['field_grouping']['filter_option1'] in str(field_grouping_format) and fv1['checked'] == 'true':
								field_grouping += field_grouping_format.replace('$' + where_group['field_grouping']['filter_option1'],fv1['title']) + ','
					else:
						field_grouping += field_grouping_format.replace('$' + where_group['field_grouping']['filter_option0'],fv0['title']) + ','
			
		if field_grouping != '':
			field_grouping = field_grouping[:-1]
			new_query = new_query.replace('$field_grouping', field_grouping)
				
		for where_key, where in where_group.items():						
			if where != "false" and where_key != "hardcodes" and 'value_id' in where and filters['layout'][where['value_id']]['status'] == 'on' and where_key != 'field_grouping':
				if line == '':
					line += 'WHERE '
				
				line += where['field'] + ' ' + where['operator_start']
				
				for option_key, option in filters['layout'][where['value_id']]['options'].items():
					if option['checked'] != "false":
						if filters['layout'][where['value_id']]['type'] == 'date':
							if 'a.' in where['field']:
								line += ' "' + option['checked']
							else:
								line += ' date_sub(str_to_date("' + option['checked'] + '","%%Y-%%m-%%d"), INTERVAL 1 YEAR)'
						else:
							if where['type'] == "string":
								line += ' "'
							line += option['title']

						if where['modifier'] != "false":
							line += where['modifier']

						if filters['layout'][where['value_id']]['type'] != 'date':
							if where['type'] == "string":
								line += '"'
						elif 'a.' in where['field']:
							line += '"'

						if filters['layout'][where['value_id']]['type'] == 'date':
							line += ' AND '
						else:
							line += ','

				if line.endswith(','):
					line = line[:-1] 
				if filters['layout'][where['value_id']]['type'] == 'date' and line.endswith(' AND '):
					line = line[:-5] 

				line += where['operator_end'] + ' AND '

		#if new_field_id != -1 and old_field != -1 and old_field_value != -1 and old_field in drilldown_list.values(): #~!@
		if drilldowns and drilldown_where != '':
			line += drilldown_where
			values.extend(drilldown_values)


		if where_group['hardcodes'] != 'false':
			for hardcode_key, hardcode in where_group['hardcodes'].items():
				if line == '':
					line = 'WHERE '
				line += hardcode['value'].replace('%', '%%') + ' AND '
				line = line.replace('$user', str(user.get_full_name()))
			
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
				if drilldowns and drilldown_previous_field in order['value']:
					order_line += drilldown_order_by
				else:
					order_line += order['value']
			elif 'field' in order.keys() and order['field'] != '':
				order_line += '"' + order['value'] + '"'

			if 'order' in order.keys() and order['order'] != '':
				order_line += ' ' + order['order']

			if order_line != '':
				new_query = new_query.replace('$' + order_key, order_line)

	if drilldowns:
		new_query += ''
	else:
		if bool(limits) and 'type' in limits:
			if str(limits['type']) == 'regular':
				new_query += ' LIMIT ' + str(limits['offset']) + ',' + str(limits['row_count'])
			elif str(limits['type']) == 'all':
				new_query += ''
			else:
				new_query += ' LIMIT 15'
		else:
			new_query += ' LIMIT 15'
	
	return new_query, values