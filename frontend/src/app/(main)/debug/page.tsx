"use client";

import { useState, useCallback } from "react";
import { apiClient } from "@/lib/api";

/* ── Types ── */
interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface Challenge {
  id: string;
  title: string;
  dataset: string;
  difficulty: "easy" | "medium" | "hard";
  description: string;
  issueType: string;
  hint: string;
  verifyQuery: string;
  expectedIssueCount: number;
}

/* ── Challenges ── */
const CHALLENGES: Challenge[] = [
  // E-Commerce
  {
    id: "dbg-001",
    title: "Find NULL Email Addresses",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Missing Data",
    description:
      "The marketing team can't send promotional emails to all customers. Some customer records are missing email addresses. Write a query to find all customers with NULL or empty email fields.",
    hint: "Check for both NULL and empty strings — they're different things in SQL.",
    verifyQuery:
      "SELECT COUNT(*) AS issue_count FROM customers WHERE email IS NULL OR email = ''",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-002",
    title: "Detect Duplicate Customer Emails",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Duplicates",
    description:
      "The CRM team noticed some customers share the same email address, which causes login conflicts. Find all email addresses that appear more than once.",
    hint: "GROUP BY the email column and use HAVING to filter for counts > 1.",
    verifyQuery:
      "SELECT email, COUNT(*) AS cnt FROM customers GROUP BY email HAVING COUNT(*) > 1",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-003",
    title: "Orders with Invalid Totals",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Calculation Error",
    description:
      "Finance flagged that some order totals don't match the sum of their line items. Find orders where the total_amount doesn't equal the sum of (quantity × unit_price) from order_items.",
    hint: "JOIN orders with a subquery that sums order_items per order, then compare.",
    verifyQuery:
      "SELECT o.id FROM orders o JOIN (SELECT order_id, SUM(quantity * unit_price) AS calc_total FROM order_items GROUP BY order_id) oi ON o.id = oi.order_id WHERE ABS(o.total_amount - oi.calc_total) > 0.01",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-004",
    title: "Orphaned Order Items",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Referential Integrity",
    description:
      "After a data migration, some order_items reference orders that no longer exist. Find all order items that point to a non-existent order_id.",
    hint: "Use a LEFT JOIN from order_items to orders and look for NULLs.",
    verifyQuery:
      "SELECT oi.id FROM order_items oi LEFT JOIN orders o ON oi.order_id = o.id WHERE o.id IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-005",
    title: "Products with Negative Stock",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Invalid Values",
    description:
      "The warehouse system may have sync issues. Find any products where stock_quantity is negative — this should never happen in a real inventory.",
    hint: "A simple WHERE clause comparing stock_quantity to zero.",
    verifyQuery:
      "SELECT id, name, stock_quantity FROM products WHERE stock_quantity < 0",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-006",
    title: "Orders Before Customer Registration",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Temporal Anomaly",
    description:
      "Some orders appear to have been placed before the customer's account was created. Find all orders where the order_date is earlier than the customer's created_at timestamp.",
    hint: "JOIN orders with customers and compare the two date columns.",
    verifyQuery:
      "SELECT o.id FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.order_date < c.created_at",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-007",
    title: "Reviews Without Purchases",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Business Logic",
    description:
      "The integrity team suspects some reviews were written by people who never purchased the product. Find all reviews where the reviewer (customer_id) never ordered the reviewed product.",
    hint: "Use NOT EXISTS with a subquery that checks order_items for that customer and product combination.",
    verifyQuery:
      "SELECT r.id FROM reviews r WHERE NOT EXISTS (SELECT 1 FROM orders o JOIN order_items oi ON o.id = oi.order_id WHERE o.customer_id = r.customer_id AND oi.product_id = r.product_id)",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-008",
    title: "Price Higher Than Cost Sanity Check",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Business Logic",
    description:
      "Some products may have been entered with the cost higher than the selling price, resulting in guaranteed losses. Find products where cost exceeds price.",
    hint: "Compare the cost and price columns directly.",
    verifyQuery:
      "SELECT id, name, price, cost FROM products WHERE cost > price",
    expectedIssueCount: 0,
  },

  // Finance
  {
    id: "dbg-009",
    title: "Accounts with Negative Balances",
    dataset: "finance",
    difficulty: "easy",
    issueType: "Invalid Values",
    description:
      "Checking accounts should never have negative balances (overdraft protection is separate). Find all checking accounts with a balance below zero.",
    hint: "Filter by account_type and check balance < 0.",
    verifyQuery:
      "SELECT id, balance FROM accounts WHERE account_type = 'checking' AND balance < 0",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-010",
    title: "Transactions with Wrong Running Balance",
    dataset: "finance",
    difficulty: "hard",
    issueType: "Calculation Error",
    description:
      "The balance_after field in transactions should reflect the account balance after each transaction. Some records have incorrect balance_after values. Find transactions where the balance_after doesn't match the expected value.",
    hint: "Use a window function to compute the running balance, then compare with the stored balance_after.",
    verifyQuery:
      "SELECT id FROM transactions WHERE balance_after != (SELECT SUM(CASE WHEN type = 'deposit' THEN amount ELSE -amount END) FROM transactions t2 WHERE t2.account_id = transactions.account_id AND t2.id <= transactions.id)",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-011",
    title: "Customers with Duplicate Emails",
    dataset: "finance",
    difficulty: "easy",
    issueType: "Duplicates",
    description:
      "Bank compliance requires unique customer identifiers. Find customer email addresses that appear more than once in the system.",
    hint: "GROUP BY email and use HAVING to find duplicates.",
    verifyQuery:
      "SELECT email, COUNT(*) AS cnt FROM customers GROUP BY email HAVING COUNT(*) > 1",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-012",
    title: "Expired Active Cards",
    dataset: "finance",
    difficulty: "medium",
    issueType: "Stale Data",
    description:
      "Some cards are still marked as 'active' but have an expiry_date in the past. Find all cards that should have been deactivated.",
    hint: "Compare expiry_date to the current date and filter by status.",
    verifyQuery:
      "SELECT id, card_number, expiry_date FROM cards WHERE status = 'active' AND expiry_date < DATE('now')",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-013",
    title: "Loan Payments Exceeding Balance",
    dataset: "finance",
    difficulty: "medium",
    issueType: "Business Logic",
    description:
      "Some loan payment totals exceed the original loan amount. Find loans where the sum of payments is greater than the loan amount.",
    hint: "JOIN loans with aggregated payments and compare totals.",
    verifyQuery:
      "SELECT l.id, l.amount, SUM(p.amount) AS total_paid FROM loans l JOIN payments p ON l.id = p.loan_id GROUP BY l.id HAVING SUM(p.amount) > l.amount",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-014",
    title: "Missing Customer Phone Numbers",
    dataset: "finance",
    difficulty: "easy",
    issueType: "Missing Data",
    description:
      "The compliance team needs to reach all customers by phone. Find customers with missing (NULL) phone numbers.",
    hint: "A simple IS NULL check on the phone column.",
    verifyQuery:
      "SELECT id, first_name, last_name FROM customers WHERE phone IS NULL",
    expectedIssueCount: 0,
  },

  // Healthcare
  {
    id: "dbg-015",
    title: "Patients with Missing Phone Numbers",
    dataset: "healthcare",
    difficulty: "easy",
    issueType: "Missing Data",
    description:
      "Emergency contact requires phone numbers. Find all patients with NULL phone fields.",
    hint: "Filter patients where phone IS NULL.",
    verifyQuery:
      "SELECT id, first_name, last_name FROM patients WHERE phone IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-016",
    title: "Duplicate Patient Emails",
    dataset: "healthcare",
    difficulty: "easy",
    issueType: "Duplicates",
    description:
      "The patient portal requires unique emails. Find email addresses shared by multiple patients.",
    hint: "GROUP BY email with HAVING COUNT(*) > 1.",
    verifyQuery:
      "SELECT email, COUNT(*) AS cnt FROM patients GROUP BY email HAVING COUNT(*) > 1",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-017",
    title: "Unpaid Overdue Bills",
    dataset: "healthcare",
    difficulty: "medium",
    issueType: "Stale Data",
    description:
      "The billing department needs to follow up on bills that are still 'pending' but were created more than 90 days ago and have no paid_at date. Find these overdue records.",
    hint: "Filter billing records by status, paid_at IS NULL, and a date calculation.",
    verifyQuery:
      "SELECT id, amount, created_at FROM billing WHERE status = 'pending' AND paid_at IS NULL AND DATE(created_at, '+90 days') < DATE('now')",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-018",
    title: "Visits Without a Doctor Assignment",
    dataset: "healthcare",
    difficulty: "easy",
    issueType: "Missing Data",
    description:
      "Every visit should have a doctor assigned. Find any visits where doctor_id is NULL.",
    hint: "Check the doctor_id column for NULL values.",
    verifyQuery:
      "SELECT id, patient_id, visit_date FROM visits WHERE doctor_id IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-019",
    title: "Lab Results for Non-Existent Visits",
    dataset: "healthcare",
    difficulty: "medium",
    issueType: "Referential Integrity",
    description:
      "After a database cleanup, some lab results may reference visits that were deleted. Find orphaned lab results.",
    hint: "LEFT JOIN lab_results with visits and look for NULL visit IDs.",
    verifyQuery:
      "SELECT lr.id FROM lab_results lr LEFT JOIN visits v ON lr.visit_id = v.id WHERE v.id IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-020",
    title: "Abnormal Lab Results Without Follow-Up Visit",
    dataset: "healthcare",
    difficulty: "hard",
    issueType: "Business Logic",
    description:
      "Patients with abnormal lab results should have a follow-up visit scheduled within 30 days. Find abnormal results where the patient has no subsequent visit after the lab result date.",
    hint: "Join lab_results with visits, checking for a later visit by the same patient within 30 days.",
    verifyQuery:
      "SELECT lr.id FROM lab_results lr JOIN visits v ON lr.visit_id = v.id WHERE lr.is_abnormal = 1 AND NOT EXISTS (SELECT 1 FROM visits v2 WHERE v2.patient_id = v.patient_id AND v2.visit_date > v.visit_date AND DATE(v2.visit_date) <= DATE(v.visit_date, '+30 days'))",
    expectedIssueCount: 0,
  },

  // ── Wrong Join Diagnosis ──
  {
    id: "dbg-021",
    title: "Inflated Revenue from Duplicate Joins",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Wrong Join",
    description:
      "A dashboard shows total revenue of $2.3M, but the CFO says it should be around $1.1M. The analyst used this query:\n\nSELECT SUM(oi.quantity * oi.unit_price) AS total_revenue\nFROM orders o\nJOIN order_items oi ON o.id = oi.order_id\nJOIN payments p ON o.id = p.order_id\n\nThe payments table has multiple rows per order (partial payments). Write a query to prove this causes row duplication and find the correct total revenue.",
    hint: "When you JOIN orders→order_items→payments, each payment row duplicates all order_items. First find orders with multiple payments, then compute revenue without the payments join.",
    verifyQuery:
      "SELECT SUM(quantity * unit_price) AS correct_revenue FROM order_items",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-022",
    title: "Patients Counted Multiple Times",
    dataset: "healthcare",
    difficulty: "medium",
    issueType: "Wrong Join",
    description:
      "A report claims the hospital treated 5,000 unique patients last year. But the actual patient count is much lower. The analyst used:\n\nSELECT COUNT(p.id) FROM patients p JOIN visits v ON p.id = v.patient_id\n\nExplain why the count is wrong and write the correct query to count unique patients who had at least one visit.",
    hint: "COUNT(p.id) counts every row after the JOIN — patients with multiple visits are counted multiple times. Use COUNT(DISTINCT p.id) instead.",
    verifyQuery:
      "SELECT COUNT(DISTINCT p.id) AS unique_patients FROM patients p JOIN visits v ON p.id = v.patient_id",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-023",
    title: "Transaction Amounts Doubled by Card Join",
    dataset: "finance",
    difficulty: "hard",
    issueType: "Wrong Join",
    description:
      "An analyst reports that total deposits are unexpectedly high. Their query joins transactions with cards through accounts, but some accounts have multiple cards. Write a query to identify accounts where the card join causes transaction amount inflation, and find the true total deposits.",
    hint: "If an account has 2 cards and 3 deposits, a JOIN through cards yields 6 rows instead of 3. Find accounts with multiple cards, then compute deposits without the cards join.",
    verifyQuery:
      "SELECT SUM(amount) AS correct_deposits FROM transactions WHERE type = 'deposit'",
    expectedIssueCount: 0,
  },

  // ── Data Pipeline Gaps ──
  {
    id: "dbg-024",
    title: "Missing Dates in Daily Orders",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Pipeline Gap",
    description:
      "The data pipeline should produce an order record for every day. Business analysts noticed gaps in their daily revenue chart. Write a query to find dates that have zero orders but fall between the earliest and latest order dates. (Hint: You can generate a date series using recursive CTEs.)",
    hint: "Use a recursive CTE to generate all dates between MIN(order_date) and MAX(order_date), then LEFT JOIN with orders grouped by date to find missing ones.",
    verifyQuery:
      "WITH RECURSIVE dates AS (SELECT MIN(DATE(order_date)) AS d FROM orders UNION ALL SELECT DATE(d, '+1 day') FROM dates WHERE d < (SELECT MAX(DATE(order_date)) FROM orders)), daily AS (SELECT DATE(order_date) AS d, COUNT(*) AS cnt FROM orders GROUP BY DATE(order_date)) SELECT dates.d FROM dates LEFT JOIN daily ON dates.d = daily.d WHERE daily.d IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-025",
    title: "Missing Monthly Billing Periods",
    dataset: "healthcare",
    difficulty: "medium",
    issueType: "Pipeline Gap",
    description:
      "The finance team expects billing records every month. Find months (YYYY-MM format) between the earliest and latest billing dates that have no billing records at all.",
    hint: "Generate a series of year-month values using a recursive CTE, then LEFT JOIN with aggregated billing data to find gaps.",
    verifyQuery:
      "WITH RECURSIVE months AS (SELECT STRFTIME('%Y-%m', MIN(billed_at)) AS m FROM billing UNION ALL SELECT STRFTIME('%Y-%m', DATE(m || '-01', '+1 month')) FROM months WHERE m < (SELECT STRFTIME('%Y-%m', MAX(billed_at)) FROM billing)), actual AS (SELECT STRFTIME('%Y-%m', billed_at) AS m FROM billing GROUP BY 1) SELECT months.m FROM months LEFT JOIN actual ON months.m = actual.m WHERE actual.m IS NULL",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-026",
    title: "Gaps in Transaction Sequence",
    dataset: "finance",
    difficulty: "hard",
    issueType: "Pipeline Gap",
    description:
      "Each account should have transactions with sequential reference_numbers. Find accounts that have gaps in their transaction IDs — meaning some transactions may have been lost during a data migration.",
    hint: "Use LAG() or LEAD() window functions over the transaction IDs per account to detect where the difference between consecutive IDs is more than 1.",
    verifyQuery:
      "SELECT account_id, id AS current_id, LAG(id) OVER (PARTITION BY account_id ORDER BY id) AS prev_id FROM transactions",
    expectedIssueCount: 0,
  },

  // ── Broken Dashboard Investigation ──
  {
    id: "dbg-027",
    title: "Dashboard Shows Wrong Average Order Value",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Broken Dashboard",
    description:
      "The executive dashboard shows an Average Order Value (AOV) of $250, but manual spot-checks suggest it should be around $85. The dashboard query is:\n\nSELECT AVG(total_amount) FROM orders\n\nInvestigate: Are there cancelled/returned orders inflating the average? Are there outlier orders? Write queries to find the root cause and the correct AOV for 'delivered' orders only.",
    hint: "Check the distribution of orders by status. Cancelled orders with high totals or test orders may be inflating the average. Filter to only completed/delivered orders.",
    verifyQuery:
      "SELECT status, COUNT(*) AS cnt, ROUND(AVG(total_amount), 2) AS avg_amount FROM orders GROUP BY status ORDER BY avg_amount DESC",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-028",
    title: "Department Revenue Report is Incorrect",
    dataset: "healthcare",
    difficulty: "hard",
    issueType: "Broken Dashboard",
    description:
      "The hospital CFO says the Cardiology department revenue looks too high on the dashboard. The dashboard joins billing → visits → doctors → departments. Investigate whether: (1) some visits have multiple billing records, (2) doctors are assigned to the wrong department, or (3) there's a data quality issue. Write queries to diagnose the root cause.",
    hint: "Check for duplicate billing per visit (GROUP BY visit_id HAVING COUNT > 1). Also check if any doctor's department_id doesn't match where they should be. Compare SUM with and without deduplication.",
    verifyQuery:
      "SELECT v.id AS visit_id, COUNT(b.id) AS bill_count, SUM(b.amount) AS total_billed FROM visits v JOIN billing b ON v.id = b.visit_id GROUP BY v.id HAVING COUNT(b.id) > 1",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-029",
    title: "Customer Churn Rate Seems Too High",
    dataset: "finance",
    difficulty: "hard",
    issueType: "Broken Dashboard",
    description:
      "The dashboard shows a 75% customer churn rate, but the business team says retention is healthy. The churn query counts customers with no transactions in the last 90 days vs total customers. Investigate: Are closed/frozen accounts being included? Are there customers who only have savings accounts (lower transaction frequency)? Write queries to find the correct active customer churn rate.",
    hint: "Filter to only active accounts first. Then check if account_type matters — savings accounts may naturally have fewer transactions. Compute churn only for checking account holders.",
    verifyQuery:
      "SELECT a.account_type, COUNT(DISTINCT a.customer_id) AS total_customers, COUNT(DISTINCT CASE WHEN t.id IS NOT NULL THEN a.customer_id END) AS active_customers FROM accounts a LEFT JOIN transactions t ON a.id = t.account_id AND DATE(t.transaction_date) >= DATE('now', '-90 days') WHERE a.status = 'active' GROUP BY a.account_type",
    expectedIssueCount: 0,
  },
  {
    id: "dbg-030",
    title: "Product Category Performance Mismatch",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Broken Dashboard",
    description:
      "The product team's dashboard shows 'Electronics' as the #1 category by revenue, but the sales team says 'Clothing' should be #1. The dashboard uses:\n\nSELECT c.name, SUM(oi.quantity * oi.unit_price) AS revenue FROM categories c JOIN products p ON c.id = p.category_id JOIN order_items oi ON p.id = oi.product_id GROUP BY c.name ORDER BY revenue DESC\n\nInvestigate if cancelled/returned orders are included, and whether discounts are being applied. Write the corrected query.",
    hint: "The dashboard doesn't filter out cancelled/returned orders, and doesn't account for the discount column in order_items. Apply both filters for correct results.",
    verifyQuery:
      "SELECT c.name, SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS net_revenue FROM categories c JOIN products p ON c.id = p.category_id JOIN order_items oi ON p.id = oi.product_id JOIN orders o ON oi.order_id = o.id WHERE o.status NOT IN ('cancelled', 'returned') GROUP BY c.name ORDER BY net_revenue DESC",
    expectedIssueCount: 0,
  },
];

