import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS company (
    no INTEGER PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL
);
''')

companies = [
    ('nj',),
    ('rsp',),
    ('parth',),
    ('hitesh',)
]

cursor.executemany('''
INSERT INTO company (company_name) 
VALUES (?);
''', companies)

conn.commit()
conn.close()

print("Table created and data inserted successfully!")