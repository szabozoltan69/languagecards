# Generated by Django 4.2.14 on 2024-07-29 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('languagecards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='categories',
        ),
        migrations.AddField(
            model_name='card',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cards', to='languagecards.category', verbose_name='category'),
        ),
    ]
