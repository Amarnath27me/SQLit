"use client";

import { useState } from "react";

/* ------------------------------------------------------------------ */
/*  Dataset schema definitions (self-contained)                       */
/* ------------------------------------------------------------------ */

interface Column {
  name: string;
  type: string;
  pk?: boolean;
  fk?: string;
}

interface TableSchema {
  name: string;
  columns: Column[];
  sampleRows: (string | number | null)[][];
}

interface DatasetDef {
  name: string;
  tables: number;
  totalRows: string;
  description: string;
  schema: TableSchema[];
  relationships: string[];
}

const DATASET_SCHEMAS: Record<string, DatasetDef> = {
  ecommerce: {
    name: "E-Commerce",
    tables: 8,
    totalRows: "~4,500",
    description: "A complete retail data model with customers, orders, products, and reviews",
    schema: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "email", type: "VARCHAR(150)" },
          { name: "city", type: "VARCHAR(100)" },
          { name: "created_at", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, "Alice Johnson", "alice@email.com", "New York", "2024-01-15"],
          [2, "Bob Smith", "bob@email.com", "San Francisco", "2024-02-20"],
          [3, "Carol White", "carol@email.com", "Chicago", "2024-03-10"],
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "customer_id", type: "INTEGER", fk: "customers.id" },
          { name: "total_amount", type: "DECIMAL(10,2)" },
          { name: "status", type: "VARCHAR(20)" },
          { name: "order_date", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, 1, 150.0, "completed", "2024-03-01"],
          [2, 2, 89.99, "completed", "2024-03-05"],
          [3, 1, 245.5, "pending", "2024-03-10"],
        ],
      },
      {
        name: "products",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(200)" },
          { name: "category_id", type: "INTEGER", fk: "categories.id" },
          { name: "price", type: "DECIMAL(10,2)" },
          { name: "stock", type: "INTEGER" },
        ],
        sampleRows: [
          [1, "Wireless Headphones", 1, 79.99, 150],
          [2, "USB-C Cable", 1, 12.99, 500],
          [3, "Running Shoes", 2, 129.99, 75],
        ],
      },
      {
        name: "order_items",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "order_id", type: "INTEGER", fk: "orders.id" },
          { name: "product_id", type: "INTEGER", fk: "products.id" },
          { name: "quantity", type: "INTEGER" },
          { name: "unit_price", type: "DECIMAL(10,2)" },
        ],
        sampleRows: [
          [1, 1, 1, 2, 79.99],
          [2, 1, 2, 1, 12.99],
          [3, 2, 3, 1, 129.99],
        ],
      },
      {
        name: "categories",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "parent_id", type: "INTEGER", fk: "categories.id" },
        ],
        sampleRows: [
          [1, "Electronics", null],
          [2, "Footwear", null],
          [3, "Audio", 1],
        ],
      },
      {
        name: "payments",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "order_id", type: "INTEGER", fk: "orders.id" },
          { name: "method", type: "VARCHAR(50)" },
          { name: "amount", type: "DECIMAL(10,2)" },
          { name: "paid_at", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, 1, "credit_card", 150.0, "2024-03-01"],
          [2, 2, "paypal", 89.99, "2024-03-05"],
        ],
      },
      {
        name: "reviews",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "product_id", type: "INTEGER", fk: "products.id" },
          { name: "customer_id", type: "INTEGER", fk: "customers.id" },
          { name: "rating", type: "INTEGER" },
          { name: "comment", type: "TEXT" },
        ],
        sampleRows: [
          [1, 1, 1, 5, "Great sound quality!"],
          [2, 3, 2, 4, "Comfortable fit"],
        ],
      },
      {
        name: "shipping",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "order_id", type: "INTEGER", fk: "orders.id" },
          { name: "carrier", type: "VARCHAR(50)" },
          { name: "tracking_number", type: "VARCHAR(100)" },
          { name: "status", type: "VARCHAR(30)" },
        ],
        sampleRows: [
          [1, 1, "FedEx", "FX123456", "delivered"],
          [2, 2, "UPS", "UP789012", "in_transit"],
        ],
      },
    ],
    relationships: [
      "orders.customer_id \u2192 customers.id",
      "order_items.order_id \u2192 orders.id",
      "order_items.product_id \u2192 products.id",
      "products.category_id \u2192 categories.id",
      "payments.order_id \u2192 orders.id",
      "reviews.product_id \u2192 products.id",
      "reviews.customer_id \u2192 customers.id",
      "shipping.order_id \u2192 orders.id",
    ],
  },
  finance: {
    name: "Finance",
    tables: 7,
    totalRows: "~4,000",
    description: "Banking data model with accounts, transactions, loans, and branches",
    schema: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "email", type: "VARCHAR(150)" },
          { name: "dob", type: "DATE" },
          { name: "risk_score", type: "INTEGER" },
        ],
        sampleRows: [
          [1, "James Wilson", "james@bank.com", "1985-06-15", 3],
          [2, "Sarah Davis", "sarah@bank.com", "1990-11-22", 1],
        ],
      },
      {
        name: "accounts",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "customer_id", type: "INTEGER", fk: "customers.id" },
          { name: "type", type: "VARCHAR(30)" },
          { name: "balance", type: "DECIMAL(12,2)" },
          { name: "opened_at", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, 1, "checking", 5420.5, "2020-01-10"],
          [2, 1, "savings", 15000.0, "2020-01-10"],
          [3, 2, "checking", 3200.75, "2021-03-15"],
        ],
      },
      {
        name: "transactions",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "account_id", type: "INTEGER", fk: "accounts.id" },
          { name: "type", type: "VARCHAR(20)" },
          { name: "amount", type: "DECIMAL(12,2)" },
          { name: "timestamp", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, 1, "debit", 50.0, "2024-03-01 10:30:00"],
          [2, 1, "credit", 2500.0, "2024-03-01 14:00:00"],
        ],
      },
      {
        name: "cards",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "account_id", type: "INTEGER", fk: "accounts.id" },
          { name: "type", type: "VARCHAR(20)" },
          { name: "last_four", type: "VARCHAR(4)" },
          { name: "expires_at", type: "DATE" },
        ],
        sampleRows: [
          [1, 1, "debit", "4521", "2027-06-01"],
          [2, 3, "credit", "8832", "2026-12-01"],
        ],
      },
      {
        name: "loans",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "customer_id", type: "INTEGER", fk: "customers.id" },
          { name: "amount", type: "DECIMAL(12,2)" },
          { name: "interest_rate", type: "DECIMAL(5,2)" },
          { name: "status", type: "VARCHAR(20)" },
        ],
        sampleRows: [
          [1, 1, 25000.0, 5.5, "active"],
          [2, 2, 10000.0, 4.25, "paid_off"],
        ],
      },
      {
        name: "payments",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "loan_id", type: "INTEGER", fk: "loans.id" },
          { name: "amount", type: "DECIMAL(12,2)" },
          { name: "paid_at", type: "TIMESTAMP" },
        ],
        sampleRows: [
          [1, 1, 500.0, "2024-03-01"],
          [2, 1, 500.0, "2024-04-01"],
        ],
      },
      {
        name: "branches",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "city", type: "VARCHAR(100)" },
          { name: "manager_id", type: "INTEGER" },
        ],
        sampleRows: [
          [1, "Downtown Branch", "New York", 101],
          [2, "Westside Branch", "San Francisco", 102],
        ],
      },
    ],
    relationships: [
      "accounts.customer_id \u2192 customers.id",
      "transactions.account_id \u2192 accounts.id",
      "cards.account_id \u2192 accounts.id",
      "loans.customer_id \u2192 customers.id",
      "payments.loan_id \u2192 loans.id",
    ],
  },
  healthcare: {
    name: "Healthcare",
    tables: 8,
    totalRows: "~4,000",
    description: "Clinical data model with patients, doctors, visits, prescriptions, and billing",
    schema: [
      {
        name: "patients",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "dob", type: "DATE" },
          { name: "gender", type: "VARCHAR(10)" },
          { name: "insurance_id", type: "INTEGER", fk: "insurance.id" },
        ],
        sampleRows: [
          [1, "Emma Brown", "1988-04-12", "F", 1],
          [2, "Michael Lee", "1975-09-03", "M", 2],
        ],
      },
      {
        name: "doctors",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "specialty", type: "VARCHAR(100)" },
          { name: "department_id", type: "INTEGER", fk: "departments.id" },
        ],
        sampleRows: [
          [1, "Dr. Patel", "Cardiology", 1],
          [2, "Dr. Kim", "Neurology", 2],
        ],
      },
      {
        name: "departments",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "name", type: "VARCHAR(100)" },
          { name: "floor", type: "INTEGER" },
          { name: "head_doctor_id", type: "INTEGER" },
        ],
        sampleRows: [
          [1, "Cardiology", 3, 1],
          [2, "Neurology", 4, 2],
        ],
      },
      {
        name: "visits",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "patient_id", type: "INTEGER", fk: "patients.id" },
          { name: "doctor_id", type: "INTEGER", fk: "doctors.id" },
          { name: "visit_date", type: "TIMESTAMP" },
          { name: "diagnosis", type: "TEXT" },
        ],
        sampleRows: [
          [1, 1, 1, "2024-03-01", "Hypertension"],
          [2, 2, 2, "2024-03-05", "Migraine"],
        ],
      },
      {
        name: "prescriptions",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "visit_id", type: "INTEGER", fk: "visits.id" },
          { name: "medication", type: "VARCHAR(200)" },
          { name: "dosage", type: "VARCHAR(50)" },
          { name: "duration_days", type: "INTEGER" },
        ],
        sampleRows: [
          [1, 1, "Lisinopril", "10mg daily", 30],
          [2, 2, "Sumatriptan", "50mg as needed", 10],
        ],
      },
      {
        name: "insurance",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "provider", type: "VARCHAR(100)" },
          { name: "plan_type", type: "VARCHAR(50)" },
          { name: "coverage_pct", type: "DECIMAL(5,2)" },
        ],
        sampleRows: [
          [1, "BlueCross", "Premium", 90.0],
          [2, "Aetna", "Standard", 75.0],
        ],
      },
      {
        name: "lab_results",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "visit_id", type: "INTEGER", fk: "visits.id" },
          { name: "test_name", type: "VARCHAR(100)" },
          { name: "result_value", type: "VARCHAR(50)" },
          { name: "reference_range", type: "VARCHAR(50)" },
        ],
        sampleRows: [
          [1, 1, "Blood Pressure", "140/90", "120/80"],
          [2, 2, "MRI Brain", "Normal", "Normal"],
        ],
      },
      {
        name: "billing",
        columns: [
          { name: "id", type: "SERIAL", pk: true },
          { name: "visit_id", type: "INTEGER", fk: "visits.id" },
          { name: "amount", type: "DECIMAL(10,2)" },
          { name: "insurance_covered", type: "DECIMAL(10,2)" },
          { name: "status", type: "VARCHAR(20)" },
        ],
        sampleRows: [
          [1, 1, 350.0, 315.0, "paid"],
          [2, 2, 1200.0, 900.0, "pending"],
        ],
      },
    ],
    relationships: [
      "patients.insurance_id \u2192 insurance.id",
      "doctors.department_id \u2192 departments.id",
      "visits.patient_id \u2192 patients.id",
      "visits.doctor_id \u2192 doctors.id",
      "prescriptions.visit_id \u2192 visits.id",
      "lab_results.visit_id \u2192 visits.id",
      "billing.visit_id \u2192 visits.id",
    ],
  },
};

