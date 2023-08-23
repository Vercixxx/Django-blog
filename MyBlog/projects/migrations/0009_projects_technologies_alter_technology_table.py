# Generated by Django 4.2.3 on 2023-08-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_technology_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='technologies',
            field=models.ManyToManyField(to='projects.technology'),
        ),
        migrations.AlterModelTable(
            name='technology',
            table='Technology',
        ),
    ]
