# Generated by Django 5.0 on 2024-04-29 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0012_ticketreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketreview',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_reviews', to='review.review'),
        ),
    ]
