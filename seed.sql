DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS summaries;

CREATE TABLE expenses (
  id SERIAL PRIMARY KEY,
  user_id integer,
  expense VARCHAR(250) NOT NULL,
  amount integer NOT NULL,
  category VARCHAR(250),
  type VARCHAR(250),
  CONSTRAINT fk_expenses_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)  
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  name VARCHAR(250),
  user_id integer,
  category VARCHAR(250),
  type VARCHAR(250)
);

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id integer,
    friend_id integer
);