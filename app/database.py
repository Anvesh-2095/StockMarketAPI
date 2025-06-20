import mysql.connector

# Establish connection
connection = mysql.connector.connect(
    host="localhost",       # Replace with your database host
    user="your_username",   # Replace with your MySQL username
    password="your_password", # Replace with your MySQL password
    database="your_database"  # Replace with your database name
)

# Create a cursor object
cursor = connection.cursor()

# Execute a query
cursor.execute("SELECT * FROM your_table")  # Replace with your table name

# Fetch and print results
for row in cursor.fetchall():
    print(row)

# Close the connection
cursor.close()
connection.close()
