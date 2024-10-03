from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth import authenticate, login, logout

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

from ..models import Chart
from ..models import Dashboard
from ..models import User_Chart
from ..models import User_Dashboard

from ..models import Role
from ..models import User_Roles

from ...Home.models import Org_Meta

from django.contrib.auth.models import Group

from ..forms import DashboardPropertiesForm
from ..forms import ChartPropertiesForm

from .... import views
import math

from django.db.models import Count

#from markdownx.models import MarkdownxFields

#from django.http import JsonResponse
from django.http import HttpResponse
import json
from collections import OrderedDict 
from datetime import date, timedelta, datetime

import logging

url = "192.241.131.173:8000"
login_redirect = "/login/?next="

def bi_view(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

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

	#dashboards_count = Dashboard.objects.filter(dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()
	dashboards_count = Dashboard.objects.extra(where=user_groups_query).exclude(status='InProgress').order_by('order_id').values()

	all_dashboards_counts = {'all': 0, 'active': 0, 'favorited': 0, 'drafts': 0, 'deleted': 0}
	for d_c in dashboards_count:
		all_dashboards_counts['all'] += 1
		if d_c['status'].lower() == 'active':
			all_dashboards_counts['active'] += 1
		elif d_c['status'].lower() == 'draft':
			all_dashboards_counts['drafts'] += 1
		elif d_c['status'].lower() == 'deleted':
			all_dashboards_counts['deleted'] += 1

	filters = {}
	filters_query = {}
	
	organization = request.user.groups.all()
	if 2 in usergroups:
		organization = Group.objects.order_by('name')
		

	submitted_organization = int(request.GET.get('organization', -1))
	if submitted_organization != -1 and submitted_organization > 0 and submitted_organization < 1000:
		if 2 in usergroups or submitted_organization in usergroups:
			filters['organization'] = submitted_organization
			filters_query['group_owner_id'] = submitted_organization

	page = request.GET.get('page', '')
	if page == '' or int(page) < 1:
		page = 1
	else:
		page = int(page)

	page_info = {'page': page, 'per_page': 15, 'prev': 'false', 'next': 'false'}
	page_info['per_this_page'] = (page_info['per_page'] * (page_info['page'] - 1)) + 1

	search = request.GET.get('search', '')
	if search != '':
		filters['search'] = search
		filters_query['name__icontains'] = search

	category = request.GET.get('category', '')
	if category in ['all', 'active', 'drafts', 'deleted', '']:
		filters['category'] = category
		if category == 'active':
			filters_query['status'] = 'Active'
		elif category == 'drafts':
			filters_query['status'] = 'Draft'
		elif category == 'deleted':
			filters_query['status'] = 'Deleted'

	if not filters_query:
		#dashboards = Dashboard.objects.filter(dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()[int(page_info['per_this_page']):int(page_info['per_this_page']) + int(page_info['per_page'])]
		dashboards = Dashboard.objects.extra(where=user_groups_query).exclude(status='InProgress').order_by('order_id').values()[int((page_info['per_this_page'] ) - 1):int(page_info['per_this_page']) + int(page_info['per_page'])]

		page_info['total_pages'] = math.ceil(all_dashboards_counts['all'] / page_info['per_page'])
	else:
		#dashboards = Dashboard.objects.filter(**filters_query, dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()[int(page_info['per_this_page']):int(page_info['per_this_page']) + int(page_info['per_page'])]
		#total_filtered_dashboards = Dashboard.objects.filter(**filters_query, dashboard_group__usergroup_id__in=usergroups).annotate(count=Count('name'))
		
		dashboards = Dashboard.objects.filter(**filters_query).extra(where=user_groups_query).exclude(status='InProgress').order_by('order_id').values()[(int(page_info['per_this_page']) - 1):int(page_info['per_this_page']) + int(page_info['per_page'])]
		total_filtered_dashboards = Dashboard.objects.filter(**filters_query).extra(where=user_groups_query).exclude(status='InProgress').count()
		

		if total_filtered_dashboards:
			page_info['total_pages'] = math.ceil(total_filtered_dashboards / page_info['per_page'])
		else:
			page_info['total_pages'] = 1

	page_info['per_this_page_total'] = (page_info['page'] * page_info['per_page'])

	#if page_info['per_this_page_total'] < #here

	org_logo_url_request = Org_Meta.objects.filter(meta_key= request.META['HTTP_HOST'] + '_url')
	org_logo_url = ''
	if org_logo_url_request.count() > 0:
		org_logo_url = org_logo_url_request[0].meta_value

	if (page - 1) > 0:
		page_info['prev'] = 'true'
	if (page + 1) <= page_info['total_pages']:
		page_info['next'] = 'true'

	if not request.user.has_perm('BI.can_change_dash'):
		access_level = 'regular'
	else:
		access_level = 'edit'

	context = {"access": "allow", 'logo_url': org_logo_url, "message":"", "groups": ', '.join(views.get_groups(request)), "dashboards": dashboards, "menu": views.get_sidebar(request), "counts":all_dashboards_counts, 'page_info': page_info, 'filters': filters, 'access_level': access_level, 'groups': organization, 'submitted_organization': submitted_organization, 'submitted_category': category}
	return render(request, "bi.html", context)

def section_view(request, section):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "bi")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "section": str(section).capitalize(), "message": "Access denied!", "menu": views.get_sidebar(request)})

	usergroups = []
	user_groups_query = []
	user_groups_string = ''
	section_query = []

	for group in request.user.groups.all():
		usergroups.append(group.id)
		user_groups_string += 'FIND_IN_SET(' + str(group.id) + ', allowed_user_groups) OR '

	user_roles = User_Roles.objects.filter(user_id=request.user.id)
	for role in user_roles.values():
		user_groups_string += 'FIND_IN_SET(' + str(role['role_id']) + ', allowed_role_groups) OR '
	user_groups_string += 'FIND_IN_SET(' + str(request.user.id) + ', allowed_individuals) OR '
	user_groups_query = [user_groups_string[:-4]]
	
	if str(section).lower() in ['accounting','advertising','circulation','editorial','production', 'admin']:
		section_query = ['section="' + str(section) + '"']
	else:
		return render(request, "bi.html", {"access": "deny", "section": str(section).capitalize(), "message": "Error: No such section!", "menu": views.get_sidebar(request)})

	#dashboards_count = Dashboard.objects.filter(dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()
	dashboards_count = Dashboard.objects.extra(where=user_groups_query).extra(where=section_query).exclude(status='InProgress').order_by('order_id').values()

	all_dashboards_counts = {'all': 0, 'active': 0, 'favorited': 0, 'drafts': 0, 'deleted': 0}
	for d_c in dashboards_count:
		all_dashboards_counts['all'] += 1
		if d_c['status'].lower() == 'active':
			all_dashboards_counts['active'] += 1
		elif d_c['status'].lower() == 'draft':
			all_dashboards_counts['drafts'] += 1
		elif d_c['status'].lower() == 'deleted':
			all_dashboards_counts['deleted'] += 1

	filters = {}
	filters_query = {}
	
	organization = request.user.groups.all()
	if 2 in usergroups:
		organization = Group.objects.order_by('name')
		

	submitted_organization = int(request.GET.get('organization', -1))
	if submitted_organization != -1 and submitted_organization > 0 and submitted_organization < 1000:
		if 2 in usergroups or submitted_organization in usergroups:
			filters['organization'] = submitted_organization
			filters_query['group_owner_id'] = submitted_organization

	page = request.GET.get('page', '')
	if page == '' or int(page) < 1:
		page = 1
	else:
		page = int(page)

	page_info = {'page': page, 'per_page': 15, 'prev': 'false', 'next': 'false'}
	page_info['per_this_page'] = (page_info['per_page'] * (page_info['page'] - 1)) + 1

	search = request.GET.get('search', '')
	if search != '':
		filters['search'] = search
		filters_query['name__icontains'] = search

	category = request.GET.get('category', '')
	if category in ['all', 'active', 'drafts', 'deleted', '']:
		filters['category'] = category
		if category == 'active':
			filters_query['status'] = 'Active'
		elif category == 'drafts':
			filters_query['status'] = 'Draft'
		elif category == 'deleted':
			filters_query['status'] = 'Deleted'

	if not filters_query:
		#dashboards = Dashboard.objects.filter(dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()[int(page_info['per_this_page']):int(page_info['per_this_page']) + int(page_info['per_page'])]
		dashboards = Dashboard.objects.extra(where=user_groups_query).extra(where=section_query).exclude(status='InProgress').order_by('order_id').values()[int((page_info['per_this_page'] ) - 1):int(page_info['per_this_page']) + int(page_info['per_page'])]

		page_info['total_pages'] = math.ceil(all_dashboards_counts['all'] / page_info['per_page'])
	else:
		#dashboards = Dashboard.objects.filter(**filters_query, dashboard_group__usergroup_id__in=usergroups).order_by('order_id').values()[int(page_info['per_this_page']):int(page_info['per_this_page']) + int(page_info['per_page'])]
		#total_filtered_dashboards = Dashboard.objects.filter(**filters_query, dashboard_group__usergroup_id__in=usergroups).annotate(count=Count('name'))
		
		dashboards = Dashboard.objects.filter(**filters_query).extra(where=user_groups_query).extra(where=section_query).exclude(status='InProgress').order_by('order_id').values()[(int(page_info['per_this_page']) - 1):int(page_info['per_this_page']) + int(page_info['per_page'])]
		total_filtered_dashboards = Dashboard.objects.filter(**filters_query).extra(where=user_groups_query).extra(where=section_query).exclude(status='InProgress').count()
		

		if total_filtered_dashboards:
			page_info['total_pages'] = math.ceil(total_filtered_dashboards / page_info['per_page'])
		else:
			page_info['total_pages'] = 1

	page_info['per_this_page_total'] = (page_info['page'] * page_info['per_page'])

	#if page_info['per_this_page_total'] < #here

	org_logo_url_request = Org_Meta.objects.filter(meta_key= request.META['HTTP_HOST'] + '_url')
	org_logo_url = ''
	if org_logo_url_request.count() > 0:
		org_logo_url = org_logo_url_request[0].meta_value

	if (page - 1) > 0:
		page_info['prev'] = 'true'
	if (page + 1) <= page_info['total_pages']:
		page_info['next'] = 'true'

	if not request.user.has_perm('BI.can_change_dash'):
		access_level = 'regular'
	else:
		access_level = 'edit'

	context = {"access": "allow", 'logo_url': org_logo_url, "settingsSidebar": "true", "section": str(section).capitalize(), "message":"", "groups": ', '.join(views.get_groups(request)), "dashboards": dashboards, "menu": views.get_sidebar(request), "counts":all_dashboards_counts, 'page_info': page_info, 'filters': filters, 'access_level': access_level, 'groups': organization, 'submitted_organization': submitted_organization, 'submitted_category': category}
	return render(request, "index.html", context)

