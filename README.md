# 🍽️ FoodHub — Online Food Ordering System

<div align="center">

![FoodHub Banner](https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=400&fit=crop)

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)](https://sqlite.org)
[![HTML5](https://img.shields.io/badge/HTML5-CSS3-orange?style=for-the-badge&logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)

> A full-stack food ordering web application inspired by Swiggy/Zomato — built with Flask, SQLite, HTML, CSS, and JavaScript.

</div>

---

## 📽️ Project Demo Video


> ▶️ [Click here to watch the project demo video](https://drive.google.com/file/d/1_sFGJ9g-jMlvMKeruix1k9A9ppDS228A/view?usp=drive_link) (https://drive.google.com/file/d/1_sFGJ9g-jMlvMKeruix1k9A9ppDS228A/view?usp=drive_link)

> 📁 [Project Folder (Google Drive)](https://drive.google.com/drive/folders/1NZZFmq9t6SfgjqYyfOAehw5dapTqu1Bs?usp=drive_link)

<!-- If you want to embed a YouTube video thumbnail that links to the video, use this format: -->
<!-- [![FoodHub Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) -->

---

## 📌 Project Description

**FoodHub** is a complete web-based food ordering system that allows users to:

- 🔐 Register and log in securely
- 🍕 Browse 20+ food items across multiple categories
- 🛒 Add items to cart and manage quantities
- ❤️ Save favourite items to a wishlist
- 📦 Place orders with delivery details and payment mode
- 🧾 View order receipts and full order history
- 🌙 Toggle between light and dark mode

The project follows a clean MVC-like structure using Flask for backend routing, SQLite for persistent data storage, and vanilla JavaScript for dynamic frontend interactions.

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3, Flask                   |
| Database   | SQLite3                           |
| Frontend   | HTML5, CSS3, JavaScript (vanilla) |
| Auth       | Werkzeug password hashing         |
| Templating | Jinja2 (Flask templates)          |

---

## 📁 Project Structure

```
foodhub/
├── app.py                  # Main Flask application & routes
├── database.py             # DB init, schema & all query functions
├── requirements.txt        # Python dependencies
├── data.db                 # SQLite database (auto-generated)
├── templates/
│   ├── base.html           # Base layout with navbar
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── index.html          # Home / food listing
│   ├── cart.html           # Shopping cart
│   ├── wishlist.html       # Wishlist page
│   ├── checkout.html       # Checkout form
│   ├── receipt.html        # Order receipt
│   └── orders.html         # Order history
└── static/
    ├── css/
    │   └── style.css       # All styles (responsive + dark mode)
    └── js/
        └── main.js         # JS utilities
```

---

## ⚙️ Steps to Run the Project

### ✅ Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)
- Git (to clone the repository)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/harshdakolte3-ux/myproject1.git
cd myproject1
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

---

### Step 2 — (Optional) Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.0
```

---

### Step 4 — Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

---

### Step 5 — Open in Browser

Go to 👉 **[http://localhost:5000](http://127.0.0.1:5000)**

- Click **"Register here"** to create a new account
- Login with your credentials
- Start browsing and ordering food! 🎉

---

### 🔄 Reset the Database (if needed)

If you face any database errors or want a fresh start:

```bash
# Windows
del data.db

# Mac / Linux
rm data.db
```

Then restart the app — it will auto-recreate the database with all 20 food items.

---

### 🔧 Change Port (if 5000 is busy)

Edit the last line of `app.py`:
```python
app.run(debug=True, port=5001)  # Use any available port
```

---

## 👥 Team Member Contributions



### 👩‍💻 Harshda Kolte — Project Lead & Full Stack Developer
- Led overall project architecture and development
- Implemented backend and frontend using Flask, HTML, CSS, and JavaScript
- Designed database structure
- Built order placement logic and APIs
- Implemented dark mode
- Created HTML templates and documentation
- Built wishlist system

### 👩‍💻 Purva Naik — Database Developer & UI Designer
- Managed database design and queries
- Seeded 20 food items
- Worked on UI/UX and responsive design
- Implemented CSS styling and validation
- Tested usability
- Built wishlist system

### 👩‍💻 Hetvi — Backend & Feature Developer
- Implemented session management
- Developed routing logic
- Worked on APIs and search feature
- Fixed bugs and did cross-browser testing
-commit half templates


---

## ✨ Features

### 🔐 Authentication
- Secure registration with password confirmation
- Login with hashed password verification (Werkzeug)
- Session-based login state
- Auto-redirect to login if not authenticated

### 🏠 Home / Dashboard
- Displays 20 food items in a responsive grid
- Each card shows image, name, category, description, and price
- Search bar filters by food name or category

### 🛒 Cart
- Add items with quantity management
- Increase / decrease / remove items
- Real-time total price calculation
- Persisted in database across sessions

### ❤️ Wishlist
- Toggle wishlist from food cards (heart button)
- Separate wishlist page
- Quick "Add to Cart" from wishlist

### 📦 Order & Checkout
- Delivery form: name, city, mobile, payment mode
- Supports Cash / Card / UPI
- Mobile number validation (10 digits)

### 🧾 Receipt & Order History
- Confirmation page with order ID and date
- Item-wise breakdown with quantities and totals
- Full order history page

### 🌙 Dark Mode
- Toggle from navbar
- Preference saved in `localStorage`

---

## 🗃️ Database Schema

```
users        → id, username, email, password, created_at
food_items   → id, name, description, price, image_url, category, created_at
cart         → id, user_id, food_id, quantity
wishlist     → id, user_id, food_id
orders       → id, user_id, items (JSON), total_price, customer_name,
               city, mobile_number, payment_mode, order_date
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/search?q=term` | Search food items |
| POST | `/login` | User login |
| POST | `/register` | User registration |
| GET | `/logout` | Logout |
| GET | `/cart` | Cart page |
| GET | `/wishlist` | Wishlist page |
| GET | `/checkout` | Checkout page |
| POST | `/place-order` | Submit order |
| GET | `/receipt/<id>` | Order receipt |
| GET | `/orders` | Order history |
| POST | `/api/add-to-cart` | Add item to cart |
| POST | `/api/remove-from-cart` | Remove from cart |
| POST | `/api/update-cart-quantity` | Update quantity |
| POST | `/api/toggle-wishlist` | Add/remove wishlist |
| GET | `/api/wishlist-status/<id>` | Check wishlist status |

---

## 🚀 Future Enhancements

- 📧 Email order confirmations
- ⭐ Restaurant ratings and reviews
- 🗺️ Live delivery tracking
- 🏷️ Promo codes and discounts
- 🔑 Admin panel for food management
- 💳 Payment gateway integration

---

## 🔒 Security Notes (for Production)

- Change `app.secret_key` to a secure random string
- Use environment variables for all secrets
- Enable HTTPS / SSL
- Add CSRF protection
- Use a WSGI server like **Gunicorn**
- Implement rate limiting on API routes

---

## 📄 License

This project is developed for **educational purposes** as part of an academic submission.

---

## 🔗 GitHub Repository

> **[https://github.com/harshdakolte3-ux/myproject1](https://github.com/harshdakolte3-ux/myproject1)**

---

<div align="center">

Made with ❤️ by the FoodHub Team &nbsp;|&nbsp; Version 1.0 &nbsp;|&nbsp; Status: ✅ Fully Functional

</div>