INSERT INTO user (username, password)
VALUES
    ('test_auth_user_1', 'pbkdf2:sha256:150000$f1FyVdgx$bd35e95d509623bf59d75fb7c3e2ee3c13d3d4f47bc7a6a2dcfe387d508f23f6'),
    ('test_auth_user_2', 'pbkdf2:sha256:150000$kZXPWPO7$086816a61e7c518dc664cb286a4f5f83ca08baeb9bc54bd4ca138e52f9c23b58');

INSERT INTO person (first_name, last_name)
VALUES
    ('Fake', 'McTester'),
    ('Test', 'Person'),
    ('Mr', 'Test');

INSERT INTO vehicle (owner_id, color, model)
VALUES
    (1, 'blue', 'hatch');