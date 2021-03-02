DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS vehicle;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  sale_opportunity INTEGER NOT NULL DEFAULT(1) CHECK(sale_opportunity in (0, 1))
);

CREATE TABLE vehicle (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER NOT NULL,
  color TEXT NOT NULL CHECK(color in ('yellow', 'blue', 'gray')),
  model TEXT NOT NULL CHECK(model in ('hatch', 'sedan', 'convertible')),
  FOREIGN KEY (owner_id) REFERENCES person (id)
);
