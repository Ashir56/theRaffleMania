# Generated by Django 4.0 on 2021-12-24 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Buyer', '0001_initial'),
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('genericmodels_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Buyer.genericmodels')),
                ('product_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('productName', models.CharField(max_length=50, null=True)),
                ('shortDesc', models.CharField(max_length=150, null=True)),
                ('product_status', models.BooleanField(default=False, max_length=1)),
                ('detailDesc', models.CharField(max_length=350, null=True)),
                ('product_price', models.IntegerField(null=True)),
                ('ticket_price', models.IntegerField(null=True)),
                ('raffleTime', models.TimeField(null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('ticket_limit', models.IntegerField()),
                ('ticket_sold', models.IntegerField(default=0)),
                ('product_size', models.JSONField(null=True)),
                ('product_rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('product_image1', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image2', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image3', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image4', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image5', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image6', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image7', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image8', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image9', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_image10', models.ImageField(null=True, upload_to='Product/Images')),
                ('product_imageList', models.JSONField(null=True)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.seller')),
            ],
            bases=('Buyer.genericmodels',),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('genericmodels_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Buyer.genericmodels')),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.products')),
            ],
            bases=('Buyer.genericmodels',),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('genericmodels_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Buyer.genericmodels')),
                ('review', models.TextField(max_length=250, null=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.products')),
            ],
            bases=('Buyer.genericmodels',),
        ),
        migrations.CreateModel(
            name='ProductBuyer',
            fields=[
                ('cartmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Buyer.cartmodel')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.products')),
            ],
            bases=('Buyer.cartmodel',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('genericmodels_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Buyer.genericmodels')),
                ('order_dispatched', models.BooleanField(default=False)),
                ('in_way', models.BooleanField(default=False)),
                ('order_delivered', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.products')),
            ],
            bases=('Buyer.genericmodels',),
        ),
    ]
