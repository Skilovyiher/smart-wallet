import sqlite3

class DatabaseManager():
    def __init__(self, db_name='wallet.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            balance REAL NOT NULL,
            currency TEXT NOT NULL
        )""")

        conn.commit()
        conn.close()

    def save_wallet(self, wallet):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO wallets (owner, balance, currency)
            VALUES (?, ?, ?)
        """, (wallet.owner, wallet.balance, wallet.currency))

        conn.commit()
        conn.close()

    def load_wallet(self, owner):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM wallets WHERE owner = ?", (owner,))
        result = cursor.fetchone()

        conn.close()
        return result