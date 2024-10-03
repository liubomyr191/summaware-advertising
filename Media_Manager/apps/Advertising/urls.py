from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views, ajax, admin, api

urlpatterns = [
	path('', views.advertising_view, name='advertising_view'),
	path('account/new/', views.create_account, name='create_account'),

	# Account Routes
	path('account/<int:id>/', views.advertising_account, name='advertising_account'),
	path('account/<int:id>/edit/', views.edit_advertising_account, name="edit_account"),
	path('account/types/new/', views.create_account_type, name='create_account_type'),
	path('account/import/', views.import_account_data, name='import_account_data'), # TODO - implement this route
    path('account/names/', views.get_account_names, name="get_account_names"),

	# Sales Person Routes
	path('salesperson/all/', views.list_salesperson, name='list_salesperson'),
	path('salesperson/new/', views.create_salesperson, name='create_salesperson'),
    path('salesperson/success/', views.success_salesperson, name='success_salesperson'),
	path('salesperson/<int:id>/', views.view_salesperson, name='view_salesperson'),
    path('salesperson/<int:id>/ad-assistants/', views.salesperson_ad_assistants, name='salesperson_ad_assistants'),

	path('merge/', views.merge_account, name='merge_account'),
	# TODO - path('account/<int:id>/merge', views.merge_account, name='merge_account') <- this sets the account from the id as the "account A"

	# Account Contacts Routes
	path('account/<int:id>/company-contacts/new/', views.create_company_contact, name='create_company_contact'),
	path('account/<int:id>/company-contacts/', views.list_company_contacts, name='list_company_contacts'),
    # path('account/<int:id>/company-contacts/<int:contact_id>/', views.company_contact_details, name='company_contact_details'),
	path('account/<int:id>/company-contacts/<int:contact_id>/edit/', views.edit_company_contact, name='edit_company_contact'),

	path('account/<int:accountId>/company-contacts/<int:contactId>/', views.account_contact_details, name='account_contact_details'),
    path('account/<int:accountId>/company-contacts/<int:contactId>/action', views.account_contact_action, name='account_contact_action'),

	# Ad Type Routes
	path('ad-types/', views.list_ad_types, name='list_ad_types'),
	path('ad_types/<int:ad_type_id>/delete', views.delete_ad_type, name='delete_ad_type'),

	# Ad Campaign Routes
	path('campaign-home', views.adHome, name='adHome'),
	path('campaign-dashboard', views.adDashboard, name='adDashboard'),

	# Publication Routes
    # path('publication/sections/new/', views.create_multiple_publication_section, name='create_multiple_publication_section'),

	path('publication-dashboard', views.pubDashboard, name='pubDashboard'),
	path('publication/new/', views.create_publication, name="create_publication"),
	path('publication/<int:id>/', views.view_publication, name="view_publication"),
	path('publication/<int:id>/edit/', views.edit_publication, name='edit_publication'),
    path('publication/<int:id>/run-days/', views.get_publication_run_days, name="get_publication_run_days"),
	path('publications/colors/', views.get_spot_colors, name="get_spot_colors"),
    path('publications/<int:publication_id>/styles/', views.default_styles_details, name="default_styles_details"),
    path('publications/<int:publication_id>/styles/new/', views.create_default_styles, name="create_default_styles"),

	# Deadline Routes 
	path('publication/<int:publication_id>/deadlines/', views.view_ad_deadlines, name="view_ad_deadlines"),
	path('publication/<int:publication_id>/deadlines/new', views.new_ad_deadline, name="new_ad_deadline"),
    path('publication/<int:publication_id>/deadlines/<int:deadline_id>/', views.ad_deadlines_details, name="ad_deadlines_details"),
	# path('publication/<int:publication_id>/deadlines/<int:deadline_id>/edit', views.edit_ad_deadlines, name="edit_ad_deadlines"),

	# Page Dimension Routes
	path('publication/<int:publication_id>/page-dimensions/', views.get_publication_page_dimensions, name='get_publication_page_dimensions'), 
	path('publication/<int:publication_id>/page-dimensions/new/', views.new_page_dimensions, name="new_page_dimensions"),
	path('publication/<int:publication_id>/page-dimensions/edit/', views.edit_page_dimensions, name="edit_page_dimensions"),
    
	# Publication Section Routes

	path('publication/<int:publication_id>/sections/new/', views.create_publication_section, name='create_publication_section'),
    path('publication/<int:publication_id>/sections/<int:section_id>/', views.publication_section_details, name='publication_section_details'), 

	# Rate Routes
	path('rate/new/', views.create_rate, name='create_rate'),
	path('rates/', views.list_rates, name='list_rates'),
	path('rate/<int:rate_id>', views.view_rate, name='view_rate'),
	path('rate/<int:id>/edit/', views.edit_rate, name='edit_rate'),
    path('rate/<int:rate_id>/details/', views.get_rate_details, name='get_rate_details'),
	path('account/<int:account_id>/rates/', views.list_account_rates, name="list_account_rates"),
    path('company/rates/', views.list_company_rates, name="list_company_rates"),
    
	path('rate/gl-codes/', views.view_rate_gl_codes, name='view_rate_gl_codes'),
	path('rate/<int:rateId>/gl-codes/', views.get_rate_gl_codes, name="get_rate_gl_codes"),
    path('rate/<int:rateId>/publications/', views.get_rate_publications, name="get_rate_publications"),
    path('rate/<int:rateId>/publication/gl-codes/', views.get_rate_publication_gl_codes, name="get_rate_publication_gl_codes"),

	path('special-rates/', views.list_special_rates, name="list_special_rates"),

	# Rate Location Routes
	path('rates/locations/', views.list_rate_locations, name='list_rate_locations'),
	path('rates/locations/new/', views.add_rate_location, name='add_rate_location'),

	# Order Routes
	path('order/new/', views.create_order, name='create_order'),
	path('order/new/<int:id>', views.create_order, name='create_order'),
	path('orders/', views.list_orders, name='list_orders'),
	path('order/<int:id>/', views.view_order, name='view_order'),
	path('order/<int:id>/edit', views.edit_order, name='edit_order'),
	path('account/<int:id>/orders/', views.list_account_orders, name='list_account_orders'),
	path('publication/<int:id>/orders/', views.list_publication_orders, name='list_publication_orders'),
	path('order/<int:orderId>/cancel/', views.cancel_order, name='cancel_order'),
	path('order/<int:orderId>/clone/', views.clone_order, name='clone_order'),

	path('order/dev/', views.create_order_dev, name='create_order_dev'),

	# TODO - fix this page (remove the Django form)
	path('order/<int:orderId>/insertion/<int:insertionId>/edit/', views.edit_insertion, name="edit_insertion"),

	# Service Charge Routes 
	path('service-charges/', views.list_service_charges, name='list_service_charges'),
	path('service-charges/new/', views.create_service_charge, name='create_service_charge'),
	path('service-charges/<int:charge_id>/edit/', views.edit_service_charge, name='edit_service_charge'),
	path('order/<int:id>/add-charge/', views.create_account_service_charge, name="create_account_service_charge"),

	# GL Codes Routes
	path('gl-code-dashboard/', views.gl_code_dashboard, name='gl_code_dashboard'),
	path('gl-codes/', views.list_gl_codes, name='list_gl_codes'),
	path('create-gl-code/', views.newGlCode, name='newGlCode'),
	path('gl-codes/new/', views.create_gl_code, name='create_gl_code'),
    path('gl-codes/<int:code_id>/', views.gl_code_details, name='gl_code_details'),
	path('gl-codes/<int:code_id>/edit/', views.edit_gl_code, name='edit_gl_code'),
	

	# Location Routes
	path('locations/', views.list_location, name='list_location'),
	path('location/new/', views.create_location, name='create_location'),
    path('location/<int:location_id>/', views.location_details, name='location_details'),
	path('location/<int:location_id>/edit/', views.edit_location, name='edit_location'),

	# Ad Rate Routes
	path('ad-rates', views.adRateIndex, name='adRateIndex'),
	path('new-ad-rate', views.newAdRate, name='newAdRate'),
	path('completed-rate', views.completedRate, name='completedRate'),
	path('edit-rate', views.editRate, name='editRate'),

	# Adjustments Routes 
	path('publication/<int:publication_id>/adjustments/', views.list_adjustments, name='list_adjustments'),
	path('publication/<int:publication_id>/adjustments/new/', views.create_adjustment, name='create_adjustment'),
	path('publication/<int:publication_id>/adjustments/<int:adjustment_id>/', views.adjustment_details, name='adjustment_details'),

	# Industry Code Routes
	path('account/<int:account_id>/industry-codes/', views.list_industry_codes, name='list_industry_codes'),
	path('account/<int:account_id>/industry-codes/new', views.create_industry_code, name="create_industry_code"),
	path('account/<int:account_id>/industry-codes/<int:code_id>/edit', views.edit_industry_code, name='edit_industry_code'),

	# Drafts Routes
	path('drafts/', views.list_drafts, name='list_drafts'),
	path('drafts/<int:id>/delete/', views.delete_draft, name='delete_draft'),
	path('account/<int:id>/drafts/', views.list_account_drafts, name='list_account_drafts'),
	path('account/<int:account_id>/drafts/<int:draft_id>/load/', views.load_draft, name='load_draft'),
	path('account/<int:account_id>/drafts/<int:draft_id>/delete/', views.delete_account_draft, name='delete_account_draft'),

	# Ad-Admin Routes
	path('adadmin/', views.admin, name='admin'),
	path('adadmin/general', views.adminGeneral, name='adminGeneral'),
  path('adadmin/general/create-region', views.adminCreateRegion, name='adminCreateRegion'),
  path('adadmin/general/edit-region', views.adminEditRegion, name='adminEditRegion'),
  path('adadmin/general/region-detail', views.adminRegionDetail, name='adminRegionDetail'),
	path('adadmin/ads', views.adminAds, name='adminAds'),
	path('adadmin/ads/create-adtype', views.adminAdsCreateAdType, name='adminAdsCreateAdType'),
	path('adadmin/ads/edit-adtype', views.adminAdsEditAdType, name='adminAdsEditAdType'),
	path('adadmin/ads/adtype-detail', views.adminAdsAdTypeDetail, name='adminAdsAdTypeDetail'),
	path('adadmin/ads/create-marketcode', views.adminCreateMarketCode, name='adminCreateMarketCode'),
	path('adadmin/ads/edit-marketcode', views.adminEditMarketCode, name='adminEditMarketCode'),
	path('adadmin/ads/marketcode-detail', views.adminMarketCodeDetail, name='adminMarketCodeDetail'),
	path('adadmin/financial', views.adminFinancial, name='adminFinancial'),
	path('adadmin/financial/create-fiscalyear', views.adminCreateFiscalYear, name='adminCreateFiscalYear'),
	path('adadmin/financial/fiscalyear-detail', views.adminFiscalYearDetail, name='adminFiscalYearDetail'),
	path('adadmin/financial/edit-fiscalyear', views.adminEditFiscalYear, name='adminEditFiscalYear'),
	path('adadmin/financial/fiscal/<int:id>', views.adminFinancialFiscal, name='adminFinancialFiscal'),
    
	# Accounting Period Routes
	path('adadmin/financial/accounting-periods/', views.adminAccountingPeriods, name='adminCreateAccountingPeriods'),
    path('adadmin/financial/edit-accounting-periods/', views.adminEditAccountingPeriods, name='adminEditAccountingPeriods'),
    path('adadmin/financial/update-status-accounting-period/', views.adminEditAccountingPeriodsStatus, name='adminEditAccountingPeriodsStatus'),
    
	# Company Codes
	path('adadmin/financial/company-codes/', views.create_company_code, name='adminCreateCompanyCodes'),
    path('adadmin/financial/edit-company-codes/', views.edit_company_code, name='adminEditCompanyCodes'),
    path('adadmin/financial/edit-company-codes-status/', views.edit_company_code_status, name='adminEditCompanyCodesStatus'),
    
	# GL Codes
    path('adadmin/financial/edit-gl-codes-status/', views.edit_gl_code_status, name='adminEditGlCodesStatus'),
    path('adadmin/financial/edit-gl-codes/', views.edit_gl_codes, name='adminEditGlCodes'),
    path('adadmin/financial/create-gl-codes/', views.create_gl_codes, name='adminCreateGlCodes'),
    
    
	# Location Codes
    path('adadmin/financial/edit-location-codes-status/', views.edit_location_code_status, name='adminEditLocationCodesStatus'),
    path('adadmin/financial/edit-location-codes/', views.edit_location_code, name='adminEditLocationCodes'),
    path('adadmin/financial/create-location-codes/', views.create_location_code, name='adminCreateLocationCodes'),
    
    
	# Department Codes
    path('adadmin/financial/edit-department-codes-status/', views.edit_department_code_status, name='adminEditDepartmentCodesStatus'),
    path('adadmin/financial/edit-department-codes/', views.edit_department_code, name='adminEditDepartmentCodes'),
    path('adadmin/financial/create-department-codes/', views.create_department_code, name='adminCreateDepartmentCodes'),
   
	# Profit Codes
    path('adadmin/financial/edit-profit-codes-status/', views.edit_profit_code_status, name='adminEditProfitCodesStatus'),
    path('adadmin/financial/edit-profit-codes/', views.edit_profit_code, name='adminEditProfitCodes'),
    path('adadmin/financial/create-profit-codes/', views.create_profit_codes, name='adminCreateProfitCodes'),

    
	path('adadmin/financial/new-magazine', views.adminNewMagazine, name='adminNewMagazine'),
	path('adadmin/financial/new-newspaper', views.adminNewNewspaper, name='adminNewNewspaper'),
	path('adadmin/financial/new-digital', views.adminNewDigital, name='adminNewDigital'),
	path('adadmin/financial/edit-newspaper/<int:id>', views.adminEditNewspaper, name='adminEditNewspaper'),
	path('adadmin/financial/edit-newspaper/<int:id>/save', views.adminSaveNewspaper, name='adminSaveNewspaper'),
	path('adadmin/financial/edit-magazine/<int:id>', views.adminEditMagazine, name='adminEditMagazine'),
	path('adadmin/financial/edit-magazine/<int:id>/save', views.adminSaveMagazine, name='adminSaveMagazine'),
	path('adadmin/financial/edit-digital/<int:id>', views.adminEditDigital, name='adminEditDigital'),
	path('adadmin/financial/edit-digital/<int:id>/save', views.adminSaveDigital, name='adminSaveDigital'),
	path('adadmin/financial/create-standardsize', views.adminCreateStandardSize, name='adminCreateStandardSize'),
	path('adadmin/pricing', views.adminPricing, name='adminPricing'),
	path('adadmin/pricing/create-adjustment', views.adminCreateAdjustment, name='adminCreateAdjustment'),
	path('adadmin/pricing/adjustment-detail', views.adminAdjustmentDetail, name='adminAdjustmentDetail'),
	path('adadmin/pricing/edit-adjustment', views.adminEditAdjustment, name='adminEditAdjustment'),
	path('adadmin/pricing/create-tax', views.adminCreateTax, name='adminCreateTax'),
	path('adadmin/pricing/tax-detail', views.adminTaxDetail, name='adminTaxDetail'),
	path('adadmin/pricing/edit-tax', views.adminEditTax, name='adminEditTax'),
	path('adadmin/pricing/create-rategroup', views.adminPricingCreateRateGroup, name='adminPricingCreateRateGroup'),
	path('adadmin/pricing/edit-rategroup/<int:groupId>', views.adminPricingEditRateGroup, name='adminPricingEditRateGroup'),
	path('adadmin/pricing/edit-rategroup/<int:groupId>/save', views.adminPricingSaveRateGroup, name='adminPricingSaveRateGroup'),
	path('adadmin/pricing/edit-rategroup/<int:groupId>/create-rate', views.adminPricingCreateRate, name='adminPricingCreateRate'),
	path('adadmin/pricing/edit-rategroup/<int:groupId>/edit-rate', views.adminPricingEditRate, name='adminPricingEditRate'),
	path('adadmin/pricing/edit-rategroup/<int:groupId>/save-rate', views.adminPricingSaveRate, name='adminPricingSaveRate'),
	path('adadmin/pubs/new-publication', views.adminNewPublication, name='adminNewPublication'),
  path('adadmin/pubs/create-publication', views.adminCreatePublication, name='adminCreatePublication'),
  path('adadmin/pubs/edit-publication/<int:id>', views.adminEditPublication, name='adminEditPublication'),
  path('adadmin/pubs/edit-publication/<int:id>/save', views.adminSavePublication, name='adminSavePublication'),
  path('adadmin/classifieds', views.adminClassifieds, name='adminClassifieds'),
	
	# Classified styles Routes
    path('adadmin/advertising/clear-session/', views.clear_session, name='adminStylesClearSession'),
    path('adadmin/advertising/list-style-publications/<int:pk>/', views.list_style_publications, name='adminListStylePublications'),
    path('adadmin/classifieds/update-style-self-service-status/<int:pk>/', views.update_status_available_for_service_status, name='adminListStylePublications'),

	path('adadmin/advertising/create-style', views.handle_classified_style_creation_progress, name='adminClassifiedStyles'),
  
	# Admin Routes 
	path('admin/', admin.view_admin_panel, name='view_admin_panel'),
	path('admin/user/<int:userId>/roles', admin.get_user_roles, name="get_user_roles"),
	path('admin/user/<int:userId>/roles/save/', admin.save_user_roles, name="save_user_roles"),
	path('admin/invoices/all/', views.list_all_invoices, name='list_all_invoices'),
	path('admin/invoices/aging-report/', views.view_aging_report, name='view_aging_report'),
	path('admin/manager-overrides/', admin.view_manager_overrides, name='view_manager_overrides'),
    path('admin/permissions/custom-size/', views.custom_size_permission, name='custom_size_permission'),
    
	# Access Control Routes
	path('admin/publication-access/', admin.view_publication_access, name='view_publication_access'),
	path('admin/<int:userId>/publication-access/', admin.user_publication_access, name='user_publication_access'),
    path('admin/account/access/', admin.view_user_account_access, name='view_user_account_access'),
    path('admin/<int:userId>/account-access/', admin.user_account_access, name='user_account_access'),
    
	# Invoicing Routes
	path('account/<int:account_id>/invoices/', views.view_account_invoices, name='view_account_invoices'),
	path('account/<int:account_id>/ledger/', views.account_ledger, name='account_ledger'),
	path('account/<int:account_id>/fiscal-years/', views.view_account_fiscal_years, name='view_account_fiscal_years'),
	path('account/<int:account_id>/invoices/aging-report/', views.view_account_aging_report, name='view_account_aging_report'),

	# Invoices Route
	path('invoice/<int:invoiceId>/pay/', views.pay_invoice, name='pay_invoice'),

	# Transaction Codes Routes
	path('transaction-codes/', views.list_transaction_codes, name='list_transaction_codes'),

	# Company Routes
	path('companies/', views.list_companies, name='list_companies'),
	path('company/new/', views.create_company, name='create_company'),
	path('company/<int:company_id>/', views.view_company_details, name='view_company_details'),
	path('company/<int:company_id>/edit', views.edit_company_details, name='edit_company_details'),
	path('company/<int:company_id>/credit-limits/', views.view_company_credit_limits, name='view_company_credit_limits'),
    path('company/current-company/', views.user_current_company, name='user_current_company'), 
    path('admin/company/access/', views.view_user_company_access, name='view_user_company_access'),
    path('admin/company/user-access/', views.get_user_company_access, name='get_user_company_access'),

	path('new-advertiser/', views.create_advertiser, name='create_advertiser'),
	path('register-advertiser/', views.register_advertiser, name='register_advertiser'),
    
	# Advertiser Dashboard
	path('advertiser_dashboard/', views.advertiser_dashboard, name='advertiser_dashboard'),
    path('advertiser_home/', views.advertiser_home, name='advertiser_home'),

	# Advertisers
  path('advertisers', views.all_advertisers, name='all_advertisers'),
	

	#advertiser walmart edit
	path('edit_new_advertiser/', views.edit_new_advertiser, name='edit_new_advertiser'),
	path('search_filter_contacts/', views.search_filter_contacts, name='search_filter_contacts'),
	path('get_id_contact/', views.get_id_contact, name='get_id_contact'),
	path('delete_id_contact/', views.delete_id_contact, name='delete_id_contact'),
	path('create_contact/', views.create_contact, name='create_contact'),
	path('getTaskList/', views.getTaskList, name='getTaskList'),
	path('taskRemove/', views.taskRemove, name='taskRemove'),
	path('taskSetActivity/', views.taskSetActivity, name='taskSetActivity'),
	path('create_task/', views.create_task, name='create_task'),


	# Classifieds Routes
	path('classifieds/', views.list_classifieds, name='list_classifieds'),
	path('classifieds/ad_types', views.fetch_ad_types, name='fetch_ad_types'),
	path('classifieds/ad_sizes', views.fetch_ad_sizes, name='fetch_ad_sizes'),

	path('classifieds/new/', views.create_classified_ad, name='create_classified_ad'),
    path('classifieds/generate-text-file/', views.generate_text_file, name='generate_text_file'),

	path('classifieds/<int:classifiedId>/', views.view_classified_ad, name='view_classified_ad'),
	path('classifieds/<int:classifiedId>/edit/', views.edit_classified_ad, name='edit_classified_ad'),
	path('classifieds/registerCampaign', views.register_campaign, name='register_campaign'),
	path('classifieds/detail/', views.campaign_detail, name='campaign_detail'),

	path('classifieds/graphics/', views.view_classifieds_graphics, name='view_classifieds_graphics'),
    path('classifieds/graphics/permissions/upload/', views.user_upload_permission, name='user_upload_permission'),
	path('classifieds/graphics/permissions/delete/', views.user_delete_permission, name='user_delete_permission'),
    path('classifieds/graphics/action/', views.classified_graphics_action, name='classified_graphics_action'), 
	
	path('classifieds/adjustments/', views.list_classified_adjustments, name='list_classified_adjustments'),
	path('classifieds/adjustments/<int:adjustmentId>/', views.classified_adjustment_details, name='classified_adjustment_details'),

	path('classifieds/adjustments/publications/', views.get_adjustments_by_publication, name='get_adjustments_by_publication'),
	path('classifieds/rates/', views.get_rates_by_publication, name='get_rates_by_publication'),

	path('classifieds/rates/', views.list_classified_rates, name='list_classified_rates'),
	path('classifieds/rates/new/', views.create_classified_rate, name='create_classified_rate'),
	path('classifieds/rates/info/', views.classified_rate_info, name='info_classified_rate'),
    path('classifieds/rates/edit/', views.classified_rate_edit, name='edit_classified_rate'),
	path('classifieds/rates/<int:rateId>/', views.classified_rate_details, name='classified_rate_details'),
	path('classifieds/rates/<int:rateId>/edit/', views.edit_classified_rate, name='edit_classified_rate'),

	path('classifieds/ad-types/', views.list_classified_ad_types, name='list_classified_ad_types'),
	path('classifieds/ad-types/details/', views.classified_ad_type_details, name='classified_ad_type_details'),

	path('classifications/', views.list_all_classifications, name='list_all_classifications'),
	path('classifications/new/', views.create_classification, name='create_classification'),
	path('classification/<int:id>/details/', views.get_classification_details, name='get_classification_details'),
	path('classification/<int:id>/edit/', views.edit_classification, name='edit_classification'),

	# API Routes
	path('api/current-ads-running/',api.get_current_ads_running, name='get_current_ads_running'),

	# Form Routes
	path('forms/order/new', views.create_order_form, name='create_order_form'),

	# AJAX Requests
	path('ajax/order/late/', ajax.late_order, name="ajax_late_order"),
	path('ajax/order/search/account/', ajax.order_search_account, name="ajax_search_order"),
	path('ajax/order/search/rates/', ajax.order_search_rates, name="ajax_search_rates"),
	path('ajax/order/search/rate-details/', ajax.order_search_rate_details, name="ajax_search_rate_details"),
	path('ajax/order/search/adjustments/', ajax.order_search_adjustments, name="ajax_search_adjustment"),
	path('ajax/order/subtotal/', views.order_subtotal, name="ajax_order_subtotal"),
	path('ajax/order/edit/rates/', ajax.edit_order_rates, name='edit_order_rates'),

	path('ajax/order/search/details/', views.search_order_details, name='order_search_details'),
	path('ajax/order/search/publication/', views.search_order_publication, name='search_order_publication'),

	path('ajax/rate/get-rate-location/', ajax.get_rate_location, name="ajax_get_rate_location"),
	path('ajax/search/account/', ajax.search_account, name="ajax_search_account"),
	
	path('ajax/company/accounts/', ajax.company_account_list, name='ajax_company_account_list'),
    
	path('ajax/account/<int:account_id>/', ajax.account_details, name="ajax_account_details"),
	path('ajax/account/<int:id>/notes/', ajax.get_account_notes, name="ajax_account_notes"),
	path('ajax/account/<int:id>/salesrep/<int:sales_rep_id>/notes/', ajax.get_salesrep_notes, name="ajax_salesrep_notes"),
	path('ajax/account/<int:account_id>/notes/<int:note_id>/', ajax.edit_account_note, name="ajax_edit_account_note"),
	path('ajax/account/<int:account_id>/salesrep/<int:sales_rep_id>/notes/<int:note_id>/', ajax.edit_salesrep_note, name="ajax_edit_salesrep_note"),
	path('ajax/account/<int:id>/salesperson/', views.get_account_salesperson_details, name='get_account_salesperson_details'),
	
	path('ajax/publications/', views.get_publication_list, name='get_publication_list'),
	path('ajax/publication/<int:publication_id>/run-days/', ajax.get_publication_run_days, name="get_publication_run_days"),
	path('ajax/publication/adjustments/', ajax.get_publication_adjustments, name="get_publication_adjustments"),

	path('ajax/import/', ajax.import_gl_codes, name='import_gl_codes'),
	path('ajax/gl-codes/', ajax.get_gl_codes, name='get_gl_codes'),

	path('ajax/<int:salesrep_id>/tasks/', ajax.get_salesreps_tasks, name='get_salesreps_tasks'),
	path('ajax/tasks/new/', ajax.new_salesrep_task, name='new_salesrep_task'),
	path('ajax/tasks/complete/', ajax.mark_task_complete, name='mark_task_complete'),
	path('ajax/tasks/delete/', ajax.delete_salesrep_task, name='delete_task'),

	path('ajax/invoicing/new/', ajax.new_invoice, name='new_invoice'),
	path('ajax/finance/get_accounting_periods', ajax.get_accounting_periods, name='get_accounting_periods'),
	path('ajax/finance/accounting-period/<int:accounting_period_id>/action/', ajax.set_accounting_period_action, name='set_accounting_period_action'),
	path('ajax/accounting_period/invoices/', ajax.get_accounting_period_invoices, name='get_accounting_period_invoices'),
	path('ajax/invoice/details/pay', ajax.get_invoice_payment, name='get_invoice_payment'), 
	path('ajax/invoice/details/', ajax.get_invoice_details, name='get_invoice_details'),

	path('ajax/service-charge/all/', ajax.get_service_charges, name='get_service_charges'),
	path('ajax/service-charge/<int:charge_id>/', ajax.get_service_charge_details, name='get_service_charge_details'),

	path('ajax/manager-overrides/credit-limits/', ajax.override_credit_limit, name='override_credit_limit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)