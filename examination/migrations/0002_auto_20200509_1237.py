# Generated by Django 3.0.6 on 2020-05-09 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_option',
        ),
        migrations.RemoveField(
            model_name='question',
            name='options',
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_content', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='examination.Question')),
            ],
        ),
    ]
