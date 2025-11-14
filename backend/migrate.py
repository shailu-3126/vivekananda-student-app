import os
import psycopg2

def run_seed(path="/seed.sql"):
    db_host = os.getenv("DB_HOST", "postgres")
    db_name = os.getenv("DB_NAME", "studentdb")
    db_user = os.getenv("DB_USER", "studentuser")
    db_password = os.getenv("DB_PASSWORD", "")
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    with open(path, "r") as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Seed applied")

if __name__ == "__main__":
    run_seed()
