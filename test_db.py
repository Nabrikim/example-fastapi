import psycopg2
import os

# USE YOUR EXTERNAL URL (The one WITHOUT the -a)
# Example: postgresql://user:password@dpg-xxx.oregon-postgres.render.com/dbname
DB_URI ="postgresql://fastapi_db_gio5_user:lqwQx9hcCmOBDtJCIMo6wV5cJwSsumiN@dpg-d69oic95pdvs738m09fg.oregon-postgres.render.com/fastapi_db_gio5"

try:
    # The 'sslmode=require' is the "secret sauce" to bypass the error
    conn = psycopg2.connect(DB_URI, sslmode='require')
    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    record = cur.fetchone()
    print(f"✅ Connection Successful!")
    print(f"Connected to: {record}")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")