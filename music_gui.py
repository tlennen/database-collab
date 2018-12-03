from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error

queries = [
    """""",  # Filler for count
    """SELECT * FROM song ORDER BY s_name DESC""",  # Query 1
    """select \'Song\' as tbl,s_name as name,s_song_id as id from song where s_name like ? 
    union 
    select \'Artist\' as tbl,a_name as name,a_artist_id as id from artist where a_name like ? 
    union
    select \'Album\' as tbl,al_name as name,al_album_id as id from album where al_name like ? 
    union
    select \'Label\' as tbl,l_name as name,l_label_id as id from label where l_name like ? 
    order by name""",  # Query 2
    """select s_times_played from song where s_song_id = ?""",  # Query 3
    """update song set s_times_played = ? where s_song_id = ?""",  # Query 4
    """insert into label values(?,(select count(*) from label)+1)""",  # Query 5
    """select l_name from label where l_label_id = ?""",  # Query 6
    """insert into artist values(?,(select count(*) from artist)+1,?)""",  # Query 7
    """select al_name from album where al_album_id = ?""",  # Query 8
    """insert into album values(?,?,?,?,(select count(*) from album)+1)""",  # Query 9
    """select al_name from album where al_album_id = ? and al_artist_id = ?""",  # Query 10
    """insert into song values(?,(select count(*) from song)+1,?,?,?,?)""",  # Query 11
]


class StartMenu():
    def __init__(self, master,database):
        self.master = master
        self.user_select()
        self.conn = self.create_connection(database)

    def create_connection(self,db_file):
        # create connection
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def user_select(self):
        lab = Label(self.master, text="Select Use Case", font=("Times New Roman", 60)).grid(row=0, column=1, sticky=W)
        b1 = Button(self.master, text="User", command=self.create_user, font=("Times New Roman", 60)).grid(row=1, column=0,sticky=NSEW)
        b2 = Button(self.master, text="Admin", command=self.create_admin, font=("Times New Roman", 60)).grid(row=1,
                                                                                                         column=2,
                                                                                                         sticky=W)
    def create_admin(self):
        new_window = Toplevel(self.master)
        new_window.wm_title("Admin Page")
        self.ad = Admin(new_window, self.conn)

    def create_user(self):
        new_window = Toplevel(self.master)
        new_window.wm_title("User Page")
        self.ad = User(new_window, self.conn)

