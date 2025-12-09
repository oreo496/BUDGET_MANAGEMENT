from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=150, null=True, blank=True)),
                ('account_type', models.CharField(max_length=50, null=True, blank=True)),
                ('currency', models.CharField(max_length=10, null=True, blank=True)),
                ('balance', models.DecimalField(max_digits=18, decimal_places=2, default=0)),
                ('api_provider', models.CharField(max_length=50, null=True, blank=True)),
                ('tokenized_account_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user', db_column='user_id')),
            ],
            options={'db_table': 'accounts'},
        ),
    ]
