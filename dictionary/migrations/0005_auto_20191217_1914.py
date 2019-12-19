# Generated by Django 3.0 on 2019-12-17 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_dataset_template_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='template_name',
            field=models.CharField(blank=True, default='content.html', help_text='Example: “flatpages/contact_page.html”. If this isn’t provided, the system will use “flatpages/default.html”.', max_length=70, verbose_name='template name'),
        ),
    ]
