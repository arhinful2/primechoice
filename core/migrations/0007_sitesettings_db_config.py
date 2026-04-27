# Generated migration for database configuration fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_sitesettings_linkedin_sitesettings_pinterest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='db_engine',
            field=models.CharField(
                blank=True,
                choices=[('sqlite3', 'SQLite3'), ('postgresql', 'PostgreSQL')],
                default='sqlite3',
                help_text='Database engine to use',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='db_host',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Database host (e.g., localhost or Vercel-provided host)',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='db_port',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Database port (e.g., 5432 for PostgreSQL)',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='db_name',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Database name',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='db_user',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Database username',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='db_password',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Database password',
                max_length=255,
            ),
        ),
    ]
