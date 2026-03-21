-- ============================================================
-- Healthcare Database Schema
-- 8 tables · SQLite-compatible types
-- ============================================================

CREATE TABLE IF NOT EXISTS insurance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_name   TEXT    NOT NULL,
    plan_type       TEXT    NOT NULL CHECK (plan_type IN ('basic', 'standard', 'premium')),
    coverage_amount REAL    NOT NULL,
    copay           REAL    NOT NULL,
    deductible      REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    floor           INTEGER NOT NULL,
    head_doctor_id  INTEGER,
    budget          REAL    NOT NULL,
    FOREIGN KEY (head_doctor_id) REFERENCES doctors (id)
);

CREATE TABLE IF NOT EXISTS doctors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT    NOT NULL,
    last_name       TEXT    NOT NULL,
    specialty       TEXT    NOT NULL,
    department_id   INTEGER NOT NULL,
    email           TEXT    NOT NULL,
    phone           TEXT    NOT NULL,
    hire_date       TEXT    NOT NULL,
    salary          REAL    NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE IF NOT EXISTS patients (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT    NOT NULL,
    last_name       TEXT    NOT NULL,
    date_of_birth   TEXT    NOT NULL,
    gender          TEXT    NOT NULL CHECK (gender IN ('M', 'F', 'Other')),
    email           TEXT    NOT NULL,
    phone           TEXT,
    blood_type      TEXT    NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    city            TEXT    NOT NULL,
    state           TEXT    NOT NULL,
    insurance_id    INTEGER,
    created_at      TEXT    NOT NULL,
    FOREIGN KEY (insurance_id) REFERENCES insurance (id)
);

CREATE TABLE IF NOT EXISTS visits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id      INTEGER NOT NULL,
    doctor_id       INTEGER NOT NULL,
    visit_date      TEXT    NOT NULL,
    diagnosis       TEXT    NOT NULL,
    notes           TEXT,
    follow_up_date  TEXT,
    status          TEXT    NOT NULL CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show')),
    FOREIGN KEY (patient_id) REFERENCES patients (id),
    FOREIGN KEY (doctor_id)  REFERENCES doctors (id)
);

CREATE TABLE IF NOT EXISTS prescriptions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id        INTEGER NOT NULL,
    medication      TEXT    NOT NULL,
    dosage          TEXT    NOT NULL,
    frequency       TEXT    NOT NULL,
    start_date      TEXT    NOT NULL,
    end_date        TEXT    NOT NULL,
    refills         INTEGER NOT NULL,
    FOREIGN KEY (visit_id) REFERENCES visits (id)
);

CREATE TABLE IF NOT EXISTS lab_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id        INTEGER NOT NULL,
    test_name       TEXT    NOT NULL,
    result_value    TEXT    NOT NULL,
    unit            TEXT    NOT NULL,
    reference_range TEXT    NOT NULL,
    is_abnormal     INTEGER NOT NULL DEFAULT 0,
    tested_at       TEXT    NOT NULL,
    FOREIGN KEY (visit_id) REFERENCES visits (id)
);

CREATE TABLE IF NOT EXISTS billing (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id               INTEGER NOT NULL,
    amount                 REAL    NOT NULL,
    insurance_covered      REAL    NOT NULL,
    patient_responsibility REAL    NOT NULL,
    status                 TEXT    NOT NULL CHECK (status IN ('pending', 'paid', 'overdue', 'insurance_processing')),
    billed_at              TEXT    NOT NULL,
    paid_at                TEXT,
    FOREIGN KEY (visit_id) REFERENCES visits (id)
);
