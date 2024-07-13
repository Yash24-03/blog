import psycopg2

# PostgreSQL database connection parameters
db_params = { 'NAME': 'techtales', 'USER': 'yash', 'PASSWORD':'Poonam@1', 'HOST': 'localhost', }  # or your_db_host if not local 'PORT': '5432',       # Default port for PostgreSQL } }

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Query to get the list of tables
cursor.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cursor.fetchall()

# Print the list of tables
for table in tables:
    print(table[0])

# Close the connection
conn.close()
