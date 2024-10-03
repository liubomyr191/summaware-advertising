import pandas as pd
from django.core.management.base import BaseCommand
from ...models import (
    DigitalProduct, MagazineProduct, NewspaperProduct, StandardSize,
    DigitalSize, MagazineSize, NewspaperSize
)

class Command(BaseCommand):
    help = 'Import product and size data from Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        excel_file = '/home/developer/Documents/Products and standard ad sizes TL (1).xlsx'

        # Process the first sheet: Magazine and Newspaper product details
        df1 = pd.read_excel(excel_file, sheet_name=0, engine='openpyxl')

        for index, row in df1.iterrows():
            product_type = row.get('Product Type', '').strip().lower()
            name = row.get('Name', '').strip()
            measurement_type = row.get('Measurement Type', '').strip()
            fold_orientation = row.get('Fold Orientation', '').strip()
            width = pd.to_numeric(row.get('Product width', 0), errors='coerce') or 0
            height = pd.to_numeric(row.get('Product height', 0), errors='coerce') or 0
            columns = pd.to_numeric(row.get('Columns Per Page', 0), errors='coerce') or 0
            column_width = pd.to_numeric(row.get('Column Width', 0), errors='coerce') or 0
            page_width = pd.to_numeric(row.get('Full Page Ad Width', 0), errors='coerce') or 0
            page_height = pd.to_numeric(row.get('Full Page Ad Height', 0), errors='coerce') or 0
            page_border = pd.to_numeric(row.get('Side Page Border', 0), errors='coerce') or 0
            gutter_size = pd.to_numeric(row.get('Gutter Size', 0), errors='coerce') or 0
            top_border = pd.to_numeric(row.get('Top Boarder', 0), errors='coerce') or 0
            bottom_border = pd.to_numeric(row.get('Bottome Boarder', 0), errors='coerce') or 0

            if product_type == 'magazine':
                MagazineProduct.objects.create(
                    product_mag=name,
                    measurement_type=measurement_type,
                    fold_orientation=fold_orientation,
                    height=height,
                    width=width,
                    columns=columns,
                    column_width=column_width,
                    page_width=page_width,
                    page_height=page_height,
                    page_border=page_border,
                    gutter_size=gutter_size,
                    active=True
                )
            elif product_type == 'newspaper':
                NewspaperProduct.objects.create(
                    product_mag=name,
                    measurement_type=measurement_type,
                    fold_orientation=fold_orientation,
                    height=height,
                    width=width,
                    columns=columns,
                    column_width=column_width,
                    page_width=page_width,
                    page_height=page_height,
                    page_border=page_border,
                    gutter_size=gutter_size,
                    top_border=top_border,
                    bottom_border=bottom_border,
                    active=True
                )

        # Process the fourth sheet: Digital product details
        df4 = pd.read_excel(excel_file, sheet_name=3, engine='openpyxl')

        for index, row in df4.iterrows():
            product_type = row.get('Product Type', '').strip().lower()
            name = row.get('Name', '').strip()
            measurement_type = row.get('Measurement type', '').strip()
            format_type = row.get('Format', '').strip()
            width = pd.to_numeric(row.get('Product width', 0), errors='coerce') or 0
            height = pd.to_numeric(row.get('Product height', 0), errors='coerce') or 0

            if product_type == 'digital':
                DigitalProduct.objects.create(
                    product_mag=name,
                    format=format_type,
                    height=height,
                    width=width,
                    active=True
                )

        # Process the second sheet: Sizes and dimensions for products
        def process_sizes(sheet_name, product_model, size_model, product_type_col):
            df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')

            for index, row in df.iterrows():
                product_type = row.get(product_type_col, '').strip().lower()
                size_description = row.get('Size Description', '').strip()

                columns = pd.to_numeric(row.get('No. of Columns', 0), errors='coerce') or 0
                height_inches = pd.to_numeric(row.get('Height in inches', 0), errors='coerce') or 0

                if product_type in ['broadsheet', 'tab', 'tab: tv book nc', 'tab: tv book ky']:
                    size_instance = StandardSize.objects.create(
                        description=size_description,
                        type=1,  # Example type value
                        columns=columns,
                        height=height_inches  # Assuming 96 DPI
                    )
                    size_model.objects.create(
                        product=product_model.objects.filter(product_mag=product_type).first(),
                        size=size_instance
                    )

                elif product_type in ['magazine 8.25 10.75', 'magazine 8.5 11', 'annual calendar']:
                    size_instance = StandardSize.objects.create(
                        description=size_description,
                        type=2,  # Example type value
                        columns=columns,
                        height=height_inches
                    )
                    size_model.objects.create(
                        product=product_model.objects.filter(product_mag=product_type).first(),
                        size=size_instance
                    )

                elif product_type == 'mini magazine':
                    size_instance = StandardSize.objects.create(
                        description=size_description,
                        type=2,  # Example type value
                        columns=columns,
                        height=height_inches
                    )
                    size_model.objects.create(
                        product=product_model.objects.filter(product_mag=product_type).first(),
                        size=size_instance
                    )

        # Process each sheet with its corresponding models
        process_sizes(1, MagazineProduct, MagazineSize, 'Product')
        process_sizes(1, NewspaperProduct, NewspaperSize, 'Product')

        # Process the third sheet: Digital product sizes
        df3 = pd.read_excel(excel_file, sheet_name=2, engine='openpyxl')

        for index, row in df3.iterrows():
            product_type = row.get('Product', '').strip().lower()
            size_description = row.get('Size Description', '').strip()
            width_pixels = pd.to_numeric(row.get('Width in pixels', 0), errors='coerce') or 0
            height_pixels = pd.to_numeric(row.get('Height in pixels', 0), errors='coerce') or 0
            columns = pd.to_numeric(row.get('No. of Columns', 0), errors='coerce') or 0
            height_inches = pd.to_numeric(row.get('Height in inches', 0), errors='coerce') or 0

            if product_type in ['desktop web display', 'mobile web display']:
                size_instance = StandardSize.objects.create(
                    description=size_description,
                    type=3,  # Example type value
                    columns=width_pixels,
                    height=height_pixels  # Assuming 96 DPI
                )
                DigitalSize.objects.create(
                    product=DigitalProduct.objects.filter(product_mag=product_type).first(),
                    size=size_instance
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
