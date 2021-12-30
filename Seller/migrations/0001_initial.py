# Generated by Django 4.0 on 2021-12-30 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('cardmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Buyer.cardmodel')),
                ('seller_id', models.CharField(default=None, max_length=1000, primary_key=True, serialize=False)),
                ('abn', models.BigIntegerField()),
                ('package', models.IntegerField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer', unique=True)),
            ],
            bases=('Buyer.cardmodel',),
        ),
    ]
