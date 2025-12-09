from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemLog',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_type', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.user', null=True, blank=True, db_column='user_id')),
            ],
            options={'db_table': 'system_logs', 'ordering': ['-timestamp']},
        ),
        migrations.CreateModel(
            name='AdminAction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.admin', db_column='admin_id')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.user', null=True, blank=True, db_column='target_user_id')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='transactions.transaction', null=True, blank=True, db_column='transaction_id')),
            ],
            options={'db_table': 'admin_actions', 'ordering': ['-timestamp']},
        ),
    ]
