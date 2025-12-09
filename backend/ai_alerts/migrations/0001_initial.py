from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIAlert',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_type', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('trigger_percentage', models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user', db_column='user_id')),
                ('related_category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='categories.category', null=True, blank=True, db_column='related_category_id')),
            ],
            options={'db_table': 'ai_alerts', 'ordering': ['-created_at']},
        ),
    ]
