# Generated by Django 2.2.5 on 2019-10-23 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0002_auto_20191023_1908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboard',
            options={'permissions': [('accounting_access', 'Can access Accounting section'), ('advertising_access', 'Can access Advertising section'), ('bi_access', 'Can access Business Intelligence section'), ('circulation_access', 'Can access Circulation section'), ('editorial_access', 'Can access Editorial section'), ('production_access', 'Can access Production section')]},
        ),
    ]
