# Generated by Django 3.2.7 on 2021-11-22 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_source', '0008_amountspend_person_spend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountspend',
            name='person_spend',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]