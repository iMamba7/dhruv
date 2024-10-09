import sqlite3

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('data.db')  # replace with your database file

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Execute the DELETE command
cursor.execute("DELETE FROM data;")  # replace 'products' with your table name

# Step 4: Commit the changes
conn.commit()

# Step 5: Close the cursor and connection
cursor.close()
conn.close()


