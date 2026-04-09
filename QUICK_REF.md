# 🚀 FoodHub - Quick Reference Guide

## 30-Second Setup

```bash
cd timepas
pip install -r requirements.txt
python app.py
```

Open: **http://localhost:5000**

---

## File Map

| File | Purpose | Lines |
|------|---------|-------|
| `app.py` | Flask routes & logic | 175+ |
| `database.py` | DB setup & queries | 280+ |
| `base.html` | Navbar template | 50+ |
| `index.html` | Home/dashboard | 120+ |
| `cart.html` | Shopping cart | 95+ |
| `checkout.html` | Order form | 75+ |
| `receipt.html` | Order confirmation | 110+ |
| `orders.html` | Order history | 50+ |
| `style.css` | All styling | 620+ |
| `main.js` | JS utilities | 70+ |

---

## API Routes

### Auth
- `GET /login` - Login page
- `POST /login` - Submit login
- `GET /register` - Register page
- `POST /register` - Submit register
- `GET /logout` - Logout

### Pages
- `GET /` - Home (protected)
- `GET /search` - Search results
- `GET /cart` - Cart page
- `GET /wishlist` - Wishlist page
- `GET /checkout` - Order form
- `GET /orders` - Order history
- `GET /receipt/<id>` - Order receipt

### AJAX APIs
- `POST /api/add-to-cart` - Add item
- `POST /api/remove-from-cart` - Remove item
- `POST /api/update-cart-quantity` - Update qty
- `POST /api/add-to-wishlist` - Add to wishlist
- `POST /api/remove-from-wishlist` - Remove wishlist
- `GET /api/is-in-wishlist/<id>` - Check wishlist
- `POST /place-order` - Create order

---

## Database Quick Reference

### Initialize
```python
from database import init_db
init_db()  # Creates tables and inserts 20 items
```

### Key Functions
```python
# Users
register_user(username, email, password) → (bool, msg)
login_user(username, password) → (bool, user_id)
get_user(user_id) → user_row

# Items
get_all_food_items(limit=20) → list
search_food_items(term) → list

# Cart
add_to_cart(user_id, food_id, qty) → bool
remove_from_cart(user_id, food_id) → bool
update_cart_quantity(user_id, food_id, qty) → bool
get_cart_items(user_id) → list
clear_cart(user_id) → bool

# Wishlist
add_to_wishlist(user_id, food_id) → bool
remove_from_wishlist(user_id, food_id) → bool
get_wishlist(user_id) → list
is_in_wishlist(user_id, food_id) → bool

# Orders
place_order(user_id, items, total, ...) → (bool, order_id)
get_orders(user_id) → list
get_order(order_id) → order_row
```

---

## Common Tasks

### Add New Food Item
```python
# Add to food_items list in database.py init_db()
("Item Name", "Description", 299, "image_url", "Category"),
```

### Change Port
Edit `app.py`:
```python
app.run(debug=True, port=5001)
```

### Reset Database
```bash
# Delete file
rm data.db
# or
del data.db  # Windows
# Restart server
python app.py
```

### Modify Styling
Edit `static/css/style.css` - colors, spacing, fonts

### Add JavaScript
Edit `static/js/main.js` - add functions, event listeners

---

## Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| Username | Any text | `john_doe` |
| Email | Valid email | `john@example.com` |
| Password | Any text | `MyPassword123` |
| Mobile | 10 digits | `9876543210` |
| City | Any text | `Mumbai` |
| Payment | Dropdown | `Cash` / `Card` / `UPI` |

---

## Dark Mode Implementation

### Toggle Button
```html
<button class="theme-toggle" onclick="toggleDarkMode()">🌙</button>
```

### JavaScript
```javascript
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', ...);
}
```

### CSS
```css
body.dark-mode {
    background-color: #1a1a1a;
    color: #f5f5f5;
}
```

---

## Food Items (20 Total)

1-2: Margherita/Pepperoni Pizza (₹299-349)
3-4: Veg/Chicken Burger (₹199-249)
5-6: Biryani/Fried Rice (₹199-299)
7-9: Tikka/Paneer/Fish Curry (₹299-399)
10: Tandoori Chicken (₹349)
11: Garlic Naan (₹79)
12-13: Coke/Sprite (₹49)
14-15: Ice Cream/Chocolate Cake (₹99-199)
16-17: Samosa/Chicken Wings (₹49-199)
18-20: Mutton Curry/Veggie/Alfredo Pasta (₹259-399)

