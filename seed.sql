INSERT INTO users (email, password_hash, first_name, last_name, friend_ids, savings_goal) VALUES ('michael.yj.zhao@gmail.com', 'pbkdf2:sha256:260000$CtGmXxAknSIcQIAA$fc1c9db9acc98b4cc5dc2c291e18c970e0e82463e22442edf6d03bc7e0d29ee7', 'Michael', 'Zhao', ARRAY[2,3]::integer[], '600');
INSERT INTO users (email, password_hash, first_name, last_name, friend_ids, savings_goal) VALUES ('johnsmith@example.com', 'pbkdf2:sha256:260000$CtGmXxAknSIcQIAA$fc1c9db9acc98b4cc5dc2c291e18c970e0e82463e22442edf6d03bc7e0d29ee7', 'John', 'Smith', ARRAY[1]::integer[], '500');
INSERT INTO users (email, password_hash, first_name, last_name, friend_ids, savings_goal) VALUES ('marysmith@example.com', 'pbkdf2:sha256:260000$CtGmXxAknSIcQIAA$fc1c9db9acc98b4cc5dc2c291e18c970e0e82463e22442edf6d03bc7e0d29ee7', 'Mary', 'Smith', ARRAY[1]::integer[], '550');

INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-01', '1', 'Income', 'Work salary', '2000', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-03', '1', 'Income', 'Dividends', '500', 'Investment', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-08', '1', 'Income', 'Work salary', '2000', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-11', '1', 'Expense', 'Drinks at Manchuria', '100', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-21', '1', 'Expense', 'Dinner at Farmers Daughter', '150', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-03', '1', 'Expense', 'Netflix', '15', 'Entertainment', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-03', '2', 'Income', 'Work salary', '1500', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-13', '2', 'Income', 'Work salary', '1500', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-13', '2', 'Expense', 'Uber eats', '35', 'Eating out', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-03-23', '2', 'Expense', 'Gym membership', '27', 'Health', 'Essentials');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-01', '3', 'Income', 'Netflix', '27', 'Entertainment', 'Splurg');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-03', '3', 'Expense', 'Work salary', '1000', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-08', '3', 'Expense', 'Work salary', '500', 'Work', 'Income');
INSERT INTO transactions (date, user_id, transaction_type, description, amount, category, type) VALUES ('2023-02-11', '3', 'Income', 'Uber eats', '80', 'Eating out', 'Splurg');

INSERT INTO posts (user_id, name, savings_amount, likes, comments, description) VALUES ('1', 'Michael Zhao', '300', ARRAY[2,3]::integer[], ARRAY['Great job','Congratulations']::text[], 'Good month!');
INSERT INTO posts (user_id, name, savings_amount, likes, comments, description) VALUES ('1', 'Michael Zhao', '250', ARRAY[2]::integer[], ARRAY['Nice one!']::text[], 'Very happy with this one.');
INSERT INTO posts (user_id, name, savings_amount, likes, comments, description) VALUES ('2', 'John Smith', '270', ARRAY[1]::integer[], ARRAY['+1', 'Amazing!']::text[], 'Good first month');
INSERT INTO posts (user_id, name, savings_amount, likes, comments, description) VALUES ('3', 'Mary Smith', '265', ARRAY[1]::integer[], ARRAY['Nice Mary!'], 'Happy with this.');