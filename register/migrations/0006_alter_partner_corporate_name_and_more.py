# Generated by Django 4.1.1 on 2022-10-19 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_alter_partner_options_remove_partner_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='corporate_name',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='partner',
            name='fantasy_name',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]
