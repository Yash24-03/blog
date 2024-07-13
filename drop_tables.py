import sqlite3

# Path to your SQLite database
db_path = 'db.sqlite3'

# List of tables to drop
tables_to_drop = ['base_CustomUser']  # Replace with your table names

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop the specified tables
for table in tables_to_drop:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table};')
        print(f'Successfully dropped table {table}')
    except Exception as e:
        print(f'Error dropping table {table}: {e}')

# Commit changes and close the connection
conn.commit()
conn.close()
