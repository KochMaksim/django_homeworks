# Generated by Django 4.1.3 on 2022-12-11 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_scope_is_main'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scope',
            options={'ordering': ['-is_main'], 'verbose_name': 'Тематическая статья', 'verbose_name_plural': 'Тематические статьи'},
        ),
    ]
