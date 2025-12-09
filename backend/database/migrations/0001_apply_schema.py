from django.db import migrations


def apply_postgres_schema(apps, schema_editor):
    """Only apply the raw PostgreSQL DDL if using PostgreSQL."""
    if schema_editor.connection.vendor != 'postgresql':
        return


schema_sql = """
CREATE TABLE users (
    user_id           SERIAL PRIMARY KEY,
    full_name         VARCHAR(150) NOT NULL,
    email             VARCHAR(150) NOT NULL UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    phone_number      VARCHAR(30),
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret  VARCHAR(128),
    backup_codes       TEXT,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login        TIMESTAMP,
    status            VARCHAR(20) NOT NULL DEFAULT 'Active'
);

CREATE TABLE accounts (
    account_id           SERIAL PRIMARY KEY,
    user_id              INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    account_name         VARCHAR(150) NOT NULL,
    account_type         VARCHAR(50) NOT NULL,
    currency             VARCHAR(10) NOT NULL,
    balance              DECIMAL(18,2) NOT NULL DEFAULT 0,
    api_provider         VARCHAR(50),
    tokenized_account_id VARCHAR(255),
    created_at           TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE categories (
    category_id    SERIAL PRIMARY KEY,
    user_id        INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    category_name  VARCHAR(100) NOT NULL,
    category_type  VARCHAR(20) NOT NULL,
    created_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE transactions (
    transaction_id   SERIAL PRIMARY KEY,
    user_id          INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    account_id       INTEGER REFERENCES accounts(account_id) ON DELETE SET NULL,
    amount           DECIMAL(18,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    category_id      INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    merchant_name    VARCHAR(150),
    transaction_date TIMESTAMP NOT NULL,
    synced_from_api  BOOLEAN NOT NULL DEFAULT FALSE,
    is_flagged       BOOLEAN NOT NULL DEFAULT FALSE,
    notes            TEXT
);

CREATE TABLE budgets (
    budget_id        SERIAL PRIMARY KEY,
    user_id          INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id      INTEGER NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    budget_amount    DECIMAL(18,2) NOT NULL,
    time_period      VARCHAR(20) NOT NULL,
    start_date       DATE NOT NULL,
    end_date         DATE NOT NULL,
    spent_amount     DECIMAL(18,2) NOT NULL DEFAULT 0,
    remaining_amount DECIMAL(18,2) NOT NULL DEFAULT 0
);

CREATE TABLE goals (
    goal_id          SERIAL PRIMARY KEY,
    user_id          INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    goal_title       VARCHAR(150) NOT NULL,
    target_amount    DECIMAL(18,2) NOT NULL,
    current_progress DECIMAL(18,2) NOT NULL DEFAULT 0,
    deadline         DATE NOT NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE ai_alerts (
    alert_id            SERIAL PRIMARY KEY,
    user_id             INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    alert_type          VARCHAR(50) NOT NULL,
    message             TEXT NOT NULL,
    related_category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    trigger_percentage  DECIMAL(5,2),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE admins (
    admin_id      SERIAL PRIMARY KEY,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(50) NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE system_logs (
    log_id      SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT,
    timestamp   TIMESTAMP NOT NULL DEFAULT NOW()
);
"""


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunPython(apply_postgres_schema),
    ]
