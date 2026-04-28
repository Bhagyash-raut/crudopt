from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
import logging
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'super_secret'

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_db():
    return pymysql.connect(**DB_CONFIG)

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Create (INSERT)
@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO contacts (name, email, number, message)
        VALUES (%s, %s, %s, %s)
    """, (data['name'], data['email'], data['phone'], data['message']))

    db.commit()
    db.close()

    return redirect('/')

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin/dashboard')
        return render_template('admin_login.html', error="Invalid credentials")

    return render_template('admin_login.html')

# Read (SELECT)
@app.route('/admin/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    db.close()

    return render_template('admin_dashboard.html', contacts=contacts)

# Update
@app.route('/admin/update/<int:id>', methods=['GET', 'POST'])
def update_contact(id):
    if not session.get('admin'):
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.form
        cursor.execute("""
            UPDATE contacts
            SET name=%s, email=%s, number=%s, message=%s
            WHERE id=%s
        """, (data['name'], data['email'], data['phone'], data['message'], id))

        db.commit()
        db.close()
        return redirect('/admin/dashboard')

    cursor.execute("SELECT * FROM contacts WHERE id=%s", (id,))
    contact = cursor.fetchone()
    db.close()

    return render_template('update_contact.html', contact=contact)

# Delete
@app.route('/admin/delete/<int:id>')
def delete_contact(id):
    if not session.get('admin'):
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=%s", (id,))
    db.commit()
    db.close()

    return redirect('/admin/dashboard')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)