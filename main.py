import mysql.connector as mycon
from login import Login
from menu import Menu

class Main:
    """Represents the main application window for the inventory management system."""
    def __init__(self):
        self.con = mycon.connect(host='localhost', user='root', passwd='root')  # replace with your MySQL user and password

        if self.con.is_connected():
            print('* Connected to MySQL server')
            self.cur = self.con.cursor()
        else:
            print('[!] Not connected to MySQL')
            return

        # Create database and tables if not exist
        self.cur.execute("CREATE DATABASE IF NOT EXISTS inventory")
        self.con.database = 'inventory'

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(20) PRIMARY KEY,
                password VARCHAR(20) NOT NULL,
                account_type VARCHAR(10) NOT NULL
            );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id VARCHAR(20) PRIMARY KEY,
                product_name VARCHAR(50) NOT NULL,
                description VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                quantity INTEGER NOT NULL
            );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer VARCHAR(20),
                date DATE,
                total_items INTEGER,
                total_amount DECIMAL(10, 2),
                payment_status VARCHAR(20)
            );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id VARCHAR(20),
                quantity INTEGER NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            );
        """)

        self.login = Login(self.con)
        self.login.window.mainloop()

        if self.login.user:
            self.menu = Menu(self.con, self.login.user, self.login.window)
            self.menu.window.mainloop()

            if self.menu.logout:
                Main()


if __name__ == "__main__":
    m = Main()
