import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("NEON_HOST"),
    port=os.getenv("NEON_PORT", 5432),
    dbname=os.getenv("NEON_DB"),
    user=os.getenv("NEON_USER"),
    password=os.getenv("NEON_PASSWORD"),
)

cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_text TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
"""

cur.execute(create_table_query)
conn.commit()
cur.close()
conn.close()

print("Table 'tasks' created successfully!")
