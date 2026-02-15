import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Создание таблицы с 10 полями + ID"""
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS classmates (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    age INTEGER,
                    group_code TEXT,
                    phone TEXT,
                    email TEXT,
                    tg_username TEXT,
                    hobby TEXT,
                    favorite_subject TEXT,
                    hometown TEXT,
                    motivation TEXT
                )
            """)

    def add_classmate(self, user_id, data: dict):
        """Запись всех собранных данных в БД"""
        with self.connection:
            return self.cursor.execute(
                """INSERT OR REPLACE INTO classmates 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, *data.values())
            )

    def close(self):
        self.connection.close()