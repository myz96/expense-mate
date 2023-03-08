from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.graph_objects as go
from datetime import date, timedelta
from models.helpers import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Placeholder Secret Key.'

@app.route('/')
def index():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')
    user = get_user(user_id)
    posts = get_feed_posts(user_id)
    users = get_all_users()
    return render_template("index.html", posts=posts, user=user, users=users)

@app.route('/dashboard')
def my_dashboard():
    user_id = session.get('user_id', '')
    if user_id:
        user = get_user(user_id)
        transactions = get_all_transactions(user_id)
        weekly_savings_goal = user.savings_goal
        latest_weekly_expenses = get_weekly_expenses(user_id)[1][0]
        latest_weekly_income = get_weekly_income(user_id)[1][0]
        weekly_savings_above_goal = (latest_weekly_income - latest_weekly_expenses) - weekly_savings_goal

        # Query for income and expenses even if there are no transactions in that week
        rows = sql_select("""
            SELECT weeks.week, 
                   COALESCE(SUM(CASE WHEN transactions.transaction_type = 'Expense' THEN transactions.amount ELSE 0 END), 0) AS expenses,
                   COALESCE(SUM(CASE WHEN transactions.transaction_type = 'Income' THEN transactions.amount ELSE 0 END), 0) AS income
            FROM (
                SELECT generate_series(
                    date_trunc('week', MIN(date)),
                    date_trunc('week', MAX(date)),
                    '1 week'
                ) AS week
                FROM transactions
                WHERE user_id = %s
            ) AS weeks
            LEFT JOIN transactions ON date_trunc('week', transactions.date) = weeks.week AND transactions.user_id = %s
            GROUP BY weeks.week
            ORDER BY weeks.week        
        """, [user_id, user_id])

        # Creating bar chart for savings by week
        weeks = [row['week'] for row in rows]
        expenses = [row['expenses'] for row in rows]
        income = [row['income'] for row in rows]
        savings = [i - e for i, e in zip(income, expenses)]

        fig = go.Figure(
            data=[go.Bar(x=weeks, y=savings)],
            layout=go.Layout(title="Total Savings by week")
        )

        bar_chart_src = fig.to_html(full_html=False)

        # SQL query to group expenses by category for the last 30 days
        last_30_days = date.today() - timedelta(days=30)
        
        rows = sql_select("""
        SELECT category, SUM(amount) AS total_amount
        FROM transactions
        WHERE transaction_type = 'Expense' AND date >= %s AND user_id = %s
        GROUP BY category
        ORDER BY total_amount DESC
        """,[last_30_days, user_id]) 

        labels = [row['category'] for row in rows]
        values = [row['total_amount'] for row in rows]

        fig = go.Figure(
            data=[go.Pie(labels=labels, values=values)],
            layout=go.Layout(title="Expenses by category for the last 30 days")
        )

        pie_chart_src = fig.to_html(full_html=False)

        return render_template('dashboard.html', transactions=transactions, user=user, weekly_savings_goal=weekly_savings_goal, latest_weekly_expenses=latest_weekly_expenses, latest_weekly_income=latest_weekly_income, weekly_savings_above_goal=weekly_savings_above_goal, bar_chart_src=bar_chart_src, pie_chart_src=pie_chart_src)
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
        create_user(email, password_hash, name, savings_goal)
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

@app.route('/create_post')
def create_post_page():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')
    user = get_user(user_id)
    weekly_savings_goal = user.savings_goal
    latest_weekly_expenses = get_weekly_expenses(user_id)[1][0]
    latest_weekly_income = get_weekly_income(user_id)[1][0]
    savings_amount = (latest_weekly_income - latest_weekly_expenses) - weekly_savings_goal

    return render_template('create_post.html', user=user, savings_amount=savings_amount)    

@app.route('/create_post_action', methods=['POST'])
def create_post_action():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')

    savings_amount = request.form.get('savings_amount', '')
    description = request.form.get('description', '')
    create_post(user_id, savings_amount, description)

    return redirect('/')

@app.route('/like_post')
def like_post():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')
    post_id = request.args.get('post_id')
    post = get_post(post_id)
    print(post) 
    post.like_unlike_post(user_id)
    return redirect('/')

@app.route('/comment_post', methods=['POST'])
def comment_post():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')
    comment = request.form.get('comment')
    post_id = request.form.get('post_id')
    post = get_post(post_id)
    post.add_comment(comment)
    return redirect('/')

@app.route('/add_friend')
def add_friend():
    user_id = session.get('user_id', '')
    if not user_id:
        return redirect('/login')
    user = get_user(user_id)
    friend_id = request.args.get('friend_id')
    user.add_remove_friend(int(friend_id))
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)