# Generated by Django 2.2.7 on 2019-11-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0008_auto_20191115_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='image',
            field=models.ImageField(null=True, upload_to='rent/static/rent/img/'),
        ),
    ]
