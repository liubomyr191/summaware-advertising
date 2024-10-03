from email.policy import default
from django import forms
from django.forms.fields import CharField, ChoiceField, EmailField

from .models.advertising import Account, AccountType, SalesPerson, CompanyContact
from .models.orders import AdvertisingOrder, AdType, Insertion, AdDeadline, RateLocation
from .models.rates import AdvertisingRate, SpecialRate
from .models.finance import ServiceCharge
from .models.publications import Publication
from .models.companies import GLCode

from ckeditor.widgets import CKEditorWidget

publications = [(pub.id, pub.name) for pub in Publication.objects.all()]
acct_types = [(type.id, type.name) for type in AccountType.objects.all()]
salespeople = [(person.id, str(person.id) + " - " + person.first_name + " " + person.last_name) for person in
               SalesPerson.objects.all()]
accounts = [(account.id, account.name) for account in Account.objects.all() if account.archived != 1]
ad_rates = [(rate.id, rate.name) for rate in AdvertisingRate.objects.all()]
ad_types = [(type.id, type.name) for type in AdType.objects.all()]
charges = [(charge.id, charge.name) for charge in ServiceCharge.objects.all()]
gl_codes = [(code.id, code.description) for code in GLCode.objects.all()]

daysOfTheWeek = [('sunday', "Sunday"), ('monday', "Monday"), ('tuesday', "Tuesday"), ('wednesday', "Wednesday"),
                 ('thursday', "Thursday"), ('friday', "Friday"), ('saturday', "Saturday")]

locationChoices = [('static', 'Static'), ('prem_insideCover', 'Inside Cover (Premium)'),
                   ('prem_backCover', 'Back Cover (Premium)'), ('prem_center', 'Center (Premium)')]


class DateInput(forms.DateInput):
    input_type = 'date'


class AdvertisingAccountForm(forms.ModelForm):
    submitter = forms.CharField(label="Submitter")
    account_type = forms.ChoiceField(label="Account Type", widget=forms.Select, choices=acct_types)
    sales_person = forms.ChoiceField(label="Sales Person", widget=forms.Select, choices=salespeople)
    industry_code = forms.CharField(label="Industry Code")
    name = forms.CharField(label="Name", )
    contact_name = forms.CharField(label="Contact Name")
    address = forms.CharField(label="Address")
    city = forms.CharField(label="City")
    state = forms.CharField(label="State")
    zip_code = forms.CharField(label="Zip Code")
    phone = forms.CharField(label="Phone Number")
    email = forms.EmailField(label="Email Address")
    website = forms.CharField(label="Website", required=False)
    notes = forms.Textarea()
    archived = forms.CheckboxInput()
    legacy_id = forms.CharField(label="Legacy ID", required=False)
    billing_email = forms.EmailField(label="Billing Email Address")

    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'notes': forms.HiddenInput(),
            'archived': forms.HiddenInput(),
            'last_modified': forms.HiddenInput(),
            'last_activity': forms.HiddenInput(),
            'last_ad_run': forms.HiddenInput(),
            'balance': forms.HiddenInput(),
        }


