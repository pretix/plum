# Generated by Django 2.2 on 2019-04-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190414_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='productversion',
            name='deliverable_file_checksum',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='package_name',
            field=models.CharField(max_length=190, null=True, unique=True),
        ),
    ]
