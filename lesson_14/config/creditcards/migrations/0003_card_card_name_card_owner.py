# Generated by Django 4.2.3 on 2023-07-17 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("creditcards", "0002_alter_card_card_issue_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="card_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="card",
            name="owner",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]