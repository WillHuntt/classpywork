from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('orders.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
   CREATE TABLE IF NOT EXISTS orders (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       coffee_name TEXT NOT NULL,
       quantity INTEGER NOT NULL,
       total_price REAL NOT NULL
   )
''')
conn.commit()
menu = [
   {'id': 1, 'name': 'Espresso', 'price': 2.50},
   {'id': 2, 'name': 'Latte', 'price': 3.50},
   {'id': 3, 'name': 'Cappuccino', 'price': 3.00},
   {'id': 4, 'name': 'Americano', 'price': 2.00},
   {'id': 5, 'name': 'Mocha', 'price': 4.00}
]
@app.route('/')
def home():
   return render_template('home1.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
   for item in menu:
       quantity = int(request.form.get(f'quantity_{item["id"]}', 0))
       if quantity > 0:
           total_price = item['price'] * quantity
           cursor.execute(
               'INSERT INTO orders (coffee_name, quantity, total_price) VALUES (?, ?, ?)',
               (item['name'], quantity, total_price)
           )
   conn.commit()
   return redirect('/cart')

@app.route('/cart')
def cart():
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()

    fixed_orders = []
    total = 0

    for order in orders:
        price = float(order[3])
        total += price

        fixed_orders.append((
            order[0],
            order[1],
            order[2],
            price
        ))

    return render_template('coffeeorder.html', orders=fixed_orders, total=total)

@app.route('/confirm', methods=['POST'])
def confirm():
   return '''
<h1>Order Confirmed!</h1>
<p>Thank you for ordering from Coffee Cafe.</p>
<a href="/">Back Home</a>
   '''

@app.route('/clear')
def clear_cart():
   cursor.execute('DELETE FROM orders')
   conn.commit()
   return redirect('/cart')
if __name__ == '__main__':
   app.run(debug=True)