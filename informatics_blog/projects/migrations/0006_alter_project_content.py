# Generated by Django 3.2.4 on 2021-07-15 20:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20210706_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
