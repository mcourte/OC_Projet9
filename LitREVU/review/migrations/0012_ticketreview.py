# Generated by Django 5.0 on 2024-04-29 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_alter_review_body_alter_review_headline_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.review')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.ticket')),
            ],
        ),
    ]