class PublicationForm(forms.ModelForm):
    name = forms.CharField(label="Name", )
    runDays = forms.MultipleChoiceField(label="Pubication Days", choices=daysOfTheWeek,
                                        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Publication
        fields = ['name', 'runDays']


class AccountTypesForm(forms.ModelForm):
    code = forms.CharField(label="Code", )
    name = forms.CharField(label="Name", )

    class Meta:
        model = AccountType
        fields = '__all__'


class SalesPersonForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    company = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    notes = forms.Textarea()

    class Meta:
        model = SalesPerson
        fields = '__all__'


class SecondaryContactForm(forms.ModelForm):
    name = CharField(label="Name", )
    email = EmailField(label="Email", )
    phone_number = CharField(label="Phone Number", )
    department = CharField(label="Department", )

    class Meta:
        model = CompanyContact
        fields = '__all__'
        widgets = {
            'account': forms.HiddenInput(),
        }


class MergeAccountForm(forms.Form):
    account1 = forms.ChoiceField(label="Account 1", widget=forms.Select, choices=accounts)
    account2 = forms.ChoiceField(label="Account 2", widget=forms.Select, choices=accounts)


unitTypeChoices = [('word', 'Word'), ('line', 'Line'), ('inch', 'Inch'), ('column', 'Column')]
taxCategoryChoices = [('none', 'No Tax')]
rateTypeChoices = [('rop', 'ROP Display'), ('liner', 'Liner'), ('unit', 'Unit Based'), ('class', 'Class Display')]

sizeChoices = [("quarter_page", "Quarter Page"), ("half_page", "Half Page"), ("full_page", "Full Page")]


class AdvertisingRateForm(forms.ModelForm):
    name = forms.CharField(label="Name", )
    description = forms.CharField(label="Description", )
    unit_type = forms.ChoiceField(label='Unit Type', widget=forms.Select, choices=unitTypeChoices)
    price = forms.FloatField(label="Price Per Unit")
    gl_code = forms.ChoiceField(label='GL Code', widget=forms.Select, choices=gl_codes)
    tax_category = forms.ChoiceField(label='Tax Category', widget=forms.Select, choices=taxCategoryChoices)
    publication = forms.MultipleChoiceField(label="Publications", widget=forms.CheckboxSelectMultiple,
                                            choices=publications)
    ad_type = forms.ChoiceField(label="Rate Type", widget=forms.Select, choices=rateTypeChoices)
    start_date = forms.DateField(label="Start Date", widget=DateInput)
    end_date = forms.DateField(label="End Date", widget=DateInput)
    size = forms.ChoiceField(label="Size", widget=forms.Select, choices=sizeChoices, required=False)
    custom_min_height = forms.IntegerField(label="Custom Minimum Height (inches)", required=False)
    custom_min_width = forms.IntegerField(label="Custom Minimum Width (inches)", required=False)
    custom_max_height = forms.IntegerField(label="Custom Maximum Height (inches)", required=False)
    custom_max_width = forms.IntegerField(label="Custom Maximum Width (inches)", required=False)
    location = forms.ChoiceField(label="Location", widget=forms.Select, choices=locationChoices)
    locked = forms.CheckboxInput()
    account = forms.ChoiceField(label="Account", widget=forms.Select, choices=accounts, required=False)

    class Meta:
        model = AdvertisingRate
        fields = '__all__'
        widgets = {
            'active': forms.HiddenInput(),
            'hidden': forms.HiddenInput()
        }


class AdvertisingOrderForm(forms.ModelForm):
    ad_type = forms.ChoiceField(label="Ad Type", widget=forms.Select, choices=ad_types)
    ad_rate = forms.ChoiceField(label="Ad Rate", widget=forms.Select, choices=ad_rates)
    account = forms.ChoiceField(label="Account", widget=forms.Select, choices=accounts)
    salesperson = forms.ChoiceField(label="Sales Person", widget=forms.Select, choices=salespeople)
    publication = forms.MultipleChoiceField(label="Publication", choices=publications,
                                            widget=forms.CheckboxSelectMultiple)
    start_date = forms.DateField(label="Start Date", widget=DateInput)
    end_date = forms.DateField(label="End Date", widget=DateInput)
    override_ad_cost = forms.CharField(label="Override Ad Cost", required=False)
    tearsheets = forms.CheckboxInput()
    locked = forms.CheckboxInput()
    active = forms.CheckboxInput()
    bill_date = forms.DateField(label="Bill Date", widget=DateInput)

    class Meta:
        model = AdvertisingOrder
        fields = ['ad_type', 'ad_rate', 'account', 'salesperson', 'publication', 'start_date', 'end_date',
                  'override_ad_cost', 'tearsheets', 'locked', 'active', 'bill_date']


class ServiceChargeForm(forms.ModelForm):
    name = forms.CharField(label="Name")
    amount = forms.IntegerField(label="Amount")
    apply_level = forms.ChoiceField(label="Apply Level", widget=forms.Select,
                                    choices=[('account', 'Account'), ('order', 'Order'), ('insertion', 'Insertion')])

    class Meta:
        model = ServiceCharge
        fields = '__all__'


# class AccountServiceChargeForm(forms.ModelForm):
#     charge = forms.ChoiceField(label="Service Charge", widget=forms.Select, choices=charges)
#     account = forms.ChoiceField(label="Account", widget=forms.Select, choices=accounts)
#     order_number = forms.IntegerField(label="Order Number")

#     class Meta:
#         model = AccountServiceCharge
#         fields = '__all__'
#         widgets = {
#             'active': forms.HiddenInput(),
#         }

class AdDeadlineForm(forms.ModelForm):
    account = forms.ChoiceField(label="Account", widget=forms.Select, choices=accounts)
    publication = forms.ChoiceField(label="Publication", widget=forms.Select, choices=publications)
    publication_day = forms.MultipleChoiceField(label="Publication Day", choices=daysOfTheWeek, widget=forms.Select)
    time = forms.TimeField(label="Time", input_formats=('%H:%M %p',))
    ad_type = forms.ChoiceField(label="Ad Type", widget=forms.Select, choices=ad_types)
    days_prior = forms.IntegerField(label="Days Prior")

    class Meta:
        model = AdDeadline
        fields = '__all__'


statuses = [('good', 'Good'), ('late', 'Late'), ('killed', 'Killed')]


class InsertionForm(forms.ModelForm):
    publication = forms.ChoiceField(label="Publication", widget=forms.Select, choices=publications)
    date = forms.DateField(label="Date", widget=DateInput)
    status = forms.ChoiceField(label="Status", widget=forms.Select, choices=statuses)

    class Meta:
        model = Insertion
        fields = ['publication', 'date', 'status']


class RateLocationForm(forms.ModelForm):
    # rate = forms.ChoiceField(label="Ad Rate", widget=forms.Select, choices=ad_rates)
    location = forms.ChoiceField(label="Location", widget=forms.Select, choices=locationChoices)
    publication = forms.ChoiceField(label="Publication", widget=forms.Select, choices=publications)
    price = forms.FloatField(label="Price")

    class Meta:
        model = RateLocation
        fields = '__all__'


class AdTypeForm(forms.ModelForm):
    code = forms.CharField(label="Code",)
    name = forms.CharField(label="Name",)

    class Meta:
        model = AdType
        fields = '__all__'


class ClassifiedsContentForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())
    # content = forms.CharField()
