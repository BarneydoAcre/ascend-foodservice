# Generated by Django 4.1.1 on 2022-10-25 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0010_alter_partner_city_alter_partner_cnpj_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='person_type',
        ),
        migrations.AddField(
            model_name='partner',
            name='type_client',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='partner',
            name='type_conveyor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='partner',
            name='type_provider',
            field=models.BooleanField(default=False),
        ),
    ]
