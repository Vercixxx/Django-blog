# Generated by Django 4.2.3 on 2023-08-23 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_technology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technology',
            name='image',
            field=models.ImageField(upload_to='images/tech'),
        ),
    ]
