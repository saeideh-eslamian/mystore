# Generated by Django 3.0.14 on 2023-05-16 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20230515_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Comment'),
        ),
    ]
