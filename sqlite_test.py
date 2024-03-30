import sqlite3
import os

def insert_data(Title, Youtube_Link, Timestamp, Phone, Creator, Compressed_Glyphdata):
    # Connect to the database
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    # Prepare the SQL statement
    insert_sql = '''
    INSERT INTO Custom_Glyphs (Title, Youtube_Link, Timestamp, Phone, Creator, Compressed_Glyphdata)
    VALUES (?, ?, ?, ?, ?, ?)
    '''

    # Execute the SQL statement with the values
    cursor.execute(insert_sql, (Title, Youtube_Link, Timestamp, Phone, Creator, Compressed_Glyphdata))

    # Commit and close the connection
    conn.commit()
    conn.close()


def get_data_by_ID(entry_id):
    # Connect to the database
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    # Prepare the SQL statement
    select_sql = 'SELECT * FROM Custom_Glyphs WHERE id=?'

    # Execute the SQL statement with the values
    cursor.execute(select_sql, (entry_id,))
    result = cursor.fetchone()

    # Extract the file
    if result is not None:
        file_data = result[6]

        # Create folder
        folder_name = str(entry_id)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the file
        file_name = os.path.join(folder_name, f'entry_{entry_id}.zip')
        with open(file_name, 'wb') as file:
            file.write(file_data)

    # Close the connection
    conn.close()


def get_data_by_Title(Title):
    # Connect to the database
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    # Prepare the SQL statement
    select_sql = 'SELECT * FROM Custom_Glyphs WHERE Title=?'

    # Execute the SQL statement with the values
    cursor.execute(select_sql, (Title,))
    result = cursor.fetchone()

    if result is not None:
        print("ID:", result[0])
        print("Title:", result[1])
        print("Youtube_Link:", result[2])
        print("Timestamp:", result[3])
        print("Phone:", result[4])
        print("Creator:", result[5])

        # Extract the file
        file_data = result[6]

        # Create folder
        folder_name = str(result[0])
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the file
        file_name = os.path.join(folder_name, f'entry_{result[0]}.zip')
        with open(file_name, 'wb') as file:
            file.write(file_data)

    # Close the connection
    conn.close()


if __name__ == '__main__':
    # Create the table if it doesn't exist
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Custom_Glyphs
        (id INTEGER PRIMARY KEY, Title TEXT, Youtube_Link TEXT, Timestamp TEXT, Phone TEXT, Creator TEXT, Compressed_Glyphdata BLOB)
    ''')
    conn.commit()
    conn.close()


    # Insert data
    insert_data("Nya", "Meow", "0-0", "Hello", "World", "test.zip")

