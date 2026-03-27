"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { apiClient } from "@/lib/api";

/* ── Types ── */
interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface QueryLog {
  query: string;
  result: QueryResult | null;
  error: string | null;
  timestamp: number;
}

interface Hint {
  label: string;
  text: string;
}

interface Step {
  title: string;
  description: string;
}

interface Investigation {
  id: string;
  title: string;
  dataset: string;
  difficulty: "easy" | "medium" | "hard";
  context: string;
  tables: string[];
  task: string;
  steps: Step[];
  hints: Hint[];
  rootCause: string;
  fix: string;
  learnings: string[];
  issueType: string;
}

/* ── Investigation Problems ── */
const INVESTIGATIONS: Investigation[] = [
  {
    id: "inv-001",
    title: "Revenue is 30% Higher Than Expected",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Duplicate Data",
    context:
      "The finance team runs a monthly revenue report. This month, the dashboard shows revenue is 30% higher than the sales team's manual tracking. The CFO needs this resolved before the board meeting tomorrow.",
    tables: ["orders", "order_items", "payments"],
    task: "Investigate why revenue is inflated. Find the root cause and write a query that shows the correct revenue.",
    steps: [
      {
        title: "Explore the data",
        description:
          "Start by checking total revenue. Query the orders table to see what the dashboard might be computing.",
      },
      {
        title: "Find the anomaly",
        description:
          "Compare order counts vs payment counts. Are there duplicate records? Check if any order_id appears more than once.",
      },
      {
        title: "Identify root cause",
        description:
          "Write a query that shows the duplicate records and quantifies the impact on revenue.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Check if any order_id appears in the payments table more than once." },
      { label: "Hint 2", text: "Try: SELECT order_id, COUNT(*) FROM payments GROUP BY order_id HAVING COUNT(*) > 1" },
      { label: "Hint 3", text: "Calculate revenue with and without deduplication: compare SUM(amount) vs SUM of DISTINCT order amounts." },
    ],
    rootCause:
      "Duplicate payment records exist — some orders have multiple payment entries (e.g., failed + successful retry), inflating the SUM(amount) calculation.",
    fix: "Use DISTINCT on order_id when summing revenue, or filter payments to only status = 'completed'. The correct query should deduplicate before aggregating.",
    learnings: [
      "Always check for duplicates before aggregating",
      "GROUP BY + HAVING COUNT(*) > 1 is your best friend for finding dupes",
      "Payment retries often create duplicate records in production systems",
    ],
  },
  {
    id: "inv-002",
    title: "Yesterday's Orders Are Missing",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Pipeline Gap",
    context:
      "The operations team notices the daily orders dashboard shows zero orders for yesterday, but the warehouse shipped 150 packages. The ETL pipeline runs at midnight UTC every day.",
    tables: ["orders", "customers"],
    task: "Investigate why yesterday's data is missing. Determine if it's a real gap or a date/timezone issue.",
    steps: [
      {
        title: "Check the date range",
        description:
          "Query the most recent orders. What's the latest created_at timestamp in the orders table?",
      },
      {
        title: "Look for gaps",
        description:
          "Generate a date series and find which dates have no orders. Are there gaps before yesterday too?",
      },
      {
        title: "Quantify the impact",
        description:
          "Count orders per day for the last 7 days. Show exactly which dates are missing or undercounted.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Start with: SELECT DATE(created_at) AS day, COUNT(*) FROM orders GROUP BY day ORDER BY day DESC LIMIT 10" },
      { label: "Hint 2", text: "Check if there are orders with future dates or incorrect timestamps." },
      { label: "Hint 3", text: "Look at the MAX(created_at) — the pipeline may have stopped ingesting data at a specific point." },
    ],
    rootCause:
      "The data pipeline stopped ingesting after a certain date. The MAX(created_at) reveals the last successful load, showing a gap between that date and today.",
    fix: "Identify when the pipeline broke by finding the last ingested timestamp. Alert the data engineering team to backfill missing dates. Add pipeline monitoring to detect ingestion gaps automatically.",
    learnings: [
      "Always check MAX(date) to detect pipeline freshness",
      "Date gaps in time-series data usually indicate ETL failures",
      "Daily aggregations hide intra-day pipeline breaks",
    ],
  },
  {
    id: "inv-003",
    title: "Revenue Doubled After a JOIN",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Join Explosion",
    context:
      "A junior analyst added a JOIN to the revenue query to include product categories. Before the change, total revenue was $500K. After adding the JOIN, it shows $1.1M. The query looks correct syntactically. The analyst is confused.",
    tables: ["orders", "order_items", "products", "categories"],
    task: "Find why the JOIN is causing revenue to double. Demonstrate the row multiplication problem.",
    steps: [
      {
        title: "Compare before and after",
        description:
          "Run the simple revenue query (SUM of order totals), then run it with the JOIN. Compare the numbers.",
      },
      {
        title: "Find the multiplication",
        description:
          "Check if any order has multiple items. When you JOIN orders to order_items, one order row becomes many rows.",
      },
      {
        title: "Show the fix",
        description:
          "Write the correct query that gets revenue by category without double-counting order amounts.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Count rows: SELECT COUNT(*) FROM orders vs SELECT COUNT(*) FROM orders JOIN order_items ON orders.id = order_items.order_id" },
      { label: "Hint 2", text: "The issue is one-to-many: each order has multiple order_items, so the order's total_amount gets counted once per item." },
      { label: "Hint 3", text: "Fix: aggregate at the order_items level (SUM of quantity * unit_price), not at the orders level (SUM of total_amount after JOIN)." },
    ],
    rootCause:
      "One-to-many JOIN explosion: each order has multiple order_items. When you JOIN orders to order_items and SUM(orders.total_amount), each order's total gets counted once per item row, inflating the result.",
    fix: "Either aggregate revenue from order_items directly (SUM of quantity * unit_price), or use a subquery to get distinct order totals before joining.",
    learnings: [
      "JOINs can multiply rows — always check COUNT before and after",
      "One-to-many JOINs are the #1 cause of inflated metrics",
      "When in doubt, aggregate first, then JOIN",
    ],
  },
  {
    id: "inv-004",
    title: "Total Revenue is Lower Than Expected",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "NULL Handling",
    context:
      "The monthly revenue report shows $180K, but the sales team manually counted $210K from their deal tracker. The finance team says the SQL query is simple: SELECT SUM(total_amount) FROM orders. So where's the missing $30K?",
    tables: ["orders"],
    task: "Find why SUM(total_amount) is returning a lower number than expected. Identify the rows affecting the calculation.",
    steps: [
      {
        title: "Check for NULLs",
        description:
          "Count how many orders have NULL total_amount. SUM() silently skips NULL values.",
      },
      {
        title: "Quantify the gap",
        description:
          "Find the orders with NULL amounts. Cross-reference with other columns — do these look like real orders?",
      },
      {
        title: "Show the impact",
        description:
          "Compare COUNT(*) vs COUNT(total_amount) to show how many rows are being excluded from the SUM.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "SUM() ignores NULLs silently — it doesn't error, it just skips them." },
      { label: "Hint 2", text: "Try: SELECT COUNT(*) AS total_orders, COUNT(total_amount) AS orders_with_amount FROM orders" },
      { label: "Hint 3", text: "Find the NULLs: SELECT * FROM orders WHERE total_amount IS NULL" },
    ],
    rootCause:
      "Several orders have NULL total_amount values. SQL's SUM() silently skips NULL rows without warning, so those orders are excluded from the revenue calculation.",
    fix: "Investigate why total_amount is NULL (data entry issue? pending orders?) and either fix the source data or use COALESCE(total_amount, 0) to include them as zero.",
    learnings: [
      "SUM() skips NULLs silently — this is one of the most common data bugs",
      "Always compare COUNT(*) vs COUNT(column) to detect NULLs",
      "COALESCE is your safety net for NULL values in aggregations",
    ],
  },
  {
    id: "inv-005",
    title: "Average Order Value is Wrong",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Aggregation Error",
    context:
      "The analytics dashboard shows the average order value (AOV) is $45. The product team says this seems too low — they expect around $85 based on pricing. The query is: SELECT AVG(total_amount) FROM orders. It runs without errors.",
    tables: ["orders", "order_items"],
    task: "Investigate why the average is so low. Find what's pulling the average down.",
    steps: [
      {
        title: "Check the distribution",
        description:
          "Look at the distribution of order amounts. Are there outliers or suspicious values pulling the average down?",
      },
      {
        title: "Find the culprits",
        description:
          "Look for orders with $0 or very low amounts. Are these test orders, cancelled orders, or free samples?",
      },
      {
        title: "Calculate the corrected AOV",
        description:
          "Write a query that excludes invalid orders (cancelled, $0, test orders) and shows the real AOV.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Check: SELECT MIN(total_amount), MAX(total_amount), AVG(total_amount) FROM orders" },
      { label: "Hint 2", text: "Look for orders with amount = 0 or status in ('cancelled', 'test', 'refunded')." },
      { label: "Hint 3", text: "Try: SELECT status, COUNT(*), AVG(total_amount) FROM orders GROUP BY status — see if cancelled/test orders skew the average." },
    ],
    rootCause:
      "The AVG includes cancelled orders ($0 amount) and test orders. These zero-value records drag the average down significantly. The query doesn't filter by order status.",
    fix: "Filter to only completed/valid orders: SELECT AVG(total_amount) FROM orders WHERE status = 'completed' AND total_amount > 0",
    learnings: [
      "AVG is easily skewed by outliers and zero-value records",
      "Always check the distribution before trusting an average",
      "Filter by status — cancelled and test orders should be excluded from metrics",
    ],
  },
  {
    id: "inv-006",
    title: "Daily Active Users Seems Inflated",
    dataset: "ecommerce",
    difficulty: "medium",
    issueType: "Duplicate Counting",
    context:
      "The growth team reports 5,000 DAU (Daily Active Users) but the product team says they only have 2,000 registered users. The DAU query counts rows in the activity log: SELECT COUNT(customer_id) FROM orders WHERE DATE(created_at) = CURRENT_DATE.",
    tables: ["orders", "customers"],
    task: "Investigate why DAU is higher than total users. Find the counting error.",
    steps: [
      {
        title: "Understand the gap",
        description:
          "Compare total customers vs the DAU number. Check if COUNT is counting correctly.",
      },
      {
        title: "Find duplicates",
        description:
          "Check if customers have multiple orders on the same day. COUNT without DISTINCT counts every row.",
      },
      {
        title: "Show the fix",
        description:
          "Demonstrate the difference between COUNT(customer_id) and COUNT(DISTINCT customer_id).",
      },
    ],
    hints: [
      { label: "Hint 1", text: "COUNT(customer_id) counts every row, including duplicates. COUNT(DISTINCT customer_id) counts unique users." },
      { label: "Hint 2", text: "Check: SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id HAVING COUNT(*) > 1" },
      { label: "Hint 3", text: "Compare: SELECT COUNT(customer_id) AS with_dupes, COUNT(DISTINCT customer_id) AS unique_users FROM orders" },
    ],
    rootCause:
      "The query uses COUNT(customer_id) instead of COUNT(DISTINCT customer_id). Users who place multiple orders in a day are counted multiple times, inflating the DAU metric.",
    fix: "Use COUNT(DISTINCT customer_id) to count unique users. This is one of the most common analytics mistakes.",
    learnings: [
      "COUNT vs COUNT(DISTINCT) is a critical difference in analytics",
      "Always ask: am I counting events or unique entities?",
      "DAU, MAU, and user metrics always need DISTINCT",
    ],
  },
  {
    id: "inv-007",
    title: "Daily Metrics Shift Every Day",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Timezone Bug",
    context:
      "The daily revenue report runs at 9 AM EST. Every morning, yesterday's numbers change slightly from what was reported the evening before. The team in the London office sees different daily totals than the NYC team. The query groups by DATE(created_at).",
    tables: ["orders"],
    task: "Investigate the timezone inconsistency. Show how the same data produces different daily totals depending on timezone interpretation.",
    steps: [
      {
        title: "Check timestamp format",
        description:
          "Examine raw created_at values. Are they in UTC? Do they have timezone info?",
      },
      {
        title: "Find the boundary issue",
        description:
          "Look at orders near midnight UTC. Show how DATE() in different timezones assigns them to different days.",
      },
      {
        title: "Quantify the drift",
        description:
          "Compare daily revenue grouped by UTC date vs a timezone-adjusted date. Show the discrepancy.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Check orders near midnight: SELECT * FROM orders WHERE EXTRACT(HOUR FROM created_at) >= 22 OR EXTRACT(HOUR FROM created_at) <= 2" },
      { label: "Hint 2", text: "Timestamps stored without timezone info are ambiguous — DATE() uses the server's timezone." },
      { label: "Hint 3", text: "Compare: SELECT DATE(created_at) AS utc_day, DATE(created_at - INTERVAL '5 hours') AS est_day, total_amount FROM orders WHERE EXTRACT(HOUR FROM created_at) BETWEEN 0 AND 5" },
    ],
    rootCause:
      "Timestamps are stored in UTC but DATE(created_at) is used without timezone conversion. Orders placed between midnight UTC and 5 AM UTC (i.e., 7-12 PM EST the previous day) get assigned to different dates depending on the viewer's timezone.",
    fix: "Always convert to a consistent timezone before extracting dates: DATE(created_at AT TIME ZONE 'America/New_York'). Or store timestamps with timezone info.",
    learnings: [
      "Timezone bugs are silent — queries run fine but produce wrong results",
      "Always convert to business timezone before DATE extraction",
      "Orders near midnight are the canary for timezone issues",
    ],
  },
  {
    id: "inv-008",
    title: "Data Pipeline Stopped Loading",
    dataset: "finance",
    difficulty: "medium",
    issueType: "Pipeline Failure",
    context:
      "The fraud detection dashboard stopped flagging suspicious transactions 3 days ago. The data team says 'the pipeline is green' but the fraud analyst sees no new data. Transactions should be loaded every hour.",
    tables: ["transactions", "accounts"],
    task: "Investigate when and where the pipeline broke. Find the exact timestamp of the last successful load.",
    steps: [
      {
        title: "Find the cutoff",
        description:
          "What's the most recent transaction_date? This tells you when the pipeline stopped.",
      },
      {
        title: "Check for partial loads",
        description:
          "Count transactions per day for the last 7 days. Did volume drop gradually or stop suddenly?",
      },
      {
        title: "Detect the pattern",
        description:
          "Compare hourly transaction counts for the last loaded day vs a normal day. Was the last day fully loaded?",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Start with: SELECT MAX(transaction_date) FROM transactions" },
      { label: "Hint 2", text: "Try: SELECT DATE(transaction_date) AS day, COUNT(*) FROM transactions GROUP BY day ORDER BY day DESC LIMIT 10" },
      { label: "Hint 3", text: "Check hourly pattern: SELECT EXTRACT(HOUR FROM transaction_date) AS hr, COUNT(*) FROM transactions WHERE DATE(transaction_date) = (SELECT MAX(DATE(transaction_date)) FROM transactions) GROUP BY hr ORDER BY hr" },
    ],
    rootCause:
      "The pipeline's last successful load shows a specific cutoff timestamp. The last day has fewer records than normal (partial load), followed by complete silence. The pipeline broke mid-batch.",
    fix: "Identify the exact failure time from MAX(transaction_date). Check pipeline logs for that timestamp. Backfill missing data after fixing the root cause. Add alerting on data freshness (MAX(timestamp) > X hours old = alert).",
    learnings: [
      "MAX(timestamp) is the fastest way to check data freshness",
      "Partial loads are harder to detect than complete outages",
      "Always build freshness monitoring into data pipelines",
    ],
  },
  {
    id: "inv-009",
    title: "Revenue Doesn't Match After Refunds",
    dataset: "ecommerce",
    difficulty: "hard",
    issueType: "Refund Double Counting",
    context:
      "The finance team reports net revenue as $850K. The accounting team says it should be $720K after refunds. The dashboard query JOINs orders with a refunds table and subtracts refund amounts. But the numbers still don't match.",
    tables: ["orders", "order_items"],
    task: "Investigate why the refund subtraction is producing wrong results. Find orders being double-counted or refunds being missed.",
    steps: [
      {
        title: "Check the join",
        description:
          "JOIN orders with order_items that have been refunded. Does the JOIN create duplicate order rows?",
      },
      {
        title: "Find mismatched records",
        description:
          "Look for orders that appear in order_items multiple times. Is the refund being applied per-item or per-order?",
      },
      {
        title: "Calculate correctly",
        description:
          "Write a query that correctly computes net revenue by aggregating at the right level before subtracting.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "Check if refunded orders have multiple items — the order total gets counted once per item in the JOIN." },
      { label: "Hint 2", text: "Try aggregating refunds in a subquery first, then joining to orders." },
      { label: "Hint 3", text: "The pattern is: SELECT SUM(o.total_amount) - COALESCE(SUM(sub.refund_total), 0) FROM orders o LEFT JOIN (SELECT order_id, SUM(...) as refund_total FROM ... GROUP BY order_id) sub ON ..." },
    ],
    rootCause:
      "When JOINing orders to order_items for refund calculations, orders with multiple items get their total_amount counted multiple times. The refund subtraction happens after the row multiplication, so both revenue and refunds are inflated.",
    fix: "Aggregate at the correct level: compute refund totals in a subquery grouped by order_id, then JOIN to orders. Never subtract after a one-to-many JOIN without pre-aggregating.",
    learnings: [
      "Refund calculations are a classic JOIN trap",
      "Always aggregate in a subquery before joining",
      "Test with a specific order: manually verify the math for one record",
    ],
  },
  {
    id: "inv-010",
    title: "Orphan Records Breaking Reports",
    dataset: "ecommerce",
    difficulty: "easy",
    issueType: "Referential Integrity",
    context:
      "The customer success team runs a report of all orders with customer details. But 15% of orders are missing from the report. The query uses an INNER JOIN between orders and customers. No SQL errors are thrown.",
    tables: ["orders", "customers"],
    task: "Investigate why 15% of orders are silently dropped from the report. Find the orphan records.",
    steps: [
      {
        title: "Count the gap",
        description:
          "Compare total orders vs orders that successfully join with customers. How many are being lost?",
      },
      {
        title: "Find the orphans",
        description:
          "Use a LEFT JOIN to find orders whose customer_id doesn't match any record in the customers table.",
      },
      {
        title: "Assess the impact",
        description:
          "Calculate the total revenue from orphan orders. This is money being excluded from reports.",
      },
    ],
    hints: [
      { label: "Hint 1", text: "INNER JOIN silently drops rows with no match. LEFT JOIN preserves all rows from the left table." },
      { label: "Hint 2", text: "Try: SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE c.id IS NULL" },
      { label: "Hint 3", text: "Check what customer_ids are in orders but not in customers: SELECT DISTINCT customer_id FROM orders WHERE customer_id NOT IN (SELECT id FROM customers)" },
    ],
    rootCause:
      "Some orders reference customer_ids that don't exist in the customers table (orphan records). The INNER JOIN silently drops these rows. This happens after customer account deletions or data migration issues.",
    fix: "Use LEFT JOIN instead of INNER JOIN to include all orders. Separately investigate why customer records are missing — likely deleted accounts or failed migrations.",
    learnings: [
      "INNER JOIN silently drops non-matching rows — this is a data loss bug",
      "LEFT JOIN + WHERE right.id IS NULL is the pattern to find orphans",
      "Referential integrity issues are common after migrations or account deletions",
    ],
  },
];

/* ── Difficulty colors ── */
const difficultyColor = {
  easy: "bg-green-500/20 text-green-400 border-green-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  hard: "bg-red-500/20 text-red-400 border-red-500/30",
};

const issueTypeColor: Record<string, string> = {
  "Duplicate Data": "bg-orange-500/20 text-orange-400",
  "Pipeline Gap": "bg-purple-500/20 text-purple-400",
  "Join Explosion": "bg-red-500/20 text-red-400",
  "NULL Handling": "bg-cyan-500/20 text-cyan-400",
  "Aggregation Error": "bg-yellow-500/20 text-yellow-400",
  "Duplicate Counting": "bg-pink-500/20 text-pink-400",
  "Timezone Bug": "bg-blue-500/20 text-blue-400",
  "Pipeline Failure": "bg-amber-500/20 text-amber-400",
  "Refund Double Counting": "bg-emerald-500/20 text-emerald-400",
  "Referential Integrity": "bg-indigo-500/20 text-indigo-400",
};

export default function DebugPage() {
  const [selected, setSelected] = useState<Investigation | null>(null);
  const [query, setQuery] = useState("");
  const [queryHistory, setQueryHistory] = useState<QueryLog[]>([]);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [revealedHints, setRevealedHints] = useState<number>(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [showRootCause, setShowRootCause] = useState(false);
  const [startTime, setStartTime] = useState<number>(0);
  const [tablesExplored, setTablesExplored] = useState<Set<string>>(new Set());
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [filterDifficulty, setFilterDifficulty] = useState<string>("all");

  // Track tables mentioned in queries
  const trackTables = useCallback(
    (sql: string) => {
      if (!selected) return;
      const lower = sql.toLowerCase();
      const found = new Set(tablesExplored);
      selected.tables.forEach((t) => {
        if (lower.includes(t.toLowerCase())) found.add(t);
      });
      setTablesExplored(found);
    },
    [selected, tablesExplored]
  );

  const handleRun = useCallback(async () => {
    if (!selected || !query.trim()) return;
    setRunning(true);
    setError(null);
    setResult(null);

    trackTables(query);

    try {
      const data = await apiClient<{
        user_result: QueryResult;
        status: string;
        error?: string;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({
          query: query.trim(),
          dataset: selected.dataset,
        }),
      });

      if (data.error) {
        setError(data.error);
        setQueryHistory((h) => [
          { query: query.trim(), result: null, error: data.error!, timestamp: Date.now() },
          ...h,
        ]);
      } else if (data.user_result) {
        const normalized: QueryResult = {
          columns: data.user_result.columns,
          rows: data.user_result.rows,
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          rowCount: (data.user_result as any).row_count ?? data.user_result.rowCount ?? 0,
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          executionTimeMs: (data.user_result as any).execution_time_ms ?? data.user_result.executionTimeMs ?? 0,
        };
        setResult(normalized);
        setQueryHistory((h) => [
          { query: query.trim(), result: normalized, error: null, timestamp: Date.now() },
          ...h,
        ]);
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Query execution failed";
      setError(msg);
      setQueryHistory((h) => [
        { query: query.trim(), result: null, error: msg, timestamp: Date.now() },
        ...h,
      ]);
    } finally {
      setRunning(false);
    }
  }, [query, selected, trackTables]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.max(120, textareaRef.current.scrollHeight) + "px";
    }
  }, [query]);

  const elapsed = startTime
    ? Math.floor((Date.now() - startTime) / 1000 / 60)
    : 0;

  const filteredInvestigations = INVESTIGATIONS.filter((inv) => {
    if (filterDifficulty !== "all" && inv.difficulty !== filterDifficulty)
      return false;
    return true;
  });

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {!selected ? (
        /* ── Investigation List ── */
        <div>
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Data Debugging
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--color-text-secondary)]">
              Don&apos;t just write SQL — learn to investigate data issues like a real analyst.
              Each scenario presents a business problem with messy data.
              Your job: find what&apos;s wrong, prove it with queries, and explain the root cause.
            </p>
          </div>

          {/* Filter */}
          <div className="mb-6 flex gap-3">
            <select
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
              aria-label="Filter by difficulty"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {/* Grid */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filteredInvestigations.map((inv) => (
              <button
                key={inv.id}
                onClick={() => {
                  setSelected(inv);
                  setQuery("");
                  setResult(null);
                  setError(null);
                  setQueryHistory([]);
                  setRevealedHints(0);
                  setCurrentStep(0);
                  setShowRootCause(false);
                  setStartTime(Date.now());
                  setTablesExplored(new Set());
                }}
                className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5 text-left transition-all hover:border-[var(--color-accent)]/50 hover:shadow-lg"
              >
                <div className="mb-3 flex items-center gap-2">
                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${difficultyColor[inv.difficulty]}`}
                  >
                    {inv.difficulty}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${
                      issueTypeColor[inv.issueType] || "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {inv.issueType}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                  {inv.title}
                </h3>
                <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-[var(--color-text-muted)]">
                  {inv.context}
                </p>
                <div className="mt-3 flex items-center gap-2 text-[10px] text-[var(--color-text-muted)]">
                  <span>Tables: {inv.tables.join(", ")}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        /* ── Investigation Detail ── */
        <div>
          <button
            onClick={() => setSelected(null)}
            className="mb-4 text-xs font-medium text-[var(--color-accent)] hover:underline"
          >
            ← Back to investigations
          </button>

          <div className="grid gap-6 lg:grid-cols-[1fr_1fr]">
            {/* Left Column: Context + Editor */}
            <div className="space-y-4">
              {/* Business Context */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
                <div className="mb-3 flex items-center gap-2">
                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${difficultyColor[selected.difficulty]}`}
                  >
                    {selected.difficulty}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${
                      issueTypeColor[selected.issueType] || "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {selected.issueType}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-[var(--color-text-primary)]">
                  {selected.title}
                </h2>
                <p className="mt-3 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                  {selected.context}
                </p>
                <div className="mt-4 rounded-md bg-[var(--color-background)] p-3">
                  <p className="text-xs font-medium text-[var(--color-accent)]">
                    Your Task
                  </p>
                  <p className="mt-1 text-sm text-[var(--color-text-primary)]">
                    {selected.task}
                  </p>
                </div>
                <div className="mt-3 text-xs text-[var(--color-text-muted)]">
                  <span className="font-medium">Available tables:</span>{" "}
                  {selected.tables.map((t, i) => (
                    <span key={t}>
                      <code className="rounded bg-[var(--color-background)] px-1 py-0.5 text-[var(--color-accent)]">
                        {t}
                      </code>
                      {i < selected.tables.length - 1 && ", "}
                    </span>
                  ))}
                </div>
              </div>

              {/* Investigation Steps */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Investigation Steps
                </h3>
                <div className="mt-3 space-y-3">
                  {selected.steps.map((step, i) => (
                    <div
                      key={i}
                      className={`flex gap-3 rounded-md p-2 transition-colors ${
                        i === currentStep
                          ? "bg-[var(--color-accent)]/10"
                          : i < currentStep
                            ? "opacity-60"
                            : "opacity-40"
                      }`}
                    >
                      <div
                        className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${
                          i < currentStep
                            ? "bg-green-500/20 text-green-400"
                            : i === currentStep
                              ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]"
                              : "bg-[var(--color-border)] text-[var(--color-text-muted)]"
                        }`}
                      >
                        {i < currentStep ? "✓" : i + 1}
                      </div>
                      <div>
                        <p className="text-xs font-medium text-[var(--color-text-primary)]">
                          {step.title}
                        </p>
                        <p className="mt-0.5 text-[11px] leading-relaxed text-[var(--color-text-muted)]">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                {currentStep < selected.steps.length && (
                  <button
                    onClick={() =>
                      setCurrentStep((s) => Math.min(s + 1, selected.steps.length))
                    }
                    className="mt-3 text-xs font-medium text-[var(--color-accent)] hover:underline"
                  >
                    Mark step as done →
                  </button>
                )}
              </div>

              {/* Hints */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Hints ({revealedHints}/{selected.hints.length})
                </h3>
                <div className="mt-3 space-y-2">
                  {selected.hints.map((hint, i) =>
                    i < revealedHints ? (
                      <div
                        key={i}
                        className="rounded-md bg-[var(--color-background)] p-3 text-xs text-[var(--color-text-secondary)]"
                      >
                        <span className="font-medium text-[var(--color-accent)]">
                          {hint.label}:
                        </span>{" "}
                        {hint.text}
                      </div>
                    ) : null
                  )}
                  {revealedHints < selected.hints.length && (
                    <button
                      onClick={() => setRevealedHints((h) => h + 1)}
                      className="text-xs font-medium text-[var(--color-accent)] hover:underline"
                    >
                      Reveal {selected.hints[revealedHints].label}
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column: Editor + Results + Investigation Panel */}
            <div className="space-y-4">
              {/* SQL Editor */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
                <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
                  <span className="text-[10px] font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                    SQL Query
                  </span>
                  <button
                    onClick={handleRun}
                    disabled={running || !query.trim()}
                    className="flex items-center gap-1.5 rounded-md bg-[var(--color-accent)] px-3 py-1 text-xs font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
                  >
                    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                    {running ? "Running..." : "Run"}
                    <kbd className="ml-1 rounded bg-white/20 px-1 py-0.5 text-[10px]">
                      {typeof navigator !== "undefined" &&
                      /Mac/.test(navigator.userAgent)
                        ? "⌘↵"
                        : "Ctrl+↵"}
                    </kbd>
                  </button>
                </div>
                <textarea
                  ref={textareaRef}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                      handleRun();
                    }
                  }}
                  placeholder="Write your investigative query here..."
                  className="min-h-[120px] w-full resize-none bg-transparent p-4 font-mono text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none"
                  spellCheck={false}
                />
              </div>

              {/* Error */}
              {error && (
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4">
                  <h3 className="text-xs font-medium text-red-400">Error</h3>
                  <p className="mt-1 font-mono text-xs text-red-300">{error}</p>
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
                    <div className="p-6 text-center">
                      <p className="text-sm text-[var(--color-text-muted)]">
                        Query returned 0 rows. Try a different approach.
                      </p>
                    </div>
                  ) : (
                    <div className="max-h-72 overflow-auto">
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
                <div className="flex h-48 items-center justify-center rounded-lg border border-dashed border-[var(--color-border)] bg-[var(--color-surface)]">
                  <div className="text-center">
                    <p className="text-sm text-[var(--color-text-muted)]">
                      Run queries to investigate the issue
                    </p>
                    <p className="mt-1 text-[10px] text-[var(--color-text-muted)]">
                      Ctrl+Enter to execute
                    </p>
                  </div>
                </div>
              )}

              {/* Investigation Panel */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Investigation Progress
                </h3>
                <div className="mt-3 grid grid-cols-3 gap-3">
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">
                      {queryHistory.length}
                    </p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">
                      Queries Run
                    </p>
                  </div>
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">
                      {elapsed}m
                    </p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">
                      Time Spent
                    </p>
                  </div>
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">
                      {tablesExplored.size}/{selected.tables.length}
                    </p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">
                      Tables Explored
                    </p>
                  </div>
                </div>
              </div>

              {/* Query History */}
              {queryHistory.length > 0 && (
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                  <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                    Query History
                  </h3>
                  <div className="mt-3 max-h-48 space-y-2 overflow-auto">
                    {queryHistory.map((log, i) => (
                      <button
                        key={i}
                        onClick={() => setQuery(log.query)}
                        className="w-full rounded-md bg-[var(--color-background)] p-2 text-left transition-colors hover:bg-[var(--color-border)]/50"
                      >
                        <code className="line-clamp-1 text-[11px] text-[var(--color-text-secondary)]">
                          {log.query}
                        </code>
                        <div className="mt-1 flex items-center gap-2 text-[10px] text-[var(--color-text-muted)]">
                          {log.error ? (
                            <span className="text-red-400">Error</span>
                          ) : (
                            <span>
                              {log.result?.rowCount} row
                              {log.result?.rowCount !== 1 ? "s" : ""} •{" "}
                              {log.result?.executionTimeMs}ms
                            </span>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Root Cause Reveal */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                {showRootCause ? (
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-red-400">
                        Root Cause
                      </h3>
                      <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                        {selected.rootCause}
                      </p>
                    </div>
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-green-400">
                        The Fix
                      </h3>
                      <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                        {selected.fix}
                      </p>
                    </div>
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-accent)]">
                        What You Learned
                      </h3>
                      <ul className="mt-2 space-y-1">
                        {selected.learnings.map((l, i) => (
                          <li
                            key={i}
                            className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]"
                          >
                            <span className="mt-0.5 text-[var(--color-accent)]">•</span>
                            {l}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowRootCause(true)}
                    className="w-full text-center text-xs font-medium text-[var(--color-accent)] hover:underline"
                  >
                    Reveal Root Cause & Solution
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
