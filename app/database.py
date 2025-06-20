import mysql.connector
from .config import settings

# Establish connection
connection = mysql.connector.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)

# Create a cursor object
cursor = connection.cursor()

# # Execute a query
# cursor.execute("SELECT * FROM your_table")  # Replace with your table name
#
# # Fetch and print results
# for row in cursor.fetchall():
#     print(row)

# Close the connection
cursor.close()
connection.close()
