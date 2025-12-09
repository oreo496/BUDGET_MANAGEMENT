from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('goal_id', models.AutoField(primary_key=True, serialize=False)),
                ('goal_title', models.CharField(max_length=150)),
                ('target_amount', models.DecimalField(max_digits=18, decimal_places=2)),
                ('current_progress', models.DecimalField(max_digits=18, decimal_places=2, default=0)),
                ('deadline', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user', db_column='user_id')),
            ],
            options={'db_table': 'goals', 'ordering': ['-created_at']},
        ),
    ]
