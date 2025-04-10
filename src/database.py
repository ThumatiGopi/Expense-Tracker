import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        # Create database directory if it doesn't exist
        os.makedirs('database', exist_ok=True)
        
        # Set up connection parameters
        self.db_path = 'database/expenses.db'
        self.timeout = 30
        self.initialize_database()
        
    def get_connection(self):
        """Get a thread-local database connection"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.timeout,
            isolation_level=None
        )
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def get_category_id(self, category_name):
        """Get category ID by name"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def initialize_database(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    email TEXT
                );

                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    category_id INTEGER,
                    amount REAL,
                    description TEXT,
                    date DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );

                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    category_id INTEGER,
                    amount REAL,
                    month DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id),
                    UNIQUE(user_id, category_id, month)
                );

                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    created_by INTEGER,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS group_expenses (
                    id INTEGER PRIMARY KEY,
                    group_id INTEGER,
                    expense_id INTEGER,
                    paid_by INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups(id),
                    FOREIGN KEY (expense_id) REFERENCES expenses(id),
                    FOREIGN KEY (paid_by) REFERENCES users(id)
                );
            ''')

            # Insert default categories
            cursor = conn.cursor()
            default_categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Others']
            for category in default_categories:
                try:
                    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
                except sqlite3.Error as e:
                    print(f"Error inserting category {category}: {e}")

    def add_user(self, username, email):
        """Add a new user"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
                    return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(0.1 * retry_count)
                        continue
                raise
            except Exception as e:
                print(f"Error adding user: {e}")
                return None
        return None

    def get_user(self, username):
        """Get user details by username"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()

    def add_expense(self, user_id, category_id, amount, description, date=None):
        """Add a new expense"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)',
                        (user_id, category_id, amount, description, date)
                    )
                    return cursor.lastrowid
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(0.1 * retry_count)
                        continue
                raise
            except Exception as e:
                print(f"Error adding expense: {e}")
                return None
        return None

    def set_budget(self, user_id, category_id, amount, month):
        """Set or update budget for a category"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Start a transaction
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO budgets (user_id, category_id, amount, month)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(user_id, category_id, month) DO UPDATE 
                        SET amount = excluded.amount
                    ''', (user_id, category_id, amount, month))
                    return True
            except sqlite3.IntegrityError:
                return False
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(0.1 * retry_count)  # Exponential backoff
                        continue
                raise
            except Exception as e:
                print(f"Error setting budget: {e}")
                return False
        return False

    def get_expenses(self, user_id, start_date=None, end_date=None):
        """Get expenses for a user within a date range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT e.*, c.name as category_name 
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
                WHERE e.user_id = ?
            '''
            params = [user_id]
            
            if start_date and end_date:
                query += ' AND e.date BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_budget_status(self, user_id, month):
        """Get budget status for all categories"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT 
                    c.id as category_id,
                    c.name as category_name,
                    COALESCE(b.amount, 0) as budget,
                    COALESCE(SUM(e.amount), 0) as spent
                FROM categories c
                LEFT JOIN budgets b ON c.id = b.category_id 
                    AND b.user_id = ? 
                    AND strftime('%Y-%m', b.month) = strftime('%Y-%m', ?)
                LEFT JOIN expenses e ON c.id = e.category_id 
                    AND e.user_id = ?
                    AND strftime('%Y-%m', e.date) = strftime('%Y-%m', ?)
                GROUP BY c.id, c.name, b.amount
            '''
            cursor.execute(query, (user_id, month, user_id, month))
            return cursor.fetchall()

    def create_group(self, name, created_by):
        """Create a new expense sharing group"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO groups (name, created_by) VALUES (?, ?)', (name, created_by))
                    return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(0.1 * retry_count)
                        continue
                raise
            except Exception as e:
                print(f"Error creating group: {e}")
                return None
        return None

    def add_group_expense(self, group_id, expense_id, paid_by):
        """Add an expense to a group"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO group_expenses (group_id, expense_id, paid_by) VALUES (?, ?, ?)',
                        (group_id, expense_id, paid_by)
                    )
                    return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(0.1 * retry_count)
                        continue
                raise
            except Exception as e:
                print(f"Error adding group expense: {e}")
                return None
        return None

    def get_group_expenses(self, group_id):
        """Get all expenses for a group"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT 
                    e.*,
                    c.name as category_name,
                    u.username as paid_by_user
                FROM group_expenses ge
                JOIN expenses e ON ge.expense_id = e.id
                JOIN categories c ON e.category_id = c.id
                JOIN users u ON ge.paid_by = u.id
                WHERE ge.group_id = ?
            '''
            cursor.execute(query, (group_id,))
            return cursor.fetchall()

    def get_user_groups(self, user_id):
        """Get all groups for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE created_by = ?', (user_id,))
            return cursor.fetchall()
