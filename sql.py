import mysql.connector

connection = mysql.connector.connect(host='localhost',database='world',user='root',password='root')
if connection.is_connected():
    print("Connection Successfully")
    cursor = connection.cursor()
    try:
        # Execute SELECT query
        cursor.execute("SELECT * FROM country")

        # Fetch all rows
        rows = cursor.fetchall()

        # Print each row
        for row in rows:
            print(row)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
else:
    print("Connection failed")

