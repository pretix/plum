# Generated by Django 2.2 on 2019-04-15 13:32

from django.db import migrations, models
import plum.core.models.product


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190414_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productscreenshot',
            name='picture',
            field=models.ImageField(upload_to=plum.core.models.product.screenshot_filename, verbose_name='Picture'),
        ),
    ]
