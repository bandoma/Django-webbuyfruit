# Generated by Django 4.1.7 on 2023-04-24 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('webclient', '0003_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('userr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='webclient.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cart_Product_Many_Many',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AddtoCartTime', models.DateTimeField(auto_now=True)),
                ('cart_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webclient.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
