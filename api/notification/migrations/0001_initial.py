# Generated by Django 5.2.1 on 2025-05-30 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('inventory', 'Inventory'), ('system', 'System')], default='system', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
