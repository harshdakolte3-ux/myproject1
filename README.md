# FoodHub - Online Food Ordering System

A complete web-based food ordering system built with Flask, HTML, CSS, JavaScript, and SQLite.

## Features Implemented

### 1. User Authentication
- ✅ Registration page with password validation
- ✅ Login page with secure password hashing
- ✅ Redirect to dashboard after successful login
- ✅ Logout functionality

### 2. Home/Dashboard Page
- ✅ Display exactly 20 food items
- ✅ Each item shows image, name, and price
- ✅ Dynamic search bar to filter items
- ✅ Navigation bar with Home, Cart, Wishlist, Orders

### 3. Cart System
- ✅ Add items to cart
- ✅ Increase/decrease item quantities
- ✅ Remove items from cart
- ✅ Dynamic total price calculation
- ✅ Cart summary

### 4. Wishlist
- ✅ Add/remove items to/from wishlist
- ✅ Display wishlist items separately
- ✅ Quick add to cart from wishlist

### 5. Order Process
- ✅ Checkout page with order summary
- ✅ Form to collect delivery details:
  - Customer name
  - City
  - Mobile number
  - Payment mode (Cash/Card/UPI)
- ✅ Order validation

### 6. Order Receipt
- ✅ Order confirmation with receipt details
- ✅ Order ID and order date
- ✅ Item-wise breakdown with quantities and prices
- ✅ Total amount display

### 7. Order History
- ✅ Orders page showing all previous orders
- ✅ View receipt for each order
- ✅ Order summary with delivery details

### 8. Database
- ✅ SQLite3 database with tables for:
  - Users (authentication)
  - Food items (menu)
  - Cart (temporary cart storage)
  - Wishlist (saved items)
  - Orders (order history)

### 9. UI/UX
- ✅ Modern, clean design inspired by Swiggy/Zomato
- ✅ Responsive design for mobile and desktop
- ✅ Dark mode toggle
- ✅ Smooth transitions and hover effects
- ✅ Gradient backgrounds and card-based layout

### 10. Backend
- ✅ Flask routing for all pages
- ✅ Proper template inheritance with base.html
- ✅ Session management for user authentication
- ✅ AJAX requests for add/remove/update actions
- ✅ JSON API endpoints

## Project Structure

```
foodhub/
├── app.py                  # Main Flask application
├── database.py             # Database initialization and functions
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── index.html         # Home/Dashboard
│   ├── cart.html          # Shopping cart
│   ├── wishlist.html      # Wishlist page
│   ├── checkout.html      # Checkout form
│   ├── receipt.html       # Order receipt
│   └── orders.html        # Order history
└── static/
    ├── css/
    │   └── style.css      # All styles (responsive, dark mode)
    └── js/
        └── main.js        # JavaScript utilities
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps

1. **Navigate to project directory:**
   ```bash
   cd /path/to/timepas
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Open `http://localhost:5000` in your web browser

5. **Create account:**
   - Click "Register here" on the login page
   - Fill in username, email, and password
   - Login with your credentials

## Default Credentials (After DB Initialization)
You'll be redirected to create new credentials on first run.

## Features in Detail

### Authentication System
- Passwords are hashed using Werkzeug security
- Session-based authentication
- Automatic redirect to login if not authenticated

### Food Items
The system comes pre-loaded with 20 diverse food items including:
- Pizzas (Margherita, Pepperoni)
- Burgers (Vegetarian, Chicken)
- Indian cuisine (Biryani, Curries, Tandoori)
- Beverages
- Desserts
- Snacks

### Cart Management
- Items stored in SQLite database
- Real-time quantity updates
- Automatic total calculation
- Persistent across sessions (until order placed)

### Order System
- Complete order placed with delivery details
- Payment mode selection (Cash/Card/UPI)
- Mobile number validation (10 digits)
- Order history with filtering

### Search Functionality
- Real-time search by food name
- Category-based filtering
- Limits results to 20 items

### Dark Mode
- Toggle dark mode with button in navbar
- Preference saved in browser localStorage
- Smooth transitions between modes

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- password (hashed)
- created_at

### Food Items Table
- id (PRIMARY KEY)
- name
- description
- price
- image_url
- category
- created_at

### Cart Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- food_id (FOREIGN KEY)
- quantity

### Wishlist Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- food_id (FOREIGN KEY)

### Orders Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- items (JSON)
- total_price
- customer_name
- city
- mobile_number
- payment_mode
- order_date

## Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (below 768px)

## Validation

### Login/Register
- Username and email validation
- Password matching confirmation
- Duplicate account prevention

### Checkout
- Name required
- Valid phone number (10 digits)
- City required
- Payment mode required

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Pages
- `GET /` - Home/Dashboard
- `GET /cart` - Cart page
- `GET /wishlist` - Wishlist page
- `GET /checkout` - Checkout page
- `GET /orders` - Order history
- `GET /search` - Search results

### AJAX API
- `POST /api/add-to-cart` - Add item to cart
- `POST /api/remove-from-cart` - Remove from cart
- `POST /api/update-cart-quantity` - Update quantity
- `POST /api/add-to-wishlist` - Add to wishlist
- `POST /api/remove-from-wishlist` - Remove from wishlist
- `GET /api/is-in-wishlist/<id>` - Check if in wishlist
- `POST /place-order` - Place order

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm data.db
python app.py
```
This will reinitialize the database with fresh data.

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port number
```

### Static Files Not Loading
Ensure the directory structure is correct:
- `static/css/style.css` exists
- `static/js/main.js` exists
- `templates/` has all HTML files

## Future Enhancements

Potential features for expansion:
- Email notifications for orders
- Restaurant ratings and reviews
- Delivery tracking
- Promo codes and discounts
- Multiple restaurants
- Admin panel for food management
- Payment gateway integration
- Order delivery estimation

## Security Notes

For production:
- Change the `app.secret_key` to a secure random string
- Use environment variables for sensitive data
- Enable HTTPS
- Add CSRF protection
- Use a production WSGI server (Gunicorn)
- Implement rate limiting

## License

This project is for educational purposes.

## Support

For issues or questions about the application, review the code comments or check individual files for more details.

---

**Created:** April 8, 2024
**Version:** 1.0
**Status:** Fully Functional ✅
