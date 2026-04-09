# FoodHub Installation & Setup Guide

## Quick Start

### Windows Users

1. **Open Command Prompt or PowerShell** in the project folder
2. **Run:**
   ```bash
   run.bat
   ```
3. **Open browser** and go to: `http://localhost:5000`

### Mac/Linux Users

1. **Open Terminal** in the project folder
2. **Make script executable:**
   ```bash
   chmod +x run.sh
   ```
3. **Run:**
   ```bash
   ./run.sh
   ```
4. **Open browser** and go to: `http://localhost:5000`

---

## Manual Installation

### Step 1: Install Python

**Windows:**
- Download from https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Verify installation:
  ```bash
  python --version
  ```

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Install Dependencies

Navigate to the project folder and run:

```bash
pip install -r requirements.txt
```

Or if that doesn't work:

```bash
python -m pip install -r requirements.txt
```

**Expected output:** Flask, Flask-SQLAlchemy, and Werkzeug should be installed successfully.

### Step 3: Run the Application

```bash
python app.py
```

Or:

```bash
python3 app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 4: Test in Browser

Open `http://localhost:5000` in your web browser.

---

## First Time Setup

### Creating Your Account

1. You'll be redirected to the **Login page**
2. Click **"Register here"** link
3. Fill in:
   - **Username:** Choose any username (letters, numbers, underscore)
   - **Email:** Valid email address
   - **Password:** At least 6 characters recommended
   - **Confirm Password:** Must match password
4. Click **Register** button
5. You'll be redirected to **Login page**
6. Login with your credentials

### Welcome to Dashboard

After login, you'll see:
- **20 Food Items** in a grid layout
- **Search bar** to find items
- **Navigation menu** in the top bar

---

## Testing the Features

### Test Checklist

- [ ] **Registration:** Create a new account
- [ ] **Login:** Login with credentials
- [ ] **View Items:** Home page shows 20 food items
- [ ] **Search:** Search for "pizza" and verify results
- [ ] **Add to Cart:** Click "Add to Cart" on any item
- [ ] **View Cart:** Click "Cart" in navbar and verify items
- [ ] **Modify Cart:** Increase/decrease quantity, remove items
- [ ] **Add to Wishlist:** Click heart icon on food items
- [ ] **View Wishlist:** Check wishlist page
- [ ] **Checkout:** Click "Proceed to Order" from cart
- [ ] **Fill Details:** Enter delivery information
- [ ] **Place Order:** Complete order and see receipt
- [ ] **View Orders:** Check "Orders" page for order history
- [ ] **Dark Mode:** Toggle dark/light mode with button
- [ ] **Logout:** Click logout button

---

## Troubleshooting

### Issue: "Python not found"

**Solution:**
- Make sure Python is installed
- Add Python to PATH and restart terminal
- Try `python3` instead of `python`

### Issue: "pip: command not found"

**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution 1:** Close other applications using port 5000

**Solution 2:** Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to any free port
```

### Issue: "Module not found (Flask, etc.)"

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Static files not loading (CSS/JS broken)"

**Verify this folder structure exists:**
```
timepas/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── (all .html files)
├── app.py
└── database.py
```

### Issue: "Database errors"

**Reset database:**
1. Delete `data.db` file
2. Restart application
3. Database will be recreated automatically

---

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with all routes |
| `database.py` | Database initialization and helper functions |
| `requirements.txt` | Python package dependencies |
| `templates/base.html` | Base template with navbar (inherited by all pages) |
| `templates/login.html` | Login page |
| `templates/register.html` | Registration page |
| `templates/index.html` | Home/Dashboard with food items |
| `templates/cart.html` | Shopping cart page |
| `templates/checkout.html` | Checkout form |
| `templates/receipt.html` | Order receipt |
| `templates/orders.html` | Order history |
| `templates/wishlist.html` | Wishlist page |
| `static/css/style.css` | All CSS styling (responsive + dark mode) |
| `static/js/main.js` | JavaScript utilities |
| `run.bat` | Windows startup script |
| `run.sh` | Mac/Linux startup script |
| `data.db` | SQLite database (created automatically) |

---

## API Endpoints Reference

### Authentication
- `GET /` → Home/Dashboard (protected)
- `GET /login` → Login page
- `POST /login` → Submit login form
- `GET /register` → Register page
- `POST /register` → Submit registration form
- `GET /logout` → Logout

### Shopping
- `GET /search` → Search results
- `GET /cart` → Cart page
- `POST /api/add-to-cart` → Add item to cart (AJAX)
- `POST /api/remove-from-cart` → Remove from cart (AJAX)
- `POST /api/update-cart-quantity` → Update quantity (AJAX)

### Wishlist
- `GET /wishlist` → Wishlist page
- `POST /api/add-to-wishlist` → Add to wishlist (AJAX)
- `POST /api/remove-from-wishlist` → Remove from wishlist (AJAX)
- `GET /api/is-in-wishlist/<id>` → Check if in wishlist (AJAX)

### Orders
- `GET /checkout` → Checkout page
- `POST /place-order` → Submit order
- `GET /receipt/<id>` → Order receipt
- `GET /orders` → Order history

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP
)
```

### Food Items Table
```sql
CREATE TABLE food_items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    price REAL,
    image_url TEXT,
    category TEXT,
    created_at TIMESTAMP
)
```

### Cart Table
```sql
CREATE TABLE cart (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    food_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (food_id) REFERENCES food_items(id)
)
```

### Wishlist Table
```sql
CREATE TABLE wishlist (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    food_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (food_id) REFERENCES food_items(id)
)
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    items TEXT,
    total_price REAL,
    customer_name TEXT,
    city TEXT,
    mobile_number TEXT,
    payment_mode TEXT,
    order_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

---

## Security Notes

⚠️ **For Production Use:**

1. Change the secret key in `app.py`:
   ```python
   app.secret_key = 'generate-a-long-random-string'
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

3. Enable HTTPS

4. Use environment variables for sensitive data

5. Add CSRF protection

6. Implement rate limiting

---

## Stopping the Server

### Windows/Mac/Linux

Press `Ctrl + C` in the terminal to stop the server.

---

## Need Help?

1. Check the **README.md** for feature overview
2. Review code comments in `app.py` and `database.py`
3. Check browser console (F12) for JavaScript errors
4. Verify file paths match exactly
5. Make sure all dependencies are installed

---

**Happy Food Ordering! 🍕🍔🍜**
