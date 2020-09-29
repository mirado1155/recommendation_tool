from tkinter import *
from random import randint
import time
import mysql.connector
from Connect import Connect


class App(Tk, Connect):
    # Initializer
    def __init__(self):

        # initialize parent classes
        Connect.__init__(self)
        Tk.__init__(self)

        # App title
        self.title("Rob's Ridiculously Rad Random Restaurant Recommend-er! (New and Improved!)")

        # Connect to database
        self.mydb = mysql.connector.connect(
            user=self.user,
            passwd=self.password,
            database=self.db
        )
        self.curr = self.mydb.cursor()

        # This will store a list of all restaurant id's to link to checkboxes
        self.id_list = []

        """*************CREATE WIDGETS*****************"""

        # Frames
        self.mainframe = Frame(height="850", width="600", bg="#FFDF64")
        self.sideframe = Frame(height="650", width="350", bg="#FFDF64")

        # Text Areas
        self.restaurant_decision = Entry(font="fixedsys 30 bold", justify="center", bg="#5ADBFF", fg="white")
        self.restaurant_input = Entry(font="fixedsys", justify="center")
        self.restaurant_display = Text(font="fixedsys", bg="#5ADBFF")

        # Buttons
        self.mainbutton = Button(text="Recommend!", font="fixedsys 20 bold", fg="#1F7A8C",
                                 command=lambda: self.output_place())
        self.addbutton = Button(text="Add Restaurant", font="fixedsys 20 bold", fg="#1F7A8C",
                                command=lambda: self.add_restaurant(self.restaurant_input))
        self.removebutton = Button(text="Remove Checked Restaurant", font="fixedsys", fg="#1F7A8C",
                                   command=lambda: self.remove_restaurant())

    # Methods

    """This method sets size attributes and positions of widgets in app"""
    def set_widgets(self):
        # sets main window size
        self.geometry('1000x900')

        # places frames
        self.mainframe.place(in_=self, x=10, y=25)
        self.sideframe.place(in_=self, x=630, y=50)
        self.restaurant_decision.place(in_=self.mainframe, height=300, width=500, x=50, y=200)
        self.restaurant_input.place(in_=self.mainframe, height=30, width=300, x=645, y=700)
        self.restaurant_display.place(in_=self.sideframe, width=300, height=600, x=25, y=25)

        # places buttons
        self.mainbutton.place(in_=self.mainframe, width=400, height=100, x=100, y=700)
        self.addbutton.place(in_=self.mainframe, width=300, height=75, x=645, y=750)
        self.removebutton.place(in_=self, width=300, height=30, x=645, y=10)

    """This method gets unique ids from database and saves them in self.id_list[]"""
    def get_ids(self):
        self.id_list = []
        get_restaurant_id_query = "SELECT id FROM restaurants ORDER BY id ASC"
        self.curr.execute(get_restaurant_id_query)
        id_results = self.curr.fetchall()
        for restaurant_id in id_results:
            self.id_list.append(str(restaurant_id)[1:-2])

    """This is a doozy - gets and displays restaurant list with checkboxes. It wasn't as simple as it sounds"""
    def create_checkbuttons(self):
        get_restaurants_query = "SELECT name FROM restaurants ORDER BY id DESC"
        self.curr.execute(get_restaurants_query)
        global name_results
        name_results = self.curr.fetchall()

        self.checkbutton_frame = Frame(height="650", width="350", bg="#5ADBFF")
        self.checkbutton_frame.place(in_=self.sideframe, width=275, height=600, x=50, y=25)
        self.var_list = []
        index = 0
        for restaurant_id in self.id_list:
            self.var_list.append("var" + str(index + 1))
            self.var_list[index] = IntVar()
            query = "SELECT name FROM restaurants WHERE id = " + restaurant_id + " ORDER BY id DESC"
            self.curr.execute(query)
            result = str(self.curr.fetchone())[2:-3]
            Checkbutton(text=result, font="fixedsys",
                        bg="#5ADBFF", variable=self.var_list[index]).grid(in_=self.checkbutton_frame, row=index)
            index += 1

    """This method grabs user-input restaurant name, stores it to the database, and refreshes list in App"""
    def add_restaurant(self, restaurant_entry):
        self.restaurant_display.delete('1.0', END)
        user_input = restaurant_entry.get()
        formatted_user_input = user_input.replace("'", "''")
        query = "INSERT INTO restaurants (name) VALUES ('" + formatted_user_input + "')"
        self.curr.execute(query)
        self.mydb.commit()
        self.restaurant_input.delete(0, END)
        self.make_changes()

    """This method removes any checked restaurants from list and DB"""
    def remove_restaurant(self):
        index = 0
        for var in self.var_list:
            if index < len(self.id_list):
                if var.get() == 1:
                    remove_query = "DELETE FROM restaurants WHERE id = " + str(self.id_list[index])
                    self.curr.execute(remove_query)
                    self.mydb.commit()
            index += 1
        self.make_changes()

    """Applies common App changes - refreshes list of id's, destroys obsolete checkbox list and builds new one"""
    def make_changes(self):
        self.get_ids()
        self.checkbutton_frame.destroy()
        self.create_checkbuttons()

    """This method cycles through restaurant names at random, displaying them to the screen, until MAX_LOOP is met"""
    def output_place(self):
        LOOP_RATE = 25  # higher number indicates higher cycle rate
        MAX_LOOP = 15  # indicates how many cycles
        for loopTimes in range(0, MAX_LOOP):
            self.restaurant_decision.delete(0, END)

            if loopTimes == (MAX_LOOP - 1):
                self.restaurant_decision.config(bg='#5ADBFF')
            else:
                self.restaurant_decision.config(bg='lightgray')

            index = randint(0, (len(name_results) - 1))
            self.restaurant_decision.insert(0, name_results[index])
            self.update_idletasks()
            time.sleep(loopTimes / LOOP_RATE)


# Instantiate main class
main = App()

# Call main functions
main.config(bg="#5ADBFF")
main.set_widgets()
main.get_ids()
main.create_checkbuttons()
mainloop()