# Generated by Django 4.1.6 on 2023-03-23 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eclData", "0004_city_costoflivingindex_city_rentindex"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="CostOfLivingPlusRentIndex",
            field=models.CharField(default="0", max_length=50),
            preserve_default=False,
        ),
    ]
