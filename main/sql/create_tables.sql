CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(24) NOT NULL UNIQUE,
    passwordHash BINARY(64) NOT NULL,
    token varchar(64) UNIQUE, -- Should have more stuff like age etc.

    email varchar(319) UNIQUE,

    first_name varchar(24),
    last_name varchar(24),

    isSeller BOOLEAN DEFAULT 0, --0 = False and 1 is True
    isAdmin BOOLEAN DEFAULT 0,
    isMod BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title varchar(28),
    price INTEGER
);

CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer INTEGER FOREIGNKEY REFERENCES user(id),
    product INTEGER FOREIGNKEY REFERENCES product(id),
    creation DATE,
    expire DATETIME -- IDK how to make a auto remove here 
);

CREATE TABLE IF NOT EXISTS special_offers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product INTEGER FOREIGNKEY REFERENCES products(id),
    discount TINYINT

);

CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comenter INTEGER FOREIGNKEY REFERENCES user(id),
    stars TINYINT,
    comment varchar(128),
    creation DATE
);

CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reported INTEGER FOREIGNKEY REFERENCES user(id),
    reporter INTEGER FOREIGNKEY REFERENCES user(id),
    info varchar(128) -- Small amount of info a user can give why they reported the user
);