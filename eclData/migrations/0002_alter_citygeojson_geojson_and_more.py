# Generated by Django 4.1.6 on 2023-03-17 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eclData", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="citygeojson", name="geojson", field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="countrygeojson", name="geojson", field=models.TextField(),
        ),
    ]