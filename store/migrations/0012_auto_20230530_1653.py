# Generated by Django 3.0.14 on 2023-05-30 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20230530_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.ShippinAddress'),
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='city',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='phone_number',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='zipcode',
            field=models.IntegerField(default=''),
        ),
    ]
