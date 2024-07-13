import sqlite3

# Path to your SQLite database
db_path = 'db.sqlite3'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the list of tables
for table in tables:
    print(table[0])

# Close the connection
conn.close()
