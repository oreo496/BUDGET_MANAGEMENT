from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('bank_accounts', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=18, decimal_places=2)),
                ('transaction_type', models.CharField(max_length=20)),
                ('merchant_name', models.CharField(max_length=150, null=True, blank=True)),
                ('transaction_date', models.DateTimeField()),
                ('synced_from_api', models.BooleanField(default=False)),
                ('is_flagged', models.BooleanField(default=False)),
                ('notes', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user', db_column='user_id')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='bank_accounts.bankaccount', null=True, blank=True, db_column='account_id')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='categories.category', null=True, blank=True, db_column='category_id')),
            ],
            options={'db_table': 'transactions', 'ordering': ['-transaction_date']},
        ),
    ]
