import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple

class SecurityDatabase:
    def __init__(self, db_path: str = "security_reports.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create security reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    status TEXT NOT NULL,
                    recommended_action TEXT NOT NULL,
                    reporter_id INTEGER NOT NULL,
                    reporter_name TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Create focal people table (authorized reporters)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS focal_people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    added_by INTEGER NOT NULL,
                    added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Create admins table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER UNIQUE NOT NULL,
                    added_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_security_report(self, location: str, status: str, recommended_action: str, 
                           reporter_id: int, reporter_name: str) -> bool:
        """Add a new security report"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO security_reports 
                    (location, status, recommended_action, reporter_id, reporter_name)
                    VALUES (?, ?, ?, ?, ?)
                ''', (location, status, recommended_action, reporter_id, reporter_name))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding security report: {e}")
            return False
    
    def get_latest_reports(self, limit: int = 10) -> List[Tuple]:
        """Get the latest security reports"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT location, status, recommended_action, reporter_name, timestamp 
                FROM security_reports 
                WHERE is_active = 1
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def get_reports_by_location(self, location: str, limit: int = 5) -> List[Tuple]:
        """Get security reports for a specific location"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT location, status, recommended_action, reporter_name, timestamp 
                FROM security_reports 
                WHERE is_active = 1 AND location LIKE ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (f'%{location}%', limit))
            return cursor.fetchall()
    
    def add_focal_person(self, telegram_user_id: int, name: str, added_by: int) -> bool:
        """Add a new focal person (authorized reporter)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO focal_people 
                    (telegram_user_id, name, added_by)
                    VALUES (?, ?, ?)
                ''', (telegram_user_id, name, added_by))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding focal person: {e}")
            return False
    
    def is_focal_person(self, telegram_user_id: int) -> bool:
        """Check if a user is an authorized focal person"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM focal_people 
                WHERE telegram_user_id = ? AND is_active = 1
            ''', (telegram_user_id,))
            return cursor.fetchone() is not None
    
    def add_admin(self, telegram_user_id: int) -> bool:
        """Add an admin user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO admins (telegram_user_id)
                    VALUES (?)
                ''', (telegram_user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding admin: {e}")
            return False
    
    def is_admin(self, telegram_user_id: int) -> bool:
        """Check if a user is an admin"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM admins 
                WHERE telegram_user_id = ?
            ''', (telegram_user_id,))
            return cursor.fetchone() is not None
    
    def get_all_focal_people(self) -> List[Tuple]:
        """Get all active focal people"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT telegram_user_id, name, added_date 
                FROM focal_people 
                WHERE is_active = 1
                ORDER BY added_date DESC
            ''')
            return cursor.fetchall()
    
    def remove_focal_person(self, telegram_user_id: int) -> bool:
        """Remove a focal person (deactivate)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE focal_people 
                    SET is_active = 0 
                    WHERE telegram_user_id = ?
                ''', (telegram_user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error removing focal person: {e}")
            return False
