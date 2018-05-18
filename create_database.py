import sqlite3

database_name = "song_list"

def create_new_table(name):
    # SQL command to create a table in the database
    sql_command = """CREATE TABLE """ + name + """( 
        song_number INTEGER PRIMARY KEY, 
        song_name VARCHAR(50), 
        artist VARCHAR(30),
        genre VARCHAR(30), 
        joining DATE);"""
    return sql_command

if __name__ == "__main__":
    # connecting to the database
    connection = sqlite3.connect("testTable.db")
    # cursor
    curse = connection.cursor()

    sql_command = create_new_table(database_name)
    # execute the statement
    curse.execute(sql_command)

    # SQL command to insert the data in the table
    sql_command = """INSERT INTO song_list VALUES (1, "Undertow", "Alvvays", "Alternative/Indie", "2016");"""
    curse.execute(sql_command)

    more_songs = [(2, "Don't Stop Me Now", "Queen", "Rock", "1978"),
                 (3, 'Mama Mia', 'Abba', "Pop", "1975"),
                 (4, 'Halo Theme Song', 'Martin O\'Donnell and Michael Salvatori', "Epic/Game", "2002"),
                ]
    curse.executemany('INSERT INTO song_list VALUES (?,?,?,?,?)', more_songs)

    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    connection.commit()
    # close the connection
    connection.close()