const DATASET_KEYS = ["ecommerce", "finance", "healthcare"] as const;

/* ------------------------------------------------------------------ */
/*  Page component                                                    */
/* ------------------------------------------------------------------ */

export default function DatasetsPage() {
  const [selectedDataset, setSelectedDataset] = useState<string>("ecommerce");
  const [expandedTable, setExpandedTable] = useState<string | null>(null);

  const ds = DATASET_SCHEMAS[selectedDataset];

  function toggleTable(tableName: string) {
    setExpandedTable((prev) => (prev === tableName ? null : tableName));
  }

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Page header */}
      <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
        Dataset Explorer
      </h1>
      <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
        Browse tables, view schemas, and preview sample data for each practice
        dataset.
      </p>

      {/* ---- Dataset tabs ---- */}
      <div className="mt-8 flex gap-2 border-b border-[var(--color-border)]">
        {DATASET_KEYS.map((key) => {
          const d = DATASET_SCHEMAS[key];
          const active = selectedDataset === key;
          return (
            <button
              key={key}
              onClick={() => {
                setSelectedDataset(key);
                setExpandedTable(null);
              }}
              className={`relative px-5 py-2.5 text-sm font-medium transition-colors ${
                active
                  ? "text-[var(--color-accent)]"
                  : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
              }`}
            >
              {d.name}
              {active && (
                <span className="absolute bottom-0 left-0 right-0 h-0.5 rounded-full bg-[var(--color-accent)]" />
              )}
            </button>
          );
        })}
      </div>

      {/* ---- Dataset overview ---- */}
      <div className="mt-6">
        <p className="text-sm leading-relaxed text-[var(--color-text-secondary)]">
          {ds.description}
        </p>

        {/* Stats row */}
        <div className="mt-4 flex flex-wrap gap-6">
          <Stat label="Tables" value={String(ds.tables)} />
          <Stat label="Total Rows" value={ds.totalRows} />
          <Stat
            label="Relationships"
            value={String(ds.relationships.length)}
          />
        </div>
      </div>

      {/* ---- ER Relationship summary ---- */}
      <div className="mt-8">
        <h2 className="text-base font-semibold text-[var(--color-text-primary)]">
          Relationships
        </h2>
        <div className="mt-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
          <ul className="grid grid-cols-1 gap-1.5 sm:grid-cols-2">
            {ds.relationships.map((rel) => (
              <li
                key={rel}
                className="flex items-center gap-2 font-mono text-xs text-[var(--color-text-secondary)]"
              >
                <span className="inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
                {rel}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* ---- Interactive table browser ---- */}
      <div className="mt-8">
        <h2 className="text-base font-semibold text-[var(--color-text-primary)]">
          Tables
        </h2>
        <div className="mt-3 flex flex-col gap-3">
          {ds.schema.map((table) => {
            const isExpanded = expandedTable === table.name;
            return (
              <div
                key={table.name}
                className="overflow-hidden rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] transition-shadow hover:shadow-sm"
              >
                {/* Table header (clickable) */}
                <button
                  onClick={() => toggleTable(table.name)}
                  className="flex w-full items-center justify-between px-4 py-3 text-left"
                >
                  <div className="flex items-center gap-3">
                    <span
                      className={`inline-flex h-5 w-5 items-center justify-center rounded text-xs transition-transform ${
                        isExpanded ? "rotate-90" : ""
                      } bg-[var(--color-accent)]/10 text-[var(--color-accent)]`}
                    >
                      &#9654;
                    </span>
                    <span className="font-mono text-sm font-semibold text-[var(--color-text-primary)]">
                      {table.name}
                    </span>
                  </div>
                  <span className="text-xs text-[var(--color-text-muted)]">
                    {table.columns.length} columns
                    {" / "}
                    {table.sampleRows.length} sample rows
                  </span>
                </button>

                {/* Expanded content */}
                {isExpanded && (
                  <div className="border-t border-[var(--color-border)] px-4 py-4">
                    {/* Column list */}
                    <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                      Columns
                    </h4>
                    <div className="mb-4 flex flex-col gap-1">
                      {table.columns.map((col) => (
                        <div
                          key={col.name}
                          className="flex items-center gap-2 rounded px-2 py-1 font-mono text-xs hover:bg-[var(--color-background)]/50"
                        >
                          <span className="w-20 shrink-0 text-[var(--color-text-primary)]">
                            {col.name}
                          </span>
                          <span className="w-28 shrink-0 text-[var(--color-text-muted)]">
                            {col.type}
                          </span>
                          {col.pk && (
                            <span className="inline-flex items-center rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold uppercase text-amber-700 dark:bg-amber-900/40 dark:text-amber-400">
                              PK
                            </span>
                          )}
                          {col.fk && (
                            <span
                              className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold uppercase text-blue-700 dark:bg-blue-900/40 dark:text-blue-400"
                              title={`References ${col.fk}`}
                            >
                              FK
                              <span className="font-normal normal-case">
                                {col.fk}
                              </span>
                            </span>
                          )}
                        </div>
                      ))}
                    </div>

                    {/* Sample data table */}
                    <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                      Sample Data
                    </h4>
                    <div className="overflow-x-auto rounded border border-[var(--color-border)]">
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="border-b border-[var(--color-border)] bg-[var(--color-background)]">
                            {table.columns.map((col) => (
                              <th
                                key={col.name}
                                className="whitespace-nowrap px-3 py-2 text-left font-mono font-semibold text-[var(--color-text-muted)]"
                              >
                                {col.name}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {table.sampleRows.map((row, ri) => (
                            <tr
                              key={ri}
                              className="border-b border-[var(--color-border)] last:border-0"
                            >
                              {row.map((cell, ci) => (
                                <td
                                  key={ci}
                                  className="whitespace-nowrap px-3 py-1.5 font-mono text-[var(--color-text-secondary)]"
                                >
                                  {cell === null ? (
                                    <span className="italic text-[var(--color-text-muted)]">
                                      NULL
                                    </span>
                                  ) : (
                                    String(cell)
                                  )}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Small helper components                                           */
/* ------------------------------------------------------------------ */

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline gap-2">
      <span className="text-lg font-bold text-[var(--color-text-primary)]">
        {value}
      </span>
      <span className="text-xs text-[var(--color-text-muted)]">{label}</span>
    </div>
  );
}
