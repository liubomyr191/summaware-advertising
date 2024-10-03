from django.shortcuts import render, redirect
from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *
from ..models.companies import *
from ..models.classified_styling import *
from Media_Manager.apps.Advertising.models.finance import *
from .... import views
from django.core import serializers
import json
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

login_redirect = "/login/?next="

def admin(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/admin.html')

# def adminUpload(request):
# 	# Check if user is logged in, if not, redirect  to login screen
# 	if request is None or not request.user.is_authenticated:
# 		return redirect(login_redirect + '/')
# 	success = False
# 	file_name = ''
# 	if request.method == 'POST' and 'file' in request.FILES:
# 		uploaded_file = request.FILES['file']
# 		current_time = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # Get timestamp with milliseconds
# 		file_name = f"{current_time}_{uploaded_file.name}"
# 		file_path = os.path.join('uploads', file_name)
		
# 		with open(file_path, 'wb+') as destination:
# 			for chunk in uploaded_file.chunks():
# 				destination.write(chunk)
# 		success = True
# 	return JsonResponse({'success': success, "url": f"/uploads/{file_name}"}, status=200)

def adminGeneral(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	all_states = AllStates.objects.all()
	magazines = MagazineProduct.objects.all()
	newspapers = NewspaperProduct.objects.all()
	digitals = DigitalProduct.objects.all()
	regions = Region.objects.all()
	publications = AdminPublication.objects.all()
	days_of_week = {'1': 'Sun', '2': 'Mon', '3': 'Tue', '4': 'Wed', '5': 'Thu', '6': 'Fri', '7': 'Sat'}
	for publication in publications:
		if publication.run_days:
			run_days = json.loads(publication.run_days)
			days = ''
			for day in run_days:
				days += (days_of_week[day] + ', ')
			publication.run_day = days
		else:
			publication.run_days = []
	context = {
		'all_states': all_states,
		'magazines': magazines,
		'newspapers': newspapers,
		'regions': regions,
		'publications': publications,
		'total_newspapers': len(newspapers),
		'total_magazines': len(magazines),
		'total_digitals': len(digitals),
		'digitals': digitals,
	}
	return render(request, 'admin/admin-general.html', context)

def adminAds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	pub_adtypes = PubAdType.objects.all()
	adtypes = AdminAdType.objects.all()
	rates = Rate.objects.all()
	publications = AdminPublication.objects.all()
	marketcodes = AdminMarketCode.objects.all()
	sections = PublicationSection.objects.all()
	context = {
		'pub_adtypes': pub_adtypes,
		'adtypes': adtypes,
		'rates': rates,
		'marketcodes': marketcodes,
		'publications': publications,
		'sections':sections
	}
	return render(request, 'admin/ads/ads.html', context)

# @csrf_exempt
# def create_multiple_publication_section(request):
#     if request.method != 'POST':
#         return JsonResponse({"message": "Error. Method not allowed."}, status=405)
    
#     # Ensure user authentication
#     if request is None or not request.user.is_authenticated:
#         return JsonResponse({"message": "Error. Access forbidden."}, status=403)

#     # Check if the user has the required permission
#     if not request.user.has_perm('BI.advertising_access'):
#         return JsonResponse({"message": "Error. Access forbidden."}, status=403)
    
#     try:
#         req_data = json.loads(request.body.decode('utf-8'))
#         name = req_data.get('name')
#         code = req_data.get('code')
#         default_rate = req_data.get('default_rate')
#         publication_ids = req_data.get('publication_ids', [])
        
#         if not name or not publication_ids or not code or not default_rate:
#             return JsonResponse({"message": "Error. Name, code, default rate, and publications are required."}, status=400)
        
#         # Create sections for each publication
#         for pub_id in publication_ids:
#             try:
#                 publication = Publication.objects.get(pk=pub_id)
#                 section = PublicationSection(
#                     name=name,
#                     code=code,
#                     default_rate_id=default_rate,  # Assuming `default_rate` is a foreign key or related field
#                     publication=publication
#                 )
#                 section.save()
#             except Publication.DoesNotExist:
#                 return JsonResponse({"message": f"Error. Publication with id {pub_id} not found."}, status=404)

#         return JsonResponse({"message": "Success! Sections created for the selected publications."}, status=201)
    
#     except Exception as ex:
#         return JsonResponse({"message": f"Error: {str(ex)}"}, status=500)
def adminAdsEditAdType(request):

	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
	
	data = json.loads(request.body.decode('utf-8'))
	adtype = AdminAdType.objects.get(pk=data['id'])
	adtype.name = data['name']
	adtype.code = data['code']
	adtype.default_rate_id = data['default_rate']
	adtype.active = data['active']
	adtype.status = data['status']
	success = True
	try:
		adtype.save()
		pub_adtypes = PubAdType.objects.filter(adminadtype=adtype)
		for pub_adtype in pub_adtypes:
			pub_adtype.delete()

		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=adtype, adminpublication=publication)
			new_pub_adtype.save()
	except Exception as e:
		success = False

	return JsonResponse({'success': success, "errors": []}, status=200)
def adminAdsAdTypeDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	adtype = AdminAdType.objects.get(pk=data['id'])
	pub_adtypes = PubAdType.objects.filter(adminadtype=adtype.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.adminpublication.id, 'name': pa.adminpublication.name} for pa in pub_adtypes]
	pub_ids = []
	for pub_adtype in pub_adtypes:
		pub_ids.append(pub_adtype.adminpublication.id)

	pub_adtypes = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_adtypes] 

	response_data = {
			'id': adtype.id,
			'adtype': serializers.serialize('json', [adtype]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)

def adminAdsCreateAdType(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
	data = json.loads(request.body.decode('utf-8'))
	new_adtype = AdminAdType(code=data['code'], name=data['name'], default_rate_id=data['default_rate'])
	success = True
	try:
		new_adtype.save()
		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=new_adtype, adminpublication=publication)
			new_pub_adtype.save()
	except Exception as e:
		success = False
	
	return JsonResponse({'success': success, "errors": []}, status=200)

def adminFinancial(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	fiscalyears = AdminFiscalYear.objects.all()
	company_codes = CompanyGLCode.objects.all()
	gl_codes = GLCode.objects.all()
	location_codes = Location.objects.all()
	departments = CompanyDepartment.objects.all()
	profit_codes = ProfitCode.objects.all()

	context = {
		'fiscalyears': fiscalyears,
		'company_codes': company_codes,
		'gl_codes': gl_codes,
		'location_codes':location_codes,
		'departments': departments,
		'profit_codes': profit_codes
	}
	return render(request, 'admin/financial/admin-financial.html', context)

def adminFinancialFiscal(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	context = {}

	fiscal_year = None
	if id != None:
		fiscal_year = AdminFiscalYear.objects.get(pk=id)
		context['fiscal_year'] = fiscal_year

	accounting_periods = AccountingPeriod.objects.filter(fiscal_year_id=id).all()
	context = {'accounting_periods': accounting_periods}
	context['fiscal_years'] = fiscal_year
	return render(request, 'admin/financial/fiscal-year.html', context=context)

def adminAccountingPeriods(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		period = AccountingPeriod()
		period.start_date = data['start-date']
		period.end_date = data['end-date']
		period.status = data['status']
		period.account_id = request.user.id
		period.fiscal_year_id = data['fiscal_year_id']
		period.save()
		return JsonResponse({'success': True}, status=200)

def adminEditAccountingPeriods(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		try:
			period = AccountingPeriod.objects.get(pk=data['id'])
		except Exception as e:
			period = None

		if period == None:
			return JsonResponse({'success': False}, status=500)
		
		period.start_date = data['start-date']
		period.end_date = data['end-date']
		period.status = data['status']
		period.account_id = request.user.id
		period.fiscal_year_id = data['fiscal_year_id']
		period.save()
		return JsonResponse({'success': True}, status=200)

def adminEditAccountingPeriodsStatus(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		try:
			period = AccountingPeriod.objects.get(pk=data['id'])
		except Exception as e:
			period = None

		if period == None:
			return JsonResponse({'success': False}, status=500)
	
		period.status = data['status']
		if period.status == 'True':
			period.status = 1
		else:
			period.status = 0
		period.save()
		return JsonResponse({'success': True}, status=200)
		
def create_company_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		company_id = Company.objects.all().order_by('-id')[0].id # TODO: Make this dynamic
		company = CompanyGLCode()
		company.description = data['description']
		company.code = data['code']
		company.company_id = company_id
		company.save()
		return JsonResponse({'success': True}, status=200)

def edit_company_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		company_id = Company.objects.all().order_by('-id')[0].id # TODO: Make this dynamic

		try:
			company = CompanyGLCode.objects.get(pk=data['id'])
		except Exception as e:
			company = None

		if company == None:
			return JsonResponse({'success': False}, status=500)
		
		company.description = data['description']
		company.code = data['code']
		company.company_id = company_id
		company.save()
		return JsonResponse({'success': True}, status=200)

def edit_company_code_status(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			company = CompanyGLCode.objects.get(pk=data['id'])
		except Exception as e:
			company = None

		if company == None:
			return JsonResponse({'success': False}, status=500)
		
		company.active = data['status']
		company.save()
		return JsonResponse({'success': True}, status=200)
	
def create_department_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			department = CompanyDepartment()
		except Exception as e:
			department = None

		if department == None:
			return JsonResponse({'success': False}, status=500)
		
		department.active = 1
		department.name = data['name']
		department.save()
		return JsonResponse({'success': True}, status=200)

def edit_department_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			department = CompanyDepartment.objects.get(pk=data['id'])
		except Exception as e:
			department = None

		if department == None:
			return JsonResponse({'success': False}, status=500)
		
		if data.get('active') is not None:
			active = data['active']
		else:
			active = department.active
		
		department.active = active
		department.name = data['name']
		department.save()
		return JsonResponse({'success': True}, status=200)

def edit_department_code_status(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			department = CompanyDepartment.objects.get(pk=data['id'])
		except Exception as e:
			department = None

		if department == None:
			return JsonResponse({'success': False}, status=500)
		
		department.active = data['status']
		department.save()
		return JsonResponse({'success': True}, status=200)
	
def create_profit_codes(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			profit_code = ProfitCode()
		except Exception as e:
			profit_code = None

		if profit_code == None:
			return JsonResponse({'success': False}, status=500)
		
		profit_code.active = 1
		profit_code.description = data['description']
		profit_code.profit_code = data['profit_code']
		profit_code.save()
		return JsonResponse({'success': True}, status=200)

def edit_profit_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			profit_code = ProfitCode.objects.get(pk=data['id'])
		except Exception as e:
			profit_code = None

		if profit_code == None:
			return JsonResponse({'success': False}, status=500)
		
		if data.get('active') is not None:
			active = data['active']
		else:
			active = profit_code.active
		
		profit_code.active = active
		profit_code.description = data['description']
		profit_code.profit_code = data['profit_code']
		profit_code.save()
		return JsonResponse({'success': True}, status=200)

def edit_profit_code_status(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			profit_code = ProfitCode.objects.get(pk=data['id'])
		except Exception as e:
			profit_code = None

		if profit_code == None:
			return JsonResponse({'success': False}, status=500)
		
		profit_code.active = data['status']
		profit_code.save()
		return JsonResponse({'success': True}, status=200)
	
def edit_location_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			location_code = Location.objects.get(pk=data['id'])
		except Exception as e:
			location_code = None

		if location_code == None:
			return JsonResponse({'success': False}, status=500)
		
		if data.get('active') is not None:
			active = data['active']
		else:
			active = location_code.active
		
		location_code.location = data['location']
		location_code.description = data['description']
		location_code.pc = data['pc']
		location_code.active = active
		location_code.save()
		return JsonResponse({'success': True}, status=200)
	
def create_location_code(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			location_code = Location()
		except Exception as e:
			location_code = None

		if location_code == None:
			return JsonResponse({'success': False}, status=500)
		
		location_code.location = data['location']
		location_code.description = data['description']
		location_code.pc = data['pc']
		location_code.active = True
		location_code.save()
		return JsonResponse({'success': True}, status=200)

def edit_location_code_status(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			location_code = Location.objects.get(pk=data['id'])
		except Exception as e:
			location_code = None

		if location_code == None:
			return JsonResponse({'success': False}, status=500)
		
		location_code.active = data['status']
		location_code.save()
		return JsonResponse({'success': True}, status=200)
	
def create_gl_codes(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			gl_code = GLCode()
		except Exception as e:
			gl_code = None

		if gl_code == None:
			return JsonResponse({'success': False}, status=500)
		
		gl_code.active = 1
		gl_code.description = data['description']
		gl_code.code = data['code']
		gl_code.pl_type = data['pl_type']
		gl_code.save()
		return JsonResponse({'success': True}, status=200)

def edit_gl_codes(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			gl_code = GLCode.objects.get(pk=data['id'])
		except Exception as e:
			gl_code = None

		if gl_code == None:
			return JsonResponse({'success': False}, status=500)
		
		if data.get('active') is not None:
			active = data['active']
		else:
			active = gl_code.active
		
		gl_code.active = active
		gl_code.description = data['description']
		gl_code.code = data['code']
		gl_code.pl_type = data['pl_type']
		gl_code.save()
		return JsonResponse({'success': True}, status=200)

def edit_gl_code_status(request):
	if request is None or not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		try:
			gl_code = GLCode.objects.get(pk=data['id'])
		except Exception as e:
			gl_code = None

		if gl_code == None:
			return JsonResponse({'success': False}, status=500)
		
		gl_code.active = data['status']
		gl_code.save()
		return JsonResponse({'success': True}, status=200)
	
def adminAdjustmentDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	adjustment = AdminAdjustment.objects.get(pk=data['id'])
	pub_adjustments = PubAdjustment.objects.filter(adminadjustment=adjustment.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.adminpublication.id, 'name': pa.adminpublication.name} for pa in pub_adjustments]
	pub_ids = []
	for pub_adjustment in pub_adjustments:
		pub_ids.append(pub_adjustment.adminpublication.id)

	pub_adjustments = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_adjustments] 

	response_data = {
			'id': adjustment.id,
			'adjustment': serializers.serialize('json', [adjustment]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)

def adminPricing(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	rategroups = RateGroup.objects.all()
	adjustments = AdminAdjustment.objects.all()
	publications = AdminPublication.objects.all()
	taxs = AdminTax.objects.all()
	sections = PublicationSection.objects.all()
	glcodes = GLCode.objects.all()

	content = {'rategroups': rategroups, 'adjustments': adjustments, 'publications': publications, 'sections': sections, 'glcodes': glcodes, 'taxs': taxs}
	return render(request, 'admin/pricing/admin-pricing.html', content)

def adminEditAdjustment(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	adjustment = AdminAdjustment.objects.get(pk=data['id'])
	adjustment.active = data['active']
	if 'status_only' in data:
		adjustment.save()
	else:
		adjustment.name = data['name']
		adjustment.code = data['code']
		adjustment.apply_level = data['apply_level']
		adjustment.gl_code_id = data['gl_code']
		adjustment.type = data['type']
		adjustment.value_type = data['value_type']
		adjustment.value = data['value']
		adjustment.section_id = data['section']
		adjustment.prompt_for_value = data['prompt_for_value']
		adjustment.status = data['status']
		adjustment.save()
		pub_adjustments = PubAdjustment.objects.filter(adminadjustment=adjustment)
		for pub_adjustment in pub_adjustments:
			pub_adjustment.delete()

		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_adjustment = PubAdjustment(adminadjustment=adjustment, adminpublication=publication)
			new_pub_adjustment.save()

	return JsonResponse({"errors": []}, status=200)

def adminCreateAdjustment(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	new_adjustment = AdminAdjustment(name=data['name'], code=data['code'], gl_code_id=data['gl_code'], apply_level=data['apply_level'],
																	type=data['type'], value_type=data['value_type'], value=data['value'], section_id=data['section'],
																	prompt_for_value=data['prompt_for_value'])
	new_adjustment.save()
	pub_ids = json.loads(data['publication_id'])
	for id in pub_ids:
		publication = AdminPublication.objects.get(pk=id)
		new_pub_adjustment = PubAdjustment(adminadjustment=new_adjustment, adminpublication=publication)
		new_pub_adjustment.save()
	return JsonResponse({"errors": []}, status=200)

def adminCreateTax(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")
	
	data = json.loads(request.body.decode('utf-8'))
	new_tax = AdminTax(name=data['name'], description=data['description'], amount=data['amount'], assigned_gl=data['assigned_gl'], format=data['format'],
										gl_code_id=data['gl_code'], start_date=data['start_date'], end_date=data['end_date'], active=data['active'], status=data['status'])
	success = True
	try:
		new_tax.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminTaxDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	tax = AdminTax.objects.get(pk=data['id'])

	response_data = {
			'id': tax.id,
			'tax': serializers.serialize('json', [tax]),
	}
	return JsonResponse(response_data, safe=False)

def adminEditTax(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	tax = AdminTax.objects.get(pk=data['id'])
	tax.name = data['name']
	tax.description = data['description']
	tax.amount = data['amount']
	tax.assigned_gl = data['assigned_gl']
	tax.format = data['format']
	tax.gl_code_id = data['gl_code']
	tax.start_date = data['start_date']
	tax.end_date = data['end_date']
	tax.active = data['active']
	tax.status = data['status']
	success = True
	try:
		tax.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminCreateFiscalYear(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")
	
	data = json.loads(request.body.decode('utf-8'))
	new_fiscalyear = AdminFiscalYear(name=data['name'], start_date=data['start_date'], end_date=data['end_date'], active=data['active'], status=data['status'])
	success = True
	try:
		new_fiscalyear.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminFiscalYearDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	fiscalyear = AdminFiscalYear.objects.get(pk=data['id'])

	response_data = {
			'id': fiscalyear.id,
			'fiscalyear': serializers.serialize('json', [fiscalyear]),
	}
	return JsonResponse(response_data, safe=False)

def adminEditFiscalYear(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")
	
	data = json.loads(request.body.decode('utf-8'))
	try:
		fiscalyear = AdminFiscalYear.objects.get(pk=data['id'])
	except Exception as e:
		fiscalyear = None

	if fiscalyear is None:
		return JsonResponse({"success": False}, status=500)
	
	fiscalyear.name=data['name'].replace(' ', '')
	data['start_date'] = data['start_date'].replace(' ', '')
	data['end_date'] = data['end_date'].replace(' ', '')
	fiscalyear.active=data['active']
	fiscalyear.status=data['status']
	success = True
	try:
		fiscalyear.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminPricingSaveRateGroup(request, groupId):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	print(data)
	rategroup = RateGroup.objects.get(pk=groupId)
	rategroup.name = data['name']
	rategroup.description = data['description']
	if data['status'] != -1:
		rategroup.status = data['status']
	if data['active'] != -1:
		rategroup.active = data['active']
	success = True
	try:
		rategroup.save()
		publications = PubRategroup.objects.filter(rategroup=rategroup)
		for publication in publications:
			publication.delete()
		pub_ids = json.loads(data['assigned_publications'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = publication)
			new_pub_rategroup.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)

def adminPricingSaveRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	rate = Rate.objects.get(pk = int(data['id']))
	rate.name=data['name']
	rate.pricing=data['pricing']
	rate.measurement_type=data['measurement_type']
	rate.tax_category=data['tax_category']
	rate.override_privileges=data['override_privileges']
	rate.assigned_groups=data['assigned_groups']
	rate.ad_type_id=data['ad_type']
	rate.start_date=data['start_date']
	rate.end_date=data['end_date']
	rate.insertion_min=data['insertion_min']
	rate.insertion_max=data['insertion_max']
	rate.line_for_ad_min=data['line_for_ad_min']
	rate.line_for_ad_max=data['line_for_ad_max']
	rate.insertion_count=data['insertion_count']
	rate.base_cost=data['base_cost']
	rate.base_count=data['base_count']
	rate.additional_cost=data['additional_cost']
	rate.additional_count=data['additional_count']
	rate.charge_for=data['charge_for']
	rate.default_gl_code_id=data['default_gl_code']
	success = True
	try:
		rate.save()
		# extra_groups = ExtraRateGroup.objects.filter(rate = rate)
		# for group in extra_groups:
		# 	group.delete()
		# extra_groups = json.loads(data['extra_groups'])
		# for id in extra_groups:
		# 	rategroup = RateGroup.objects.get(pk=id)
		# 	new_extra_group = ExtraRateGroup(rate=rate, rategroup=rategroup)
		# 	new_extra_group.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminPricingEditRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	print(data)
	rate = Rate.objects.get(pk = data['id'])
	extra_groups = ExtraRateGroup.objects.filter(rate = data['id']).select_related('rategroup')
	assigned_groups = [{'id': pa.rategroup.id, 'name': pa.rategroup.name} for pa in extra_groups]
	print(assigned_groups)
	response_data = {
			'id': rate.id,
			'rate': serializers.serialize('json', [rate]),
			'start_date': rate.start_date.isoformat(),
			'end_date': rate.end_date.isoformat(),
			'assigned_groups': assigned_groups,
	}
	return JsonResponse(response_data)

def adminPricingCreateRateGroup(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	rategroup = RateGroup(name = data['name'], description = data['description'], active = data['active'])
	success = True
	try:
		rategroup.save()
		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = publication)
			new_pub_rategroup.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)
def adminPricingEditRateGroup(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	rategroup = RateGroup.objects.get(pk=groupId)
	publications = AdminPublication.objects.all()
	rate_id = ExtraRateGroup.objects.filter(rategroup=groupId)
	rate_ids = []
	for rate in rate_id:
		rate_ids.append(rate.rate.id)
	rates = Rate.objects.filter(id__in=rate_ids)
	assigned_publications = []
	unsigned_publications = publications
	adtypes = AdminAdType.objects.all()
	glcodes = GLCode.objects.all()
	extra_groups = RateGroup.objects.exclude(id=groupId)
	pub_rategroups = PubRategroup.objects.filter(rategroup=rategroup.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.adminpublication.id, 'name': pa.adminpublication.name} for pa in pub_rategroups]
	pub_ids = []
	for pub_rategroup in pub_rategroups:
		pub_ids.append(pub_rategroup.adminpublication.id)

	pub_rategroups = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_rategroups]
	context = {
		'rategroup': rategroup, 
		'assigned_publications': assigned_publications, 
		'publications': publications, 
		'unsigned_publications': unsigned_publications,
		'adtypes': adtypes,
		'glcodes': glcodes,
		'extra_groups': extra_groups,
		'rates': rates,
	}
	return render(request, 'admin/pricing/edit-rategroup.html', context)

def adminPricingCreateRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_rate = Rate(name=data['name'], pricing=data['pricing'], measurement_type=data['measurement_type'], tax_category=data['tax_category'], override_privileges=data['override_privileges'], 
								 assigned_groups=data['assigned_groups'], ad_type_id=data['ad_type'], start_date=data['start_date'], end_date=data['end_date'],
								 insertion_min=data['insertion_min'], insertion_max=data['insertion_max'], line_for_ad_min=data['line_for_ad_min'], line_for_ad_max=data['line_for_ad_max'],
								 insertion_count=data['insertion_count'], base_cost=data['base_cost'], base_count=data['base_count'], additional_cost=data['additional_cost'], 
								 additional_count=data['additional_count'], charge_for=data['charge_for'], default_gl_code_id=data['default_gl_code'])
	success = True
	try:
		new_rate.save()
		extra_groups = json.loads(data['extra_groups'])
		for id in extra_groups:
			rategroup = RateGroup.objects.get(pk=id)
			new_extra_group = ExtraRateGroup(rate=new_rate, rategroup=rategroup)
			new_extra_group.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)

def adminClassifieds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	publications = Publication.objects.all()
	styles = ClassifiedStyle.objects.all()
	styles_publications = ClassifiedPublicationStyle.objects.all()
	
	# Add the arrays to the context
	context = {
		'publications': publications,
		'styles': styles,
		'styles_publications': styles_publications
	}
	return render(request, 'admin/classifieds/classifieds.html', context)

def adminSavePublication(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	pub = AdminPublication.objects.get(pk=id)
	pub.name = data['name']
	pub.address = data['address']
	pub.city = data['city']
	pub.state_id = data['state']
	pub.zip_code = data['zip_code']
	pub.product_name = data['product_name']
	pub.gl_override = data['gl_override']
	pub.gl_code_id = data['gl_code']
	pub.start_date = data['start_date']
	# pub.end_date = data['end_date']
	pub.calendar_type = data['calendar_type']
	product_type= 'digital'
	product = DigitalProduct.objects.filter(product_mag=data['product_name']).first()
	if not product:
		product = NewspaperProduct.objects.filter(product_mag=data['product_name']).first()
		product_type= 'newspaper'

	if not product:
		product = MagazineProduct.objects.filter(product_mag=data['product_name']).first()

		product_type= 'magazine'
	if not product:
		product_type = 'custom'
	

	pub.product_type = product_type
	pub.active = data['active']
	pub.status = data['status']
	pub.repeat = data['repeat']
	pub.schedule_type = data['schedule_type']
	pub.run_days = data['run_days']
	success = True
	try:
		pub.save()
		if data['calendar_type'] == 'non-repeating':
			schedules = AdminPublicationSchedule.objects.filter(adminpublication=pub)
			for schedule in schedules:
				schedule.delete()
			for schedule in data['schedules']:
				new_schedule = AdminPublicationSchedule(product_name = schedule['product_name'], product_type = schedule['product_type'], start_date = schedule['start_date'], end_date = schedule['end_date'],
																						gl_override = schedule['gl_override'], gl_code_id = int(schedule['gl_code']), adminpublication = pub)
				new_schedule.save()
		rategroups = PubRategroup.objects.filter(adminpublication=pub)
		for rategroup in rategroups:
			rategroup.delete()
		rategroup_ids = json.loads(data['rategroup_id'])
		for id in rategroup_ids:
			rategroup = RateGroup.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = pub)
			new_pub_rategroup.save()
		adminadtypes = PubAdType.objects.filter(adminpublication=pub)
		for adminadtype in adminadtypes:
			adminadtype.delete()
		adtype_ids = json.loads(data['adtype_id'])
		for id in adtype_ids:
			adtype = AdminAdType.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype = adtype, adminpublication = pub)
			new_pub_adtype.save()
		adminadjustments = PubAdjustment.objects.filter(adminpublication=pub)
		for adminadjustment in adminadjustments:
			adminadjustment.delete()
		adjustment_ids = json.loads(data['adjustment_id'])
		for id in adjustment_ids:
			adjustment = AdminAdjustment.objects.get(pk=id)
			new_pub_adjustment = PubAdjustment(adminadjustment = adjustment, adminpublication = pub)
			new_pub_adjustment.save()
		sections = PubSection.objects.filter(adminpublication=pub)
		for section in sections:
			section.delete()
		section_ids = json.loads(data['section_id'])
		for id in section_ids:
			section = PublicationSection.objects.get(pk=id)
			new_pub_section = PubSection(adminsection = section, adminpublication = pub)
			new_pub_section.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({'success': success}, status = 200)
def adminCreatePublication(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	print(data)
	new_publication = AdminPublication(name = data['name'], address = data['address'], city = data['city'], state_id = int(data['state']), zip_code=data['zip_code'],
																		location = '', parent_id = data['parent_id'], product_name = data['product_name'], gl_override = data['gl_override'],account = 'Times Leader',
																		gl_code_id = int(data['gl_code']), start_date = data['start_date'], end_date = data['end_date'], created_by = data['created_by'], run_days = data['run_days'],
																		calendar_type = data['calendar_type'], product_type = data['product_type'], schedule_type = data['schedule_type'], repeat = data['repeat'])
	success = True
	print(new_publication)
	try:
		new_publication.save()
		if data['calendar_type'] == 'non-repeating':
			for schedule in data['schedules']:
				new_schedule = AdminPublicationSchedule(product_name = schedule['product_name'], product_type = schedule['product_type'], start_date = schedule['start_date'], end_date = schedule['end_date'],
																						gl_override = schedule['gl_override'], gl_code_id = int(schedule['gl_code']), adminpublication = new_publication)
				new_schedule.save()
		rategroup_ids = json.loads(data['rategroup_id'])
		for id in rategroup_ids:
			rategroup = RateGroup.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = new_publication)
			new_pub_rategroup.save()
		adtype_ids = json.loads(data['adtype_id'])
		for id in adtype_ids:
			adtype = AdminAdType.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype = adtype, adminpublication = new_publication)
			new_pub_adtype.save()
		adjustment_ids = json.loads(data['adjustment_id'])
		for id in adjustment_ids:
			adjustment = AdminAdjustment.objects.get(pk=id)
			new_pub_adjustment = PubAdjustment(adminadjustment = adjustment, adminpublication = new_publication)
			new_pub_adjustment.save()
		section_ids = json.loads(data['section_id'])
		for id in section_ids:
			section = PublicationSection.objects.get(pk=id)
			new_pub_section = PubSection(adminsection = section, adminpublication = new_publication)
			new_pub_section.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({'success': success}, status = 200)
def adminEditPublication(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	pub = AdminPublication.objects.get(pk=id)
	gl_codes = GLCode.objects.all()
	publications = AdminPublication.objects.all()
	all_states = AllStates.objects.all()
	pub_rategroups = PubRategroup.objects.filter(adminpublication=pub.id).select_related('rategroup')
	assigned_rategroups = [{'id': pa.rategroup.id, 'name': pa.rategroup.name} for pa in pub_rategroups]
	rategroup_ids = []
	for pub_rategroup in pub_rategroups:
		rategroup_ids.append(pub_rategroup.rategroup.id)

	unsigned = RateGroup.objects.exclude(id__in=rategroup_ids)
	unsigned_rategroups = [{'id': pa.id, 'name': pa.name} for pa in unsigned]

	pub_adminadtypes = PubAdType.objects.filter(adminpublication=pub.id).select_related('adminadtype')
	assigned_adminadtypes = [{'id': pa.adminadtype.id, 'name': pa.adminadtype.name} for pa in pub_adminadtypes]
	adminadtype_ids = []
	for pub_adminadtype in pub_adminadtypes:
		adminadtype_ids.append(pub_adminadtype.adminadtype.id)

	unsigned = AdminAdType.objects.exclude(id__in=adminadtype_ids)
	unsigned_adminadtypes = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	
	pub_adminadjustments = PubAdjustment.objects.filter(adminpublication=pub.id).select_related('adminadjustment')
	assigned_adminadjustments = [{'id': pa.adminadjustment.id, 'name': pa.adminadjustment.name} for pa in pub_adminadjustments]
	adminadjustment_ids = []
	for pub_adminadjustment in pub_adminadjustments:
		adminadjustment_ids.append(pub_adminadjustment.adminadjustment.id)

	unsigned = AdminAdjustment.objects.exclude(id__in=adminadjustment_ids)
	unsigned_adminadjustments = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	
	pub_sections = PubSection.objects.filter(adminpublication=pub.id).select_related('adminsection')
	assigned_sections = [{'id': pa.adminsection.id, 'name': pa.adminsection.name} for pa in pub_sections]
	section_ids = []
	for pub_section in pub_sections:
		section_ids.append(pub_section.adminsection.id)

	unsigned = PublicationSection.objects.exclude(id__in=section_ids)
	unsigned_sections = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	run_days = json.loads(pub.run_days)
	daysOfWeek = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat']
	schedules = AdminPublicationSchedule.objects.filter(adminpublication = id)
	start_date = pub.start_date.isoformat()
	end_date = None
	if pub.end_date:
		end_date = pub.end_date.isoformat()

	magazines = MagazineProduct.objects.all()
	newspapers = NewspaperProduct.objects.all()
	digitals = DigitalProduct.objects.all()
    # Combine all products into a single list
	combined_products = list(magazines) + list(newspapers) + list(digitals)
	context = {
        "access": "allow",
        "message": "",
        "gl_codes": gl_codes,
				"publications": publications,
				"all_states": all_states,
				"assigned_rategroups": assigned_rategroups,
				"unsigned_rategroups": unsigned_rategroups,
				"assigned_adminadtypes": assigned_adminadtypes,
				"unsigned_adminadtypes": unsigned_adminadtypes,
				"assigned_adminadjustments": assigned_adminadjustments,
				"unsigned_adminadjustments": unsigned_adminadjustments,
				"assigned_sections": assigned_sections,	
				"unsigned_sections": unsigned_sections,
				"pub": pub,
        "days_of_week": daysOfWeek,
				"run_days": run_days,
				"schedules": schedules,
				"start_date": start_date,
				"end_date": end_date,
				"products":combined_products	
    }
	return render(request, 'admin/pubs/edit-publication.html', context)
def adminNewPublication(request):
    # Check if user is logged in, if not, redirect to login screen
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + '/')
    
    adTypes = AdminAdType.objects.all()
    gl_codes = GLCode.objects.all()
    magazines = MagazineProduct.objects.all()
    newspapers = NewspaperProduct.objects.all()
    digitals = DigitalProduct.objects.all()
    adjustments = AdminAdjustment.objects.all()
    rategroups = RateGroup.objects.all()
    sections = PublicationSection.objects.all()
    publications = AdminPublication.objects.all()
    all_states = AllStates.objects.all()
    # Combine all products into a single list
    combined_products = list(magazines) + list(newspapers) + list(digitals)

    context = {
        "access": "allow",
        "message": "",
        "adtypes": adTypes,
        "gl_codes": gl_codes,
        "products": combined_products,
        "adjustments": adjustments,
        "rategroups": rategroups,
        "sections": sections,
        "publications": publications,
        "all_states": all_states
    }
    return render(request, 'admin/pubs/new-publication.html', context)


def adminNewMagazine(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request.method == 'GET':
		standardsizes = StandardSize.objects.filter(type = 2)
		return render(request, 'admin/products/new-magazine.html', {'standardsizes': standardsizes})
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = MagazineProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = MagazineProduct(
		product_mag =  data['product_mag'],
		measurement_type = data['measurement_type'],
		fold_orientation = data['fold_orientation'],
		height = data['height'],
		width = data['width'],
		columns = data['columns'],
		column_width = data['column_width'],
		page_width = data['page_width'],
		page_height = data['page_height'],
		page_border = data['page_border'],
		gutter_size = data['gutter_size']
	)
	success = True
	try:
		task.save()
		for id in data['sizes']:
			size = StandardSize.objects.get(pk = id)
			print(size)
			new_product_size = MagazineSize(product = task, size = size)
			new_product_size.save()
	except Exception as e:
		success = False
		print(e)
	return JsonResponse({'success': success}, status = 200)
def adminEditMagazine(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = MagazineProduct.objects.get(pk=id)
	standardsizes = StandardSize.objects.filter(type = 2)
	selectedsizes = MagazineSize.objects.filter(product = product)
	sizes = []
	for size in standardsizes:
		active = False
		for selected in selectedsizes:
			if size.id == selected.size_id:
				sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': True,'total_columns_in':size.total_columns_in})
				active = True
		if active == False:
			sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': False,'total_columns_in':size.total_columns_in})
	return render(request, 'admin/products/edit-magazine.html', {'product': product, 'standardsizes': sizes})

def adminSaveMagazine(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = MagazineProduct.objects.get(pk=id)
	success = True
	if 'status_only' in data:
		product.active = data['active']
		try:
			product.save()
		except Exception as e:
			success = False
	else:
		product.product_mag = data['product_mag']
		product.measurement_type = data['measurement_type']
		product.fold_orientation = data['fold_orientation']
		product.height = data['height']
		product.width = data['width']
		product.columns = data['columns']
		product.column_width = data['column_width']
		product.page_width = data['page_width']
		product.page_height = data['page_height']
		product.page_border = data['page_border']
		product.gutter_size = data['gutter_size']
		try:
			product.save()
			sizes = MagazineSize.objects.filter(product = product)
			for size in sizes:
				size.delete()
			for id in data['sizes']:
				size = StandardSize.objects.get(pk = id)
				new_product_size = MagazineSize(product = product, size = size)
				new_product_size.save()
		except Exception as e:
			success = False
	return JsonResponse({'success': success}, status = 200)

def adminNewNewspaper(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request.method == 'GET':
		standardsizes = StandardSize.objects.filter(type = 1)
		return render(request, 'admin/products/new-newspaper.html', {'standardsizes': standardsizes})
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = NewspaperProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = NewspaperProduct(
		product_mag =  data['product_mag'],
		measurement_type = data['measurement_type'],
		fold_orientation = data['fold_orientation'],
		height = data['height'],
		width = data['width'],
		columns = data['columns'],
		column_width = data['column_width'],
		page_width = data['page_width'],
		page_height = data['page_height'],
		page_border = data['page_border'],
		gutter_size = data['gutter_size']
	)
	success = True
	try:
		task.save()
		for id in data['sizes']:
			size = StandardSize.objects.get(pk = id)
			print(size)
			new_product_size = NewspaperSize(product = task, size = size)
			new_product_size.save()
	except Exception as e:
		success = False
		print(e)
	return JsonResponse({'success': success}, status = 200)

def adminEditNewspaper(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = NewspaperProduct.objects.get(pk=id)
	standardsizes = StandardSize.objects.filter(type = 1)
	selectedsizes = NewspaperSize.objects.filter(product = product)
	sizes = []
	for size in standardsizes:
		active = False
		for selected in selectedsizes:
			if size.id == selected.size_id:
				sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': True,'total_columns_in':size.total_columns_in})
				active = True
		if active == False:
			sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': False,'total_columns_in':size.total_columns_in})
	return render(request, 'admin/products/edit-newspaper.html', {'product': product, 'standardsizes': sizes})

def adminSaveNewspaper(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = NewspaperProduct.objects.get(pk=id)
	success = True
	if 'status_only' in data:
		product.active = data['active']
		try:
			product.save()
		except Exception as e:
			success = False
	else:
		product.product_mag = data['product_mag']
		product.measurement_type = data['measurement_type']
		product.fold_orientation = data['fold_orientation']
		product.height = data['height']
		product.width = data['width']
		product.columns = data['columns']
		product.column_width = data['column_width']
		product.page_width = data['page_width']
		product.page_height = data['page_height']
		product.page_border = data['page_border']
		product.gutter_size = data['gutter_size']
		try:
			product.save()
			sizes = NewspaperSize.objects.filter(product = product)
			for size in sizes:
				size.delete()
			for id in data['sizes']:
				size = StandardSize.objects.get(pk = id)
				new_product_size = NewspaperSize(product = product, size = size)
				new_product_size.save()
		except Exception as e:
			success = False
	return JsonResponse({'success': success}, status = 200)

def adminNewDigital(request):
	if request.method == 'GET':
		adtypes = AdminAdType.objects.all()
		standardsizes = StandardSize.objects.filter(type = 3)
		return render(request, 'admin/products/new-digital.html', {'adtypes': adtypes, 'standardsizes': standardsizes})
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = DigitalProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = DigitalProduct(
		product_mag =  data['product_mag'],
		format = data['format'],
		adminadtype_id = data['adminadtype'],
		height = data['height'],
		width = data['width'],
	)
	success = True
	try:
		task.save()
		for id in data['sizes']:
			size = StandardSize.objects.get(pk = id)
			new_product_size = DigitalSize(product = task, size = size)
			new_product_size.save()
	except Exception as e:
		success = False
		print(e)
	return JsonResponse({'success': success}, status = 200)

def adminEditDigital(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = DigitalProduct.objects.get(pk=id)
	adtypes = AdminAdType.objects.all()
	standardsizes = StandardSize.objects.filter(type = 3)
	selectedsizes = DigitalSize.objects.filter(product = product)
	sizes = []
	for size in standardsizes:
		active = False
		for selected in selectedsizes:
			if size.id == selected.size_id:
				sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': True,'total_columns_in':size.total_columns_in})
				active = True
		if active == False:
			sizes.append({'id': size.id, 'description': size.description, 'columns': size.columns, 'height': size.height, 'status': size.status, 'active': False,'total_columns_in':size.total_columns_in})
	return render(request, 'admin/products/edit-digital.html', {'product': product, 'standardsizes': sizes, 'adtypes': adtypes})

def adminSaveDigital(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = DigitalProduct.objects.get(pk=id)
	success = True
	if 'status_only' in data:
		product.active = data['active']
		try:
			product.save()
		except Exception as e:
			success = False
	else:
		product.product_mag = data['product_mag']
		product.format = data['format']
		product.adminadtype_id = data['adminadtype']
		product.height = data['height']
		product.width = data['width']
		try:
			product.save()
			sizes = DigitalSize.objects.filter(product = product)
			for size in sizes:
				size.delete()
			for id in data['sizes']:
				size = StandardSize.objects.get(pk = id)
				new_product_size = DigitalSize(product = product, size = size)
				new_product_size.save()
		except Exception as e:
			success = False
	return JsonResponse({'success': success}, status = 200)

def adminCreateStandardSize(request):
	body = request.body.decode('utf-8')
	data = json.loads(body)
	standardsize = StandardSize(type = data['type'], description = data['description'], columns = data['columns'], height = data['height'])
	success = True
	try:
		standardsize.save()
	except Exception as e:
		success = False		
	return JsonResponse({'success': success, "errors": [], 'id': standardsize.id}, status=200)
def adminCreateRegion(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_region = Region(name = data['name'], code = data['code'])
	success = True
	try:
		new_region.save()
		pub_regions = json.loads(data['publication_id'])
		for id in pub_regions:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_region = PubRegion(region = new_region, adminpublication = publication)
			new_pub_region.save()
	except Exception as e:
		success = False
	return JsonResponse({"success":success, "id": new_region.id, "errors": []}, status=200)
def adminEditRegion(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	region = Region.objects.get(pk=data['id'])
	region.name = data['name']
	region.code = data['code']
	region.active = data['active']
	region.status = data['status']
	region.save()
	pub_regions = PubRegion.objects.filter(region=region)
	for pub_region in pub_regions:
		pub_region.delete()

	pub_ids = json.loads(data['publication_id'])
	for id in pub_ids:
		publication = AdminPublication.objects.get(pk=id)
		new_pub_region = PubRegion(region=region, adminpublication=publication)
		new_pub_region.save()

	return JsonResponse({"errors": []}, status=200)
def adminRegionDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	region = Region.objects.get(pk=data['id'])
	pub_regions = PubRegion.objects.filter(region=region.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.adminpublication.id, 'name': pa.adminpublication.name} for pa in pub_regions]
	pub_ids = []
	for pub_region in pub_regions:
		pub_ids.append(pub_region.adminpublication.id)

	unsigned = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in unsigned] 

	response_data = {
			'id': region.id,
			'region': serializers.serialize('json', [region]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)
def adminCreateMarketCode(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_adminmarketcode = AdminMarketCode(name = data['name'], code = data['code'])
	success = True
	try:
		new_adminmarketcode.save()
	except Exception as e:
		success = False
	return JsonResponse({"success":success, "errors": []}, status=200)
def adminEditMarketCode(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	marketcode = AdminMarketCode.objects.get(pk=data['id'])
	success = True
	if 'status_only' in data:
		marketcode.active = data['active']
		try:
			marketcode.save()
		except Exception as e:
			success = False
	else:
		marketcode.name = data['name']
		marketcode.code = data['code']
		marketcode.active = data['active']
		marketcode.status = data['status']
		success = True
		try:
			marketcode.save()
		except Exception as e:
			success = False
	return JsonResponse({"success":success, "errors": []}, status=200)
def adminMarketCodeDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	marketcode = AdminMarketCode.objects.get(pk=data['id'])

	response_data = {
			'id': marketcode.id,
			'marketcode': serializers.serialize('json', [marketcode]),
	}
	return JsonResponse(response_data, safe=False)

@csrf_exempt
def clear_session(request):
	if request.method == 'POST':
		try:
			if 'style_id' in request.session:
				del request.session['style_id']
				return JsonResponse({'success': True})
		except Exception as e:
			pass
	return JsonResponse({'success': False}, status=200)

def create_style(data):
	success = {}

	try:
		style_id = data.get('style_id', None)
		style = ClassifiedStyle.objects.get(pk=style_id)
	except Exception as e:
		style = ClassifiedStyle()

	style.name = data['name']
	style.self_service_status = True if data.get('self_service_status') == 'yes' else False
	
	try:
		style.save()
		success['style_id'] = style.id
		success['status'] = True
	except Exception as e:
		success['status'] = False
	return success

def create_style_publication(data):
	success = {}
	for publication in data.get('selectedPublications', None):
		try:
			publication_style = ClassifiedPublicationStyle.objects.get(style_id=data['style_id'], publication_id=publication)
		except Exception as e:
			publication_style = ClassifiedPublicationStyle()

		publication_style.style_id = data['style_id']
		publication_style.publication_id = publication
		publication_style.save()
	
	try:
		ClassifiedPublicationStyle.objects.filter(style_id=data['style_id']).exclude(publication_id__in=data.get('selectedPublications', [])).delete()
		success['status'] = True
	except Exception as e:
		print(e)
	return success

def update_status_available_for_service_status(request, pk):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')

	if request.method == 'GET':
		style_id = pk
		is_status = request.GET.get('is_status', None)
		status_value = request.GET.get('status', None)

		is_available_for_service = request.GET.get('is_available_for_service', None)
		available_for_service_value = request.GET.get('self_service_status', None)

		if style_id is None:
			return JsonResponse({'success': False}, status=500)
		else:
			try:
				style = ClassifiedStyle.objects.get(pk=style_id)
				if not is_status == 'null':
					if status_value == 'true':
						style.status = True
					else:
						style.status = False
				elif not is_available_for_service == 'null':
					if available_for_service_value == 'true':
						style.self_service_status = True
					else:
						style.self_service_status = False
				style.save()
				return JsonResponse({'success': True}, status=200)
			except Exception as e:
				return JsonResponse({'success': False}, status=500)

def list_style_publications(request, pk):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	if request.method == 'GET':
		style_id = pk
		if style_id is None:
			return JsonResponse({'success': False}, status=500)
		else:
			style_publications = ClassifiedPublicationStyle.objects.filter(style_id=style_id).values('publication_id').distinct()
			publications_data = Publication.objects.filter(pk__in=[publication['publication_id'] for publication in style_publications])

			publications_list = []
			for publication in publications_data:
				publications_list.append({
					'id': publication.id,
					'name': publication.name,
					'address': publication.address,
					'city': publication.city,
					'state': publication.state,
					'zip_code': publication.zip_code,
					'spot_color': publication.spot_color,
					'charge_tax': publication.charge_tax,
					'credit_memo': publication.credit_memo
				})
			return JsonResponse({'success': True, 'style_publications': publications_list}, status=200)

@transaction.atomic
def create_font_color(data=None):
	if data == None:
		return JsonResponse({'success': False}, status=500)
	
	style_id = data.get('style_id', None)
	colors = data.get('colors', None)
	fonts = data.get('fonts', None)

	ClassifiedStyleFontColor.objects.filter(style_id=style_id).delete()

	for color in colors:
		color_obj, created = ClassifiedStyleFontColor.objects.update_or_create(
			style_id=style_id,
			color=color,
			defaults={'color': color}
		)

	for font in fonts:
		font_obj, created = ClassifiedStyleFontColor.objects.update_or_create(
			style_id=style_id,
			font=font,
			defaults={'font': font}
		)

	return JsonResponse({'success': True}, status=200)

@transaction.atomic
def create_font_specs(data=None):
	if data == None or data.get('style_id') is None:
		return JsonResponse({'success': False}, status=500)
	
	try:
		font_spec_obj = ClassifiedStyleFontSpec.objects.get(style_id=data.get('style_id'))
		font_spec_obj.delete()
		font_spec_obj = ClassifiedStyleFontSpec()
	except Exception as e:
		font_spec_obj = ClassifiedStyleFontSpec()

	font_spec_obj.style_id = data.get('style_id')
	font_spec_obj.specs = data.get('specs')
	font_spec_obj.save()

	return True

@csrf_exempt
def handle_classified_style_creation_progress(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')

	data = json.loads(request.body.decode('utf-8'))

	step_name = data.get('step_name', None)
	data = data.get('data', None)

	if step_name is None:
		return JsonResponse({'success': False}, status=500)
	
	if step_name == 'style_creation_step':
		style_id = request.session.get('style_id')
		if style_id is not None:
			data['style_id'] = style_id
		success_creation = create_style(data)
		if not success_creation.get('status'):
			return JsonResponse({'success': False}, status=500)
		else:
			data['style_id'] = success_creation.get('style_id')
			request.session['style_id'] = success_creation.get('style_id')
			if data.get('style_id') is None:
				return JsonResponse({'success': False}, status=500)
			else:
				success_publication_creation = create_style_publication(data)
				if not success_publication_creation:
					ClassifiedStyle.objects.get(pk=data.get('style_id')).delete()
					return JsonResponse({'success': False}, status=500)
	elif step_name == 'font_color_creation_step':
		style_id = request.session.get('style_id')
		if style_id is not None:
			data['style_id'] = style_id
			colors = data.get('selectedColors', None)
			fonts = data.get('fontNames', None)
			data = {
				'style_id': style_id,
				'colors': colors,
				'fonts': fonts
			}
			success_font_color_creation = create_font_color(data)
			if not success_font_color_creation:
				return JsonResponse({'success': False}, status=500)
	elif step_name == 'font-spec-step':
		style_id = request.session.get('style_id')
		if style_id is not None:
			new_data = {}
			new_data['specs'] = data
			new_data['style_id'] = style_id
			success_font_spec_creation = create_font_specs(new_data)
			if not success_font_spec_creation:
				return JsonResponse({'success': False}, status=500)
	elif step_name == 'final-step':
		style_id = request.session.get('style_id')
		if style_id is not None:
			try:
				del request.session['style_id']
			except Exception as e:
				print(e)
			return JsonResponse({'success': True, 'style_id' : style_id}, status=200)
	return JsonResponse({'success': step_name, 'style_id' : data.get('style_id')}, status=200)