import sqlite3
import json
from datetime import datetime
import tempfile
import os

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            if self.db_path is None:
                # Use a temporary file for the database if no path is provided
                # This is useful for environments like Streamlit Cloud where 
                # standard paths might not be writable.
                # The database will be in-memory or a temporary file that resets
                # with each new app session/restart.
                self.db_path = os.path.join(tempfile.gettempdir(), "app.db")
            self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create journal_entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_text TEXT NOT NULL,
                entry_date DATE NOT NULL,
                detected_keywords TEXT,
                keyword_category VARCHAR(50),
                ai_emotion VARCHAR(50),
                ai_intensity INTEGER,
                ai_themes TEXT,
                ai_recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Create affirmation_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS affirmation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                affirmation_id INTEGER NOT NULL,
                displayed_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        self.close_connection()
    
    def save_journal_entry(self, user_id, text, keyword_result, ai_result):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO journal_entries 
            (user_id, entry_text, entry_date, detected_keywords, 
             keyword_category, ai_emotion, ai_intensity, ai_themes, ai_recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            text,
            datetime.now().date(),
            json.dumps(keyword_result['keywords']),
            keyword_result['category'],
            ai_result['primary_emotion'],
            ai_result['intensity'],
            json.dumps(ai_result['themes']),
            ai_result['suggestion']
        ))
        
        conn.commit()
        self.close_connection()
    
    def get_journal_entries_by_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT entry_date, entry_text, detected_keywords, keyword_category, 
                   ai_emotion, ai_intensity, ai_themes, ai_recommendation, created_at
            FROM journal_entries
            WHERE user_id = ?
            ORDER BY entry_date ASC
        ''', (user_id,))
        
        entries = cursor.fetchall()
        self.close_connection()
        return entries

    def save_affirmation_log(self, user_id, affirmation_id, displayed_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO affirmation_logs 
            (user_id, affirmation_id, displayed_date)
            VALUES (?, ?, ?)
        ''', (
            user_id,
            affirmation_id,
            displayed_date
        ))
        conn.commit()
        self.close_connection()

    def get_last_affirmation_date(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT displayed_date
            FROM affirmation_logs
            WHERE user_id = ?
            ORDER BY displayed_date DESC
            LIMIT 1
        ''', (user_id,))
        last_date = cursor.fetchone()
        self.close_connection()
        return last_date[0] if last_date else None