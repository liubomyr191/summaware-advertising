from django import forms

class DashboardPropertiesForm(forms.Form):
	STATUS_CHOICES = (
		(0, 'Active'),
		(1, 'Inactive'),
	)
	TAGS_CHOICES = (
		(0,'Ads'),
		(1,'Preprints'),
		(2, 'Other'),
	)

	dashboardName = forms.CharField()
	dashboardDescription = forms.CharField(widget=forms.Textarea)
	dashboardStatus = forms.ChoiceField(choices=STATUS_CHOICES)
	dashboardTags = forms.MultipleChoiceField(choices=TAGS_CHOICES, required=False)

class ChartPropertiesForm(forms.Form):
	TYPE_CHOICES = (
		(0,'Table'),
		(1,'Chart'),
	)
	STATUS_CHOICES = (
		(0, 'Active'),
		(1, 'Inactive'),
	)
	chartName = forms.CharField()
	chartType = forms.ChoiceField(choices=TYPE_CHOICES)
	chartStatus = forms.ChoiceField(choices=STATUS_CHOICES)