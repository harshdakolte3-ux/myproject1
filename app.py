from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (
    init_db, register_user, login_user, get_user, get_all_food_items,
    search_food_items, add_to_cart, remove_from_cart, update_cart_quantity,
    get_cart_items, clear_cart, add_to_wishlist, remove_from_wishlist,
    get_wishlist, is_in_wishlist, place_order, get_orders, get_order
)
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# ✅ FIX 1: Always reinitialize DB to pick up latest image URLs
# Change this to `if not os.path.exists('data.db'):` once images are confirmed working
init_db()

# ✅ FIX 2: Allow external images (Unsplash) via Content Security Policy
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src * data: blob:; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    return response

# Middleware to check login
def check_login():
    return 'user_id' in session

# Home/Dashboard page
@app.route('/')
def index():
    if not check_login():
        return redirect(url_for('login'))

    items = get_all_food_items(limit=20)
    user = get_user(session['user_id'])
    return render_template('index.html', items=items, user=user)

# Search functionality
@app.route('/search')
def search():
    if not check_login():
        return redirect(url_for('login'))

    search_term = request.args.get('q', '')
    items = search_food_items(search_term) if search_term else get_all_food_items(limit=20)
    user = get_user(session['user_id'])
    return render_template('index.html', items=items, user=user, search_term=search_term)

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        success, message = register_user(username, email, password)
        if success:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=message)

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, user_id = login_user(username, password)
        if success:
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Add to cart (AJAX)
@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')
    quantity = data.get('quantity', 1)

    success = add_to_cart(session['user_id'], food_id, quantity)
    return jsonify({'success': success})

# Remove from cart
@app.route('/api/remove-from-cart', methods=['POST'])
def api_remove_from_cart():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')

    success = remove_from_cart(session['user_id'], food_id)
    return jsonify({'success': success})

# Update cart quantity
@app.route('/api/update-cart-quantity', methods=['POST'])
def api_update_cart_quantity():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')
    quantity = data.get('quantity')

    success = update_cart_quantity(session['user_id'], food_id, quantity)
    return jsonify({'success': success})

# ✅ FIX 3: Wishlist toggle API (was missing)
@app.route('/api/toggle-wishlist', methods=['POST'])
def api_toggle_wishlist():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')
    user_id = session['user_id']

    if is_in_wishlist(user_id, food_id):
        success = remove_from_wishlist(user_id, food_id)
        return jsonify({'success': success, 'in_wishlist': False})
    else:
        success = add_to_wishlist(user_id, food_id)
        return jsonify({'success': success, 'in_wishlist': True})

# Cart page
@app.route('/cart')
def cart():
    if not check_login():
        return redirect(url_for('login'))

    items = get_cart_items(session['user_id'])
    user = get_user(session['user_id'])
    total = sum(item['price'] * item['quantity'] for item in items)

    return render_template('cart.html', items=items, user=user, total=total)

# Wishlist page
@app.route('/wishlist')
def wishlist():
    if not check_login():
        return redirect(url_for('login'))

    items = get_wishlist(session['user_id'])
    user = get_user(session['user_id'])

    return render_template('wishlist.html', items=items, user=user)

# Checkout
@app.route('/checkout')
def checkout():
    if not check_login():
        return redirect(url_for('login'))

    items = get_cart_items(session['user_id'])
    if not items:
        return redirect(url_for('cart'))

    user = get_user(session['user_id'])
    total = sum(item['price'] * item['quantity'] for item in items)

    return render_template('checkout.html', items=items, user=user, total=total)

# Place order
@app.route('/place-order', methods=['POST'])
def place_order_route():
    if not check_login():
        return redirect(url_for('login'))

    customer_name = request.form.get('customer_name')
    city = request.form.get('city')
    mobile_number = request.form.get('mobile_number')
    payment_mode = request.form.get('payment_mode')

    items = get_cart_items(session['user_id'])
    if not items:
        return redirect(url_for('cart'))

    total_price = sum(item['price'] * item['quantity'] for item in items)

    order_items = []
    for item in items:
        order_items.append({
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item['price'] * item['quantity']
        })

    success, order_id = place_order(
        session['user_id'], order_items, total_price,
        customer_name, city, mobile_number, payment_mode
    )

    if success:
        clear_cart(session['user_id'])
        return redirect(url_for('receipt', order_id=order_id))

    return redirect(url_for('checkout'))

# Receipt
@app.route('/receipt/<int:order_id>')
def receipt(order_id):
    if not check_login():
        return redirect(url_for('login'))

    order = get_order(order_id)
    if not order:
        return redirect(url_for('orders'))

    user = get_user(session['user_id'])
    items = json.loads(order['items']) if order['items'] else []

    return render_template('receipt.html', order=order, items=items, user=user)

# Orders
@app.route('/orders')
def orders():
    if not check_login():
        return redirect(url_for('login'))

    user_orders = get_orders(session['user_id'])
    user = get_user(session['user_id'])

    return render_template('orders.html', orders=user_orders, user=user)

if __name__ == '__main__':
    app.run(debug=True)