CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    grade VARCHAR(10)
);

INSERT INTO students (name, age, grade)
VALUES ('Vivekananda', 23, 'A')
ON CONFLICT DO NOTHING;
