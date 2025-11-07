-- 테스트 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS gym_test;

-- 테스트 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS 'test_user'@'localhost' IDENTIFIED BY 'test1234';
GRANT ALL PRIVILEGES ON gym_test.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;

USE gym_test;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS membership_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    duration_days INT NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    membership_type_id INT,
    membership_start_date DATE,
    membership_end_date DATE,
    FOREIGN KEY (membership_type_id) REFERENCES membership_types(id)
);

CREATE TABLE IF NOT EXISTS checkin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS locker_rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT UNIQUE,
    locker_number INT NOT NULL,
    rental_start_date DATE NOT NULL,
    rental_end_date DATE NOT NULL,
    rental_type ENUM('daily', 'monthly', 'yearly') NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS uniform_rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT UNIQUE,
    rental_start_date DATE NOT NULL,
    rental_end_date DATE NOT NULL,
    rental_type ENUM('daily', 'monthly', 'yearly') NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id)
);