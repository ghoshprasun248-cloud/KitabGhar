-- =====================================================
-- KitabGhar Database
-- =====================================================

DROP DATABASE IF EXISTS kitabghar;
CREATE DATABASE kitabghar;
USE kitabghar;

-- =====================================================
-- USERS TABLE
-- =====================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    profile_image VARCHAR(255) DEFAULT 'default.png',
    bio TEXT,
    role ENUM('user','admin') DEFAULT 'user',
    status ENUM('active','blocked') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- CATEGORIES
-- =====================================================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- BOOKS TABLE
-- =====================================================

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    author VARCHAR(255) NOT NULL,

    description TEXT,

    isbn VARCHAR(50),

    language VARCHAR(50),

    publisher VARCHAR(150),

    publish_year YEAR,

    pages INT,

    file_name VARCHAR(255),

    cover_image VARCHAR(255),

    uploaded_by INT,

    category_id INT,

    total_downloads INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (uploaded_by)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY (category_id)
    REFERENCES categories(id)
    ON DELETE SET NULL
);

-- =====================================================
-- DOWNLOAD HISTORY
-- =====================================================

CREATE TABLE downloads (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    book_id INT,

    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY(book_id)
    REFERENCES books(id)
    ON DELETE CASCADE
);

-- =====================================================
-- BOOKMARKS
-- =====================================================

CREATE TABLE bookmarks (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    book_id INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY(book_id)
    REFERENCES books(id)
    ON DELETE CASCADE
);

-- =====================================================
-- REVIEWS
-- =====================================================

CREATE TABLE reviews (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    book_id INT,

    rating INT CHECK(rating BETWEEN 1 AND 5),

    review TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY(book_id)
    REFERENCES books(id)
    ON DELETE CASCADE
);

-- =====================================================
-- SAMPLE CATEGORIES
-- =====================================================

INSERT INTO categories(category_name,description)
VALUES

('Programming','Programming Books'),

('Artificial Intelligence','AI & ML Books'),

('Data Science','Data Science Books'),

('Machine Learning','Machine Learning Books'),

('Deep Learning','Deep Learning Books'),

('Python','Python Books'),

('Java','Java Books'),

('C Programming','C Books'),

('Database','SQL Books'),

('Networking','Networking Books'),

('Operating System','OS Books'),

('Cyber Security','Security Books'),

('Cloud Computing','Cloud Books'),

('Web Development','HTML CSS JS'),

('Mathematics','Math Books'),

('Electronics','Electronics Books');

-- =====================================================
-- DEFAULT ADMIN
-- Password:
-- Admin@123
-- (Replace with hashed password later)
-- =====================================================

INSERT INTO users
(
full_name,
username,
email,
phone,
password,
role,
status
)

VALUES
(
'Administrator',
'admin',
'admin@kitabghar.com',
'9999999999',
'Admin@123',
'admin',
'active'
);

-- =====================================================
-- END
-- =====================================================