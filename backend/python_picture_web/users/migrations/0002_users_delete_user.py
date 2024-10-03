# Generated by Django 5.1.1 on 2024-09-28 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=32, verbose_name='login')),
                ('password', models.CharField(max_length=32, verbose_name='password')),
                ('key', models.IntegerField(verbose_name='key')),
                ('authorization', models.BooleanField(verbose_name='authorization')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
