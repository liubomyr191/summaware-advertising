# Generated by Django 2.2.5 on 2019-11-18 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0005_auto_20191030_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='filters',
            field=models.CharField(default='{}', max_length=5000),
            preserve_default=False,
        ),
    ]
