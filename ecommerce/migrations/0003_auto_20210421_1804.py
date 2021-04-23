# Generated by Django 3.1.7 on 2021-04-21 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_genre',
            new_name='product_model',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='page_number',
            new_name='product_size',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='author',
            new_name='seller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_number',
        ),
        migrations.RemoveField(
            model_name='product',
            name='publisher',
        ),
        migrations.RemoveField(
            model_name='product',
            name='translator',
        ),
        migrations.RemoveField(
            model_name='product',
            name='year',
        ),
    ]
