# Generated by Django 4.1.2 on 2022-10-19 08:37

import bill.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0007_alter_bill_bill_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_number',
            field=models.CharField(default=bill.models.bill_number, editable=False, max_length=1500, unique=True),
        ),
    ]
