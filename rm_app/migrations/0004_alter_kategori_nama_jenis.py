# Generated by Django 5.0.6 on 2024-05-14 13:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rm_app', '0003_kategori'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategori',
            name='nama',
            field=models.CharField(max_length=170),
        ),
        migrations.CreateModel(
            name='Jenis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=130)),
                ('data_created', models.DateTimeField(auto_now_add=True)),
                ('data_last_update', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='status_jenis', to='rm_app.statusmodel')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_jenis', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_jenis', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
