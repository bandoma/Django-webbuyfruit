# Generated by Django 4.1.7 on 2023-04-17 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webclient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('encode', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webclient.user')),
            ],
        ),
    ]