import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_api_keys (
            user_id INTEGER PRIMARY KEY,
            api_key TEXT NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def set_user_api_key(self, user_id, api_key):
        query = "REPLACE INTO user_api_keys (user_id, api_key) VALUES (?, ?)"
        self.conn.execute(query, (user_id, api_key))
        self.conn.commit()

    def get_user_api_key(self, user_id):
        query = "SELECT api_key FROM user_api_keys WHERE user_id = ?"
        cursor = self.conn.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
