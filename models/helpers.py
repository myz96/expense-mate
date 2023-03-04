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

class Expense:
    def __init__(self, id, date, user_id, description, amount, category, type):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.category = category
        self.type = type

def get_expense(expense_id):
    rows = sql_select("SELECT * FROM expenses WHERE id = %s;", [expense_id])

    id = rows[0]["id"]
    date = rows[0]["date"]
    user_id = rows[0]["user_id"]
    description = rows[0]["description"]
    amount = rows[0]["amount"]
    category = rows[0]["category"]
    type = rows[0]["type"]

    expense = Expense(id, date, user_id, description, amount, category, type)

    return expense

def get_all_expenses(user_id):
    expenses = []

    rows = sql_select("SELECT * FROM expenses WHERE user_id = %s", [user_id])
    for row in rows:
        id = row["id"]
        expense = get_expense(id)
        expenses.append(expense)
    
    return expenses

class User:
    def __init__(self, id, email, password_hash, name, friend_ids):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.friend_ids = []

    def add_friend(self, user_id):
        self.friend_ids.append(user_id)

    def validate_password(self, password):
        password_match = check_password_hash(self.password_hash, password)
        return password_match

def get_user_id(email):
    rows = sql_select("SELECT id FROM users where email = %s", [email])
    user_id = rows[0]['id']
    
    return user_id

def get_user(user_id):
    rows = sql_select("SELECT * FROM users where id = %s", [user_id])

    id = rows[0]["id"]
    email = rows[0]["email"]
    password_hash = rows[0]["password_hash"]
    name = rows[0]["name"]
    friend_ids = rows[0]["friend_ids"]

    user = User(id, email, password_hash, name, friend_ids)

    return user