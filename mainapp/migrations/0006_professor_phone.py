# Generated by Django 5.1.1 on 2024-10-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0005_remove_student_email_remove_student_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="professor",
            name="phone",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
