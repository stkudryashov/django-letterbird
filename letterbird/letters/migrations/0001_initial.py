# Generated by Django 3.1.7 on 2021-03-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=3000, verbose_name='письмо')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='дата')),
                ('views', models.IntegerField(default=0, editable=False, verbose_name='просмотров')),
                ('saves', models.IntegerField(default=0, editable=False, verbose_name='сохранений')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
                'ordering': ['-datetime', '-author'],
            },
        ),
    ]
