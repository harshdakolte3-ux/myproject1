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

    ("Pepperoni Pizza", "Pizza with pepperoni and cheese", 349, "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&h=300&fit=crop", "Pizza"),
    ("Vegetarian Burger", "Fresh veggies in a bun", 199, "https://images.unsplash.com/photo-1550317138-10000687a72b?w=300&h=300&fit=crop", "Burgers"),
    ("Chicken Burger", "Grilled chicken patty burger", 249, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=300&fit=crop", "Burgers"),
    ("Biryani", "Fragrant rice with chicken", 299, "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300&h=300&fit=crop", "Rice"),
    ("Fried Rice", "Stir-fried rice with vegetables", 199, "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=300&fit=crop", "Rice"),
    ("Chicken Tikka Masala", "Creamy curry with chicken", 349, "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=300&h=300&fit=crop", "Curry"),
    ("Paneer Butter Masala", "Rich paneer curry", 299, "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=300&fit=crop", "Curry"),
    ("Tandoori Chicken", "Spiced grilled chicken", 349, "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=300&h=300&fit=crop", "Grill"),
    ("Garlic Naan", "Soft bread with garlic butter", 79, "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=300&fit=crop", "Bread"),
    ("Coke", "Coca Cola 330ml", 49, "https://images.unsplash.com/photo-1561758033-7e924f619b47?w=300&h=300&fit=crop", "Beverages"),
    ("Sprite", "Sprite 330ml", 49, "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=300&h=300&fit=crop", "Beverages"),
    ("Ice Cream", "Vanilla ice cream", 99, "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=300&h=300&fit=crop", "Desserts"),
    ("Chocolate Cake", "Rich chocolate cake", 199, "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "Desserts"),
    ("Samosa", "Crispy triangular pastry", 49, "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=300&h=300&fit=crop", "Snacks"),
    ("Chicken Wings", "Spicy chicken wings", 199, "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=300&h=300&fit=crop", "Snacks"),
    ("Fish Curry", "Spiced fish in gravy", 329, "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=300&fit=crop", "Curry"),
    ("Mutton Curry", "Tender mutton pieces", 399, "https://images.unsplash.com/photo-1574653853027-5382a3d23a15?w=300&h=300&fit=crop", "Curry"),
    ("Veggie Pasta", "Italian pasta with vegetables", 229, "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=300&fit=crop", "Pasta"),
    ("Alfredo Pasta", "Creamy white pasta sauce", 259, "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=300&fit=crop", "Pasta"),
    ]

         
    (
            "Margherita Pizza",
            "Classic tomato and mozzarella pizza",
            299,
            "/static/images/margherita_pizza.jpg",
            "Pizza"
        ),
    (
            "Pepperoni Pizza",
            "Pizza with pepperoni and cheese",
            349,
            "/static/images/pepperoni_pizza.jpg",
            "Pizza"
        ),
    (
            "Vegetarian Burger",
            "Fresh veggies in a soft bun",
            199,
            "/static/images/veg_burger.jpg",
            "Burgers"
        ),
    (
            "Chicken Burger",
            "Grilled chicken patty burger",
            249,
            "/static/images/chicken_burger.jpg",
            "Burgers"
        ),
    (
            "Biryani",
            "Fragrant basmati rice with spiced chicken",
            299,
            "/static/images/biryani.jpg",
            "Rice"
        ),
    (
            "Fried Rice",
            "Stir-fried rice with vegetables and egg",
            199,
            "/static/images/fried_rice.jpg",
            "Rice"
        ),
    (
            "Chicken Tikka Masala",
            "Tender chicken in creamy tomato curry",
            349,
            "/static/images/chicken_tikka.jpg",
            "Curry"
        ),
    (
            "Paneer Butter Masala",
            "Rich and creamy paneer curry",
            299,
            "/static/images/paneer_masala.jpg",
            "Curry"
        ),
    (
            "Tandoori Chicken",
            "Smoky spiced grilled chicken",
            349,
            "/static/images/tandoori_chicken.jpg",
            "Grill"
        ),
    (
            "Garlic Naan",
            "Soft fluffy bread with garlic butter",
            79,
            "/static/images/garlic_naan.jpg",
            "Bread"
        ),
    (
            "Coke",
            "Coca Cola 330ml chilled",
            49,
            "/static/images/coke.jpg",
            "Beverages"
        ),
    (
            "Sprite",
            "Sprite 330ml chilled",
            49,
            "/static/images/sprite.jpg",
            "Beverages"
        ),
    (
            "Ice Cream",
            "Creamy vanilla ice cream scoop",
            99,
            "/static/images/ice_cream.jpg",
            "Desserts"
        ),
    (
            "Chocolate Cake",
            "Rich moist chocolate layer cake",
            199,
            "/static/images/chocolate_cake.jpg",
            "Desserts"
        ),
    (
            "Samosa",
            "Crispy triangular pastry with spiced filling",
            49,
            "/static/images/samosa.jpg",
            "Snacks"
        ),
    (
            "Chicken Wings",
            "Spicy crispy chicken wings",
            199,
            "/static/images/chicken_wings.jpg",
            "Snacks"
        ),
    (
            "Fish Curry",
            "Spiced fish pieces in tangy gravy",
            329,
            "/static/images/fish_curry.jpg",
            "Curry"
        ),
    (
            "Mutton Curry",
            "Slow-cooked tender mutton in rich gravy",
            399,
            "/static/images/mutton_curry.jpg",
            "Curry"
        ),
    (
            "Veggie Pasta",
            "Italian penne pasta with fresh vegetables",
            229,
            "/static/images/veggie_pasta.jpg",
            "Pasta"
        ),
    (
            "Alfredo Pasta",
            "Creamy white sauce fettuccine pasta",
            259,
            "/static/images/alfredo_pasta.jpg",
            "Pasta"
        ),

        
    ("Pepperoni Pizza", "Pizza with pepperoni and cheese", 349, "https://images.unsplash.com/photo-1628840042765-356cda07f4ee", "Pizza"),
    ("Vegetarian Burger", "Fresh veggies in a bun", 199, "https://images.unsplash.com/photo-1585617372265-a5ae3d1ad02c?w=300&h=300&fit=crop", "Burgers"),
    ("Chicken Burger", "Grilled chicken patty burger", 249, "https://images.unsplash.com/photo-1562547256-f6f9c5c1dae1?w=300&h=300&fit=crop", "Burgers"),
    ("Biryani", "Fragrant rice with chicken", 299, "https://images.unsplash.com/photo-1478201143081-80f7f84ca84d?w=300&h=300&fit=crop", "Rice"),
    ("Fried Rice", "Stir-fried rice with vegetables", 199, "https://images.unsplash.com/photo-1609501676725-7186f017a4b8?w=300&h=300&fit=crop", "Rice"),
    ("Chicken Tikka Masala", "Creamy curry with chicken", 349, "https://images.unsplash.com/photo-1565557623814-43db76f89c0b?w=300&h=300&fit=crop", "Curry"),
    ("Paneer Butter Masala", "Rich paneer curry", 299, "https://images.unsplash.com/photo-1526231761103-f898f6e7cecd?w=300&h=300&fit=crop", "Curry"),
    ("Tandoori Chicken", "Spiced grilled chicken", 349, "https://images.unsplash.com/photo-1565557623814-43db76f89c0b?w=300&h=300&fit=crop", "Grill"),
    ("Garlic Naan", "Soft bread with garlic butter", 79, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=300&fit=crop", "Bread"),
    ("Coke", "Coca Cola 330ml", 49, "https://images.unsplash.com/photo-1554866585-c5c9a8b19a11?w=300&h=300&fit=crop", "Beverages"),
    ("Sprite", "Sprite 330ml", 49, "https://images.unsplash.com/photo-1589985643662-4b090ec23247?w=300&h=300&fit=crop", "Beverages"),
    ("Ice Cream", "Vanilla ice cream", 99, "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=300&h=300&fit=crop", "Desserts"),
    ("Chocolate Cake", "Rich chocolate cake", 199, "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "Desserts"),
    ("Samosa", "Crispy triangular pastry", 49, "https://images.unsplash.com/photo-1585457469293-fa476e9e0ca0?w=300&h=300&fit=crop", "Snacks"),
    ("Chicken Wings", "Spicy chicken wings", 199, "https://images.unsplash.com/photo-1608039755401-742f15d70a8a?w=300&h=300&fit=crop", "Snacks"),
    ("Fish Curry", "Spiced fish in gravy", 329, "https://images.unsplash.com/photo-1626973289835-39e1e0a0b3ba?w=300&h=300&fit=crop", "Curry"),
    ("Mutton Curry", "Tender mutton pieces", 399, "https://images.unsplash.com/photo-1588200201387-d99a706c7d98?w=300&h=300&fit=crop", "Curry"),
    ("Veggie Pasta", "Italian pasta with vegetables", 229, "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=300&h=300&fit=crop", "Pasta"),
    ("Alfredo Pasta", "Creamy white pasta sauce", 259, "https://images.unsplash.com/photo-1645112411341-6c4ee32510d8?w=300&h=300&fit=crop", "Pasta"),
 

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