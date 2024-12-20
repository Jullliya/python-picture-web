# Generated by Django 5.1.2 on 2024-11-09 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analyse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='user id')),
                ('image', models.FileField(upload_to='', verbose_name='image')),
                ('first_model', models.CharField(max_length=8, verbose_name='model 1')),
                ('second_model', models.CharField(max_length=8, verbose_name='model 2')),
                ('third_model', models.CharField(max_length=8, verbose_name='model 3')),
                ('result', models.CharField(max_length=8, verbose_name='result')),
            ],
        ),
    ]
