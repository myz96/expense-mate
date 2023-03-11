import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
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
    def __init__(self, id, email, password_hash, first_name, last_name, friend_ids, savings_goal):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.friend_ids = friend_ids
        self.savings_goal = savings_goal

    def validate_password(self, password):
        password_match = check_password_hash(self.password_hash, password)
        return password_match
    
    def get_friends(self):
        friends = [get_user(friend_id) for friend_id in self.friend_ids]
        return friends

    def add_remove_friend(self, friend_id):
        print(type(friend_id))
        print(friend_id)
        print(self.friend_ids)
        print(int(friend_id) in self.friend_ids)
        if int(friend_id) in self.friend_ids:
            sql_write("UPDATE users SET friend_ids = array_remove(friend_ids, %s) WHERE id = %s", [friend_id, self.id])
            sql_write("UPDATE users SET friend_ids = array_remove(friend_ids, %s) WHERE id = %s", [self.id, friend_id])
        else:
            sql_write("UPDATE users SET friend_ids = array_append(friend_ids, %s) WHERE id = %s", [friend_id, self.id])
            sql_write("UPDATE users SET friend_ids = array_append(friend_ids, %s) WHERE id = %s", [self.id, friend_id])

def create_user(email, password_hash, first_name, last_name, savings_goal):
    sql_write("INSERT INTO users (email, password_hash, first_name, last_name, savings_goal, friend_ids) VALUES (%s, %s, %s, %s, %s, ARRAY[]::integer[])", [email, password_hash, first_name, last_name, savings_goal])
    print(get_all_users())

def get_user_id(email):
    rows = sql_select("SELECT id FROM users WHERE email = %s", [email])
    user_id = rows[0]['id']
    return user_id 

def get_user(user_id):
    rows = sql_select("SELECT * FROM users WHERE id = %s", [user_id])

    id = rows[0]["id"]
    email = rows[0]["email"]
    password_hash = rows[0]["password_hash"]
    first_name = rows[0]["first_name"]
    last_name = rows[0]["last_name"]
    friend_ids = rows[0]["friend_ids"]
    savings_goal = rows[0]["savings_goal"]

    user = User(id, email, password_hash, first_name, last_name, friend_ids, savings_goal)

    return user

def get_all_users():
    rows = sql_select("SELECT * FROM users", [])
    users = [get_user(row['id']) for row in rows]
    return users

class Post:
    def __init__(self, id, date, user_id, first_name, last_name, savings_amount, description, likes, comments):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.savings_amount = savings_amount
        self.description = description
        self.likes = likes
        self.comments = comments
    
    def like_unlike_post(self, user_id):
        if user_id in self.likes:
            sql_write("UPDATE posts SET likes = array_remove(likes, %s) WHERE id = %s", [user_id, self.id])
        else:
            sql_write("UPDATE posts SET likes = array_append(likes, %s) WHERE id = %s", [user_id, self.id])
    
    def add_comment(self, comment):
        sql_write("UPDATE posts SET comments = array_append(comments, %s) WHERE id = %s", [comment, self.id])

    # def delete_comment(self, id, date, content):
    #     comment = Comment(id, date, self.id, self.user_id, self.first_name, content)
    #     sql_write("UPDATE posts SET comments = array_remove(comments, %s) WHERE id = %s AND %s = ANY(comments.id)", [comment, self.id])

    def edit_post(self, description):
        sql_write("UPDATE posts SET description = %s WHERE id = %s", [description, self.id])

    def delete_post(self):
        sql_write("DELETE FROM posts WHERE id = %s", [self.id])

def create_post(user_id, savings_amount, description):
    user = get_user(user_id)
    current_date = datetime.date.today()
    sql_write("INSERT INTO posts (date, user_id, first_name, last_name, savings_amount, description, likes, comments) VALUES (%s, %s, %s, %s, %s, %s, ARRAY[]::integer[], ARRAY[]::text[])", [current_date, user_id, user.first_name, user.last_name, savings_amount, description])

def get_post(post_id):
    rows = sql_select("SELECT * FROM posts WHERE id = %s", [post_id])

    id = rows[0]["id"]
    date = rows[0]["date"]
    user_id = rows[0]["user_id"]
    first_name = get_user(user_id).first_name
    last_name = get_user(user_id).last_name
    savings_amount = rows[0]["savings_amount"]
    description = rows[0]["description"]
    likes = rows[0]["likes"]
    comments = rows[0]["comments"]

    post = Post(id, date, user_id, first_name, last_name, savings_amount, description, likes, comments)

    return post

def get_feed_posts(user_id):
    rows = sql_select("SELECT posts.id AS post_id FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE %s = ANY(users.friend_ids) ORDER BY posts.date DESC", [user_id])

    posts = [get_post(row['post_id']) for row in rows]

    return posts

def get_user_posts(user_id):
    rows = sql_select("SELECT * FROM posts WHERE user_id = %s", [user_id])

    posts = [get_post(row['id']) for row in rows]
    
    return posts

class Comment:
    def __init__(self, id, date, post_id, user_id, name, content):
        self.id = id
        self.date = date
        self.post_id = post_id
        self.user_id = user_id
        self.name = name
        self.content = content


