# Generated by Django 3.2.3 on 2022-02-08 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userbase',
            options={'verbose_name': 'Accounts', 'verbose_name_plural': 'Accounts'},
        ),
    ]
