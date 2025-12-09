from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(unique=True, max_length=150)),
                ('password_hash', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=30, null=True, blank=True)),
                ('two_factor_enabled', models.BooleanField(default=False)),
                ('two_factor_secret', models.CharField(max_length=128, null=True, blank=True)),
                ('backup_codes', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default='Active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
            ],
            options={'db_table': 'users'},
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(unique=True, max_length=150)),
                ('password_hash', models.CharField(max_length=255)),
                ('role', models.CharField(default='admin', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'admins'},
        ),
    ]
