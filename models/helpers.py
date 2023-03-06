import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash

def sql_select(query, parameters):
    db_connection = psycopg2.connect("dbname=expense_mate")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    
    db_cursor.execute(query, parameters)
    
    rows = db_cursor.fetchall()

    db_cursor.close()
    db_connection.close()

    return rows

def sql_write(query, parameters):
    db_connection = psycopg2.connect("dbname=expense_mate")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    
    db_cursor.execute(query, parameters)

    db_connection.commit()

    db_cursor.close()
    db_connection.close()

class Transaction:
    def __init__(self, id, date, user_id, description, amount, category, type, transaction_type):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.category = category
        self.type = type
        self.transaction_type = transaction_type

def get_transaction(transaction_id):
    rows = sql_select("SELECT * FROM transactions WHERE id = %s;", [transaction_id])

    id = rows[0]["id"]
    date = rows[0]["date"]
    user_id = rows[0]["user_id"]
    description = rows[0]["description"]
    amount = rows[0]["amount"]
    category = rows[0]["category"]
    type = rows[0]["type"]
    transaction_type = rows[0]["transaction_type"]

    transaction = Transaction(id, date, user_id, description, amount, category, type, transaction_type)

    return transaction

def get_all_transactions(user_id):
    transactions = []

    rows = sql_select("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC", [user_id])
    for row in rows:
        id = row["id"]
        transaction = get_transaction(id)
        transactions.append(transaction)
    
    return transactions

def add_transaction(user_id, date, description, amount, category, type, transaction_type):
    sql_write("INSERT INTO transactions (date, user_id, description, amount, category, type, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", [date, user_id, description, amount, category, type, transaction_type])

def edit_transaction(transaction_id, date, description, amount, category, type, transaction_type):
    sql_write("UPDATE transactions SET date = %s, description = %s, amount = %s, category = %s, type = %s, transaction_type = %s WHERE id = %s;", [date, description, amount, category, type, transaction_type, transaction_id])

def delete_transaction(transaction_id):
    sql_write("DELETE FROM transactions WHERE id = %s", [transaction_id])

def get_weekly_expenses(user_id):
    rows = sql_select("SELECT date_trunc('week', date) as week, category, SUM(amount) AS sum_expenses FROM transactions WHERE transaction_type = 'Expense'  GROUP BY 1,2 ORDER BY 1,2 DESC",[user_id])
    weeks = [row['week'] for row in rows]
    weekly_expenses = [row['sum_expenses'] for row in rows]
    return [weeks, weekly_expenses]

def get_weekly_income(user_id):
    rows = sql_select("SELECT date_trunc('week', date) as week, category, SUM(amount) AS sum_income FROM transactions WHERE transaction_type = 'Income' AND user_id = %s GROUP BY 1,2 ORDER BY 1,2 DESC",[user_id])
    weeks = [row['week'] for row in rows]
    weekly_income = [row['sum_income'] for row in rows]
    return [weeks, weekly_income]

class User:
    def __init__(self, id, email, password_hash, name, friend_ids, savings_goal):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.friend_ids = friend_ids
        self.savings_goal = savings_goal

    def add_friend(self, user_id):
        self.friend_ids.append(user_id)

    def validate_password(self, password):
        password_match = check_password_hash(self.password_hash, password)
        return password_match

def get_user_id(email):
    rows = sql_select("SELECT id FROM users WHERE email = %s", [email])
    user_id = rows[0]['id']
    
    return user_id 

def get_user(user_id):
    rows = sql_select("SELECT * FROM users WHERE id = %s", [user_id])

    id = rows[0]["id"]
    email = rows[0]["email"]
    password_hash = rows[0]["password_hash"]
    name = rows[0]["name"]
    friend_ids = rows[0]["friend_ids"]
    savings_goal = rows[0]["savings_goal"]

    user = User(id, email, password_hash, name, friend_ids, savings_goal)

    return user

