import os
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db_connection():
    # Read connection settings from environment variables
    db_host = os.getenv("DB_HOST", "postgres")
    db_name = os.getenv("DB_NAME", "studentdb")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")
    cloud_sql_conn = os.getenv("CLOUD_SQL_CONNECTION_NAME")

    # Cloud Run (connect through Unix socket)
    if cloud_sql_conn:
        host = f"/cloudsql/{cloud_sql_conn}"
    else:
        host = db_host

    conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=db_user,
        password=db_password,
        cursor_factory=RealDictCursor
    )
    return conn

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}

@app.get("/students")
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return {"students": data}

@app.post("/students")
def add_student(student: dict):
    name = student.get("name")
    age = student.get("age")
    grade = student.get("grade")

    if not all([name, age, grade]):
        raise HTTPException(status_code=400, detail="Missing fields")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s);",
        (name, age, grade),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Student added successfully"}

@app.put("/students/{id}")
def update_student(id: int, student: dict):
    name = student.get("name")
    age = student.get("age")
    grade = student.get("grade")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s;",
        (name, age, grade, id),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Student updated successfully"}

@app.patch("/students/{id}")
def patch_student(id: int, student: dict):
    fields = []
    values = []
    for key, value in student.items():
        fields.append(f"{key}=%s")
        values.append(value)
    values.append(id)

    query = f"UPDATE students SET {', '.join(fields)} WHERE id=%s;"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Student partially updated"}

@app.delete("/students/{id}")
def delete_student(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Student deleted successfully"}
