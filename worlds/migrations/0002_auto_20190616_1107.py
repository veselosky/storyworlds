# Generated by Django 2.2.2 on 2019-06-16 15:07

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worlds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worlds.Place'),
        ),
        migrations.AddField(
            model_name='place',
            name='geo_detail',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326, verbose_name='detailed geography'),
        ),
        migrations.AddField(
            model_name='place',
            name='point_location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='point location'),
        ),
    ]