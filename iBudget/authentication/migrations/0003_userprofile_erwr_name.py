# Generated by Django 2.1.1 on 2018-09-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180921_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='erwr_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
