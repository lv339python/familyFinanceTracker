# Generated by Django 2.1.1 on 2018-10-30 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20181012_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='one_time_token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
