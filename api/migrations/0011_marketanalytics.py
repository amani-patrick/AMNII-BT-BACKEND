# Generated by Django 5.1.5 on 2025-02-08 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('loss', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
