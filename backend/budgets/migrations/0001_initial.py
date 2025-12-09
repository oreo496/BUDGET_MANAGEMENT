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
            name='Budget',
            fields=[
                ('budget_id', models.AutoField(primary_key=True, serialize=False)),
                ('budget_amount', models.DecimalField(max_digits=18, decimal_places=2)),
                ('time_period', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('spent_amount', models.DecimalField(max_digits=18, decimal_places=2, default=0)),
                ('remaining_amount', models.DecimalField(max_digits=18, decimal_places=2, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user', db_column='user_id')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category', db_column='category_id')),
            ],
            options={'db_table': 'budgets'},
        ),
    ]
