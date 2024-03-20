import sqlite3
import os

""" # This will create a new database file called 'my_database.db' if it doesn't already exist.
conn = sqlite3.connect('Custom_Glyphs.db')

cursor = conn.cursor()

# SQL statement to create a table with four TEXT columns for strings and one BLOB column for the file.
create_table_sql = '''
CREATE TABLE IF NOT EXISTS Custom_Glyphs (
    id INTEGER PRIMARY KEY,
    string1 TEXT NOT NULL,
    string2 TEXT NOT NULL,
    string3 TEXT NOT NULL,
    string4 TEXT NOT NULL,
    file_data BLOB
)
'''

cursor.execute(create_table_sql)

# Save the changes
conn.commit()

# Close the connection when done
conn.close()
 """
def insert_data(Title, Youtube_Link, Timestamp, Phone, Creator, Compressed_Glyphdata):
    # Convert file to binary data
    with open(Compressed_Glyphdata, 'rb') as file:
        file_data = file.read()

    # Reconnect to the database
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    # Insert data
    insert_sql = '''
    INSERT INTO Custom_Glyphs (Title, Youtube_Link, Timestamp, Phone, Creator, Compressed_Glyphdata)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_sql, (Title, Youtube_Link, Timestamp, Phone, Creator, file_data))

    # Commit and close
    conn.commit()
    conn.close()


def get_data_by_ID(entry_id):
    # get the entry
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    select_sql = f"SELECT * FROM Custom_Glyphs WHERE id = {entry_id} LIMIT 1"
    cursor.execute(select_sql)
    result = cursor.fetchone()

    # extract the file
    file_data = result[6]

    # create folder
    folder_name = str(entry_id)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # save the file
    file_name = os.path.join(folder_name, f'entry_{entry_id}.zip')
    with open(file_name, 'wb') as file:
        file.write(file_data)

    # close the connection
    conn.close()

def get_data_by_Title(Title):
    # get the entry
    conn = sqlite3.connect('Custom_Glyphs.db')
    cursor = conn.cursor()

    select_sql = f"SELECT * FROM Custom_Glyphs WHERE Title = '{Title}' LIMIT 1"
    cursor.execute(select_sql)
    result = cursor.fetchone()

    if result is None:
        print("Title not found")
        return

    print("ID:", result[0])
    print("Title:", result[1])
    print("Youtube_Link:", result[2])
    print("Timestamp:", result[3])
    print("Phone:", result[4])
    print("Creator:", result[5])

    # extract the file
    file_data = result[6]

    # create folder
    folder_name = str(result[0])
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # save the file
    file_name = os.path.join(folder_name, f'entry_{result[0]}.zip')
    with open(file_name, 'wb') as file:
        file.write(file_data)

    # close the connection
    conn.close()

if not os.path.exists('Custom_Glyphs.db'):
    conn = sqlite3.connect('Custom_Glyphs.db', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES, timeout=10)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Custom_Glyphs (id INTEGER PRIMARY KEY, Title TEXT, Youtube_Link TEXT, Timestamp TEXT, Phone TEXT, Creator TEXT, Compressed_Glyphdata BLOB);')
    conn.commit()
    conn.close()



insert_data("Nya", "Meow", "0-0", "Hello", "World", "Test.zip")
insert_data("RATATA", "https://www.youtube.com/watch?v=xkejbXejA-0&pp=ygUGcmF0YXRh", "42.581-61.935", "A065", "Mr Steel", "RATATA.zip")

get_data_by_ID(1)
get_data_by_Title("RATATA")
