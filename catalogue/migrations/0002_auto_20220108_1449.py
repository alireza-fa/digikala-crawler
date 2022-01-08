# Generated by Django 3.2 on 2022-01-08 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImageLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='productattribute',
            name='title',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
