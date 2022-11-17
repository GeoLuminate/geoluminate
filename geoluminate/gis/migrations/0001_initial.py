# Generated by Django 3.2.16 on 2022-11-09 10:35

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import geoluminate.fields
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeographicLocation',
            fields=[
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=13)),
                ('poly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name': 'continent',
                'verbose_name_plural': 'continents',
                'db_table': 'core_gis_geographiclocation',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='23456789ABCDEFGHJKLMNPQRSTUVWXYZ', length=10, max_length=15, prefix='GHFS-', primary_key=True, serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('elevation', geoluminate.fields.RangeField(blank=True, help_text='elevation with reference to mean sea level (m)', null=True, validators=[django.core.validators.MaxValueValidator(9000), django.core.validators.MinValueValidator(-12000)], verbose_name='elevation (m)')),
                ('geographic', models.ForeignKey(blank=True, help_text='Continent land boundaries', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site', to='geoluminate_gis.geographiclocation', verbose_name='continent')),
            ],
            options={
                'verbose_name': 'Geographic site',
                'verbose_name_plural': 'Geographic sites',
                'db_table': 'core_gis_site',
                'default_related_name': 'site',
            },
        ),
    ]
