# Generated by Django 4.1.3 on 2022-12-06 10:15

from django.db import migrations, models
import jewellery.models


class Migration(migrations.Migration):

    dependencies = [
        ('jewellery', '0004_alter_pearl_options_alter_pearl_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateField(default=jewellery.models.get_due_date, verbose_name='due date'),
        ),
    ]
