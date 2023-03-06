INSERT INTO users (email, password_hash, name, savings_goal) VALUES ('michael.yj.zhao@gmail.com', 'pbkdf2:sha256:260000$2RXR7ssqOh8HHsFA$a51e5dfa4c3ff976ca26fc785b65efec79b196e03364b1ba75fba0fcdccfa03e', 'Michael  Zhao', '1100');
INSERT INTO users (email, password_hash, name, savings_goal) VALUES ('johnsmith@example.com', 'pbkdf2:sha256:260000$RZyGA6GZYZcAmy2Q$8ca49a18e53a66ce366b08f7e1d33b7ae7d234996daa6468b8aa99e012dede17', 'John Smith', '1000');

INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-01', '1', 'Income', 'Work salary', '2000', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-03', '1', 'Income', 'Dividends', '500', 'Investment', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-08', '1', 'Income', 'Work salary', '2000', 'Work', 'Salary');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-11', '1', 'Expense', 'Drinks at Manchuria', '100', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-21', '1', 'Expense', 'Dinner at Farmers Daughter', '150', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-03', '1', 'Expense', 'Netflix', '15', 'Entertainment', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-03', '2', 'Income', 'Work salary', '1500', 'Work', 'Salary');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-13', '2', 'Income', 'Work salary', '1500', 'Work', 'Salary');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-13', '2', 'Expense', 'Uber eats', '35', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-23', '2', 'Expense', 'Gym membership', '27', 'Health', 'Essentials');

INSERT INTO friends (user_id, friend_id) VALUES ('1', '2');
INSERT INTO friends (user_id, friend_id) VALUES ('2', '1');

