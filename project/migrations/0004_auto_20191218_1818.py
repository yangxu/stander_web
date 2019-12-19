# Generated by Django 3.0 on 2019-12-18 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20191218_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproject',
            name='template_name',
            field=models.CharField(blank=True, help_text='Example: “flatpages/contact_page.html”. If this isn’t provided, the system will use “flatpages/default.html”.', max_length=70, verbose_name='template name'),
        ),
        migrations.AddField(
            model_name='project',
            name='template_name',
            field=models.CharField(blank=True, help_text='Example: “flatpages/contact_page.html”. If this isn’t provided, the system will use “flatpages/default.html”.', max_length=70, verbose_name='template name'),
        ),
    ]