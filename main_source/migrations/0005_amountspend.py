# Generated by Django 3.2.7 on 2021-11-21 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_source', '0004_meals'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountSpend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spend_on', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('mess', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_source.mess')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
