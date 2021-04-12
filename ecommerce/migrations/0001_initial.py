# Generated by Django 3.1.7 on 2021-04-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30, primary_key=True, serialize=False)),
                ('address', models.TextField(max_length=200, null=True)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
    ]
