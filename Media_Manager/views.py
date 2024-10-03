def get_groups(request):
	groups = []
	if request is not None and request.user.is_authenticated:
		for g in request.user.groups.all():
			groups.append(g.name)
	return groups
	
def get_sidebar(request):
	check_list = ["BI.accounting_access", "BI.advertising_access", "BI.bi_access", "BI.circulation_access", "BI.editorial_access", "BI.financial_access", "BI.production_access"]
	return_list = []

	for item in check_list:
		if request.user.has_perm(item):
			return_list.append(item)
	return return_list