class Admin():
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self.master.geometry("600x600")
        self.nb = ttk.Notebook(master)
        self.create_ui()

    def create_ui(self):
        self.nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
        page1 = ttk.Frame(self.nb)
        self.nb.add(page1, text='   Search Term   ')
        page2 = ttk.Frame(self.nb)
        self.nb.add(page2, text='   Update song   ')
        page3 = ttk.Frame(self.nb)
        self.nb.add(page3, text='   Add song   ')
        page4 = ttk.Frame(self.nb)
        self.nb.add(page4, text='   Add album   ')
        page5 = ttk.Frame(self.nb)
        self.nb.add(page5, text='   Add artist   ')
        page6 = ttk.Frame(self.nb)
        self.nb.add(page6, text='   Add label   ')
        self.look_up_table(page1)
        self.update_times_played(page2)
        self.add_song(page3)
        self.add_album(page4)
        self.add_artist(page5)
        self.add_label(page6)

    def look_up_table(self,master):
        self.tree = ttk.Treeview(master, columns=('Table', 'Name'), height=30)
        self.tree.heading('#0', text='Table')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='ID')
        self.tree.grid(row=1, column=1, columnspan=6, sticky='nsew')
        self.treeview = self.tree
        search_label = Label(master, text='Enter search term: ')
        search_entry = Entry(master)
        search_button = Button(master, text='   Search   ', command=lambda: self.search_tree(search_entry.get()))
        search_label.grid(row=0, column=1)
        search_entry.grid(row=0, column=2)
        search_button.grid(row=0, column=3)

    def update_times_played(self,master):
        label1 = Label(master, text='Update Times Played for a Song',font=('Arial',25))
        label2 = Label(master, text='Song ID', font=('Arial', 15))
        label3 = Label(master, text='Times Played', font=('Arial', 15))
        entry1 = Entry(master,font=('Arial',25))
        entry2 = Entry(master, font=('Arial', 25))
        entry3 = Entry(master, font=('Arial', 25))
        b1 = Button(master, text='Update times played',width = 20,height =5,padx=10, pady=10,font=('Arial', 15),command = lambda: self.run_update(entry1,entry2.get(),entry3))
        label1.grid(row=0, column=0,padx=10, pady=10,columnspan = 10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0, padx=10, pady=10)
        entry1.grid(row=1, column=1,padx=10, pady=10)
        entry2.grid(row=2, column=1, padx=10, pady=10)
        entry3.grid(row=4, column=1, padx=10, pady=10)
        b1.grid(row=3, column=0,columnspan = 10)

    def run_update(self,id,times,output):
        db_rows = self.run_query(queries[3], [id.get()])
        count = 0
        for row in db_rows:
            count= count +1
            print("Previous: " + str(row[0]) + " , New: " + str(times))
        if count == 0:
            id.delete(0, END)
            id.insert(0, 'Invalid')
        else:
            db_rows = self.run_query(queries[4], [times, id.get()])
            output.delete(0, END)
            output.insert(0, "Prev: " + str(row[0]) + " ,New: " + str(times))

    def add_song(self,master):
        label1 = Label(master, text='Add new song', font=('Arial', 25))
        label2 = Label(master, text='Song Name', font=('Arial', 15))
        label3 = Label(master, text='Artist ID', font=('Arial', 15))
        label4 = Label(master, text='Song Length', font=('Arial', 15))
        label5 = Label(master, text='Times Played', font=('Arial', 15))
        label6 = Label(master, text='Album ID', font=('Arial', 15))
        entry1 = Entry(master, font=('Arial', 25))
        entry2 = Entry(master, font=('Arial', 25))
        entry3 = Entry(master, font=('Arial', 25))
        entry4 = Entry(master, font=('Arial', 25))
        entry5 = Entry(master, font=('Arial', 25))
        b1 = Button(master, text='Insert new song', width=20, height=5, padx=10, pady=10, font=('Arial', 15),
                    command=lambda: self.run_song(entry1.get(),entry2,entry3.get(),entry4.get(),entry5))
        label1.grid(row=0, column=0, padx=10, pady=10, columnspan=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0, padx=10, pady=10)
        label4.grid(row=3, column=0, padx=10, pady=10)
        label5.grid(row=4, column=0, padx=10, pady=10)
        label6.grid(row=5, column=0, padx=10, pady=10)
        entry1.grid(row=1, column=1, padx=10, pady=10)
        entry2.grid(row=2, column=1, padx=10, pady=10)
        entry3.grid(row=3, column=1, padx=10, pady=10)
        entry4.grid(row=4, column=1, padx=10, pady=10)
        entry5.grid(row=5, column=1, padx=10, pady=10)
        b1.grid(row=6, column=0, columnspan=10)

    def run_song(self,name, artist, length,times_played,album):
        db_rows = self.run_query(queries[10], [album.get(),artist.get()])
        count = 0
        for row in db_rows:
            count = count + 1
        if count == 0:
            artist.delete(0, END)
            artist.insert(0, 'Invalid')
            album.delete(0, END)
            album.insert(0, 'Invalid')
        else:
            db_rows = self.run_query(queries[11], [name, artist.get(), length, times_played,album.get()])
            print("Song has been added!")

    def add_album(self,master):
        label1 = Label(master, text='Add new album', font=('Arial', 25))
        label2 = Label(master, text='Album Name', font=('Arial', 15))
        label3 = Label(master, text='Artist ID', font=('Arial', 15))
        label4 = Label(master, text='Release Date', font=('Arial', 15))
        label5 = Label(master, text='Genre', font=('Arial', 15))
        entry1 = Entry(master, font=('Arial', 25))
        entry2 = Entry(master, font=('Arial', 25))
        entry3 = Entry(master, font=('Arial', 25))
        entry4 = Entry(master, font=('Arial', 25))
        b1 = Button(master, text='Insert new artist', width=20, height=5, padx=10, pady=10, font=('Arial', 15),
                    command=lambda: self.run_album(entry1.get(),entry2,entry3.get(),entry4.get()))
        label1.grid(row=0, column=0, padx=10, pady=10, columnspan=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0, padx=10, pady=10)
        label4.grid(row=3, column=0, padx=10, pady=10)
        label5.grid(row=4, column=0, padx=10, pady=10)
        entry1.grid(row=1, column=1, padx=10, pady=10)
        entry2.grid(row=2, column=1, padx=10, pady=10)
        entry3.grid(row=3, column=1, padx=10, pady=10)
        entry4.grid(row=4, column=1, padx=10, pady=10)
        b1.grid(row=5, column=0, columnspan=10)

    def run_album(self,name,artist,date,genre):
        db_rows = self.run_query(queries[8], [artist.get()])
        count = 0
        for row in db_rows:
            count = count + 1
        if count == 0:
            artist.delete(0, END)
            artist.insert(0, 'Invalid')
        else:
            db_rows = self.run_query(queries[9], [name, artist.get(),date, genre])
            print("Album has been added!")

    def add_artist(self,master):
        label1 = Label(master, text='Add new artist', font=('Arial', 25))
        label2 = Label(master, text='Artist Name', font=('Arial', 15))
        label3 = Label(master, text='Label ID', font=('Arial', 15))
        entry1 = Entry(master, font=('Arial', 25))
        entry2 = Entry(master, font=('Arial', 25))
        b1 = Button(master, text='Insert new artist', width=20, height=5, padx=10, pady=10, font=('Arial', 15),
                    command=lambda: self.run_artist(entry1.get(),entry2))
        label1.grid(row=0, column=0, padx=10, pady=10, columnspan=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0,padx=10, pady=10)
        entry1.grid(row=1, column=1, padx=10, pady=10)
        entry2.grid(row=2, column=1, padx=10, pady=10)
        b1.grid(row=3, column=0, columnspan=10)

    def run_artist(self,name,label):
        db_rows = self.run_query(queries[6], [label.get()])
        count = 0
        for row in db_rows:
            count = count + 1
        if count == 0:
            label.delete(0, END)
            label.insert(0, 'Invalid')
        else:
            db_rows = self.run_query(queries[7], [name, label.get()])
            print("Artist has been added!")

    def add_label(self,master):
        label1 = Label(master, text='Add new label', font=('Arial', 25))
        label2 = Label(master, text='Label Name', font=('Arial', 15))
        entry1 = Entry(master, font=('Arial', 25))
        b1 = Button(master, text='Insert new label', width=20, height=5, padx=10, pady=10, font=('Arial', 15),
                    command=lambda: self.run_label(entry1.get()))
        label1.grid(row=0, column=0, padx=10, pady=10, columnspan=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        entry1.grid(row=1, column=1, padx=10, pady=10)
        b1.grid(row=3, column=0, columnspan=10)

    def run_label(self,name):
        db_rows = self.run_query(queries[5], [name])
        print("Label inserted!")

    def search_tree(self,term):
        term = '%'+term+'%'
        self.tree.delete(*self.tree.get_children())
        query = queries[2]
        db_rows = self.run_query(query,[term,term,term,term])
        for row in db_rows:
            print(row)
            self.tree.insert('', 0, text=row[0], values=row[1:])

    def run_query(self, query, parameters=()):
        with self.conn:
            cursor = self.conn.cursor()
            query_result = cursor.execute(query, parameters)
            self.conn.commit()
        return query_result


class User():
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self.master.geometry("1600x600")
        self.nb = ttk.Notebook(master)
        self.create_ui()

    def create_ui(self):
        self.nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
        page1 = ttk.Frame(self.nb)
        self.nb.add(page1, text='Home')
        page2 = ttk.Frame(self.nb)
        self.nb.add(page2, text='Search for songs')
        page3 = ttk.Frame(self.nb)
        self.nb.add(page3, text='Find new songs')
        page4 = ttk.Frame(self.nb)
        self.nb.add(page4, text='Manage playlist')
        self.tree = ttk.Treeview(page1,columns=('Name', 'Song Id', 'Artist Id', 'Song length', 'Times Played'),height=20)
        self.tree.heading('#0', text='Song name')
        self.tree.heading('#1', text='song_id')
        self.tree.heading('#2', text='artist id')
        self.tree.heading('#3', text='song_length')
        self.tree.heading('#4', text='Times played')
        self.tree.heading('#5', text='Album')
        self.tree.grid(row=0, column=0, columnspan=6, sticky='nsew')
        ttk.Button(page1, text='Delete song').grid(row=5, column=0)
        ttk.Button(page1, text='Edit song').grid(row=5, column=1)
        self.viewing_records()

    def run_query(self, query, parameters=()):
        with self.conn:
            cursor = self.conn.cursor()
            query_result = cursor.execute(query, parameters)
            self.conn.commit()
        return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = queries[1]
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[0], values=row[1:])

def main():
    database = "mixer.db"
    master = Tk()
    master.title('Music Mixer')
    start = StartMenu(master,database)
    master.resizable(False, False)
    master.mainloop()


if __name__ == '__main__':
    main()

