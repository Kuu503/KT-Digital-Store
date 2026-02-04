from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Database တည်ဆောက်ပုံအသစ်
def init_db():
    conn = sqlite3.connect('orders.db')
    # ဂိမ်းအမျိုးအစားများ (Categories) သိမ်းရန်
    conn.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, icon_url TEXT)')
    # ပစ္စည်းများ (Products) ကို Category နဲ့ ချိတ်ရန်
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, name TEXT, price TEXT, image_url TEXT)')
    # Order ရာဇဝင် သိမ်းရန်
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id TEXT, zone_id TEXT, item_name TEXT, item_price TEXT, time TEXT)')
    conn.close()

init_db()

# Telegram Bot Setting
BOT_TOKEN = "8301402771:AAH4_R5p86C8yOn4CyjeiICE7i2GooOvtnc"
CHAT_ID = "5014593564"

@app.route('/')
def index():
    conn = sqlite3.connect('orders.db')
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('index.html', categories=categories)

@app.route('/category/<int:cat_id>')
def category_page(cat_id):
    conn = sqlite3.connect('orders.db')
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (cat_id,)).fetchone()
    products = conn.execute('SELECT * FROM products WHERE category_id = ?', (cat_id,)).fetchall()
    conn.close()
    return render_template('category.html', category=category, products=products)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('orders.db')
    categories = conn.execute('SELECT * FROM categories').fetchall()
    products = conn.execute('SELECT p.*, c.name FROM products p JOIN categories c ON p.category_id = c.id').fetchall()
    conn.close()
    return render_template('admin.html', categories=categories, products=products)

@app.route('/admin/add_category', methods=['POST'])
def add_category():
    name = request.form.get('name')
    icon = request.form.get('icon_url')
    conn = sqlite3.connect('orders.db')
    conn.execute('INSERT INTO categories (name, icon_url) VALUES (?,?)', (name, icon))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    cat_id = request.form.get('category_id')
    name = request.form.get('name')
    price = request.form.get('price')
    img = request.form.get('img_url')
    conn = sqlite3.connect('orders.db')
    conn.execute('INSERT INTO products (category_id, name, price, image_url) VALUES (?,?,?,?)', (cat_id, name, price, img))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/buy', methods=['POST'])
def buy():
    p_id = request.form.get('player_id')
    z_id = request.form.get('zone_id', 'N/A')
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    now = datetime.now().strftime("%I:%M %p (%d/%m)")
    
    msg = f"🎮 **New Order Alert!**\n\n👤 Player ID: `{p_id}` ({z_id})\n💎 Item: {item_name}\n💰 Price: {item_price} Ks\n⏰ Time: {now}"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    conn = sqlite3.connect('orders.db')
    conn.execute('INSERT INTO orders (player_id, zone_id, item_name, item_price, time) VALUES (?,?,?,?,?)', (p_id, z_id, item_name, item_price, now))
    conn.commit()
    conn.close()
    return "အော်ဒါတင်ခြင်း အောင်မြင်ပါသည်။"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", default=8080))
