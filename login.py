import tkinter
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from utils import error
import mysql.connector

class Login:
    """Represents a login window for user authentication."""
    def __init__(self, con):  # fixed __init__ method
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Sign In")
        self.window.geometry("500x600")
        self.con = con
        self.cur = con.cursor()
        self.user = None
        self.login_window()

    def login_window(self, event=None):
        """Function to create login window."""
        self.window.title("Sign In")
        self.window.bind('<Return>', self.login)

        try:
            img = ctk.CTkImage(dark_image=Image.open("./imgs/bg.jpg").resize((500,600)), size=(500,600))
            bg = ctk.CTkLabel(master=self.window, image=img)
            bg.place(x=0, y=0)
        except:
            bg = ctk.CTkLabel(master=self.window, text="Login", font=('Arial', 20))
            bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = ctk.CTkFrame(master=bg, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.login_label = ctk.CTkLabel(master=self.frame, text="Log in", font=('Century Gothic', 30))
        self.login_label.place(x=100, y=45)

        self.username = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.username.place(x=50, y=110)

        self.password = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*")
        self.password.place(x=50, y=165)

        self.label_link = ctk.CTkLabel(master=self.frame, text="Don't have an account? Register", font=('Century Gothic', 13))
        self.label_link.place(x=60, y=210)
        self.label_link.bind("<Button-1>", self.register_window)

        self.login_button = ctk.CTkButton(master=self.frame, width=220, text="Login", command=self.login, corner_radius=6)
        self.login_button.place(x=50, y=250)

    def register_window(self, event=None):
        """Function to display register window."""
        self.window.title("Create an account")
        self.window.bind('<Return>', self.register)
        self.login_label.configure(text="Register")
        self.label_link.configure(text="Already have an account? Sign in")
        self.label_link.bind("<Button-1>", self.login_window)
        self.login_button.configure(text="Continue", command=self.register)

    def login(self, event=None):
        """Authenticate the user."""
        uname = self.username.get()
        pwd = self.password.get()

        # Ensure admin exists
        self.cur.execute("INSERT IGNORE INTO users (username, password, account_type) VALUES ('ADMIN', 'ADMIN', 'ADMIN');")
        self.con.commit()

        self.cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        f = self.cur.fetchone()
        if f:
            print(f"└─Logged in as {uname}")
            self.user = f
            self.window.quit()
        else:
            error("Invalid Username or Password")

    def register(self, event=None):
        """Register a new user."""
        uname = self.username.get()
        pwd = self.password.get()

        if len(uname) == 0 or len(pwd) == 0:
            error("Length of the Username and Password should be greater than 0")
            return
        if len(uname) > 20 or len(pwd) > 20:
            error("Length of the Username and Password should be less than 20")
            return

        self.cur.execute("SELECT * FROM users WHERE username=%s", (uname,))
        if self.cur.fetchone():
            error("Username already exists")
        else:
            self.cur.execute("INSERT INTO users VALUES (%s, %s, 'USER')", (uname, pwd))
            self.con.commit()
            messagebox.showinfo("Account created", "Your account has been successfully created!")
            self.user = (uname, pwd, 'USER')
            self.window.quit()

# --- Main Driver Code ---
if __name__ == "__main__":  # fixed here
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",            # Change if your DB user is different
            password="root",        # Update with your MySQL password
            database="inventory"    # Make sure this DB exists
        )

        app = Login(connection)
        app.window.mainloop()

        if app.user:
            print("Login/Register successful:", app.user)
        else:
            print("No user logged in.")

        connection.close()

    except mysql.connector.Error as e:
        print("Database Connection Failed:", e)
