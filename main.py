from tkinter import *
from tkinter import messagebox
from blackjack import Blackjack
import mysql.connector
import random
import tkinter.ttk as ttk


class LoginWindow:
    def __init__(self, master, db):
        self.master = master
        self.master.title("Blackjack Login")
        self.master.geometry("600x600")

        # Set up background image
        self.bg_image = PhotoImage(file="background.png")
        self.bg_label = Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set up font styles
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 14)
        self.button_font = ("Arial", 14, "bold")

        # Set up login form
        self.title_label = Label(self.master, text="Blackjack Login", font=self.title_font, bg="#182E44", fg="#FFFFFF")
        self.title_label.pack(fill=X, padx=20, pady=20)

        self.username_label = Label(self.master, text="Username:", font=self.label_font, bg="#182E44", fg="#FFFFFF")
        self.username_label.pack(pady=(0, 10))

        self.username_entry = Entry(self.master, font=self.label_font, width=20)
        self.username_entry.pack()

        self.password_label = Label(self.master, text="Password:", font=self.label_font, bg="#182E44", fg="#FFFFFF")
        self.password_label.pack(pady=(10, 0))

        self.password_entry = Entry(self.master, font=self.label_font, width=20, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.master, text="Login", font=self.button_font, bg="#1F7A8C", fg="#FFFFFF", command=self.login)
        self.login_button.pack(pady=(20, 0))

        self.register_button = Button(self.master, text="Register", font=self.button_font, bg="#1F7A8C", fg="#FFFFFF", command=self.register)
        self.register_button.pack(pady=(10, 0))

        


        # Save database object
        self.db = db


    def login(self):
    # Get username and password from entry fields
            username = self.username_entry.get()
            password = self.password_entry.get()

    # Check if username and password are not empty
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password")
                return

    # Check if user exists in database
            cursor = self.db.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "Invalid username or password")
                return

    # Open game window
            game_window = Toplevel(self.master)
            game_window.geometry("600x600")

            BlackjackGame(game_window,username, password)



    def register(self):

        
    # Open registration window
        reg_window = Toplevel(self.master)
        reg_window.title("Blackjack Register")
        self.master.geometry("600x600")

        

    # Set up registration form
        reg_title_label = Label(reg_window, text="Blackjack Register", font=self.title_font, bg="#182E44", fg="#FFFFFF")
        reg_title_label.pack(fill=X, padx=20, pady=20)

        reg_username_label = Label(reg_window, text="Username:", font=self.label_font, bg="#182E44", fg="#FFFFFF")
        reg_username_label.pack(pady=(0, 10))

        reg_username_entry = Entry(reg_window, font=self.label_font, width=20, bg="#FFFFFF")
        reg_username_entry.pack()

        reg_password_label = Label(reg_window, text="Password:", font=self.label_font, bg="#182E44", fg="#FFFFFF")
        reg_password_label.pack(pady=(10, 0))

        reg_password_entry = Entry(reg_window, font=self.label_font, width=20, show="*", bg="#FFFFFF")
        reg_password_entry.pack()

        reg_confirm_password_label = Label(reg_window, text="Confirm Password:", font=self.label_font, bg="#182E44", fg="#FFFFFF")
        reg_confirm_password_label.pack(pady=(10, 0))

        reg_confirm_password_entry = Entry(reg_window, font=self.label_font, width=20, show="*", bg="#FFFFFF")
        reg_confirm_password_entry.pack()

        reg_button = Button(reg_window, text="Register", font=self.button_font, bg="#1F7A8C", fg="#FFFFFF", command=lambda: self.save_user(reg_username_entry.get(), reg_password_entry.get(), reg_confirm_password_entry.get(), reg_window))
        reg_button.pack(pady=(20, 0))


    def save_user(self, username, password, confirmed_password, window):
        # Check if password and confirmed password match
        if password != confirmed_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Save new user to database
        cursor = self.db.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(query, values)
        self.db.commit()

        # Show success message and close registration window
        messagebox.showinfo("Registration Successful", "You have been registered successfully!")
        window.destroy()


def show_scoreboard(self):
    # Connect to the database and fetch the data
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SAchi#98",
        database="blackjack"
    )
    cursor = db.cursor()
    cursor.execute('SELECT username, winnings, losses FROM users')
    rows = cursor.fetchall()

    # Create a new window to display the scoreboard
    scoreboard_window = Toplevel(self)

    # Create a treeview widget to display the data in a table
    tree = ttk.Treeview(scoreboard_window, columns=('username', 'winnings', 'losses'), show='headings')
    tree.heading('username', text='Username')
    tree.heading('winnings', text='Winnings')
    tree.heading('losses', text='Losses')
    tree.pack()

    # Insert the fetched data into the table
    for row in rows:
        tree.insert('', 'end', values=row)

    # Close the database connection
    db.close()


