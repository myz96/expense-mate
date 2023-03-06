from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.graph_objects as go
import pandas as pd
from models.helpers import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Placeholder Secret Key.'

@app.route('/')
def index():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        transactions = get_all_transactions(user_id)
        weekly_savings_goal = user.savings_goal
        latest_weekly_expenses = get_weekly_expenses(user_id)[1][0]
        latest_weekly_income = get_weekly_income(user_id)[1][0]
        weekly_savings_above_goal = (latest_weekly_income - latest_weekly_expenses) - weekly_savings_goal

        # Creating bar chart
        all_transactions = sql_select("SELECT date_trunc('week', date) as week, transaction_type as type, SUM(amount) AS total FROM transactions WHERE user_id = %s GROUP BY 1,2 ORDER BY 1,2 DESC")

        df = pd.DataFrame(all_transactions, columns=['week', 'type', 'total'])
        df.pivot(index='week', columns='type', values='total')

        fig = go.Figure(data=[go.Bar(x=get_weekly_expenses(user_id)[0], y=get_weekly_expenses(user_id)[1])])
        chart = fig.to_html(full_html=False)

        return render_template('index.html', transactions=transactions, user=user, weekly_savings_goal=weekly_savings_goal, latest_weekly_expenses=latest_weekly_expenses, latest_weekly_income=latest_weekly_income, weekly_savings_above_goal=weekly_savings_above_goal, chart=chart)
    else:
        return redirect('/login')

@app.route('/add_transaction')
def add_transaction_page():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        return render_template('add_transaction.html', user=user)
    else:
        return redirect('/login')

@app.route('/add_transaction_action', methods=['POST'])
def add_transaction_action():
    user_id = session.get('user_id', '')
    if user_id:
        add_transaction(
            user_id = user_id, 
            transaction_type = request.form.get('transaction_type'),
            date = request.form.get('date'), 
            description = request.form.get('description'), 
            amount = request.form.get('amount'), 
            category = request.form.get('category'), 
            type = request.form.get('type')
            )
        return redirect('/')
    else:
        return redirect('/')

@app.route('/edit_transaction')
def edit_transaction_page():
    transaction_id = request.args.get('transaction_id')
    transaction = get_transaction(transaction_id)
    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/edit_transaction_action', methods=['POST'])
def edit_transaction_action():
    user_id = session.get('user_id', '')
    if user_id:
        edit_transaction(
            transaction_id = request.form.get('id'),
            transaction_type = request.form.get('transaction_type'),
            date = request.form.get('date'),
            description = request.form.get('description'),
            amount = request.form.get('amount'),
            category = request.form.get('category'),
            type = request.form.get('type')                 
            )
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delete_transaction')
def delete_confirmation():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        transaction_id = request.args.get('transaction_id')
        transaction = get_transaction(transaction_id)
        return render_template('delete_transaction.html', transaction=transaction, user=user)

@app.route('/delete_transaction_action')
def delete_transaction_action():
    transaction_id = request.args.get('id')
    delete_transaction(transaction_id)
    return redirect('/')

@app.route('/sign_up')
def sign_up_page():
    user_id = session.get('user_id', '')
    if user_id:
        redirect('/')
    else:
        return render_template('sign_up.html', passwords_match = True)

@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    passwords_match = password == password_confirmation
    savings_goal = request.form.get('savings_goal')

    if passwords_match:
        password_hash = generate_password_hash(password)
        sql_write("INSERT INTO users (email, password_hash, name, savings_goal) VALUES (%s, %s, %s, %s)", [email, password_hash, name, savings_goal])

        return redirect('/login')
    else:
        passwords_match = False
        return render_template('sign_up.html', passwords_match=passwords_match)

@app.route('/settings')
def settings_page():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        return render_template('settings.html', user=user, passwords_match = True)
    else:
        return redirect('/login')

@app.route('/settings_action', methods=['POST'])
def settings_action():
    user_id = session.get('user_id', '')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    passwords_match = password == password_confirmation
    savings_goal = request.form.get('savings_goal')

    if passwords_match:
        password_hash = generate_password_hash(password)
        sql_write("UPDATE users SET email =%s, password_hash = %s, name = %s, savings_goal = %s WHERE id = %s", [email, password_hash, name, savings_goal, user_id])

        return redirect('/login')
    else:
        passwords_match = False
        return render_template('settings.html', passwords_match=passwords_match)


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
            session['user_id'] = user.id
            return redirect('/')
        else:
            return render_template('login.html', wrong_password=True)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)