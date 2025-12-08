# Database Migrations

This directory contains database migration scripts and seeders.

## Running Migrations

Since we're using a custom schema with BINARY(16) UUIDs, Django's automatic migrations may need adjustment.

1. First, run the SQL schema file:
   ```bash
   mysql -u root -p funder < ../../schema.sql
   ```

2. Then generate Django migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Seeders

Use the seed scripts to populate the database with test data.

