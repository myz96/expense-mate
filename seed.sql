INSERT INTO users (email, name) VALUES ('michael.yj.zhao@gmail.com', 'Michael Zhao');
INSERT INTO users (email, name) VALUES ('johnsmith@example.com', 'John Smith');

INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('1', 'Drinks at Manchuria', '100', 'Eating out', 'Splurg');
INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('1', 'Date night at Farmers Daughter', '150', 'Eating out', 'Splurg');
INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('1', 'Groceries', '120', 'Groceries', 'Essentials');
INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('2', 'Netflix', '15', 'Entertainment', 'Splurg');
INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('2', 'Gym membership', '27', 'Health', 'Essentials');
INSERT INTO expenses (user_id, expense, amount, category, type) VALUES ('2', 'Uber eats', '35', 'Lazy eats', 'Splurg');

INSERT INTO friends (user_id, friend_id) VALUES ('1', '2');
INSERT INTO friends (user_id, friend_id) VALUES ('2', '1');

