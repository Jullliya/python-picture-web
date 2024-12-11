# Generated by Django 5.1.1 on 2024-12-11 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_analyse_user_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyse',
            name='datetime',
            field=models.CharField(default='27-11-2024 00:00:00', max_length=128, verbose_name='date'),
        ),
        migrations.AddField(
            model_name='analyse',
            name='description',
            field=models.TextField(default='Patient analyse description.', verbose_name='description'),
        ),
        migrations.AddField(
            model_name='analyse',
            name='patient',
            field=models.CharField(default='patient', max_length=32, verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='analyse',
            name='image',
            field=models.ImageField(upload_to='images/', verbose_name='image'),
        ),
    ]
