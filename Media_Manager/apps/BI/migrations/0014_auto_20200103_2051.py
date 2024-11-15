# Generated by Django 2.2.5 on 2020-01-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0013_auto_20200103_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='attributes',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='chart',
            name='groups_bys',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='chart',
            name='order_bys',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='chart',
            name='query',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='chart',
            name='title',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='chart',
            name='wheres',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='charts',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='drilldowns',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='filters',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='name',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mail',
            name='message',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='task',
            name='subject',
            field=models.TextField(max_length=250),
        ),
    ]
