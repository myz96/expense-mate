DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT,
  password_hash TEXT,
  first_name VARCHAR(512),
  last_name VARCHAR(512),
  friend_ids integer[],
  savings_goal integer
);

CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  transaction_type VARCHAR(50),
  user_id integer,
  date DATE,
  description TEXT,
  amount integer,
  category VARCHAR(512),
  type VARCHAR(512),
  CONSTRAINT fk_transactions_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)  
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  date DATE,
  user_id integer,
  first_name VARCHAR(512),
  last_name VARCHAR(512),
  savings_amount integer, -- Replace with URL string to donut graph that shows savings over and above target
  description TEXT,
  likes integer[],
  comments TEXT[],
  CONSTRAINT fk_posts_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)
);