def view_dashboard_view(request, section, id=0):
	#update_cache()

	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "viewdashboard")

	if not request.user.has_perm('BI.bi_access'):
		return render(request, "bi.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	if id == 0 or id == '':
		return render(request, "viewdashboard.html", {"message":"No dashboard specified!", "menu": views.get_sidebar(request)})

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

	#dashboard_access_check = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)
	dashboard_access_check = Dashboard.objects.filter(id=id).extra(where=user_groups_query)

	todays_date = date.today()
	yesterdays_date = todays_date - timedelta(days = 1)

	if len(dashboard_access_check) < 1:
		return HttpResponse(json.dumps({"access": "allow", "section": str(section).capitalize(), "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")
	'''
	usergroups = []
	for group in request.user.groups.all():
		usergroups.append(group.id)
	'''

	if 'update' in request.POST:
		update = request.POST.get('update', -1)
		if update != -1:
			dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)

			if not dashboard:
				#default_dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)
				default_dashboard = Dashboard.objects.filter(id=id).extra(where=user_groups_query)

				User_Dashboard.objects.create(dashboard_id=id,user_id=request.user.id, name=default_dashboard[0].name, time=default_dashboard[0].time, charts=default_dashboard[0].charts, filters=default_dashboard[0].filters, description=default_dashboard[0].description, status=default_dashboard[0].status, allowed_user_groups= default_dashboard[0].allowed_user_groups, allowed_role_groups=default_dashboard[0].allowed_role_groups, allowed_individuals=default_dashboard[0].allowed_individuals, group_owner_id=default_dashboard[0].group_owner_id)
				dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)

			filters = json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict)
			if update != 'Update All':
				for option_key, option in filters['layout'][update]['options'].items():
					if filters['layout'][update]['type'] == 'date':
						start_date = request.POST.get('run_date_start',-1)
						end_date = request.POST.get('run_date_end',-1)
						if start_date != -1 and end_date != -1:
							if 'start_date' in option['title'].lower():
								option['checked'] = start_date
							elif 'end_date' in option['title'].lower():
								option['checked'] = end_date
					else:
						value = request.POST.getlist('values[' + update + ']', -1)
						if value != -1 and option['title'] in value:
							option['checked'] = "true"
						else:
							option['checked'] = "false"
			else:
				for filter_key, filter_value in filters['layout'].items():
					for option_key, option in filter_value['options'].items():
						if filter_value['type'] == 'date':
							start_date = request.POST.get('run_date_start',-1)
							end_date = request.POST.get('run_date_end',-1)
							if start_date != -1 and end_date != -1:
								if 'start_date' in option['title'].lower():
									option['checked'] = start_date
								elif 'end_date' in option['title'].lower():
									option['checked'] = end_date
						else:
							value = request.POST.getlist('values[' + filter_key + ']', -1)
							if value != -1 and option['title'] in value:
								option['checked'] = "true"
							else:
								option['checked'] = "false"

			User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id).update(filters=json.dumps(filters))

	dashboard = User_Dashboard.objects.filter(dashboard_id=id, user_id=request.user.id)
	if not dashboard:
		#dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups).annotate(dashboard_id=F('id'))	
		dashboard = Dashboard.objects.filter(id=id).annotate(dashboard_id=F('id')).extra(where=user_groups_query)

	#dashboard = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)

	if not request.user.has_perm('BI.can_change_dash'):
		dash_access_level = 'regular'
	else:
		dash_access_level = 'edit'

	if not request.user.has_perm('BI.can_change_chart'):
		chart_access_level = 'regular'
	else:
		chart_access_level = 'edit'

	if len(dashboard) > 0:
		context = {"access": "allow", "settingsSidebar": "true", "section": str(section).capitalize(), "message":"", "groups": ', '.join(views.get_groups(request)), "dashboard": dashboard[0], "charts":json.loads(dashboard[0].charts, object_pairs_hook=OrderedDict), "filters":json.loads(dashboard[0].filters, object_pairs_hook=OrderedDict), "menu": views.get_sidebar(request), 'dash_access_level': dash_access_level, 'chart_access_level': chart_access_level, "todays_date": todays_date.strftime('%Y-%m-%d'), "yesterdays_date": yesterdays_date.strftime('%Y-%m-%d')}
	else:
		context = {"access": "allow", "section": str(section).capitalize(), "message": "No such dashboard exists!", "menu": views.get_sidebar(request)}

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