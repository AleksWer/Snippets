# Generated by Django 4.2.6 on 2023-10-10 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='lang',
            field=models.CharField(choices=[('py', 'Python'), ('js', 'JavaScript'), ('cpp', 'C++')], max_length=30),
        ),
    ]