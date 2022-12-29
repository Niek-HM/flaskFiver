CREATE TABLE IF NOT EXISTS user( -- The main user account
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    name varchar(24) NOT NULL UNIQUE,
    pfp varchar(64), -- maybe save as BLOB data type??

    first_name varchar(24),
    last_name varchar(24),
    passwordHash BINARY(64) NOT NULL,
    
    email varchar(319) UNIQUE,
    phone varchar(24),
    rating TINYINT,
    
    website varchar(24),
    github varchar(24),
    insta varchar(24),
    facebook varchar(24),
    twitter varchar(24),

    
    token varchar(64) UNIQUE, -- Should have more stuff like age etc.

    isSeller BOOLEAN DEFAULT 0, --0 = False and 1 is True
    privacy BOOLEAN DEFAULT 0,
    isAdmin BOOLEAN DEFAULT 0,
    isMod BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products( -- Products sold on the website
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator INTEGER FOREIGNKEY REFERENCES user(id),
    description varchar(64),
    title varchar(28),
    body varchar(1024),
    price INTEGER
);

CREATE TABLE IF NOT EXISTS productimg(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product INTEGER FOREIGNKEY REFERENCES products(id),
    img varchar(64),
    pos TINYINT
);

CREATE TABLE IF NOT EXISTS orders( -- People who bought a product
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer INTEGER FOREIGNKEY REFERENCES user(id),
    product INTEGER FOREIGNKEY REFERENCES product(id),
    creation DATE,
    expire DATETIME, -- IDK how to make a auto remove here 
    canceled BOOLEAN
);

CREATE TABLE IF NOT EXISTS special_offers( -- Make people able to discount products
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product INTEGER FOREIGNKEY REFERENCES products(id),
    discount TINYINT,
    expires DATETIME
);

CREATE TABLE IF NOT EXISTS comments( -- Comments for products (also ratings)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    for INTEGER FOREIGNKEY REFERENCES product(id),
    comenter INTEGER FOREIGNKEY REFERENCES user(id),
    stars TINYINT,
    comment varchar(128),
    creation DATE
);

CREATE TABLE IF NOT EXISTS ratings( -- Ratings for users
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating TINYINT,
    for INTEGER FOREIGNKEY REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS reports( -- Reporting scammers etc
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reported INTEGER FOREIGNKEY REFERENCES user(id),
    reporter INTEGER FOREIGNKEY REFERENCES user(id),
    types varchar(24),
    info varchar(128) -- Small amount of info a user can give why they reported the user
);

CREATE TABLE IF NOT EXISTS messages( -- Send messages to other users
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- NOTE there is no way to send messages yet
    sender INTEGER FOREIGNKEY REFERENCES user(id),
    receiver INTEGER FOREIGNKEY REFERENCES user(id),
    title varchar(64),
    body varchar(256)
    -- Maybe add file support?
);