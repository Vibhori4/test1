# Generated by Django 5.0.6 on 2024-06-10 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserShard',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('country_code', models.CharField(blank=True, max_length=10, null=True)),
                ('is_email_verified', models.BooleanField(default=False, null=True)),
                ('profile_image', models.CharField(blank=True, max_length=255, null=True)),
                ('is_public', models.BooleanField(default=False, null=True)),
                ('is_blocked', models.BooleanField(default=False, null=True)),
                ('is_influencer', models.BooleanField(default=False, null=True)),
                ('bio_description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('health_goal', models.TextField(blank=True, null=True)),
                ('alias', models.CharField(blank=True, max_length=50, null=True)),
                ('diagnosis_selected_ids', models.JSONField(blank=True, null=True)),
                ('symptoms_selected_ids', models.JSONField(blank=True, null=True)),
                ('meta', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users_shard',
                'managed': False,
            },
        ),
    ]
