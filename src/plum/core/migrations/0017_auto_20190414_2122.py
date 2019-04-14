# Generated by Django 2.2 on 2019-04-14 19:22

from django.conf import settings
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20190414_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address_city',
            field=models.CharField(default='', max_length=190, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='account',
            name='address_country',
            field=django_countries.fields.CountryField(default='DE', max_length=2, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='account',
            name='address_street',
            field=models.CharField(default='', max_length=190, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='account',
            name='address_supplement',
            field=models.CharField(blank=True, default='', max_length=190, verbose_name='Address supplement'),
        ),
        migrations.AddField(
            model_name='account',
            name='address_vat_id',
            field=models.CharField(blank=True, default='', help_text='If you are located in the EU but outside Germany, we need your VAT ID. If you do not provide one, we will need to charge you VAT on our services and can not issue reverse charge invoices.', max_length=190, verbose_name='EU VAT ID'),
        ),
        migrations.AddField(
            model_name='account',
            name='address_zipcode',
            field=models.CharField(default='', max_length=190, verbose_name='ZIP code'),
        ),
        migrations.AddField(
            model_name='account',
            name='primary_email',
            field=models.EmailField(default='', help_text='We will contact you at this address for everything concerning your contract, billing, invoices, and important informations about your purchases.', max_length=254, verbose_name='Primary contact email'),
        ),
        migrations.AddField(
            model_name='account',
            name='primary_name',
            field=models.CharField(default='', max_length=190, verbose_name='Primary contact person'),
        ),
        migrations.AddField(
            model_name='account',
            name='primary_phone',
            field=models.CharField(default='', max_length=190, verbose_name='Contact phone number'),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=190, verbose_name='Company name'),
        ),
        migrations.AlterField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
