# Generated by Django 5.1.4 on 2025-01-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptsActivity',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('database_reset_is_active', models.BooleanField(default=False)),
            ],
        ),
    ]