# Generated by Django 3.1.1 on 2022-12-29 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20221229_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryproduct',
            name='image',
            field=models.ImageField(null=True, upload_to='products/images'),
        ),
    ]