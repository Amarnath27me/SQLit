-- Finance Dataset Schema
-- 7 tables for a banking/finance database

CREATE TABLE IF NOT EXISTS branches (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    manager_name TEXT NOT NULL,
    opened_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    date_of_birth TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    account_type TEXT NOT NULL CHECK (account_type IN ('checking', 'savings', 'investment', 'credit')),
    balance REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    opened_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'closed', 'frozen')),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('deposit', 'withdrawal', 'transfer', 'fee', 'interest')),
    amount REAL NOT NULL,
    balance_after REAL NOT NULL,
    description TEXT,
    reference_number TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    card_number TEXT NOT NULL,
    card_type TEXT NOT NULL CHECK (card_type IN ('debit', 'credit')),
    expiry_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'blocked', 'expired')),
    credit_limit REAL,
    issued_at TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    loan_type TEXT NOT NULL CHECK (loan_type IN ('personal', 'mortgage', 'auto', 'business')),
    principal REAL NOT NULL,
    interest_rate REAL NOT NULL,
    term_months INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'paid', 'defaulted')),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL,
    principal_paid REAL NOT NULL,
    interest_paid REAL NOT NULL,
    remaining_balance REAL NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loans(id)
);
