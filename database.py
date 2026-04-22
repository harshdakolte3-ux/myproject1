import sqlite3
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = get_db()
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Food items table
    c.execute('''CREATE TABLE food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image_url TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Cart table
    c.execute('''CREATE TABLE cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        food_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (food_id) REFERENCES food_items (id)
    )''')

    # Wishlist table
    c.execute('''CREATE TABLE wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        food_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (food_id) REFERENCES food_items (id)
    )''')

    # Orders table
    c.execute('''CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        items TEXT NOT NULL,
        total_price REAL NOT NULL,
        customer_name TEXT NOT NULL,
        city TEXT NOT NULL,
        mobile_number TEXT NOT NULL,
        payment_mode TEXT NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')

    # ----------------------------------------------------------------
    # 20 food items — all images use picsum.photos (always works,
    # no API key, no expiry, no internet restrictions on most networks)
    # Format: https://picsum.photos/seed/<unique_word>/300/300
    # ----------------------------------------------------------------
    food_items = [

    ]

    c.executemany(
        'INSERT INTO food_items (name, description, price, image_url, category) VALUES (?, ?, ?, ?, ?)',
        food_items
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully with 20 food items.")


# ----------------------------------------------------------------
# User functions
# ----------------------------------------------------------------

def register_user(username, email, password):
    try:
        conn = get_db()
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful"
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    except Exception as e:
        return False, str(e)


def login_user(username, password):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            return True, user['id']
        return False, None
    except Exception:
        return False, None


def get_user(user_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    except Exception:
        return None


# ----------------------------------------------------------------
# Food item functions
# ----------------------------------------------------------------

def get_all_food_items(limit=20):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM food_items LIMIT ?', (limit,))
        items = c.fetchall()
        conn.close()
        return items
    except Exception:
        return []


def search_food_items(search_term):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'SELECT * FROM food_items WHERE name LIKE ? OR category LIKE ? LIMIT 20',
            (f'%{search_term}%', f'%{search_term}%')
        )
        items = c.fetchall()
        conn.close()
        return items
    except Exception:
        return []


def get_food_item(food_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM food_items WHERE id = ?', (food_id,))
        item = c.fetchone()
        conn.close()
        return item
    except Exception:
        return None


# ----------------------------------------------------------------
# Cart functions
# ----------------------------------------------------------------

def add_to_cart(user_id, food_id, quantity):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM cart WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        existing = c.fetchone()
        if existing:
            c.execute(
                'UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND food_id = ?',
                (quantity, user_id, food_id)
            )
        else:
            c.execute(
                'INSERT INTO cart (user_id, food_id, quantity) VALUES (?, ?, ?)',
                (user_id, food_id, quantity)
            )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def remove_from_cart(user_id, food_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM cart WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def update_cart_quantity(user_id, food_id, quantity):
    try:
        conn = get_db()
        c = conn.cursor()
        if quantity <= 0:
            c.execute('DELETE FROM cart WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        else:
            c.execute(
                'UPDATE cart SET quantity = ? WHERE user_id = ? AND food_id = ?',
                (quantity, user_id, food_id)
            )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_cart_items(user_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            '''SELECT c.id, f.id as food_id, f.name, f.price, c.quantity, f.image_url
               FROM cart c
               JOIN food_items f ON c.food_id = f.id
               WHERE c.user_id = ?''',
            (user_id,)
        )
        items = c.fetchall()
        conn.close()
        return items
    except Exception:
        return []


def clear_cart(user_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ----------------------------------------------------------------
# Wishlist functions
# ----------------------------------------------------------------

def add_to_wishlist(user_id, food_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'INSERT OR IGNORE INTO wishlist (user_id, food_id) VALUES (?, ?)',
            (user_id, food_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def remove_from_wishlist(user_id, food_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM wishlist WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_wishlist(user_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            '''SELECT f.id, f.name, f.price, f.image_url, f.description
               FROM wishlist w
               JOIN food_items f ON w.food_id = f.id
               WHERE w.user_id = ?''',
            (user_id,)
        )
        items = c.fetchall()
        conn.close()
        return items
    except Exception:
        return []


def is_in_wishlist(user_id, food_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM wishlist WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        item = c.fetchone()
        conn.close()
        return item is not None
    except Exception:
        return False


# ----------------------------------------------------------------
# Order functions
# ----------------------------------------------------------------

def place_order(user_id, items, total_price, customer_name, city, mobile_number, payment_mode):
    try:
        import json
        conn = get_db()
        c = conn.cursor()
        items_json = json.dumps(items)
        c.execute(
            '''INSERT INTO orders (user_id, items, total_price, customer_name, city, mobile_number, payment_mode)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user_id, items_json, total_price, customer_name, city, mobile_number, payment_mode)
        )
        conn.commit()
        order_id = c.lastrowid
        conn.close()
        return True, order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return False, None


def get_orders(user_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC', (user_id,))
        orders = c.fetchall()
        conn.close()
        return orders
    except Exception:
        return []


def get_order(order_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = c.fetchone()
        conn.close()
        return order
    except Exception:
        return None