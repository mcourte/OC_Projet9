# Generated by Django 5.0 on 2024-04-18 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_alter_review_body_alter_review_headline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user_ticket_number',
            field=models.IntegerField(default=1),
        ),
    ]
