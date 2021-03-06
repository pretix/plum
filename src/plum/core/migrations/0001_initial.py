# Generated by Django 2.2 on 2019-04-13 13:59

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import plum.core.models.product


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Category name')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Version name')),
                ('release_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Variable name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Name')),
                ('long_description', models.TextField(verbose_name='Long description')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved and visible')),
                ('certified', models.BooleanField(default=False, verbose_name='Certified plugin')),
                ('stability', models.CharField(choices=[('alpha', 'alpha'), ('beta', 'beta'), ('stable', 'stable')], max_length=190)),
                ('delivery_method', models.CharField(choices=[('pypi', 'PyPI'), ('pip', 'Local python package index')], max_length=190)),
                ('is_paid', models.BooleanField(default=False)),
                ('pricing_timeframe', models.CharField(choices=[('monthly', 'monthly'), ('yearly', 'yearly'), ('lifetime', 'one-off')], max_length=190, null=True, verbose_name='Pricing timeframe')),
                ('github_url', models.URLField(blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Category', verbose_name='Product category')),
                ('pricing_tiers_variable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.PriceVariable', verbose_name='Pricing variable')),
            ],
            options={
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Name')),
                ('certified', models.BooleanField(default=False, verbose_name='Certified vendor')),
                ('support_contact_phone', models.CharField(blank=True, max_length=190, verbose_name='Support phone number')),
                ('support_contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Support email address')),
                ('support_contact_url', models.URLField(blank=True, verbose_name='Support form URL')),
                ('support_contact_info', models.TextField(blank=True, verbose_name='Additional support information')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Version name')),
                ('release_date', models.DateField()),
                ('release_notes', models.TextField(blank=True)),
                ('deliverable_url', models.URLField(blank=True)),
                ('deliverable_file', models.FileField(null=True, upload_to=plum.core.models.product.deliverable_filename)),
                ('max_platform_version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products_upto', to='core.PlatformVersion', verbose_name='Maximum platform version')),
                ('min_platform_version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products_from', to='core.PlatformVersion', verbose_name='Minimum platform version')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='core.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(upload_to=plum.core.models.product.screenshot_filename, verbose_name='Picture')),
                ('title', models.CharField(max_length=190, verbose_name='title')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='core.Product')),
            ],
            options={
                'verbose_name': 'Screenshot',
            },
        ),
        migrations.CreateModel(
            name='ProductPriceTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_to_value', models.IntegerField(verbose_name='Maximum value of pricing variable')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiers', to='core.Product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
