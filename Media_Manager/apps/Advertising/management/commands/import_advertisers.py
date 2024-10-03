import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Account, AccountType, SalesPerson, IndustryCode

class Command(BaseCommand):
    help = 'Imports accounts from a specific sheet in an Excel file into the Account model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file.')
        parser.add_argument('--sheet', type=str, default='ALL TL Customers 7 15 2024_2024', help='The name of the sheet to import from.')

    def handle(self, *args, **options):
        file_path = options['file_path']
        sheet_name = options['sheet']

        # Load the Excel file using pandas and the specified sheet name
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading the Excel file: {str(e)}'))
            return

        self.stdout.write(self.style.SUCCESS('Starting the import process...'))
        # Iterate through each row in the DataFrame and insert it into the model
        for index, row in df.iterrows():
            try:
                # Handle ForeignKey relations (AccountType, SalesPerson, IndustryCode)
                account_type, _ = AccountType.objects.get_or_create(name=row['Account Type'],code=row['Acount Type Code'])
                sales_person, _ = SalesPerson.objects.get_or_create(company=row['Salesperson'],first_name=row['Salesperson'],last_name=row['Salesperson'] )
                industry_code, _ = IndustryCode.objects.get_or_create(code=row['Acount Type Code'],description=row['Acount Type Code'])
                print(index)

                # Create and save the Account object
                account = Account(
                    submitter='alex@summaware.com',
                    account_type=account_type,
                    account_number=row['Account Number '],
                    alt_account_number=row['Alt Account Number'],
                    customer_number = row['Customer Number'],
                    sales_person=sales_person,
                    industry_code=industry_code,
                    name=row['Label Line 2'],
                    contact_name_first=row['First Name'],
                    contact_name_last=row['Last Name'],
                    company_name_1=row['Company 1'],
                    company_name_2=row['Company 2'],
                    address=row['Address 1'],
                    address_2=row['Address 2'],
                    city=row['City'],
                    state=row['State'],
                    zip_code=row['Zip'],
                    country=row['Country'],
                    phone=row['Phone'],
                    email=row['Email'],
                    url=row['URL'],
                    website=row['URL'],
                    balance=row['Balance'],
                    account_type_code=row['Acount Type Code'],
                    account_type_descr=row['Account Type Descr'],
                    business_unit=row['Business Unit'],
                    active=bool(row['Active']),
                    export_ar=bool(row['Export AR']),
                    subscriber=bool(row['Subscriber']),
                    credit_limit=row['Credit Limit'],
                    tax_exempt=bool(row['Tax Exempt']),
                    in_collection=bool(row['In Collection']),
                    notify_manager=bool(row['Notify Manager']),
                    do_not_publish=bool(row['Do Not Publish']),
                    no_new_ads=bool(row['No New Ads']),
                    setaside_new_ads_code=row['Setaside New Ads Code'],
                    setaside_new_ads_descr=row['Setaside New Ads Descr'],
                    prepay_required=bool(row['Prepay Required']),
                    prepay_cash_required=bool(row['Prepay Cash Required']),
                    po_required=bool(row['PO Required']),
                    label_line_1=row['Label Line 1'],
                    label_line_2=row['Label Line 2'],
                    label_line_3=row['Label Line 3'],
                    label_line_4=row['Label Line 4'],
                    label_line_5=row['Label Line 5'],
                    label_line_6=row['Label Line 6'],
                )
                account.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully imported account: {account.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing row {index}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import process completed.'))
