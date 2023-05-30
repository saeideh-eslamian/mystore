# Generated by Django 3.0.14 on 2023-05-15 14:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='phone_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='shippinaddress',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]