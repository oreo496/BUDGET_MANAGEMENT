import os
import django
import MySQLdb
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

db = settings.DATABASES['default']
conn = MySQLdb.connect(
    host=db['HOST'],
    user=db['USER'],
    password=db['PASSWORD'],
    database=db['NAME']
)
cursor = conn.cursor()

try:
    # Add username column
    cursor.execute("ALTER TABLE users ADD COLUMN username VARCHAR(50) UNIQUE AFTER id")
    print("✅ Username column added!")
except Exception as e:
    if '1060' in str(e):  # Duplicate column
        print("✅ Username column already exists!")
    else:
        print(f"❌ Error: {e}")

try:
    # Set default usernames from email
    cursor.execute("UPDATE users SET username = SUBSTRING_INDEX(email, '@', 1) WHERE username IS NULL OR username = ''")
    conn.commit()
    print(f"✅ Set usernames for {cursor.rowcount} users!")
except Exception as e:
    print(f"❌ Error setting usernames: {e}")

cursor.execute("SELECT COUNT(*) FROM users")
print(f"✅ Total users in database: {cursor.fetchone()[0]}")

conn.close()
print("\n🎉 DONE! Restart your Django server now!")