---

## Testing Script

```python
# Quick test in Python shell
from database import *

# Create user
register_user('testuser', 'test@example.com', 'password')

# Login
success, user_id = login_user('testuser', 'password')

# Get items
items = get_all_food_items()

# Add to cart
add_to_cart(user_id, 1, 2)

# View cart
cart = get_cart_items(user_id)

# Place order
place_order(user_id, [...], 500, 'Name', 'City', '9876543210', 'Cash')
```

---

## Directory Structure Rules

```
✅ CORRECT:
timepas/
├── app.py
├── database.py
├── templates/
│   └── (html files)
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js

❌ WRONG:
timepas/
├── templates/
│   ├── css/  ← Wrong location
│   └── js/
```

---

## Debugging Tips

### Database Issue?
```bash
rm data.db
python app.py  # Recreates fresh DB
```

### Static Files Not Loading?
- Check file paths in HTML
- Verify `static/css/style.css` exists
- Verify `static/js/main.js` exists
- Restart server

### AJAX Not Working?
- Check browser console (F12)
- Verify JSON in request/response
- Check IP routing

### Style Not Changing?
- Hard refresh browser (Ctrl+F5)
- Clear browser cache
- Check CSS selector specificity

---

## Browser Console Tips

```javascript
// Check session
console.log(sessionStorage);

// Test AJAX
fetch('/api/add-to-cart', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({food_id: 1, quantity: 1})
});

// Dark mode
document.body.classList.toggle('dark-mode');
```

---

## Key Components

### Session Management
```python
session['user_id'] = user_id  # Login
session.clear()  # Logout
```

### Flash Messages
```python
return render_template('page.html', error='Message')
```

### JSON Response
```python
return jsonify({'success': True, 'data': data})
```

---

## Performance Tips

- 20-item limit keeps page fast
- AJAX prevents full page reloads
- CSS animations use GPU acceleration
- JavaScript is vanilla (no jQuery bloat)
- Images use placeholder service

---

## Security Notes

⚠️ **For Production:**
- Change `app.secret_key`
- Use HTTPS
- Use environment variables
- Use production server (Gunicorn)
- Add CSRF tokens
- Validate/sanitize all inputs
- Use parameterized queries

---

## Deployment Steps

```bash
# 1. Install production server
pip install gunicorn

# 2. Change secret key in app.py
app.secret_key = 'long-random-string'

# 3. Set debug to False
app.run(debug=False)

# 4. Run with Gunicorn
gunicorn -w 4 app:app

# 5. Configure reverse proxy (Nginx)
# 6. Set up HTTPS (Let's Encrypt)
```

---

## Sample Test Accounts (After Registration)

You create your own! The system is blank initially.

1. Register: username=`testuser1`, email=`test1@example.com`, pwd=`password123`
2. Register: username=`testuser2`, email=`test2@example.com`, pwd=`password123`

Each user has separate cart, wishlist, and orders.

---

## Helpful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python app.py

# Run with Gunicorn (production)
gunicorn app:app

# Database reset
rm data.db && python app.py

# Check Python version
python --version

# List installed packages
pip list

# Create requirements.txt
pip freeze > requirements.txt
```

---

## File Modification Guide

### To extend features:
1. **Add routes** → Modify `app.py`
2. **Change DB** → Modify `database.py`
3. **Update UI** → Modify `templates/*.html`
4. **Change styles** → Modify `static/css/style.css`
5. **Add JS** → Modify `static/js/main.js`

### Example: Add New Page
1. Create `templates/newpage.html`
2. Extend from `base.html`
3. Add route in `app.py`:
   ```python
   @app.route('/newpage')
   def newpage():
       if not check_login():
           return redirect(url_for('login'))
       return render_template('newpage.html', user=get_user(session['user_id']))
   ```
4. Add link to `base.html` navbar

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Not authenticated |
| 404 | Page not found |
| 500 | Server error |

---

## Remember

- **Always** validate user input
- **Always** check if user is logged in
- **Always** use parameterized queries
- **Always** hash passwords
- **Always** test in multiple browsers
- **Always** backup database
- **Always** use try-catch for DB operations

---

**Happy Coding! 🚀**
