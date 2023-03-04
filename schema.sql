DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friends;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT,
  password_hash TEXT,
  name VARCHAR(250),
  friend_ids integer[]
);

CREATE TABLE expenses (
  id SERIAL PRIMARY KEY,
  user_id integer,
  date DATE,
  description TEXT,
  amount integer,
  category VARCHAR(250),
  type VARCHAR(250),
  CONSTRAINT fk_expenses_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)  
);

CREATE TABLE income (
  id SERIAL PRIMARY KEY,
  user_id integer,
  date DATE,
  description TEXT,
  amount integer,
  category VARCHAR(250),
  type VARCHAR(250),
  CONSTRAINT fk_income_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)  
);

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id integer,
    friend_id integer
);

-- Watch video best back end for likes on social media