/* ── Difficulty colors ── */
const difficultyColor = {
  easy: "bg-green-500/20 text-green-400 border-green-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  hard: "bg-red-500/20 text-red-400 border-red-500/30",
};

const issueTypeColor: Record<string, string> = {
  "Missing Data": "bg-purple-500/20 text-purple-400",
  Duplicates: "bg-orange-500/20 text-orange-400",
  "Calculation Error": "bg-red-500/20 text-red-400",
  "Referential Integrity": "bg-blue-500/20 text-blue-400",
  "Invalid Values": "bg-pink-500/20 text-pink-400",
  "Temporal Anomaly": "bg-cyan-500/20 text-cyan-400",
  "Business Logic": "bg-emerald-500/20 text-emerald-400",
  "Stale Data": "bg-amber-500/20 text-amber-400",
  "Wrong Join": "bg-orange-500/10 text-orange-400",
  "Pipeline Gap": "bg-purple-500/10 text-purple-400",
  "Broken Dashboard": "bg-pink-500/10 text-pink-400",
};

const datasetLabel: Record<string, string> = {
  ecommerce: "E-Commerce",
  finance: "Finance",
  healthcare: "Healthcare",
};

export default function DebugPage() {
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(
    null
  );
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [filterDataset, setFilterDataset] = useState<string>("all");
  const [filterType, setFilterType] = useState<string>("all");

  const filteredChallenges = CHALLENGES.filter((c) => {
    if (filterDataset !== "all" && c.dataset !== filterDataset) return false;
    if (filterType !== "all" && c.issueType !== filterType) return false;
    return true;
  });

  const issueTypes = [...new Set(CHALLENGES.map((c) => c.issueType))];

  const handleRun = useCallback(async () => {
    if (!selectedChallenge || !query.trim()) return;
    setRunning(true);
    setError(null);
    setResult(null);

    try {
      const data = await apiClient<{
        user_result: QueryResult;
        status: string;
        error?: string;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({
          query: query.trim(),
          dataset: selectedChallenge.dataset,
        }),
      });

      if (data.error) {
        setError(data.error);
      } else if (data.user_result) {
        // Normalize snake_case from API to camelCase
        setResult({
          columns: data.user_result.columns,
          rows: data.user_result.rows,
          rowCount: (data.user_result as any).row_count ?? data.user_result.rowCount ?? 0,
          executionTimeMs: (data.user_result as any).execution_time_ms ?? data.user_result.executionTimeMs ?? 0,
        });
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Query execution failed");
    } finally {
      setRunning(false);
    }
  }, [query, selectedChallenge]);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Data Debugging
        </h1>
        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
          Real databases have messy data. Find NULL values, duplicates,
          referential integrity violations, and business logic errors using SQL.
        </p>
      </div>

      {!selectedChallenge ? (
        /* ── Challenge List ── */
        <div>
          {/* Filters */}
          <div className="mb-6 flex gap-3">
            <select
              value={filterDataset}
              onChange={(e) => setFilterDataset(e.target.value)}
              aria-label="Filter by dataset"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Datasets</option>
              <option value="ecommerce">E-Commerce</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
            </select>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              aria-label="Filter by issue type"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Issue Types</option>
              {issueTypes.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>

          {/* Grid */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filteredChallenges.map((c) => (
              <button
                key={c.id}
                onClick={() => {
                  setSelectedChallenge(c);
                  setQuery("");
                  setResult(null);
                  setError(null);
                  setShowHint(false);
                }}
                aria-label={`${c.title} - ${c.difficulty} difficulty, ${c.issueType}`}
                className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-left transition-all hover:border-[var(--color-accent)]/50 hover:shadow-lg"
              >
                <div className="mb-2 flex items-center gap-2">
                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${
                      difficultyColor[c.difficulty]
                    }`}
                  >
                    {c.difficulty}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${
                      issueTypeColor[c.issueType] || "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {c.issueType}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                  {c.title}
                </h3>
                <p className="mt-1 line-clamp-2 text-xs text-[var(--color-text-muted)]">
                  {c.description}
                </p>
                <div className="mt-3 text-[10px] text-[var(--color-text-muted)]">
                  {datasetLabel[c.dataset]}
                </div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        /* ── Challenge Detail ── */
        <div>
          {/* Back button */}
          <button
            onClick={() => {
              setSelectedChallenge(null);
              setResult(null);
              setError(null);
            }}
            aria-label="Back to challenge list"
            className="mb-4 text-xs font-medium text-[var(--color-accent)] hover:underline"
          >
            ← Back to challenges
          </button>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Left: Problem + Editor */}
            <div className="space-y-4">
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
                <div className="mb-3 flex items-center gap-2">
                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${
                      difficultyColor[selectedChallenge.difficulty]
                    }`}
                  >
                    {selectedChallenge.difficulty}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${
                      issueTypeColor[selectedChallenge.issueType] ||
                      "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {selectedChallenge.issueType}
                  </span>
                  <span className="text-[10px] text-[var(--color-text-muted)]">
                    {datasetLabel[selectedChallenge.dataset]}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-[var(--color-text-primary)]">
                  {selectedChallenge.title}
                </h2>
                <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                  {selectedChallenge.description}
                </p>

                {/* Hint */}
                <div className="mt-4">
                  {showHint ? (
                    <div className="rounded-md bg-[var(--color-background)] p-3 text-xs text-[var(--color-text-secondary)]">
                      <span className="font-medium text-[var(--color-accent)]">
                        Hint:
                      </span>{" "}
                      {selectedChallenge.hint}
                    </div>
                  ) : (
                    <button
                      onClick={() => setShowHint(true)}
                      aria-label="Show hint for this challenge"
                      className="text-xs font-medium text-[var(--color-accent)] hover:underline"
                    >
                      Show hint
                    </button>
                  )}
                </div>
              </div>

              {/* SQL Editor */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
                <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
                  <span className="text-[10px] font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                    SQL Query
                  </span>
                  <button
                    onClick={handleRun}
                    disabled={running || !query.trim()}
                    aria-label="Run SQL query"
                    className="rounded-md bg-[var(--color-accent)] px-3 py-1 text-xs font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
                  >
                    {running ? "Running..." : "▶ Run"}
                  </button>
                </div>
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                      handleRun();
                    }
                  }}
                  placeholder="Write your SQL query to find the data issues..."
                  className="h-40 w-full resize-none bg-transparent p-4 font-mono text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none"
                  spellCheck={false}
                />
              </div>
            </div>

            {/* Right: Results */}
            <div className="space-y-4" role="status" aria-live="polite">
              {/* Error */}
              {error && (
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4">
                  <h3 className="text-xs font-medium text-red-400">Error</h3>
                  <p className="mt-1 font-mono text-xs text-red-300">
                    {error}
                  </p>
                </div>
              )}

              {/* Results table */}
              {result && (
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
                  <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
                    <span className="text-xs font-medium text-[var(--color-text-primary)]">
                      Results
                    </span>
                    <span className="text-[10px] text-[var(--color-text-muted)]">
                      {result.rowCount} row{result.rowCount !== 1 ? "s" : ""} •{" "}
                      {result.executionTimeMs}ms
                    </span>
                  </div>

                  {result.rowCount === 0 ? (
                    <div className="p-8 text-center">
                      <div className="text-2xl">✅</div>
                      <p className="mt-2 text-sm font-medium text-green-400">
                        No issues found
                      </p>
                      <p className="mt-1 text-xs text-[var(--color-text-muted)]">
                        Your query returned 0 rows — the data looks clean for
                        this check.
                      </p>
                    </div>
                  ) : (
                    <div className="max-h-96 overflow-auto">
                      <table className="w-full text-xs">
                        <thead className="sticky top-0 bg-[var(--color-surface)]">
                          <tr className="border-b border-[var(--color-border)]">
                            {result.columns.map((col) => (
                              <th
                                key={col}
                                className="px-3 py-2 text-left font-medium text-[var(--color-text-muted)]"
                              >
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {result.rows.map((row, i) => (
                            <tr
                              key={i}
                              className="border-b border-[var(--color-border)]/50 hover:bg-[var(--color-background)]"
                            >
                              {row.map((cell, j) => (
                                <td
                                  key={j}
                                  className={`px-3 py-1.5 font-mono ${
                                    cell === null
                                      ? "italic text-[var(--color-text-muted)]"
                                      : "text-[var(--color-text-secondary)]"
                                  }`}
                                >
                                  {cell === null ? "NULL" : String(cell)}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}

              {/* Idle state */}
              {!result && !error && (
                <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-[var(--color-border)] bg-[var(--color-surface)]">
                  <div className="text-center">
                    <div className="text-3xl opacity-30">🔍</div>
                    <p className="mt-2 text-sm text-[var(--color-text-muted)]">
                      Write a query to investigate the data issue
                    </p>
                    <p className="mt-1 text-[10px] text-[var(--color-text-muted)]">
                      Ctrl+Enter to run
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
