from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (
    init_db, register_user, login_user, get_user, get_all_food_items,
    search_food_items, add_to_cart, remove_from_cart, update_cart_quantity,
    get_cart_items, clear_cart, add_to_wishlist, remove_from_wishlist,
    get_wishlist, is_in_wishlist, place_order, get_orders, get_order, get_food_item
)
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Initialize database on first run
import os
if not os.path.exists('data.db'):
    init_db()

# Middleware to check login
def check_login():
    return 'user_id' in session

# Home/Dashboard page
@app.route('/')
def index():
    if not check_login():
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
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
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    data = request.get_json()
    food_id = data.get('food_id')
    quantity = data.get('quantity', 1)

    success = add_to_cart(session['user_id'], food_id, quantity)
    if success:
        return jsonify({'success': True, 'message': 'Added to cart'})
    else:
        return jsonify({'success': False, 'message': 'Failed to add to cart'})

# Remove from cart (AJAX)
@app.route('/api/remove-from-cart', methods=['POST'])
def api_remove_from_cart():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')

    success = remove_from_cart(session['user_id'], food_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Update cart quantity (AJAX)
@app.route('/api/update-cart-quantity', methods=['POST'])
def api_update_cart_quantity():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')
    quantity = data.get('quantity')

    success = update_cart_quantity(session['user_id'], food_id, quantity)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Cart page
@app.route('/cart')
def cart():
    if not check_login():
        return redirect(url_for('login'))

    items = get_cart_items(session['user_id'])
    user = get_user(session['user_id'])
    total = sum(item['price'] * item['quantity'] for item in items)
    return render_template('cart.html', items=items, user=user, total=total)

# Add to wishlist (AJAX)
@app.route('/api/add-to-wishlist', methods=['POST'])
def api_add_to_wishlist():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')

    success = add_to_wishlist(session['user_id'], food_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Remove from wishlist (AJAX)
@app.route('/api/remove-from-wishlist', methods=['POST'])
def api_remove_from_wishlist():
    if not check_login():
        return jsonify({'success': False}), 401

    data = request.get_json()
    food_id = data.get('food_id')

    success = remove_from_wishlist(session['user_id'], food_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Check if in wishlist (AJAX)
@app.route('/api/is-in-wishlist/<int:food_id>')
def api_is_in_wishlist(food_id):
    if not check_login():
        return jsonify({'inWishlist': False}), 401

    in_wishlist = is_in_wishlist(session['user_id'], food_id)
    return jsonify({'inWishlist': in_wishlist})

# Wishlist page
@app.route('/wishlist')
def wishlist():
    if not check_login():
        return redirect(url_for('login'))

    items = get_wishlist(session['user_id'])
    user = get_user(session['user_id'])
    return render_template('wishlist.html', items=items, user=user)

# Checkout page
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

    # Prepare order items
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
        session['last_order_id'] = order_id
        return redirect(url_for('receipt', order_id=order_id))
    else:
        return redirect(url_for('checkout'))

# Receipt page
@app.route('/receipt/<int:order_id>')
def receipt(order_id):
    if not check_login():
        return redirect(url_for('login'))

    order = get_order(order_id)
    if not order or order['user_id'] != session['user_id']:
        return redirect(url_for('index'))

    user = get_user(session['user_id'])
    try:
        order_items = json.loads(order['items']) if order['items'] else []
    except (json.JSONDecodeError, TypeError):
        order_items = []
    return render_template('receipt.html', order=order, items=order_items, user=user)

# Orders page
@app.route('/orders')
def orders():
    if not check_login():
        return redirect(url_for('login'))

    user_orders = get_orders(session['user_id'])
    user = get_user(session['user_id'])

    # Parse items for each order
    parsed_orders = []
    for order in user_orders:
        order_dict = dict(order)
        try:
            order_dict['items_list'] = json.loads(order_dict['items']) if order_dict['items'] else []
        except (json.JSONDecodeError, TypeError):
            order_dict['items_list'] = []
        parsed_orders.append(order_dict)

    return render_template('orders.html', orders=parsed_orders, user=user)

if __name__ == '__main__':
    app.run(debug=True)
