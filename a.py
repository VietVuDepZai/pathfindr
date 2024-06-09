import sqlite3
import psycopg2

# SQLite database connection
sqlite_db_file = 'db.sqlite3'  # replace with your SQLite database file
sqlite_conn = sqlite3.connect(sqlite_db_file)
sqlite_cur = sqlite_conn.cursor()

# PostgreSQL database connection
pg_host = 'john.db.elephantsql.com'
pg_database = 'wdktemon'
pg_user = 'wdktemon'
pg_password = '7JaXeX6o7ray037VEmiqz-dOwUUw0keh'
pg_port = '5432'

pg_conn = psycopg2.connect(
    host=pg_host,
    database=pg_database,
    user=pg_user,
    password=pg_password,
    port=pg_port
)
pg_cur = pg_conn.cursor()
# Get table names from SQLite database
sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = [row[0] for row in sqlite_cur.fetchall() if not row[0].startswith(('pg_', 'ql_'))]

# Migrate data from SQLite to PostgreSQL
for table_name in table_names:
    print(f"Migrating table: {table_name}")

    # Get column names from SQLite table
    sqlite_cur.execute(f"PRAGMA table_info({table_name});")
    columns = [row[1] for row in sqlite_cur.fetchall()]

    # Create table in PostgreSQL if it doesn't exist
    column_defs = [f'"{col}" text' for col in columns]
    pg_cur.execute(f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            {', '.join(column_defs)}
        );
    """)

    # Insert data from SQLite to PostgreSQL
    sqlite_cur.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cur.fetchall()
    for row in rows:
        pg_cur.execute(f"""
            INSERT INTO "{table_name}" ({', '.join([f'"{col}"' for col in columns])})
            VALUES ({', '.join(['%s'] * len(columns))});
        """, row)

    # Commit changes to PostgreSQL
    pg_conn.commit()
# Close database connections
sqlite_conn.close()
pg_conn.close()

print("Data migration complete!")