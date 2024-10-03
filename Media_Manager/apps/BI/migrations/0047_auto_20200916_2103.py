# Generated by Django 2.2.5 on 2020-09-16 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0046_auto_20200910_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboard',
            name='organization',
        ),
        migrations.AddField(
            model_name='chart',
            name='allowed_individuals',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='chart',
            name='allowed_role_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='chart',
            name='allowed_user_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='allowed_individuals',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='allowed_role_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='allowed_user_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_chart',
            name='allowed_individuals',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_chart',
            name='allowed_role_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_chart',
            name='allowed_user_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_dashboard',
            name='allowed_individuals',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_dashboard',
            name='allowed_role_groups',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user_dashboard',
            name='allowed_user_groups',
            field=models.TextField(default=''),
        ),
    ]