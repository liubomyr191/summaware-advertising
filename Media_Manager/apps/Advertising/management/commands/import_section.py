from django.core.management.base import BaseCommand
from ...models import PublicationSection

class Command(BaseCommand):
    help = 'Import static publication section data'

    def handle(self, *args, **kwargs):
        # Static data to be imported
        data = [
            {"name": "Section A", "code": "SecA", "default_rates": 0.0, "status": True},
            {"name": "Section B", "code": "SecB", "default_rates": 0.0, "status": True},
            {"name": "Section C", "code": "SecC", "default_rates": 0.0, "status": True},
            {"name": "Sports", "code": "Sports", "default_rates": 0.0, "status": True},
            {"name": "Classifieds", "code": "Classifieds", "default_rates": 0.0, "status": True},
            {"name": "Politics", "code": "Politics", "default_rates": 0.0, "status": True},
            {"name": "Local News", "code": "Local", "default_rates": 0.0, "status": True},
            {"name": "Editorials", "code": "Editorials", "default_rates": 0.0, "status": True},
            {"name": "Weather", "code": "Weather", "default_rates": 0.0, "status": True},
            {"name": "Front Page", "code": "FrontPG", "default_rates": 0.0, "status": True},
            {"name": "Lifestyle", "code": "Lifestyle", "default_rates": 0.0, "status": True},
            {"name": "Opinion", "code": "Opinion", "default_rates": 0.0, "status": True},
            {"name": "Business", "code": "Business", "default_rates": 0.0, "status": True},
            {"name": "Feature", "code": "Feature", "default_rates": 0.0, "status": True},
            {"name": "Comics", "code": "Comics", "default_rates": 0.0, "status": True},
        ]

        # Import data into the PublicationSection model
        for item in data:
            try:
                PublicationSection.objects.create(
                    name=item['name'],
                    code=item['code'],
                    default_rates=item['default_rates'],
                    active=item['status']
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating {item["name"]}: {e}'))

        self.stdout.write(self.style.SUCCESS('Publication section data imported successfully!'))
