# Generated by Django 3.1.7 on 2021-03-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0002_letter_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='is_spam',
            field=models.BooleanField(default=False, verbose_name='спам'),
        ),
        migrations.AddField(
            model_name='letter',
            name='spam',
            field=models.IntegerField(default=0, verbose_name='оценок спам'),
        ),
    ]
