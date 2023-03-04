from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from models.helpers import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Placeholder Secret Key.'

@app.route('/')
def index():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        expenses = get_all_expenses(user_id)
        return render_template('index.html', expenses=expenses, user=user)
    else:
        return redirect('/login')

@app.route('/add_expense')
def add_expense_page():
    return render_template('add_expense.html')

@app.route('/add_expense_action', methods=['POST'])
def add_expense_action():
    user_id = 1 #Placeholder
    date = request.form.get('date')
    description = request.form.get('description')
    amount = request.form.get('amount')
    category = request.form.get('category')
    type = request.form.get('type')

    sql_write("INSERT INTO expenses (date, user_id, description, amount, category, type) VALUES (%s, %s, %s, %s, %s, %s)", [date, user_id, description, amount, category, type])

    return redirect('/')

@app.route('/edit_expense')
def edit_expense_page():
    expense_id = request.args.get('expense_id')
    expense = get_expense(expense_id)
    return render_template('edit_expense.html', expense=expense)

@app.route('/edit_expense_action', methods=['POST'])
def edit_expense_action():
    expense_id = request.form.get('id')
    date = request.form.get('date')
    description = request.form.get('description')
    amount = request.form.get('amount')
    category = request.form.get('category')
    type = request.form.get('type')

    sql_write("UPDATE expenses SET date = %s, description = %s, amount = %s, category = %s, type = %s WHERE id = %s;", [date, description, amount, category, type, expense_id])

    return redirect('/')

@app.route('/delete_expense')
def delete_confirmation():
    expense_id = request.args.get('expense_id')
    expense = get_expense(expense_id)
    return render_template('delete_expense.html', expense=expense)

@app.route('/delete_expense_action')
def delete_expense_action():
    expense_id = request.args.get('expense_id')
    sql_write("DELETE FROM expenses WHERE id = %s", [expense_id])
    return redirect('/')

@app.route('/sign_up')
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    passwords_match = password == password_confirmation

    if passwords_match:
        password_hash = generate_password_hash(password)
        sql_write("INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s)", [email, password_hash, name])

        return redirect('/login')
    else:
        passwords_match = False
        return render_template('sign_up.html', passwords_match=passwords_match)

@app.route('/login')
def login_page():
    user_id = session.get('user_id', '')    
    if user_id:
        return redirect('/')    
    else:
        return render_template('login.html')

@app.route('/login_action', methods=["POST"])
def check_login():
    user_id = session.get('user_id', '')    
    if user_id:
        return redirect('/')    
    else:    
        email = request.form.get('email')
        password = request.form.get('password')
        user_id = get_user_id(email)
        user = get_user(user_id)
        password_match = user.validate_password(password)

        if password_match:
            user = sql_select("SELECT * FROM users WHERE email = %s", [email])
            user_id = user[0]['id']

            session['user_id'] = user_id

            return redirect('/')
        else:
            wrong_password = True
            return render_template('login.html', wrong_password=wrong_password)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)