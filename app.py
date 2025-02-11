from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'rahasia123'  # Ubah ke secret key yang aman

# Konfigurasi database
db_config = {
    'host': 'w-mif.h.filess.io',
    'user': 'merchananime_fiercetoat',
    'password': '7ff5e0f530311b0dd54f2de586af0fbe54772652',  # Ganti dengan password MySQL Anda
    'database': 'merchananime_fiercetoat',  # Nama database
    'port' : '3305'
}

# Admin credentials
ADMIN_USERNAME = 'gugugaga'
ADMIN_PASSWORD = 'mendhokiawan123'

# Fungsi untuk koneksi database
def get_db_connection():
    return mysql.connector.connect(**db_config)



# Route untuk halaman utama
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('merchandise'))
    return redirect(url_for('login'))

# Route untuk login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('merchandise'))
        else:
            flash('Username atau password salah!')
    return render_template('login.html')

# Route untuk registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            conn.commit()
            flash('Registrasi berhasil! Silakan login.')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username atau email sudah digunakan.')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

# Route untuk halaman merchandise
@app.route('/merchandise')
def merchandise():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM merchandise")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('merchandise.html', products=products)

# Route untuk login admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!', 'error')

    return render_template('admin_login.html')

# Route untuk dashboard admin (CRUD merchandise)
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM merchandise")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', products=products)

# Route untuk mengedit merchandise
@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']
        whatsapp_link = request.form['whatsapp_link']
        image_url = request.form['image_url']

        cursor.execute("""
            UPDATE merchandise SET name = %s, stock = %s, price = %s, whatsapp_link = %s, image_url = %s
            WHERE id = %s
        """, (name, stock, price, whatsapp_link, image_url, id))
        conn.commit()
        flash('Produk berhasil diperbarui!', 'success')
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM merchandise WHERE id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin_edit.html', product=product)

# Route untuk logout admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('admin_login'))

# Route untuk logout user
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
  #  init_db()
    app.run(debug=True)
