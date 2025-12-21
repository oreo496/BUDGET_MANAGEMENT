-- ======================================================
-- FUNDER PERSONAL FINANCE APPLICATION DATABASE SCHEMA
-- MySQL DDL Script
-- ======================================================

-- Database for FUNDER application
CREATE DATABASE IF NOT EXISTS funder CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE funder;

-- ======================================================
-- USERS TABLE
-- ======================================================
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    two_factor_enabled BOOLEAN DEFAULT 0,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================================================
-- ADMINS TABLE
-- ======================================================
CREATE TABLE admins (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================================================
-- CATEGORIES TABLE
-- ======================================================
CREATE TABLE categories (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,
    type ENUM('INCOME', 'EXPENSE') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_category_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ======================================================
-- BANK ACCOUNTS (TOKENIZED DATA ONLY)
-- ======================================================
CREATE TABLE bank_accounts (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    institution_name VARCHAR(100),
    account_type VARCHAR(50),
    token VARBINARY(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bank_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ======================================================
-- TRANSACTIONS TABLE
-- ======================================================
CREATE TABLE transactions (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    category_id CHAR(36),
    bank_account_id CHAR(36),
    amount DECIMAL(10,2) NOT NULL,
    type ENUM('INCOME', 'EXPENSE') NOT NULL,
    merchant VARCHAR(255),
    date DATE NOT NULL,
    source ENUM('MANUAL', 'SYNCED') DEFAULT 'MANUAL',
    flagged_fraud BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transaction_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_transaction_bank
        FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id)
        ON DELETE SET NULL
);

-- ======================================================
-- BUDGETS TABLE
-- ======================================================
CREATE TABLE budgets (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    category_id CHAR(36) NOT NULL,
    period ENUM('WEEKLY', 'MONTHLY') NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_budget_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_budget_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE CASCADE
);

-- ======================================================
-- GOALS TABLE
-- ======================================================
CREATE TABLE goals (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    title VARCHAR(100) NOT NULL,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    deadline DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_goal_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ======================================================
-- AI ALERTS TABLE
-- ======================================================
CREATE TABLE ai_alerts (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('BUDGET_ALERT','SPENDING_PATTERN','FRAUD','GOAL_RECOMMENDATION') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ai_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ======================================================
-- SYSTEM LOGS (USER & ADMIN ACTIVITY)
-- ======================================================
CREATE TABLE system_logs (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    admin_id CHAR(36),
    action VARCHAR(255) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_logs_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_logs_admin FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE SET NULL
);

-- ======================================================
-- ADMIN ACTIONS TABLE
-- ======================================================
CREATE TABLE admin_actions (
    id CHAR(36) PRIMARY KEY,
    admin_id CHAR(36) NOT NULL,
    action VARCHAR(255) NOT NULL,
    target_user_id CHAR(36),
    transaction_id CHAR(36),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_admin_action_admin FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    CONSTRAINT fk_admin_action_user FOREIGN KEY (target_user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_admin_action_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);

-- Notes:
-- This schema uses CHAR(36) for UUID string storage (e.g. 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx').
-- To connect the project, set your MySQL DATABASE_URL or Django DATABASES in `backend/.env` or environment:
-- Example `DATABASES` snippet for `backend/funder/settings.py`:
-- DATABASES = {
--   'default': {
--       'ENGINE': 'django.db.backends.mysql',
--       'NAME': 'funder',
--       'USER': 'your_db_user',
--       'PASSWORD': 'your_db_password',
--       'HOST': '127.0.0.1',
--       'PORT': '3306',
--       'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
--   }
-- }

