from tkinter import *
from tkinter import messagebox
from blackjack import Blackjack
import mysql.connector
import random



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
            game_window.title("BlackjackGame")
            game_window.geometry("600x600")





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
