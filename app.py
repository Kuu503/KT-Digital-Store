from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Database တည်ဆောက်ပုံ
def init_db():
    conn = sqlite3.connect('orders.db')
    conn.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, icon_url TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, name TEXT, price TEXT, image_url TEXT)')
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
    return render