class BlackjackGame(Frame):

    def __init__(self,game_window,username, password):
        self._username = username
        self._password = password
        Frame.__init__(self, game_window)
        self.master.title("Blackjack")
        self.grid()
        
        #Add the command buttons
        self._hitButton = Button(self, text="Hit", command=self._hit)
        self._hitButton.grid(row=0, column=0)
        
        self._passButton = Button(self, text="Pass", command=self._pass)
        self._passButton.grid(row=0, column=1)
        
        self._newGameButton = Button(self, text="New Game", command=self._newGame)
        self._newGameButton.grid(row=0, column=2)
        
        # Add the scoreboard button
        self._scoreboardButton = Button(self, text="Scoreboard", command=self._showScoreboard)
        self._scoreboardButton.grid(row=0, column=3)
        
        # Add the status field
        self._statusVar = StringVar()
        self._statusField = Entry(self, textvariable=self._statusVar)
        self._statusField.grid(row=1, column=0, columnspan=4)
        
        # Add the panes for the player and dealer cards
        self._playerPane = Frame(self)
        self._playerPane.grid(row=2, column=0, columnspan=4)
        self._dealerPane = Frame(self)
        self._dealerPane.grid(row=3, column=0, columnspan=4)
        self._newGame()

    # Create the event handler methods
    def _newGame(self):
        """Instantiates the model and establishes the GUI"""
        self._model = Blackjack()
        
        # Refresh the card panes
        # Player Cards
        self._playerImages = list(map(lambda card: PhotoImage(file=card.getFilename()), self._model.getPlayerCards()))
        self._playerLabels = list(map(lambda i: Label(self._playerPane, image=i), self._playerImages))
        for col in range(len(self._playerLabels)):
            self._playerLabels[col].grid(row=0, column=col)
            
        # Dealer Cards    
        self._dealerImages = list(map(lambda card: PhotoImage(file=card.getFilename()), self._model.getDealerCards()))
        self._dealerLabels = list(map(lambda i: Label(self._dealerPane, image=i), self._dealerImages))
        for col in range(len(self._dealerLabels)):
            self._dealerLabels[col].grid(row=0, column=col)
            
        # Re-enable the buttons and clear the status field
        self._hitButton["state"] = NORMAL
        self._passButton["state"] = NORMAL
        self._statusVar.set("")

    def _hit(self):
        """Hits the player in the data model and updates its card pane. If the player points reach or exceed 21, hits the dealer too."""
        (card, points) = self._model.hitPlayer()
        cardImage = PhotoImage(file=card.getFilename())
        self._playerImages.append(cardImage)
        label = Label(self._playerPane, image=cardImage)
        self._playerLabels.append(label)
        label.grid(row=0, column=len(self._playerLabels) - 1)
        if points >= 21:
            self._pass()   # Hits the dealer to finish

    def _pass(self):
	  
    
    #Hit dealer and refresh card pane
        outcome = self._model.hitDealer()
        self._dealerImages = list(map(lambda card: PhotoImage(file = card.getFilename()), self._model.getDealerCards()))
        self._dealerLabels = list(map(lambda i: Label(self._dealerPane, image = i), self._dealerImages))
        for col in range(len(self._dealerLabels)):
            self._dealerLabels[col].grid(row = 0, column = col)
        self._statusVar.set(outcome)
    
    #Disable hit and pass buttons
        self._hitButton["state"] = DISABLED
        self._passButton["state"] = DISABLED
    
    #Display the scoreboard button
        self._scoreboardButton = Button(self, text = "Scoreboard", command = self._showScoreboard)
        self._scoreboardButton.grid(row = 0, column = 3)


        if (outcome == "Congrats! You win!" or outcome == "Blackjack! You Win!"):
            self._updateDatabase("winnings", 1)
        elif(outcome =="Dealer Blackjack! You lose!" or outcome =="You bust and lose!"):
            self._updateDatabase("losses", 1)


    def _updateDatabase(self, column, value):
        db = None
        try:
        # Establish a connection to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="SAchi#98",
                database="blackjack"
            )
            cursor = db.cursor()

        # Update the user's record
            query = "UPDATE users SET {} = {} + %s WHERE username = %s AND password = %s".format(column, column)
            values = (value, self._username, self._password)
            cursor.execute(query, values)
            db.commit()
        except Exception as e:
            print("Error updating database: {}".format(e))
        finally:
        # Close the connection
            db.close()


    
    def _showScoreboard(self):
        """Displays the scoreboard window"""
        scoreboardWindow = Toplevel(self)
        scoreboardWindow.title("Scoreboard")

        # Add the scoreboard table
        tableFrame = Frame(scoreboardWindow)
        tableFrame.pack(side=TOP)

        # Table headers
        usernameHeader = Label(tableFrame, text="Username")
        usernameHeader.grid(row=0, column=0)
        winningsHeader = Label(tableFrame, text="Winnings")
        winningsHeader.grid(row=0, column=1)
        lossesHeader = Label(tableFrame, text="Losses")
        lossesHeader.grid(row=0, column=2)

        try:
            # Establish a connection to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="SAchi#98",
                database="blackjack"
            )
            cursor = db.cursor()
            
           

        # Retrieve the scoreboard data
            cursor.execute("SELECT username, winnings, losses FROM users ORDER BY winnings DESC")
            scoreboardData = cursor.fetchall()

        # Display the scoreboard data in the table
            for i, rowData in enumerate(scoreboardData):
                for j, data in enumerate(rowData):
                    label = Label(tableFrame, text=data)
                    label.grid(row=i+1, column=j)

        except Exception as e:
            print("Error retrieving scoreboard data: {}".format(e))

        finally:
            # Close the connection
            if db:
                db.close()


		

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SAchi#98",
        database="blackjack"
    )

    root = Tk()
    login = LoginWindow(root, db)
    root.mainloop()
