# Generated by Django 4.1.2 on 2022-10-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0005_alter_bill_product_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='product_key',
            field=models.ManyToManyField(db_constraint=False, to='bill.productdescription'),
        ),
    ]
