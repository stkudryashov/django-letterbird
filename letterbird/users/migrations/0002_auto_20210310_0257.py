# Generated by Django 3.1.7 on 2021-03-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0002_letter_author'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined'], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='views',
        ),
        migrations.AddField(
            model_name='user',
            name='recently',
            field=models.ManyToManyField(blank=True, related_name='letter_views', to='letters.Letter', verbose_name='просмотренные'),
        ),
    ]
