# Generated by Django 3.2.7 on 2021-11-22 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_source', '0011_cashdeposit_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='mess',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_source.mess'),
        ),
    ]