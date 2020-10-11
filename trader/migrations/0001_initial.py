# Generated by Django 3.1.1 on 2020-10-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=25)),
                ('balance', models.DecimalField(decimal_places=4, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('shares', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('orderDate', models.DateField()),
            ],
        ),
    ]
