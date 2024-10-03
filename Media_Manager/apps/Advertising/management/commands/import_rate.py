import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Rate, AdType, GLCode ,RateGroup,ExtraRateGroup # Update with your app name
from datetime import datetime

class Command(BaseCommand):
    help = 'Import rate data from Excel into the database'

    def handle(self, *args, **kwargs):
        # Load the Excel file and specify the sheet name
        file_path = '/home/developer/Documents/TL rate upload (1).xlsx'  # Replace with your file path
        df = pd.read_excel(file_path, sheet_name='Upload')
        ad_types = AdType.objects.all()

        # Iterate through the rows of the DataFrame
        for index, row in df.iterrows():
            # Convert date strings to datetime objects
            start_date = row['Start Date'].date() if pd.notna(row['Start Date']) else None
            if row['End Date (optional)'] == '(open)':
                end_date = None
            elif isinstance(row['End Date (optional)'], str):
                end_date = datetime.strptime(row['End Date (optional)'], '%m/%d/%Y')
            else:
                end_date = row['End Date (optional)'] 
            # Check if 'Ad Type' is null, and handle accordingly
            # if pd.notna(row['Ad Type']):
                # ad_type, _ = AdType.objects.get_or_create(name=row['Ad Type'])

            # Get or create the related ForeignKey instances
            gl_code, _ = GLCode.objects.get_or_create(code=row['Default GL Code (Optional)'])

            # Insert the data into the Rate model
            for ad_type in ad_types:
               rate = Rate.objects.create(
                    name=row['Rate Code'],
                    pricing=(row['Pricing '] == 'Standard'),
                    measurement_type=row['Measurement Type'],
                    tax_category=row['Tax Category'],
                    override_privileges=(row['Override Previlieges'] == 'Yes'),
                    active=True,
                    assigned_groups=(row['Assign Rate to other Groups'] == 'Yes'),
                    ad_type=ad_type,  # This can be None if the Ad Type is null
                    start_date=start_date,
                    end_date=end_date,
                    insertion_min=row['Min Number of Insertions'],
                    insertion_max=row['Max Number of Insertions'],
                    line_for_ad_min=row['Min Number of X for an ad'],
                    line_for_ad_max=row['Max number of X for an ad'],
                    insertion_count=row['Enter No. of Insertions'],
                    base_cost=row['Base Cost'],
                    base_count=row['No. of X allowed for starting Charge'],
                    additional_cost=row['Additional Cost (optional)'],
                    additional_count=row['No of extra X'],
                    charge_for=(row['Number of insertions toggle'] == 'On'),
                    account=None,  # Adjust if you have an Account object
                    default_gl_code=gl_code,
                    status=1  # Assuming status is always 1
                )
            rate_group = RateGroup.objects.latest('id')
            extra_rate_group = ExtraRateGroup.objects.create(rate=rate,rategroup=rate_group)

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
