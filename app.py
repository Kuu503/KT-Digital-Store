from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('orders.db')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id TEXT, zone_id TEXT, item_name TEXT, item_price TEXT, status TEXT, time TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, image_url TEXT)')
    conn.close()

init_db()

BOT_TOKEN = "8301402771:AAH4_R5p86C8yOn4CyjeiICE7i2GooOvtnc"
CHAT_ID = "5014593564"

@app.route('/')
def home():
    conn = sqlite3.connect('orders.db')
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/buy', methods=['POST'])
def buy():
    p_id = request.form.get('player_id')
    z_id = request.form.get('zone_id', 'N/A')
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    now = datetime.now().strftime("%I:%M %p (%d/%m)")
    msg = f"🎯 **Order အသစ်တက်ပြီ!**\n\n👤 ID: `{p_id}` ({z_id})\n💎 Item: **{item_name}**\n💰 Price: {item_price} Ks\n⏰ Time: {now}"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return "အော်ဒါတင်ခြင်း အောင်မြင်ပါသည်။ ကိုတင့် ဆီကို အကြောင်းကြားစာ ပို့လိုက်ပါပြီ။"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('orders.db')
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    img = request.form.get('img')
    conn = sqlite3.connect('orders.db')
    conn.execute('INSERT INTO products (name, price, image_url) VALUES (?,?,?)', (name, price, img))
    conn.commit()
    conn.close()
    return redirect('/admin')

# --- ဒီအပိုင်းက ပစ္စည်းပြန်ဖျက်ဖို့ အသစ်ထည့်လိုက်တာပါ ---
@app.route('/admin/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('orders.db')
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", default=8080))
