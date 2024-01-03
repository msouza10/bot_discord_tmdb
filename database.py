import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.create_tables()

    def create_tables(self):
        user_api_key_query = """
        CREATE TABLE IF NOT EXISTS user_api_keys (
            user_id INTEGER PRIMARY KEY,
            api_key TEXT NOT NULL
        );
        """
        notification_channel_query = """
        CREATE TABLE IF NOT EXISTS notification_channel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER
        );
        """
        notified_movies_query = """
        CREATE TABLE IF NOT EXISTS notified_movies (
            movie_id INTEGER PRIMARY KEY,
            notified_date TIMESTAMP NOT NULL
        );
        """
        user_session_query = """
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_id INTEGER PRIMARY KEY,
            session_id TEXT,
            account_id TEXT
        );
        """
        self.conn.execute(user_session_query)
        self.conn.execute(user_api_key_query)
        self.conn.execute(notification_channel_query)
        self.conn.execute(notified_movies_query)
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

    def set_notification_channel(self, channel_id):
      query = "REPLACE INTO notification_channel (id, channel_id) VALUES (1, ?)"
      self.conn.execute(query, (channel_id,))
      self.conn.commit()

    def get_notification_channel(self):
      query = "SELECT channel_id FROM notification_channel WHERE id = 1"
      cursor = self.conn.execute(query)
      result = cursor.fetchone()
      return result[0] if result else None

    def add_notified_movie(self, movie_id):
      query = "REPLACE INTO notified_movies (movie_id, notified_date) VALUES (?, ?)"
      self.conn.execute(query, (movie_id, datetime.now()))
      self.conn.commit()

    def get_notified_movies(self):
      query = "SELECT movie_id FROM notified_movies"
      cursor = self.conn.execute(query)
      return [row[0] for row in cursor.fetchall()]

    def clean_notified_movies(self):
      cutoff_date = datetime.now() - timedelta(hours=48)
      query = "DELETE FROM notified_movies WHERE notified_date < ?"
      self.conn.execute(query, (cutoff_date,))
      self.conn.commit()

    def set_user_session(self, user_id, session_id):
      query = "REPLACE INTO user_sessions (user_id, session_id) VALUES (?, ?, ?)"
      self.conn.execute(query, (user_id, session_id))
      self.conn.commit()

    def get_user_session_id(self, user_id):
      query = "SELECT session_id, account_id FROM user_sessions WHERE user_id = ?"
      cursor = self.conn.execute(query, (user_id,))
      result = cursor.fetchone()
      return result if result else (None, None)

