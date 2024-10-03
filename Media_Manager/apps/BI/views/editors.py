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
from ..models import Source
from ..models import Source_Group

from ..models import Role
from ..models import User_Roles

from ..forms import DashboardPropertiesForm
from ..forms import ChartPropertiesForm

from .... import views

#from markdownx.models import MarkdownxFields

#from django.http import JsonResponse
from django.http import HttpResponse
import json
from collections import OrderedDict 

import logging

from django.db import connections

url = "192.241.131.173:8000"
login_redirect = "/login/?next="

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

					'''
					for group in request.user.groups.all():
						g = Dashboard_Group.objects.create(dashboard=d, usergroup_id=group.id)
						g.save()
					'''

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
		
		 # Check if user has access to see chart
		#dashboard_access_check = Dashboard.objects.filter(id=id, dashboard_group__usergroup_id__in=usergroups)
		dashboard_access_check = Dashboard.objects.filter(id=id).extra(where=user_groups_query)

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

					'''
					for group in request.user.groups.all():
						g = Chart_Group.objects.create(chart=c, usergroup_id=group.id)
						g.save()
					'''

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

		 # Check if user has access to see chart
		#chart_access_check = Chart.objects.filter(id=id, chart_group__usergroup_id__in=usergroups)
		chart_access_check = Chart.objects.filter(id=id).extra(where=user_groups_query)

		if len(chart_access_check) < 1:
			return HttpResponse(json.dumps({"access": "allow", "message": "No dashboard found!", "menu": views.get_sidebar(request)}, cls=DjangoJSONEncoder), content_type="application/json")
		
		# User doesn't have appropriate permissions to edit chart
		if not request.user.has_perm('BI.can_add_chart'):
			return render(request, "chart.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

		chart = Chart.objects.filter(id=id)
		chart = chart[0]

		sources = Source.objects.filter(source_group__group_id__in=usergroups)
		source_list = []
		for source in sources:
			source_list.append(source.name)

		if chart.source_id not in connections:
			chart_source = Source.objects.filter(id=chart.source_id)
			chart_source = chart_source[0]
			newDB = {}
			newDB['ENGINE'] = source.engine
			newDB['NAME'] = source.name #decrypt(source.name)
			newDB['USER'] = source.user #decrypt(source.user)
			newDB['PASSWORD'] = source.password #decrypt(source.password)
			newDB['HOST'] = source.host #decrypt(source.host)
			newDB['PORT'] = source.port
			connections.databases[chart.source_id] = newDB

		conn = connections[chart.source_id]
		try:
			with conn.cursor() as cursor:
				cursor.execute('show columns from ' + str(chart.table_name))
				columns_query = cursor.fetchall()
				columns = []
				for columns_row in columns_query:
					columns.append(str(columns_row[0]).lower())

				set_drilldowns_full = json.loads(chart.drilldown_options)
				set_drilldowns_full = list(set_drilldowns_full.values())[0]
				set_drilldowns = {}

				for k, sdf in set_drilldowns_full.items():
					set_drilldowns[int(k)] = str(sdf).lower()
				
				available_drilldowns = columns
				
				for ad in available_drilldowns:
					for k2, sd in set_drilldowns.items():
						if str(ad).strip() == str(sd).strip():
							available_drilldowns.remove(ad)
				
				available_drilldowns = sorted(available_drilldowns)
				columns = sorted(columns)

				cursor.execute('show tables')
				tables_query = cursor.fetchall()
				tables = []
				for t in tables_query:
					tables.append(t[0])

		except OperationalError as e:
			return render(request, "chart.html", {"access": "deny", "message": "Database access denied!", "menu": views.get_sidebar(request)})

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "chart": chart, "id": str(id), "menu": views.get_sidebar(request), 'source_list': source_list, 'columns': columns, 'set_drilldowns': set_drilldowns, 'available_drilldowns': available_drilldowns, 'tables': tables, 'parser': parser(chart.query), 'selects':json.loads(chart.selects, object_pairs_hook=OrderedDict)}
	return render(request, "chart.html", context)

def parser(string):
	tree = {'select': {}, 'from': {}, 'group_by': {}, 'order_by': {}}
	depth = 0
	flagDepth = 0 
	flagList = []
	words = ''
	previous = ''
	varIgnores = ['$where', '$select']
	otherIgnores = ['group', 'order', 'a', 'b', 'ab', 'abc', 'union', 'all']

	for word in string.split():
		lword = word.lower().replace('(', '').replace(')','')
		if lword in ['select', 'from']:
			if words != '':
				tree[str(flagList[-1])][int(len(tree[str(flagList[-1])]) - 1)].append(words)
				words = ''
			flagList.append(str(lword))
			tree[str(flagList[-1])][len(tree[str(flagList[-1])])] = []
			previous = word
			continue
		elif previous.lower() == 'group':
			if lword == 'by':
				if words != '':
					tree[str(flagList[-1])][int(len(tree[str(flagList[-1])]) - 1)].append(words)
					words = ''
				flagList.append('group_by')
				tree[str(flagList[-1])][len(tree[str(flagList[-1])])] = []
				previous = word
				continue 
		elif previous.lower() == 'order':
			if lword == 'by':
				if words != '':
					tree[str(flagList[-1])][int(len(tree[str(flagList[-1])]) - 1)].append(words)
					words = ''
				flagList.append('order_by')
				tree[str(flagList[-1])][len(tree[str(flagList[-1])])] = []
				previous = word
				continue
		elif lword not in otherIgnores and not any(v in lword for v in varIgnores):
			words += word + ' '

		for letter in word:
			lletter = letter.lower()

			if lletter == '(':
				depth += 1
			elif lletter == ')':
				depth -= 1
			elif lletter == ',':
				if depth == 0:
					tree[str(flagList[-1])][int(len(tree[str(flagList[-1])]) - 1)].append(words)
					words = ''

			if previous.lower() in ['select', 'from', 'by'] and lletter == '(':
				flagList.append(previous)
				flagDepth += 1
			elif flagDepth > 0 and lletter == ')':
				flagList.pop()
				flagDepth -= 1

		previous = word

	if words != ' ':
		tree[str(flagList[-1])][int(len(tree[str(flagList[-1])]) - 1)].append(words)

	return tree