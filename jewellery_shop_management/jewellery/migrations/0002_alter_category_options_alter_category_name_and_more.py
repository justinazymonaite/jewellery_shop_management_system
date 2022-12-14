# Generated by Django 4.1.3 on 2022-12-01 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewellery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Enter the name of jewellery category', max_length=80, verbose_name='category'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='reviewproduct',
            name='review',
            field=models.TextField(max_length=2000, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(help_text='Choose category(-ies) for this product', to='jewellery.category', verbose_name='category(-ies)'),
        ),
    ]
