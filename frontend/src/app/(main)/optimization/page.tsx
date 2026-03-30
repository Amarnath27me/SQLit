"use client";

import { useState, useMemo, useCallback } from "react";
import { Badge } from "@/components/ui/Badge";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface OptimizationChallenge {
  id: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  slowQuery: string;
  issue: string;
  hint: string;
  optimizedQuery: string;
  tags: string[];
  performanceNote?: { before: string; after: string };
}

interface OptimizationConcept {
  title: string;
  icon: string;
  description: string;
  keyPoints: string[];
  example?: string;
}

interface BeforeAfterPair {
  id: string;
  title: string;
  description: string;
  before: { query: string; time: string; rows: string; plan: string };
  after: { query: string; time: string; rows: string; plan: string };
}

/* ── EXPLAIN Visualizer types ── */

interface PlanNode {
  id: string;
  nodeType: string;
  relation?: string;
  detail: string;
  cost: { startup: number; total: number };
  rows: number;
  width: number;
  actualTime?: { startup: number; total: number };
  actualRows?: number;
  loops?: number;
  filter?: string;
  indexCond?: string;
  sortKey?: string;
  joinType?: string;
  children: PlanNode[];
}

interface ExamplePlan {
  id: string;
  title: string;
  query: string;
  root: PlanNode;
  totalTime: number;
  annotations: { nodeId: string; text: string; type: "info" | "warning" | "tip" }[];
}

/* ------------------------------------------------------------------ */
/*  Optimization Challenges Data                                       */
/* ------------------------------------------------------------------ */

const CHALLENGES: OptimizationChallenge[] = [
  {
    id: "ch1",
    title: "Missing Index on Filter Column",
    difficulty: "easy",
    slowQuery: `SELECT * FROM orders
WHERE customer_id = 12345
ORDER BY created_at DESC;`,
    issue: "Missing index usage — full table scan on 500K rows",
    hint: "The WHERE clause filters by customer_id. Without an index on that column, every row must be read.",
    optimizedQuery: `-- Add the index first:
CREATE INDEX idx_orders_customer_id
  ON orders(customer_id, created_at DESC);

-- Query remains the same but now uses Index Scan
SELECT * FROM orders
WHERE customer_id = 12345
ORDER BY created_at DESC;`,
    tags: ["Index", "WHERE optimization", "B-tree"],
    performanceNote: { before: "2.3s (Seq Scan, 500K rows)", after: "4ms (Index Scan, 38 rows)" },
  },
  {
    id: "ch2",
    title: "The SELECT * Anti-Pattern",
    difficulty: "easy",
    slowQuery: `SELECT *
FROM products
WHERE category_id = 5
ORDER BY price DESC
LIMIT 20;`,
    issue: "Unnecessary columns fetched — table has 40 columns including large TEXT/BLOB fields",
    hint: "Only 3 columns are actually needed. Selecting all 40 wastes I/O, memory, and prevents index-only scans.",
    optimizedQuery: `SELECT id, name, price
FROM products
WHERE category_id = 5
ORDER BY price DESC
LIMIT 20;`,
    tags: ["SELECT optimization", "I/O reduction", "Covering Index"],
    performanceNote: { before: "180ms (reads 40 cols, 6.2MB)", after: "12ms (reads 3 cols, 0.4MB)" },
  },
  {
    id: "ch3",
    title: "Correlated Subquery N+1 Problem",
    difficulty: "medium",
    slowQuery: `SELECT c.name,
  (SELECT COUNT(*)
   FROM orders o
   WHERE o.customer_id = c.id) AS order_count
FROM customers c
WHERE c.status = 'active';`,
    issue: "N+1 query pattern — correlated subquery executes once per row (100K customers = 100K subqueries)",
    hint: "Restructure as a LEFT JOIN with GROUP BY to process everything in a single pass.",
    optimizedQuery: `SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.status = 'active'
GROUP BY c.id, c.name;`,
    tags: ["JOIN vs Subquery", "N+1 pattern", "GROUP BY"],
    performanceNote: { before: "12.8s (100K subqueries)", after: "340ms (single Hash Join + Aggregate)" },
  },
  {
    id: "ch4",
    title: "Function on Indexed Column",
    difficulty: "medium",
    slowQuery: `SELECT *
FROM transactions
WHERE EXTRACT(YEAR FROM created_at) = 2024
  AND EXTRACT(MONTH FROM created_at) = 3;`,
    issue: "Function wrapping indexed column — prevents index usage, forces full table scan",
    hint: "Applying a function to a column in WHERE prevents the B-tree index from matching. Use a range comparison instead.",
    optimizedQuery: `SELECT *
FROM transactions
WHERE created_at >= '2024-03-01'
  AND created_at < '2024-04-01';`,
    tags: ["WHERE optimization", "Index", "Sargable predicates"],
    performanceNote: { before: "3.1s (Seq Scan on 2M rows)", after: "25ms (Index Range Scan)" },
  },
  {
    id: "ch5",
    title: "N+1 Query from Application Code",
    difficulty: "medium",
    slowQuery: `-- Query 1: fetch orders
SELECT id, total FROM orders
WHERE customer_id = 42 LIMIT 500;

-- Then for EACH order (x500 round-trips):
-- SELECT * FROM order_items
--   WHERE order_id = ?;`,
    issue: "N+1 query pattern — 501 database round-trips instead of 1",
    hint: "Combine the two queries into a single JOIN to fetch all data in one database call.",
    optimizedQuery: `SELECT o.id, o.total,
  oi.product_id, oi.quantity, oi.price
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.customer_id = 42
ORDER BY o.id
LIMIT 500;`,
    tags: ["N+1 pattern", "JOIN vs Subquery", "Round-trip reduction"],
    performanceNote: { before: "4.2s (501 queries, network overhead)", after: "45ms (1 query, Hash Join)" },
  },
  {
    id: "ch6",
    title: "DISTINCT on Large JOIN",
    difficulty: "hard",
    slowQuery: `SELECT DISTINCT c.id, c.name, c.email
FROM customers c
JOIN orders o ON o.customer_id = c.id;`,
    issue: "DISTINCT after JOIN builds massive result set then deduplicates — O(n*m) then sort",
    hint: "EXISTS can short-circuit after finding the first match per customer, avoiding the full cross product.",
    optimizedQuery: `SELECT c.id, c.name, c.email
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id
);`,
    tags: ["JOIN vs Subquery", "EXISTS optimization", "Deduplication"],
    performanceNote: { before: "2.8s (2.3M intermediate rows, then sort)", after: "180ms (semi-join, early exit)" },
  },
  {
    id: "ch7",
    title: "OR Preventing Index Usage",
    difficulty: "medium",
    slowQuery: `SELECT id, name, email
FROM users
WHERE email = 'test@example.com'
   OR phone = '+1234567890';`,
    issue: "OR between differently-indexed columns forces sequential scan or expensive bitmap merge",
    hint: "Split the OR into two index-friendly queries connected with UNION ALL.",
    optimizedQuery: `SELECT id, name, email FROM users
WHERE email = 'test@example.com'
UNION ALL
SELECT id, name, email FROM users
WHERE phone = '+1234567890'
  AND email != 'test@example.com';`,
    tags: ["WHERE optimization", "UNION ALL", "Index"],
    performanceNote: { before: "890ms (Seq Scan on 5M rows)", after: "2ms (two Index Scans)" },
  },
  {
    id: "ch8",
    title: "Pagination with OFFSET",
    difficulty: "hard",
    slowQuery: `SELECT id, title, created_at
FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 20000;`,
    issue: "OFFSET scans and discards 20,000 rows — gets slower on every page",
    hint: "Use keyset (cursor-based) pagination: filter by the last seen value instead of skipping rows.",
    optimizedQuery: `-- Keyset / cursor-based pagination
SELECT id, title, created_at
FROM posts
WHERE created_at < '2024-01-15T10:30:00'
ORDER BY created_at DESC
LIMIT 20;`,
    tags: ["Pagination", "Cursor-based", "OFFSET anti-pattern"],
    performanceNote: { before: "8.2s on page 1000 (scans 20K rows)", after: "3ms on any page (reads 20 rows)" },
  },
  {
    id: "ch9",
    title: "Covering Index for Aggregation",
    difficulty: "hard",
    slowQuery: `SELECT status,
  COUNT(*) AS cnt,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY status;`,
    issue: "Reads entire wide table (20 columns, 2M rows) when only 2 columns are needed for the aggregation",
    hint: "A covering index with INCLUDE lets PostgreSQL do an Index Only Scan, reading a compact index instead of the full table.",
    optimizedQuery: `-- Create a covering index
CREATE INDEX idx_orders_status_covering
  ON orders(status) INCLUDE (total_amount);

-- Same query, now uses Index Only Scan
SELECT status,
  COUNT(*) AS cnt,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY status;`,
    tags: ["Index", "Covering Index", "Index Only Scan"],
    performanceNote: { before: "1.4s (Seq Scan, reads 2M wide rows)", after: "120ms (Index Only Scan, compact)" },
  },
  {
    id: "ch10",
    title: "Composite Index Column Order",
    difficulty: "hard",
    slowQuery: `-- Two separate indexes exist:
-- idx_tickets_status (status)
-- idx_tickets_created (created_at)

SELECT id, title, status, created_at
FROM tickets
WHERE status = 'open'
ORDER BY created_at DESC
LIMIT 50;`,
    issue: "Two separate indexes force bitmap merge + sort instead of a single efficient scan",
    hint: "A composite index on (status, created_at DESC) serves both the filter and the sort in one operation.",
    optimizedQuery: `-- Replace two indexes with one composite index
CREATE INDEX idx_tickets_status_created
  ON tickets(status, created_at DESC);

-- Query now uses single Index Scan Backward
-- No separate sort step needed
SELECT id, title, status, created_at
FROM tickets
WHERE status = 'open'
ORDER BY created_at DESC
LIMIT 50;`,
    tags: ["Index", "Composite Index", "Sort elimination"],
    performanceNote: { before: "650ms (Bitmap Scan + Sort)", after: "8ms (Index Scan Backward, pre-sorted)" },
  },
  /* ── New challenges (ch11–ch50) ── */
  {
    id: "ch11",
    title: "Implicit Type Casting Kills Index",
    difficulty: "easy",
    slowQuery: `SELECT * FROM users
WHERE phone = 5551234567;`,
    issue: "phone is VARCHAR but compared to an integer — PostgreSQL casts every row's phone to numeric, preventing index usage",
    hint: "Always match the literal type to the column type. Wrap the value in quotes so the index can be used directly.",
    optimizedQuery: `SELECT * FROM users
WHERE phone = '5551234567';`,
    tags: ["WHERE optimization", "Type casting", "Index"],
    performanceNote: { before: "1.9s (Seq Scan, implicit cast per row)", after: "0.3ms (Index Scan, direct match)" },
  },
  {
    id: "ch12",
    title: "LIKE with Leading Wildcard",
    difficulty: "easy",
    slowQuery: `SELECT id, name, email
FROM customers
WHERE email LIKE '%@gmail.com';`,
    issue: "Leading wildcard % prevents B-tree index usage — full table scan on every row",
    hint: "Reverse the column and pattern to use a functional index, or use a trigram (pg_trgm) GIN index for arbitrary LIKE patterns.",
    optimizedQuery: `-- Option 1: Reverse index trick
CREATE INDEX idx_customers_email_rev
  ON customers(reverse(email));

SELECT id, name, email
FROM customers
WHERE reverse(email) LIKE reverse('%@gmail.com');
-- becomes: LIKE 'moc.liamg@%' (trailing wildcard, index-friendly)

-- Option 2: Trigram GIN index (more general)
-- CREATE INDEX idx_customers_email_trgm
--   ON customers USING gin(email gin_trgm_ops);`,
    tags: ["LIKE optimization", "Index", "Functional Index"],
    performanceNote: { before: "2.1s (Seq Scan 3M rows)", after: "15ms (Index Scan)" },
  },
  {
    id: "ch13",
    title: "COUNT(*) on Entire Table",
    difficulty: "easy",
    slowQuery: `SELECT COUNT(*)
FROM logs;
-- logs table has 50M rows`,
    issue: "PostgreSQL must do a full table scan for exact COUNT(*) — MVCC means no stored row count",
    hint: "Use an approximate count from pg_stat or maintain a counter table if exact count isn't critical.",
    optimizedQuery: `-- Fast approximate count (within ~5% accuracy)
SELECT reltuples::bigint AS approx_count
FROM pg_class
WHERE relname = 'logs';

-- For exact count on filtered subsets, add a partial index:
-- CREATE INDEX idx_logs_recent ON logs(id)
--   WHERE created_at > NOW() - INTERVAL '1 day';
-- SELECT COUNT(*) FROM logs
--   WHERE created_at > NOW() - INTERVAL '1 day';`,
    tags: ["Aggregation", "Table statistics", "Approximate counts"],
    performanceNote: { before: "28s (Seq Scan 50M rows)", after: "0.1ms (catalog lookup)" },
  },
  {
    id: "ch14",
    title: "NOT IN with NULL Trap",
    difficulty: "medium",
    slowQuery: `SELECT id, name
FROM products
WHERE id NOT IN (
  SELECT product_id FROM order_items
);`,
    issue: "NOT IN returns no rows if the subquery contains any NULL — also prevents index usage and builds a full hash",
    hint: "Use NOT EXISTS which handles NULLs correctly and can short-circuit via an anti-join.",
    optimizedQuery: `SELECT p.id, p.name
FROM products p
WHERE NOT EXISTS (
  SELECT 1 FROM order_items oi
  WHERE oi.product_id = p.id
);`,
    tags: ["EXISTS optimization", "NULL handling", "Anti-join"],
    performanceNote: { before: "4.2s (Hash Anti Join, NULL risk)", after: "180ms (Nested Loop Anti Join, index-backed)" },
  },
  {
    id: "ch15",
    title: "Unnecessary DISTINCT Hiding a JOIN Bug",
    difficulty: "easy",
    slowQuery: `SELECT DISTINCT c.id, c.name, c.email
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id;`,
    issue: "DISTINCT masks a many-to-many explosion — 100K customers × 5 orders × 3 items = 1.5M rows sorted and deduplicated",
    hint: "You only need customers who have orders. Use EXISTS to avoid multiplying rows entirely.",
    optimizedQuery: `SELECT c.id, c.name, c.email
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  WHERE o.customer_id = c.id
);`,
    tags: ["EXISTS optimization", "Deduplication", "JOIN vs Subquery"],
    performanceNote: { before: "5.1s (1.5M rows → sort → unique)", after: "120ms (semi-join, early exit)" },
  },
  {
    id: "ch16",
    title: "Partial Index for Hot Path",
    difficulty: "medium",
    slowQuery: `-- 95% of orders are 'completed', only 2% are 'pending'
-- Full index exists: idx_orders_status (status)

SELECT * FROM orders
WHERE status = 'pending'
ORDER BY created_at;`,
    issue: "Full index on status includes 95% completed rows that are never queried on this path — bloated index, more I/O",
    hint: "A partial index that only includes pending rows is 50x smaller and faster to scan.",
    optimizedQuery: `-- Partial index: only index rows we actually query
CREATE INDEX idx_orders_pending
  ON orders(created_at)
  WHERE status = 'pending';

-- Same query, now uses tiny partial index
SELECT * FROM orders
WHERE status = 'pending'
ORDER BY created_at;`,
    tags: ["Index", "Partial Index", "Selective indexing"],
    performanceNote: { before: "320ms (scans 2M-entry index)", after: "5ms (scans 40K-entry partial index)" },
  },
  {
    id: "ch17",
    title: "Window Function Recomputing on Every Row",
    difficulty: "hard",
    slowQuery: `SELECT *,
  (SELECT AVG(price) FROM products p2
   WHERE p2.category_id = p.category_id) AS avg_category_price
FROM products p;`,
    issue: "Correlated subquery recalculates the average for each row — same average recomputed 500 times per category",
    hint: "Use a window function to compute the average once per partition, or JOIN to a pre-aggregated CTE.",
    optimizedQuery: `SELECT *,
  AVG(price) OVER (PARTITION BY category_id) AS avg_category_price
FROM products;`,
    tags: ["Window Functions", "N+1 pattern", "Partition optimization"],
    performanceNote: { before: "3.8s (correlated subquery per row)", after: "45ms (single WindowAgg pass)" },
  },
  {
    id: "ch18",
    title: "Expensive CTE Evaluated Multiple Times",
    difficulty: "hard",
    slowQuery: `WITH order_stats AS (
  SELECT customer_id,
    COUNT(*) AS cnt,
    SUM(total_amount) AS revenue
  FROM orders
  GROUP BY customer_id
)
SELECT 'high_value' AS segment, COUNT(*) FROM order_stats WHERE revenue > 10000
UNION ALL
SELECT 'medium_value', COUNT(*) FROM order_stats WHERE revenue BETWEEN 1000 AND 10000
UNION ALL
SELECT 'low_value', COUNT(*) FROM order_stats WHERE revenue < 1000;`,
    issue: "In PostgreSQL <12, CTEs are optimization fences — the aggregation runs 3 times. In 12+, the planner may still not inline complex CTEs",
    hint: "Use conditional aggregation to classify and count in a single pass.",
    optimizedQuery: `SELECT
  COUNT(*) FILTER (WHERE revenue > 10000) AS high_value,
  COUNT(*) FILTER (WHERE revenue BETWEEN 1000 AND 10000) AS medium_value,
  COUNT(*) FILTER (WHERE revenue < 1000) AS low_value
FROM (
  SELECT customer_id, SUM(total_amount) AS revenue
  FROM orders
  GROUP BY customer_id
) stats;`,
    tags: ["CTE optimization", "FILTER clause", "Single-pass aggregation"],
    performanceNote: { before: "2.4s (3x aggregation passes)", after: "420ms (single pass + conditional counts)" },
  },
  {
    id: "ch19",
    title: "UPDATE Without Index on WHERE",
    difficulty: "medium",
    slowQuery: `UPDATE orders
SET status = 'archived'
WHERE created_at < '2022-01-01'
  AND status = 'completed';`,
    issue: "No index on (status, created_at) — UPDATE does a sequential scan locking rows as it goes, blocking other queries",
    hint: "Add an index for the WHERE clause, and batch the update to reduce lock contention.",
    optimizedQuery: `-- Add index for the filter
CREATE INDEX idx_orders_archive_candidates
  ON orders(status, created_at)
  WHERE status = 'completed';

-- Batch update to reduce lock duration
UPDATE orders
SET status = 'archived'
WHERE id IN (
  SELECT id FROM orders
  WHERE created_at < '2022-01-01'
    AND status = 'completed'
  LIMIT 5000
);
-- Repeat in a loop until 0 rows affected`,
    tags: ["UPDATE optimization", "Batch processing", "Lock contention"],
    performanceNote: { before: "45s (Seq Scan + 800K row locks)", after: "200ms per batch (Index Scan + 5K locks)" },
  },
  {
    id: "ch20",
    title: "Excessive JOIN Columns in GROUP BY",
    difficulty: "medium",
    slowQuery: `SELECT c.id, c.name, c.email, c.phone,
  c.address, c.city, c.state,
  COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name, c.email, c.phone,
  c.address, c.city, c.state;`,
    issue: "Grouping by 7 columns creates a huge hash key — slow hashing and high memory usage",
    hint: "Group by the primary key only, then join back to get the other columns. PostgreSQL allows this when grouping by PK.",
    optimizedQuery: `-- PostgreSQL: GROUP BY primary key implies all columns in that table
SELECT c.id, c.name, c.email, c.phone,
  c.address, c.city, c.state,
  COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id;  -- PK is sufficient`,
    tags: ["GROUP BY", "Primary Key optimization", "Hash memory"],
    performanceNote: { before: "1.8s (HashAggregate with 7-col key)", after: "650ms (HashAggregate with 1-col key)" },
  },
  {
    id: "ch21",
    title: "Sorting Without Index Support",
    difficulty: "easy",
    slowQuery: `SELECT id, name, created_at
FROM products
ORDER BY created_at DESC
LIMIT 10;`,
    issue: "No index on created_at — sorts entire 500K-row table in memory just to return 10 rows",
    hint: "An index on created_at DESC lets PostgreSQL read the first 10 rows directly from the index without sorting.",
    optimizedQuery: `CREATE INDEX idx_products_created
  ON products(created_at DESC);

-- Now uses Index Scan, reads only 10 rows
SELECT id, name, created_at
FROM products
ORDER BY created_at DESC
LIMIT 10;`,
    tags: ["Sort elimination", "Index", "LIMIT optimization"],
    performanceNote: { before: "420ms (Seq Scan + Sort 500K rows)", after: "0.5ms (Index Scan, 10 rows)" },
  },
  {
    id: "ch22",
    title: "Materialized View for Dashboard Queries",
    difficulty: "hard",
    slowQuery: `-- Dashboard query runs every page load (50 req/sec)
SELECT DATE_TRUNC('day', created_at) AS day,
  COUNT(*) AS orders,
  SUM(total_amount) AS revenue,
  AVG(total_amount) AS avg_order
FROM orders
WHERE created_at > NOW() - INTERVAL '90 days'
GROUP BY 1
ORDER BY 1;`,
    issue: "Aggregates 5M rows on every request — 50 identical expensive queries per second",
    hint: "Pre-compute the results in a materialized view and refresh it periodically.",
    optimizedQuery: `-- Create materialized view (one-time)
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT DATE_TRUNC('day', created_at) AS day,
  COUNT(*) AS orders,
  SUM(total_amount) AS revenue,
  AVG(total_amount) AS avg_order
FROM orders
WHERE created_at > NOW() - INTERVAL '90 days'
GROUP BY 1
ORDER BY 1;

CREATE UNIQUE INDEX ON mv_daily_revenue(day);

-- Dashboard reads from materialized view
SELECT * FROM mv_daily_revenue ORDER BY day;

-- Refresh every 5 minutes via cron
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_revenue;`,
    tags: ["Materialized View", "Caching", "Dashboard optimization"],
    performanceNote: { before: "3.2s per request × 50 rps", after: "2ms per request (pre-computed)" },
  },
  {
    id: "ch23",
    title: "HAVING vs WHERE Placement",
    difficulty: "easy",
    slowQuery: `SELECT category_id, COUNT(*) AS cnt
FROM products
GROUP BY category_id
HAVING category_id IN (1, 2, 3);`,
    issue: "HAVING filters after aggregation — groups ALL categories first, then discards most results",
    hint: "Move non-aggregate filters to WHERE so rows are eliminated before grouping.",
    optimizedQuery: `SELECT category_id, COUNT(*) AS cnt
FROM products
WHERE category_id IN (1, 2, 3)
GROUP BY category_id;`,
    tags: ["WHERE optimization", "HAVING vs WHERE", "Filter pushdown"],
    performanceNote: { before: "180ms (groups all 200 categories)", after: "12ms (groups only 3 categories)" },
  },
  {
    id: "ch24",
    title: "Redundant Subquery in FROM",
    difficulty: "medium",
    slowQuery: `SELECT sub.customer_id, sub.total_orders
FROM (
  SELECT customer_id, COUNT(*) AS total_orders,
    MAX(created_at) AS last_order
  FROM orders
  GROUP BY customer_id
) sub
WHERE sub.total_orders > 5;`,
    issue: "Subquery computes MAX(created_at) for every customer but it's never used — wasted CPU and memory",
    hint: "Remove unused computed columns from subqueries. Less data = faster aggregation.",
    optimizedQuery: `SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;`,
    tags: ["Subquery simplification", "Dead column elimination", "HAVING"],
    performanceNote: { before: "680ms (computes unused MAX per group)", after: "410ms (aggregate only what's needed)" },
  },
  {
    id: "ch25",
    title: "Multi-Column IN vs EXISTS",
    difficulty: "hard",
    slowQuery: `SELECT * FROM inventory
WHERE (warehouse_id, product_id) IN (
  SELECT warehouse_id, product_id
  FROM stock_alerts
  WHERE alert_type = 'low_stock'
);`,
    issue: "Multi-column IN builds a full hash set of all alert pairs — can't leverage indexes efficiently on composite check",
    hint: "EXISTS with correlated conditions lets the planner use indexes on each individual column.",
    optimizedQuery: `SELECT i.* FROM inventory i
WHERE EXISTS (
  SELECT 1 FROM stock_alerts sa
  WHERE sa.warehouse_id = i.warehouse_id
    AND sa.product_id = i.product_id
    AND sa.alert_type = 'low_stock'
);`,
    tags: ["EXISTS optimization", "Multi-column lookup", "Semi-join"],
    performanceNote: { before: "1.6s (Hash Semi Join, full materialization)", after: "85ms (Nested Loop Semi Join, index-backed)" },
  },
  {
    id: "ch26",
    title: "String Concatenation in WHERE",
    difficulty: "medium",
    slowQuery: `SELECT * FROM customers
WHERE first_name || ' ' || last_name = 'John Smith';`,
    issue: "Concatenation expression on every row prevents any index usage — full table scan",
    hint: "Split the condition into separate column comparisons that can each use their own index.",
    optimizedQuery: `SELECT * FROM customers
WHERE first_name = 'John'
  AND last_name = 'Smith';

-- With a composite index:
-- CREATE INDEX idx_customers_name
--   ON customers(first_name, last_name);`,
    tags: ["Sargable predicates", "WHERE optimization", "Expression index"],
    performanceNote: { before: "1.2s (Seq Scan, concat per row)", after: "0.4ms (Index Scan on composite index)" },
  },
  {
    id: "ch27",
    title: "LEFT JOIN When INNER JOIN Suffices",
    difficulty: "easy",
    slowQuery: `SELECT o.id, o.total_amount, c.name
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id
WHERE c.status = 'active';`,
    issue: "LEFT JOIN preserves NULLs from customers, but WHERE c.status = 'active' filters NULLs out anyway — contradictory logic wastes planner effort",
    hint: "If your WHERE clause filters on the right table, the LEFT JOIN effectively becomes an INNER JOIN. Make it explicit.",
    optimizedQuery: `SELECT o.id, o.total_amount, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE c.status = 'active';`,
    tags: ["JOIN optimization", "LEFT vs INNER", "Query semantics"],
    performanceNote: { before: "520ms (Left Join + Filter NULLs)", after: "380ms (Hash Join, smaller result set)" },
  },
  {
    id: "ch28",
    title: "DELETE Without Batching",
    difficulty: "hard",
    slowQuery: `DELETE FROM audit_logs
WHERE created_at < '2023-01-01';
-- Deletes 30M rows in a single transaction`,
    issue: "Single massive DELETE holds locks for minutes, bloats WAL, and can cause OOM with undo log",
    hint: "Delete in small batches with a loop, or use table partitioning to DROP entire old partitions instantly.",
    optimizedQuery: `-- Option 1: Batch delete
DELETE FROM audit_logs
WHERE id IN (
  SELECT id FROM audit_logs
  WHERE created_at < '2023-01-01'
  LIMIT 10000
);
-- Repeat until 0 rows affected

-- Option 2: Partition by month (best for time-series)
-- DROP TABLE audit_logs_2022_01; -- instant!`,
    tags: ["DELETE optimization", "Batch processing", "Table partitioning"],
    performanceNote: { before: "8min (30M rows, WAL bloat, lock contention)", after: "0.5s per 10K batch or instant DROP" },
  },
  {
    id: "ch29",
    title: "UNION vs UNION ALL",
    difficulty: "easy",
    slowQuery: `SELECT name FROM customers_us
UNION
SELECT name FROM customers_eu;`,
    issue: "UNION deduplicates by sorting/hashing the entire result set — expensive when duplicates are impossible or acceptable",
    hint: "Use UNION ALL when you know there are no duplicates or don't need dedup. It just appends results.",
    optimizedQuery: `SELECT name FROM customers_us
UNION ALL
SELECT name FROM customers_eu;`,
    tags: ["UNION ALL", "Deduplication", "Sort elimination"],
    performanceNote: { before: "1.2s (Sort + Unique on 2M rows)", after: "180ms (Append, no sort)" },
  },
  {
    id: "ch30",
    title: "CASE Inside Aggregate vs FILTER",
    difficulty: "medium",
    slowQuery: `SELECT
  COUNT(CASE WHEN status = 'active' THEN 1 END) AS active,
  COUNT(CASE WHEN status = 'inactive' THEN 1 END) AS inactive,
  COUNT(CASE WHEN status = 'suspended' THEN 1 END) AS suspended
FROM users;`,
    issue: "Three CASE expressions evaluated per row — verbose and harder for the planner to optimize",
    hint: "PostgreSQL's FILTER clause is clearer and can be optimized better by the planner.",
    optimizedQuery: `SELECT
  COUNT(*) FILTER (WHERE status = 'active') AS active,
  COUNT(*) FILTER (WHERE status = 'inactive') AS inactive,
  COUNT(*) FILTER (WHERE status = 'suspended') AS suspended
FROM users;`,
    tags: ["FILTER clause", "Conditional aggregation", "PostgreSQL-specific"],
    performanceNote: { before: "340ms (3 CASE evals per row)", after: "290ms (FILTER, same speed but cleaner + optimizable)" },
  },
  {
    id: "ch31",
    title: "Index-Only Scan Blocked by Visibility",
    difficulty: "hard",
    slowQuery: `-- Table has heavy UPDATE/DELETE activity
-- Index exists on (status, total_amount)

VACUUM; -- hasn't run in weeks

SELECT status, SUM(total_amount)
FROM orders
GROUP BY status;`,
    issue: "Index Only Scan is available but falls back to regular Index Scan because the visibility map is stale (too many dead tuples)",
    hint: "Run VACUUM to update the visibility map so PostgreSQL can use Index Only Scan without checking the heap.",
    optimizedQuery: `-- Run VACUUM to update visibility map
VACUUM orders;

-- Or configure autovacuum more aggressively
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_analyze_scale_factor = 0.02
);

-- Now the same query uses Index Only Scan
SELECT status, SUM(total_amount)
FROM orders
GROUP BY status;`,
    tags: ["VACUUM", "Visibility map", "Index Only Scan", "Autovacuum"],
    performanceNote: { before: "2.1s (Index Scan + heap fetch per row)", after: "380ms (Index Only Scan, no heap)" },
  },
  {
    id: "ch32",
    title: "Cartesian Product from Missing JOIN Condition",
    difficulty: "easy",
    slowQuery: `SELECT c.name, p.name AS product
FROM customers c, products p
WHERE c.city = 'New York';`,
    issue: "No join condition between customers and products — creates a Cartesian product (1K customers × 10K products = 10M rows)",
    hint: "This is almost always a bug. Add a proper JOIN condition linking the tables through an intermediate table like orders.",
    optimizedQuery: `SELECT DISTINCT c.name, p.name AS product
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE c.city = 'New York';`,
    tags: ["Cartesian product", "JOIN optimization", "Query correctness"],
    performanceNote: { before: "45s (10M row cross product)", after: "35ms (proper joins, ~2K rows)" },
  },
  {
    id: "ch33",
    title: "Expression Index for Computed Filter",
    difficulty: "medium",
    slowQuery: `SELECT * FROM events
WHERE DATE(created_at) = '2024-03-15';`,
    issue: "Wrapping created_at in DATE() prevents index usage — evaluates function on every row",
    hint: "Create a functional (expression) index on DATE(created_at), or rewrite as a range condition.",
    optimizedQuery: `-- Option 1: Range condition (preferred)
SELECT * FROM events
WHERE created_at >= '2024-03-15'
  AND created_at < '2024-03-16';

-- Option 2: Expression index
-- CREATE INDEX idx_events_date
--   ON events(DATE(created_at));
-- Then DATE(created_at) = '2024-03-15' uses the index`,
    tags: ["Sargable predicates", "Expression index", "Date optimization"],
    performanceNote: { before: "1.8s (Seq Scan, DATE() per row)", after: "3ms (Index Range Scan)" },
  },
  {
    id: "ch34",
    title: "Aggregation on Joined Table Before JOIN",
    difficulty: "hard",
    slowQuery: `SELECT c.name,
  COUNT(oi.id) AS total_items,
  SUM(oi.quantity * oi.price) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name;`,
    issue: "Three-way JOIN creates a massive intermediate result before aggregating — 100K customers × 5 orders × 3 items = 1.5M rows grouped",
    hint: "Pre-aggregate order_items per order in a subquery, then join to a smaller result set.",
    optimizedQuery: `SELECT c.name,
  SUM(os.item_count) AS total_items,
  SUM(os.order_total) AS total_spent
FROM customers c
JOIN (
  SELECT o.customer_id,
    COUNT(oi.id) AS item_count,
    SUM(oi.quantity * oi.price) AS order_total
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  GROUP BY o.customer_id
) os ON os.customer_id = c.id
GROUP BY c.id, c.name;`,
    tags: ["Pre-aggregation", "JOIN optimization", "Intermediate result reduction"],
    performanceNote: { before: "4.5s (1.5M row intermediate)", after: "800ms (100K row intermediate)" },
  },
  {
    id: "ch35",
    title: "LATERAL JOIN for Top-N Per Group",
    difficulty: "hard",
    slowQuery: `-- Get latest 3 orders per customer
SELECT c.id, c.name, o.*
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.id IN (
  SELECT o2.id FROM orders o2
  WHERE o2.customer_id = c.id
  ORDER BY o2.created_at DESC
  LIMIT 3
);`,
    issue: "Correlated subquery in WHERE with LIMIT — hard for planner to optimize, often falls back to nested loop without index",
    hint: "Use LATERAL JOIN which is designed for exactly this pattern — top-N per group with index support.",
    optimizedQuery: `SELECT c.id, c.name, lo.*
FROM customers c
CROSS JOIN LATERAL (
  SELECT o.id, o.total_amount, o.created_at
  FROM orders o
  WHERE o.customer_id = c.id
  ORDER BY o.created_at DESC
  LIMIT 3
) lo;`,
    tags: ["LATERAL JOIN", "Top-N per group", "Correlated subquery"],
    performanceNote: { before: "8.5s (nested correlated subquery)", after: "350ms (LATERAL + index scan per customer)" },
  },
  {
    id: "ch36",
    title: "GIN Index for JSONB Queries",
    difficulty: "medium",
    slowQuery: `SELECT * FROM events
WHERE payload->>'event_type' = 'purchase'
  AND (payload->>'amount')::numeric > 100;`,
    issue: "No index on JSONB fields — sequential scan parses JSON on every row",
    hint: "A GIN index on the JSONB column supports containment and key-exists operators efficiently.",
    optimizedQuery: `-- GIN index for containment queries
CREATE INDEX idx_events_payload
  ON events USING gin(payload);

-- Use containment operator @> for index support
SELECT * FROM events
WHERE payload @> '{"event_type": "purchase"}'
  AND (payload->>'amount')::numeric > 100;

-- Or use expression index for specific paths:
-- CREATE INDEX idx_events_type
--   ON events((payload->>'event_type'));`,
    tags: ["GIN Index", "JSONB", "NoSQL in SQL"],
    performanceNote: { before: "3.5s (Seq Scan + JSON parse per row)", after: "25ms (GIN Index Scan)" },
  },
  {
    id: "ch37",
    title: "Excessive Indexes Slowing Writes",
    difficulty: "medium",
    slowQuery: `-- Table has 12 indexes including:
-- idx_orders_1 (customer_id)
-- idx_orders_2 (created_at)
-- idx_orders_3 (status)
-- idx_orders_4 (customer_id, created_at)  -- supersedes idx_1
-- idx_orders_5 (status, created_at)
-- ... 7 more rarely-used indexes

INSERT INTO orders (customer_id, total_amount, status)
VALUES (42, 99.99, 'pending');`,
    issue: "Every INSERT/UPDATE must maintain 12 indexes — write amplification makes inserts 10x slower than necessary",
    hint: "Audit index usage with pg_stat_user_indexes. Drop unused indexes and consolidate overlapping ones.",
    optimizedQuery: `-- Find unused indexes
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused/redundant indexes
DROP INDEX idx_orders_1; -- superseded by idx_orders_4
DROP INDEX idx_orders_7; -- 0 scans in 90 days
-- ... keep only 4-5 essential indexes

-- Inserts are now 3-4x faster`,
    tags: ["Index maintenance", "Write optimization", "Index bloat"],
    performanceNote: { before: "8ms per INSERT (12 index updates)", after: "2ms per INSERT (5 index updates)" },
  },
  {
    id: "ch38",
    title: "Row-Level Security Overhead",
    difficulty: "hard",
    slowQuery: `-- RLS policy on orders:
-- USING (customer_id = current_setting('app.customer_id')::int)

SELECT SUM(total_amount)
FROM orders
WHERE status = 'completed';`,
    issue: "RLS adds a hidden filter evaluated per row — without index on customer_id, it triggers a Seq Scan even if status is indexed",
    hint: "Ensure the RLS column is indexed and appears in a composite index with commonly filtered columns.",
    optimizedQuery: `-- Create composite index matching RLS + query filters
CREATE INDEX idx_orders_rls_status
  ON orders(customer_id, status)
  INCLUDE (total_amount);

-- Query + RLS filter both use the index
-- Plan: Index Only Scan on idx_orders_rls_status
-- Filter: customer_id = 42 AND status = 'completed'`,
    tags: ["Row-Level Security", "Hidden filters", "Composite Index"],
    performanceNote: { before: "1.9s (Seq Scan, RLS filter per row)", after: "8ms (Index Only Scan covers both filters)" },
  },
  {
    id: "ch39",
    title: "Recursive CTE for Hierarchy vs Closure Table",
    difficulty: "hard",
    slowQuery: `-- Get all descendants of category id=5
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, 0 AS depth
  FROM categories WHERE id = 5
  UNION ALL
  SELECT c.id, c.name, c.parent_id, t.depth + 1
  FROM categories c
  JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;`,
    issue: "Recursive CTE walks the tree one level at a time — each iteration does an Index Scan. Deep trees (20+ levels) mean 20+ passes",
    hint: "Pre-compute hierarchy with a closure table or materialized path for O(1) lookups.",
    optimizedQuery: `-- Pre-computed closure table approach
-- category_closure(ancestor_id, descendant_id, depth)
-- Populated by trigger on category insert/update

SELECT c.id, c.name, cc.depth
FROM category_closure cc
JOIN categories c ON c.id = cc.descendant_id
WHERE cc.ancestor_id = 5
ORDER BY cc.depth;

-- Or: materialized path column
-- SELECT * FROM categories
-- WHERE path LIKE '5/%';  -- with index on path`,
    tags: ["Recursive CTE", "Closure table", "Hierarchy optimization"],
    performanceNote: { before: "450ms (20 recursive iterations)", after: "2ms (single index scan on closure table)" },
  },
  {
    id: "ch40",
    title: "Connection Overhead from Short-Lived Queries",
    difficulty: "medium",
    slowQuery: `-- Application opens new connection per request:
-- connect() → query → disconnect() (x1000/sec)

SELECT balance FROM accounts WHERE id = 42;
-- 2ms query, but 15ms connect + 5ms disconnect = 22ms total`,
    issue: "Connection setup (TCP handshake + SSL + auth) takes 10x longer than the actual query",
    hint: "Use a connection pooler (PgBouncer) that maintains persistent connections and multiplexes queries.",
    optimizedQuery: `-- PgBouncer configuration (pgbouncer.ini):
-- pool_mode = transaction
-- max_client_conn = 1000
-- default_pool_size = 20

-- Same query but through PgBouncer:
-- Connection already established → query → return to pool
SELECT balance FROM accounts WHERE id = 42;
-- 2ms query + 0ms connect = 2ms total`,
    tags: ["Connection pooling", "PgBouncer", "Latency reduction"],
    performanceNote: { before: "22ms per query (15ms connect overhead)", after: "2ms per query (pooled connection)" },
  },
  {
    id: "ch41",
    title: "Bloom Index for Multi-Column Equality",
    difficulty: "hard",
    slowQuery: `-- Users search by any combination of columns:
-- WHERE color = 'red' AND size = 'L'
-- WHERE material = 'cotton' AND brand = 'Nike'
-- 6 columns, would need 64 composite indexes

SELECT * FROM products
WHERE color = 'red' AND size = 'L' AND material = 'cotton';`,
    issue: "No single B-tree index can serve arbitrary column combinations — creating all permutations is impractical",
    hint: "A Bloom index supports equality checks on any combination of columns with a single compact index.",
    optimizedQuery: `-- Single Bloom index covers all combinations
CREATE INDEX idx_products_bloom
  ON products USING bloom(color, size, material, brand, style, fit)
  WITH (length=80, col1=2, col2=2, col3=2, col4=2, col5=2, col6=2);

-- Any combination of these columns now uses the Bloom index
SELECT * FROM products
WHERE color = 'red' AND size = 'L' AND material = 'cotton';`,
    tags: ["Bloom Index", "Multi-column filter", "Index strategy"],
    performanceNote: { before: "1.4s (Seq Scan, no usable index)", after: "45ms (Bloom Index Scan)" },
  },
  {
    id: "ch42",
    title: "EXPLAIN ANALYZE on Write Query in Production",
    difficulty: "medium",
    slowQuery: `-- Debugging a slow UPDATE in production:
EXPLAIN ANALYZE
UPDATE orders SET status = 'processed'
WHERE id BETWEEN 1 AND 50000;`,
    issue: "EXPLAIN ANALYZE actually EXECUTES the query — this UPDATE modifies 50K rows in production while profiling",
    hint: "Wrap in a transaction and ROLLBACK, or use EXPLAIN without ANALYZE for write queries in production.",
    optimizedQuery: `-- Safe option 1: EXPLAIN only (no execution)
EXPLAIN
UPDATE orders SET status = 'processed'
WHERE id BETWEEN 1 AND 50000;

-- Safe option 2: Execute but rollback
BEGIN;
EXPLAIN ANALYZE
UPDATE orders SET status = 'processed'
WHERE id BETWEEN 1 AND 50000;
ROLLBACK;  -- changes are undone`,
    tags: ["EXPLAIN safety", "Production debugging", "Transaction rollback"],
    performanceNote: { before: "Modifies 50K rows while profiling!", after: "Zero data modification, same plan info" },
  },
  {
    id: "ch43",
    title: "Nested Loop on Large Tables",
    difficulty: "hard",
    slowQuery: `SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.total_amount > 500;

-- Planner chooses Nested Loop:
-- Seq Scan on orders (filter: total > 500)
--   → Index Scan on customers (per row)`,
    issue: "Nested Loop does an index lookup per order row — fine for 100 rows, but 200K qualifying rows means 200K index lookups",
    hint: "Increase work_mem or add statistics so the planner chooses Hash Join for large result sets.",
    optimizedQuery: `-- Tell planner the result set is large enough for Hash Join
SET work_mem = '256MB';  -- per-operation memory

-- Or add statistics to help planner estimate cardinality
ANALYZE orders;
ANALYZE customers;

-- Same query now uses Hash Join
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.total_amount > 500;`,
    tags: ["Join strategy", "work_mem", "Hash Join", "Planner hints"],
    performanceNote: { before: "4.2s (200K Nested Loop index lookups)", after: "380ms (single Hash Join pass)" },
  },
  {
    id: "ch44",
    title: "Unnecessary ORDER BY in Subquery",
    difficulty: "easy",
    slowQuery: `SELECT category_id, avg_price
FROM (
  SELECT category_id, AVG(price) AS avg_price
  FROM products
  GROUP BY category_id
  ORDER BY avg_price DESC
) sub
WHERE avg_price > 100
ORDER BY category_id;`,
    issue: "ORDER BY in the subquery is pointless — the outer query re-sorts by a different column anyway",
    hint: "Remove ORDER BY from subqueries unless used with LIMIT. The outer query's sort is the only one that matters.",
    optimizedQuery: `SELECT category_id, AVG(price) AS avg_price
FROM products
GROUP BY category_id
HAVING AVG(price) > 100
ORDER BY category_id;`,
    tags: ["Sort elimination", "Subquery simplification", "Query rewrite"],
    performanceNote: { before: "210ms (double sort: inner + outer)", after: "130ms (single sort)" },
  },
  {
    id: "ch45",
    title: "SELECT FOR UPDATE Lock Scope",
    difficulty: "hard",
    slowQuery: `-- Processing pending orders one at a time
SELECT * FROM orders
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE;
-- Locks ALL pending orders while processing one`,
    issue: "FOR UPDATE locks every row in the result set — blocks other workers from processing any pending order",
    hint: "Use FOR UPDATE SKIP LOCKED with LIMIT 1 to lock only one row and skip already-locked rows.",
    optimizedQuery: `-- Each worker picks one unlocked order
SELECT * FROM orders
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;

-- Process the order, then:
-- UPDATE orders SET status = 'processing' WHERE id = ?;
-- COMMIT;`,
    tags: ["Locking", "SKIP LOCKED", "Concurrent processing", "Queue pattern"],
    performanceNote: { before: "Sequential processing (1 worker)", after: "Parallel processing (N workers, no contention)" },
  },
  {
    id: "ch46",
    title: "GiST Index for Range Queries",
    difficulty: "hard",
    slowQuery: `-- Find all events overlapping a time range
SELECT * FROM events
WHERE start_time <= '2024-03-15 18:00'
  AND end_time >= '2024-03-15 09:00';`,
    issue: "Two-sided range comparison can't be served by a single B-tree index — at best uses one side, then filters",
    hint: "Use PostgreSQL's range types with a GiST index for native overlap queries.",
    optimizedQuery: `-- Add a tsrange column (or use expression index)
ALTER TABLE events
  ADD COLUMN time_range tsrange
  GENERATED ALWAYS AS (tsrange(start_time, end_time)) STORED;

CREATE INDEX idx_events_range ON events USING gist(time_range);

-- Native overlap query
SELECT * FROM events
WHERE time_range && tsrange('2024-03-15 09:00', '2024-03-15 18:00');`,
    tags: ["GiST Index", "Range types", "Overlap queries"],
    performanceNote: { before: "1.8s (Seq Scan, two-sided filter)", after: "12ms (GiST Index Scan, native overlap)" },
  },
  {
    id: "ch47",
    title: "Unnecessary COALESCE Preventing Index",
    difficulty: "medium",
    slowQuery: `SELECT * FROM products
WHERE COALESCE(discount_price, price) < 50;`,
    issue: "COALESCE wraps indexed columns in an expression — no index can match, full table scan required",
    hint: "Split into two OR conditions that each reference a bare column, or use a computed column with an index.",
    optimizedQuery: `-- Option 1: Split into two index-friendly conditions
SELECT * FROM products
WHERE (discount_price IS NOT NULL AND discount_price < 50)
   OR (discount_price IS NULL AND price < 50);

-- Option 2: Expression index
-- CREATE INDEX idx_products_effective_price
--   ON products(COALESCE(discount_price, price));`,
    tags: ["Sargable predicates", "COALESCE", "Expression index"],
    performanceNote: { before: "680ms (Seq Scan, COALESCE per row)", after: "35ms (Bitmap OR of two Index Scans)" },
  },
  {
    id: "ch48",
    title: "Unbounded SELECT Without LIMIT",
    difficulty: "easy",
    slowQuery: `-- API endpoint: GET /api/orders?status=pending
SELECT * FROM orders
WHERE status = 'pending';
-- Returns 150K rows to the application`,
    issue: "No LIMIT clause — returns entire result set, consuming memory on both database and application side",
    hint: "Always add LIMIT for user-facing queries. Implement pagination for large result sets.",
    optimizedQuery: `-- Add LIMIT with a sensible default
SELECT id, total_amount, created_at
FROM orders
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 50;

-- API should enforce max page size
-- and return pagination metadata`,
    tags: ["LIMIT", "API safety", "Memory management"],
    performanceNote: { before: "3.2s (150K rows transferred, 45MB)", after: "8ms (50 rows, 0.015MB)" },
  },
  {
    id: "ch49",
    title: "Table Partitioning for Time-Series Data",
    difficulty: "hard",
    slowQuery: `-- 500M rows in a single table, growing daily
SELECT COUNT(*), SUM(amount)
FROM transactions
WHERE created_at BETWEEN '2024-03-01' AND '2024-03-31';`,
    issue: "Single monolithic table — index scans still touch a huge B-tree, VACUUM takes hours, index bloat compounds",
    hint: "Partition by month so queries only scan the relevant partition. Maintenance operations are per-partition.",
    optimizedQuery: `-- Create partitioned table
CREATE TABLE transactions (
  id bigint,
  amount numeric,
  created_at timestamptz
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE transactions_2024_03
  PARTITION OF transactions
  FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Same query now only scans March partition
SELECT COUNT(*), SUM(amount)
FROM transactions
WHERE created_at BETWEEN '2024-03-01' AND '2024-03-31';
-- Partition pruning: only scans ~15M rows in one partition`,
    tags: ["Table partitioning", "Partition pruning", "Time-series"],
    performanceNote: { before: "28s (Index Scan on 500M-row B-tree)", after: "1.8s (Seq Scan on 15M-row partition)" },
  },
  {
    id: "ch50",
    title: "Parallel Query Underutilization",
    difficulty: "hard",
    slowQuery: `-- Server has 16 cores but query uses only 1
SET max_parallel_workers_per_gather = 0;

SELECT COUNT(*), AVG(total_amount)
FROM orders
WHERE created_at > '2024-01-01';`,
    issue: "Parallel query disabled or under-configured — large aggregation runs on a single CPU core while 15 cores idle",
    hint: "Enable parallel workers and ensure the table is large enough to trigger parallel scan.",
    optimizedQuery: `-- Enable parallel query (per-session or globally)
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.01;
SET min_parallel_table_scan_size = '8MB';

-- Same query now uses Parallel Seq Scan
-- with Partial + Finalize Aggregate
SELECT COUNT(*), AVG(total_amount)
FROM orders
WHERE created_at > '2024-01-01';

-- Plan: Gather (4 workers)
--   → Partial Aggregate
--     → Parallel Seq Scan on orders`,
    tags: ["Parallel query", "Multi-core", "Configuration tuning"],
    performanceNote: { before: "4.8s (single-core Seq Scan)", after: "1.2s (4 parallel workers)" },
  },
];

/* ------------------------------------------------------------------ */
/*  Optimization Concepts Data                                         */
/* ------------------------------------------------------------------ */

const CONCEPTS: OptimizationConcept[] = [
  {
    title: "Index Usage & Design",
    icon: "IDX",
    description: "Indexes are the single most impactful optimization tool. A well-designed index turns O(n) scans into O(log n) lookups.",
    keyPoints: [
      "B-tree indexes for equality and range queries",
      "Composite indexes: leftmost prefix rule matters",
      "Partial indexes for filtered subsets (WHERE active = true)",
      "INCLUDE columns for covering indexes (avoid table lookups)",
    ],
    example: "CREATE INDEX idx_orders_status_date\n  ON orders(status, created_at DESC)\n  INCLUDE (total)\n  WHERE status != 'cancelled';",
  },
  {
    title: "JOIN Order Optimization",
    icon: "JOIN",
    description: "The order of JOINs can dramatically affect performance. The query planner usually handles this, but understanding it helps write better queries.",
    keyPoints: [
      "Start with the most selective (smallest result set) table",
      "Filter rows early with WHERE before joining",
      "Hash Join is fast for large datasets; Nested Loop for small ones",
      "Use EXPLAIN to verify the planner's chosen join strategy",
    ],
  },
  {
    title: "Avoiding SELECT *",
    icon: "SEL",
    description: "SELECT * fetches every column, wasting bandwidth, memory, and preventing index-only scans. Always specify only the columns you need.",
    keyPoints: [
      "Reduces I/O by skipping unused TEXT/BLOB columns",
      "Enables Index Only Scan when all selected columns are in the index",
      "Prevents breakage when table schema changes",
      "Improves clarity: readers know which columns matter",
    ],
  },
  {
    title: "Subquery vs JOIN Performance",
    icon: "SUB",
    description: "Correlated subqueries execute once per outer row (N+1). JOINs process data in a single pass using hash or merge strategies.",
    keyPoints: [
      "Replace correlated subqueries with LEFT JOIN + GROUP BY",
      "Use EXISTS instead of IN for existence checks (short-circuits)",
      "CTEs (WITH) can improve readability but may prevent optimization in older PostgreSQL",
      "Scalar subqueries in SELECT are correlated — watch for N+1",
    ],
  },
  {
    title: "EXPLAIN Plan Reading",
    icon: "EXP",
    description: "EXPLAIN ANALYZE shows the actual execution plan with real timings. It is the most important tool for diagnosing slow queries.",
    keyPoints: [
      "Seq Scan = full table scan (red flag on large tables)",
      "Index Scan = targeted lookup (good)",
      "Index Only Scan = reads only the index (best)",
      "Sort node = explicit sort (can be eliminated with proper index)",
      "Nested Loop = watch for with large outer tables",
    ],
    example: "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)\nSELECT * FROM orders\nWHERE customer_id = 42;",
  },
  {
    title: "Pagination Strategies",
    icon: "PAG",
    description: "OFFSET-based pagination degrades linearly with page depth. Keyset (cursor) pagination delivers consistent performance on any page.",
    keyPoints: [
      "OFFSET N scans and discards N rows every time",
      "Keyset pagination: WHERE id > last_seen_id ORDER BY id LIMIT N",
      "Requires a unique, indexed sort column",
      "Use opaque cursors (base64 encoded) in APIs for flexibility",
    ],
  },
  {
    title: "Query Caching",
    icon: "QC",
    description: "Caching query results at the application layer avoids hitting the database entirely for repeated reads.",
    keyPoints: [
      "Materialized views for expensive aggregations refreshed periodically",
      "Application-level cache (Redis) for hot data with TTL",
      "Prepared statements reduce parse/plan overhead",
      "Connection pooling (PgBouncer) reduces connection overhead",
    ],
  },
  {
    title: "Denormalization Tradeoffs",
    icon: "DEN",
    description: "Denormalization adds redundant data to avoid expensive JOINs at read time. It trades write complexity for read performance.",
    keyPoints: [
      "Add computed/cached columns (e.g., order_count on customers)",
      "Use triggers or application logic to keep denormalized data in sync",
      "JSON columns for semi-structured data that's always read together",
      "Consider read replicas before denormalizing",
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Before vs After Pairs                                              */
/* ------------------------------------------------------------------ */

const BEFORE_AFTER_PAIRS: BeforeAfterPair[] = [
  {
    id: "ba1",
    title: "Full Table Scan vs Index Scan",
    description: "Adding a composite index eliminates both the sequential scan and the sort step.",
    before: {
      query: "SELECT * FROM orders\nWHERE customer_id = 12345\nORDER BY created_at DESC\nLIMIT 20;",
      time: "2,340ms",
      rows: "500,000 scanned",
      plan: "Seq Scan -> Sort -> Limit",
    },
    after: {
      query: "-- After: CREATE INDEX ON orders(customer_id, created_at DESC)\nSELECT * FROM orders\nWHERE customer_id = 12345\nORDER BY created_at DESC\nLIMIT 20;",
      time: "4ms",
      rows: "20 scanned",
      plan: "Index Scan Backward -> Limit",
    },
  },
  {
    id: "ba2",
    title: "Correlated Subquery vs JOIN",
    description: "Replacing the per-row subquery with a single JOIN reduces 100K queries to 1.",
    before: {
      query: "SELECT c.name,\n  (SELECT COUNT(*) FROM orders o\n   WHERE o.customer_id = c.id)\nFROM customers c;",
      time: "12,800ms",
      rows: "100K subqueries executed",
      plan: "Seq Scan customers -> SubPlan (per row)",
    },
    after: {
      query: "SELECT c.name, COUNT(o.id)\nFROM customers c\nLEFT JOIN orders o\n  ON o.customer_id = c.id\nGROUP BY c.id, c.name;",
      time: "340ms",
      rows: "1 Hash Join pass",
      plan: "Hash Join -> HashAggregate",
    },
  },
  {
    id: "ba3",
    title: "OFFSET Pagination vs Keyset Pagination",
    description: "Keyset pagination reads only the rows it returns, regardless of page depth.",
    before: {
      query: "SELECT id, title, created_at\nFROM posts\nORDER BY created_at DESC\nLIMIT 20 OFFSET 20000;",
      time: "8,200ms",
      rows: "20,020 scanned, 20,000 discarded",
      plan: "Index Scan -> Limit (offset 20000)",
    },
    after: {
      query: "SELECT id, title, created_at\nFROM posts\nWHERE created_at < :last_seen\nORDER BY created_at DESC\nLIMIT 20;",
      time: "3ms",
      rows: "20 scanned, 0 discarded",
      plan: "Index Scan -> Limit",
    },
  },
  {
    id: "ba4",
    title: "OR Split into UNION ALL",
    description: "Splitting OR across different indexes lets each branch use its own index.",
    before: {
      query: "SELECT id, name FROM users\nWHERE email = 'a@b.com'\n   OR phone = '+1234567890';",
      time: "890ms",
      rows: "5M rows scanned (Seq Scan)",
      plan: "Seq Scan -> Filter (OR)",
    },
    after: {
      query: "SELECT id, name FROM users\nWHERE email = 'a@b.com'\nUNION ALL\nSELECT id, name FROM users\nWHERE phone = '+1234567890'\n  AND email != 'a@b.com';",
      time: "2ms",
      rows: "2 Index Scans (1-2 rows each)",
      plan: "Append -> Index Scan (email) + Index Scan (phone)",
    },
  },
];

/* ------------------------------------------------------------------ */
/*  EXPLAIN Plan Example Data                                          */
/* ------------------------------------------------------------------ */

const EXAMPLE_PLANS: ExamplePlan[] = [
  {
    id: "ep1",
    title: "Simple Seq Scan with Filter",
    query: "SELECT * FROM orders WHERE total_amount > 500;",
    totalTime: 1243.5,
    root: {
      id: "n1",
      nodeType: "Seq Scan",
      relation: "orders",
      detail: "Filter: (total_amount > 500)",
      cost: { startup: 0.0, total: 12345.67 },
      rows: 48230,
      width: 124,
      actualTime: { startup: 0.021, total: 1243.5 },
      actualRows: 47891,
      loops: 1,
      filter: "total_amount > 500 (rows removed: 452109)",
      children: [],
    },
    annotations: [
      { nodeId: "n1", text: "Sequential scan reads every row in the table — very slow on 500K rows. Add an index on total_amount for range queries.", type: "warning" },
    ],
  },
  {
    id: "ep2",
    title: "Index Scan with Sort + Limit",
    query: "SELECT id, name, created_at FROM customers ORDER BY created_at DESC LIMIT 10;",
    totalTime: 0.089,
    root: {
      id: "n1",
      nodeType: "Limit",
      detail: "Rows: 10",
      cost: { startup: 0.43, total: 1.28 },
      rows: 10,
      width: 48,
      actualTime: { startup: 0.043, total: 0.089 },
      actualRows: 10,
      loops: 1,
      children: [
        {
          id: "n2",
          nodeType: "Index Scan Backward",
          relation: "customers",
          detail: "Using idx_customers_created_at",
          cost: { startup: 0.43, total: 8541.22 },
          rows: 100000,
          width: 48,
          actualTime: { startup: 0.039, total: 0.082 },
          actualRows: 10,
          loops: 1,
          indexCond: "created_at IS NOT NULL",
          children: [],
        },
      ],
    },
    annotations: [
      { nodeId: "n1", text: "Limit stops after 10 rows — combined with Index Scan Backward, this is very efficient.", type: "tip" },
      { nodeId: "n2", text: "Index Scan Backward uses the B-tree index in reverse order, eliminating the need for a separate Sort node.", type: "info" },
    ],
  },
  {
    id: "ep3",
    title: "Hash Join with Aggregation",
    query: "SELECT c.name, COUNT(o.id) AS order_count\nFROM customers c\nLEFT JOIN orders o ON o.customer_id = c.id\nGROUP BY c.id, c.name;",
    totalTime: 342.8,
    root: {
      id: "n1",
      nodeType: "HashAggregate",
      detail: "Group Key: c.id, c.name",
      cost: { startup: 18500.0, total: 19750.0 },
      rows: 100000,
      width: 44,
      actualTime: { startup: 310.2, total: 342.8 },
      actualRows: 100000,
      loops: 1,
      children: [
        {
          id: "n2",
          nodeType: "Hash Left Join",
          detail: "Hash Cond: (c.id = o.customer_id)",
          cost: { startup: 12500.0, total: 17250.0 },
          rows: 500000,
          width: 44,
          actualTime: { startup: 180.5, total: 285.3 },
          actualRows: 487392,
          loops: 1,
          joinType: "Left",
          children: [
            {
              id: "n3",
              nodeType: "Seq Scan",
              relation: "customers",
              detail: "Full table read",
              cost: { startup: 0.0, total: 2134.0 },
              rows: 100000,
              width: 36,
              actualTime: { startup: 0.012, total: 28.4 },
              actualRows: 100000,
              loops: 1,
              children: [],
            },
            {
              id: "n4",
              nodeType: "Hash",
              detail: "Buckets: 65536, Batches: 8, Memory: 24576kB",
              cost: { startup: 8230.0, total: 8230.0 },
              rows: 500000,
              width: 8,
              actualTime: { startup: 145.2, total: 145.2 },
              actualRows: 500000,
              loops: 1,
              children: [
                {
                  id: "n5",
                  nodeType: "Seq Scan",
                  relation: "orders",
                  detail: "Full table read",
                  cost: { startup: 0.0, total: 6120.0 },
                  rows: 500000,
                  width: 8,
                  actualTime: { startup: 0.009, total: 65.8 },
                  actualRows: 500000,
                  loops: 1,
                  children: [],
                },
              ],
            },
          ],
        },
      ],
    },
    annotations: [
      { nodeId: "n1", text: "HashAggregate groups 487K rows into 100K groups. Memory-efficient for moderate cardinality.", type: "info" },
      { nodeId: "n2", text: "Hash Left Join is the optimal strategy here — it builds a hash table from orders and probes with customers.", type: "tip" },
      { nodeId: "n4", text: "Hash uses 24MB across 8 batches. If work_mem is too low, more batches are needed (spilling to disk).", type: "warning" },
    ],
  },
  {
    id: "ep4",
    title: "Nested Loop with Index Lookup",
    query: "SELECT o.id, o.total_amount, c.name\nFROM orders o\nJOIN customers c ON c.id = o.customer_id\nWHERE o.status = 'pending'\n  AND o.created_at > '2024-01-01';",
    totalTime: 12.4,
    root: {
      id: "n1",
      nodeType: "Nested Loop",
      detail: "Inner Join",
      cost: { startup: 0.85, total: 234.5 },
      rows: 156,
      width: 52,
      actualTime: { startup: 0.052, total: 12.4 },
      actualRows: 148,
      loops: 1,
      children: [
        {
          id: "n2",
          nodeType: "Index Scan",
          relation: "orders",
          detail: "Using idx_orders_status_created",
          cost: { startup: 0.43, total: 128.7 },
          rows: 156,
          width: 20,
          actualTime: { startup: 0.035, total: 4.8 },
          actualRows: 148,
          loops: 1,
          indexCond: "status = 'pending' AND created_at > '2024-01-01'",
          children: [],
        },
        {
          id: "n3",
          nodeType: "Index Scan",
          relation: "customers",
          detail: "Using customers_pkey",
          cost: { startup: 0.28, total: 0.67 },
          rows: 1,
          width: 36,
          actualTime: { startup: 0.003, total: 0.048 },
          actualRows: 1,
          loops: 148,
          indexCond: "id = o.customer_id",
          children: [],
        },
      ],
    },
    annotations: [
      { nodeId: "n1", text: "Nested Loop is efficient here because the outer scan returns only 148 rows — each triggers one fast index lookup.", type: "tip" },
      { nodeId: "n2", text: "Composite index on (status, created_at) perfectly serves both the equality and range filter.", type: "info" },
      { nodeId: "n3", text: "148 loops × 0.048ms each = 7.1ms total. Primary key lookup is the fastest possible access.", type: "info" },
    ],
  },
  {
    id: "ep5",
    title: "Bitmap Index Scan (OR condition)",
    query: "SELECT id, name, email FROM users\nWHERE email = 'test@example.com'\n   OR phone = '+1234567890';",
    totalTime: 892.3,
    root: {
      id: "n1",
      nodeType: "Bitmap Heap Scan",
      relation: "users",
      detail: "Recheck Cond: (email = 'test@example.com' OR phone = '+1234567890')",
      cost: { startup: 1245.0, total: 18934.0 },
      rows: 2,
      width: 52,
      actualTime: { startup: 450.2, total: 892.3 },
      actualRows: 2,
      loops: 1,
      children: [
        {
          id: "n2",
          nodeType: "BitmapOr",
          detail: "Combines two bitmap index results",
          cost: { startup: 1244.5, total: 1244.5 },
          rows: 2,
          width: 0,
          actualTime: { startup: 448.1, total: 448.1 },
          actualRows: 0,
          loops: 1,
          children: [
            {
              id: "n3",
              nodeType: "Bitmap Index Scan",
              detail: "Using idx_users_email",
              cost: { startup: 0.0, total: 622.2 },
              rows: 1,
              width: 0,
              actualTime: { startup: 0.0, total: 224.1 },
              actualRows: 1,
              loops: 1,
              indexCond: "email = 'test@example.com'",
              children: [],
            },
            {
              id: "n4",
              nodeType: "Bitmap Index Scan",
              detail: "Using idx_users_phone",
              cost: { startup: 0.0, total: 622.3 },
              rows: 1,
              width: 0,
              actualTime: { startup: 0.0, total: 224.0 },
              actualRows: 1,
              loops: 1,
              indexCond: "phone = '+1234567890'",
              children: [],
            },
          ],
        },
      ],
    },
    annotations: [
      { nodeId: "n1", text: "Bitmap Heap Scan fetches rows after combining two index scans. On large tables, this OR pattern can be slow — consider UNION ALL instead.", type: "warning" },
      { nodeId: "n2", text: "BitmapOr merges two bitmap sets. Each bitmap scan must read its entire index, even for 1 row.", type: "info" },
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Node type classifications for coloring                             */
/* ------------------------------------------------------------------ */

const NODE_TYPE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  "Seq Scan": { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/30" },
  "Index Scan": { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/30" },
  "Index Scan Backward": { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/30" },
  "Index Only Scan": { bg: "bg-green-500/10", text: "text-green-400", border: "border-green-500/30" },
  "Bitmap Heap Scan": { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" },
  "Bitmap Index Scan": { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" },
  BitmapOr: { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" },
  BitmapAnd: { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/30" },
  "Hash Join": { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/30" },
  "Hash Left Join": { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/30" },
  "Merge Join": { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/30" },
  "Nested Loop": { bg: "bg-purple-500/10", text: "text-purple-400", border: "border-purple-500/30" },
  Hash: { bg: "bg-cyan-500/10", text: "text-cyan-400", border: "border-cyan-500/30" },
  Sort: { bg: "bg-orange-500/10", text: "text-orange-400", border: "border-orange-500/30" },
  Limit: { bg: "bg-gray-500/10", text: "text-gray-400", border: "border-gray-500/30" },
  HashAggregate: { bg: "bg-indigo-500/10", text: "text-indigo-400", border: "border-indigo-500/30" },
  GroupAggregate: { bg: "bg-indigo-500/10", text: "text-indigo-400", border: "border-indigo-500/30" },
  Aggregate: { bg: "bg-indigo-500/10", text: "text-indigo-400", border: "border-indigo-500/30" },
};

const getNodeColors = (nodeType: string) =>
  NODE_TYPE_COLORS[nodeType] || { bg: "bg-gray-500/10", text: "text-gray-400", border: "border-gray-500/30" };

/* ------------------------------------------------------------------ */
/*  PlanNodeCard Component                                             */
/* ------------------------------------------------------------------ */

function PlanNodeCard({
  node,
  depth,
  totalTime,
  annotations,
  selectedNode,
  onSelect,
}: {
  node: PlanNode;
  depth: number;
  totalTime: number;
  annotations: ExamplePlan["annotations"];
  selectedNode: string | null;
  onSelect: (id: string) => void;
}) {
  const colors = getNodeColors(node.nodeType);
  const nodeTime = node.actualTime?.total ?? 0;
  const timePct = totalTime > 0 ? (nodeTime / totalTime) * 100 : 0;
  const isSelected = selectedNode === node.id;
  const annotation = annotations.find((a) => a.nodeId === node.id);

  return (
    <div className="relative">
      {/* Connector line */}
      {depth > 0 && (
        <div className="absolute -top-3 left-6 h-3 w-px bg-[var(--color-border)]" />
      )}

      <button
        onClick={() => onSelect(node.id)}
        aria-label={`Plan node: ${node.nodeType}${node.relation ? ` on ${node.relation}` : ""}`}
        aria-expanded={isSelected}
        className={`w-full text-left rounded-lg border p-3 transition-all ${
          isSelected
            ? `${colors.border} ${colors.bg} ring-1 ring-[var(--color-accent)]/30`
            : `border-[var(--color-border)] bg-[var(--color-surface)] hover:${colors.bg}`
        }`}
      >
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-bold ${colors.bg} ${colors.text}`}>
              {node.nodeType}
            </span>
            {node.relation && (
              <span className="text-xs font-medium text-[var(--color-text-primary)] truncate">
                on {node.relation}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 shrink-0">
            {node.actualRows !== undefined && (
              <span className="text-[10px] text-[var(--color-text-muted)]">
                {node.actualRows.toLocaleString()} rows
              </span>
            )}
            {node.actualTime && (
              <span className={`text-[10px] font-bold ${timePct > 50 ? "text-red-400" : timePct > 20 ? "text-amber-400" : "text-emerald-400"}`}>
                {node.actualTime.total.toFixed(1)}ms
              </span>
            )}
          </div>
        </div>

        {/* Time bar */}
        {totalTime > 0 && node.actualTime && (
          <div className="mt-2 h-1 w-full rounded-full bg-[var(--color-background)]">
            <div
              className={`h-full rounded-full transition-all ${timePct > 50 ? "bg-red-500" : timePct > 20 ? "bg-amber-500" : "bg-emerald-500"}`}
              style={{ width: `${Math.max(timePct, 1)}%` }}
            />
          </div>
        )}

        {/* Detail row */}
        <p className="mt-1.5 text-[10px] text-[var(--color-text-muted)] truncate">
          {node.detail}
        </p>

        {/* Extended info when selected */}
        {isSelected && (
          <div className="mt-2 space-y-1 border-t border-[var(--color-border)] pt-2">
            <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-[10px]">
              <div>
                <span className="text-[var(--color-text-muted)]">Est. Cost: </span>
                <span className="text-[var(--color-text-secondary)]">{node.cost.startup.toFixed(2)}..{node.cost.total.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-[var(--color-text-muted)]">Est. Rows: </span>
                <span className="text-[var(--color-text-secondary)]">{node.rows.toLocaleString()}</span>
              </div>
              {node.actualTime && (
                <div>
                  <span className="text-[var(--color-text-muted)]">Actual Time: </span>
                  <span className="text-[var(--color-text-secondary)]">{node.actualTime.startup.toFixed(3)}..{node.actualTime.total.toFixed(3)}ms</span>
                </div>
              )}
              {node.loops !== undefined && node.loops > 1 && (
                <div>
                  <span className="text-[var(--color-text-muted)]">Loops: </span>
                  <span className="text-[var(--color-text-secondary)]">{node.loops}</span>
                </div>
              )}
              <div>
                <span className="text-[var(--color-text-muted)]">Width: </span>
                <span className="text-[var(--color-text-secondary)]">{node.width} bytes</span>
              </div>
            </div>
            {node.indexCond && (
              <p className="text-[10px]">
                <span className="text-emerald-500 font-medium">Index Cond: </span>
                <span className="text-[var(--color-text-secondary)] font-mono">{node.indexCond}</span>
              </p>
            )}
            {node.filter && (
              <p className="text-[10px]">
                <span className="text-amber-500 font-medium">Filter: </span>
                <span className="text-[var(--color-text-secondary)] font-mono">{node.filter}</span>
              </p>
            )}
            {node.sortKey && (
              <p className="text-[10px]">
                <span className="text-orange-500 font-medium">Sort Key: </span>
                <span className="text-[var(--color-text-secondary)] font-mono">{node.sortKey}</span>
              </p>
            )}
          </div>
        )}

        {/* Annotation badge */}
        {annotation && (
          <div className={`mt-2 flex items-start gap-1.5 rounded px-2 py-1 text-[10px] ${
            annotation.type === "warning" ? "bg-amber-500/10 text-amber-400" :
            annotation.type === "tip" ? "bg-emerald-500/10 text-emerald-400" :
            "bg-blue-500/10 text-blue-400"
          }`}>
            <span className="shrink-0 font-bold">
              {annotation.type === "warning" ? "⚠" : annotation.type === "tip" ? "✓" : "ℹ"}
            </span>
            <span>{annotation.text}</span>
          </div>
        )}
      </button>

      {/* Children */}
      {node.children.length > 0 && (
        <div className="ml-6 mt-1 space-y-1 border-l border-[var(--color-border)] pl-4">
          {node.children.map((child) => (
            <PlanNodeCard
              key={child.id}
              node={child}
              depth={depth + 1}
              totalTime={totalTime}
              annotations={annotations}
              selectedNode={selectedNode}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Node Type Legend                                                    */
/* ------------------------------------------------------------------ */

function NodeTypeLegend() {
  const groups = [
    { label: "Scans", types: ["Seq Scan", "Index Scan", "Index Only Scan", "Bitmap Heap Scan"] },
    { label: "Joins", types: ["Hash Join", "Merge Join", "Nested Loop"] },
    { label: "Other", types: ["Sort", "HashAggregate", "Limit", "Hash"] },
  ];

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
      <h4 className="text-[10px] font-semibold uppercase tracking-wider text-[var(--color-text-muted)] mb-2">
        Node Types
      </h4>
      <div className="space-y-2">
        {groups.map((group) => (
          <div key={group.label}>
            <p className="text-[10px] text-[var(--color-text-muted)] mb-1">{group.label}</p>
            <div className="flex flex-wrap gap-1">
              {group.types.map((type) => {
                const colors = getNodeColors(type);
                return (
                  <span key={type} className={`rounded px-1.5 py-0.5 text-[9px] font-medium ${colors.bg} ${colors.text}`}>
                    {type}
                  </span>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-3 border-t border-[var(--color-border)] pt-2">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-[var(--color-text-muted)] mb-1.5">
          Time Cost
        </p>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1">
            <span className="h-2 w-4 rounded-full bg-emerald-500" />
            <span className="text-[9px] text-[var(--color-text-muted)]">&lt;20%</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="h-2 w-4 rounded-full bg-amber-500" />
            <span className="text-[9px] text-[var(--color-text-muted)]">20-50%</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="h-2 w-4 rounded-full bg-red-500" />
            <span className="text-[9px] text-[var(--color-text-muted)]">&gt;50%</span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Page Component                                                     */
/* ------------------------------------------------------------------ */

type TabKey = "challenges" | "concepts" | "compare" | "explain";

export default function OptimizationPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("challenges");
  const [revealedSolutions, setRevealedSolutions] = useState<Set<string>>(new Set());
  const [revealedHints, setRevealedHints] = useState<Set<string>>(new Set());
  const [tagFilter, setTagFilter] = useState<string>("all");
  const [expandedPair, setExpandedPair] = useState<string | null>(null);
  const [selectedPlan, setSelectedPlan] = useState<string>(EXAMPLE_PLANS[0].id);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const allTags = useMemo(() => {
    const tags = new Set<string>();
    CHALLENGES.forEach((c) => c.tags.forEach((t) => tags.add(t)));
    return Array.from(tags).sort();
  }, []);

  const filteredChallenges = useMemo(() => {
    if (tagFilter === "all") return CHALLENGES;
    return CHALLENGES.filter((c) => c.tags.includes(tagFilter));
  }, [tagFilter]);

  const activePlan = useMemo(() => EXAMPLE_PLANS.find((p) => p.id === selectedPlan) || EXAMPLE_PLANS[0], [selectedPlan]);

  const toggleSolution = (id: string) => {
    setRevealedSolutions((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleHint = (id: string) => {
    setRevealedHints((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleSelectNode = useCallback((id: string) => {
    setSelectedNode((prev) => (prev === id ? null : id));
  }, []);

  const TABS = [
    { key: "challenges" as const, label: "Optimization Challenges" },
    { key: "explain" as const, label: "EXPLAIN Visualizer" },
    { key: "concepts" as const, label: "Key Concepts" },
    { key: "compare" as const, label: "Before vs After" },
  ];

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Query Optimization
        </h1>
        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
          Learn to write efficient SQL by identifying bottlenecks, reading EXPLAIN plans, designing
          indexes, and rewriting slow queries. Practice with real-world optimization challenges.
        </p>
      </div>

      {/* Tabs */}
      <div role="tablist" aria-label="Optimization sections" className="mt-6 flex items-center gap-1 border-b border-[var(--color-border)] overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            role="tab"
            aria-selected={activeTab === tab.key}
            aria-label={tab.label}
            className={`whitespace-nowrap border-b-2 px-4 py-2 text-sm font-medium transition-colors ${
              activeTab === tab.key
                ? "border-[var(--color-accent)] text-[var(--color-accent)]"
                : "border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ============================================================ */}
      {/*  Challenges Tab                                               */}
      {/* ============================================================ */}
      {activeTab === "challenges" && (
        <div className="mt-6">
          {/* Tag filter */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setTagFilter("all")}
              aria-label={`Show all challenges (${CHALLENGES.length})`}
              aria-pressed={tagFilter === "all"}
              className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                tagFilter === "all"
                  ? "bg-[var(--color-accent)] text-white"
                  : "bg-[var(--color-surface)] text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
              }`}
            >
              All ({CHALLENGES.length})
            </button>
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setTagFilter(tag)}
                aria-label={`Filter by ${tag}`}
                aria-pressed={tagFilter === tag}
                className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                  tagFilter === tag
                    ? "bg-[var(--color-accent)] text-white"
                    : "bg-[var(--color-surface)] text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
                }`}
              >
                {tag}
              </button>
            ))}
          </div>

          {/* Challenge cards */}
          <div className="mt-6 space-y-4">
            {filteredChallenges.map((challenge) => (
              <div
                key={challenge.id}
                className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] overflow-hidden"
              >
                <div className="p-5">
                  <div className="flex items-center gap-3 flex-wrap">
                    <Badge variant={challenge.difficulty}>{challenge.difficulty}</Badge>
                    <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                      {challenge.title}
                    </h3>
                  </div>

                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {challenge.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full bg-[var(--color-accent)]/10 px-2 py-0.5 text-[10px] font-medium text-[var(--color-accent)]"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="mt-3 flex items-start gap-2 rounded-lg bg-red-500/5 border border-red-500/10 px-3 py-2">
                    <span className="mt-0.5 text-red-500 text-xs font-bold shrink-0">!</span>
                    <p className="text-xs text-red-400">{challenge.issue}</p>
                  </div>

                  <div className="mt-4">
                    <h4 className="text-xs font-semibold text-red-500 mb-2">Slow Query</h4>
                    <pre className="overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-red-700 dark:text-red-300">
                      <code>{challenge.slowQuery}</code>
                    </pre>
                  </div>

                  {challenge.performanceNote && (
                    <div className="mt-3 grid grid-cols-2 gap-3">
                      <div className="rounded-lg bg-red-500/5 border border-red-500/10 px-3 py-2">
                        <p className="text-[10px] font-medium text-red-400 uppercase tracking-wider">Before</p>
                        <p className="mt-0.5 text-xs text-[var(--color-text-secondary)]">{challenge.performanceNote.before}</p>
                      </div>
                      <div className="rounded-lg bg-emerald-500/5 border border-emerald-500/10 px-3 py-2">
                        <p className="text-[10px] font-medium text-emerald-400 uppercase tracking-wider">After</p>
                        <p className="mt-0.5 text-xs text-[var(--color-text-secondary)]">{challenge.performanceNote.after}</p>
                      </div>
                    </div>
                  )}

                  <div className="mt-4">
                    <button
                      onClick={() => toggleHint(challenge.id)}
                      aria-label={revealedHints.has(challenge.id) ? "Hide hint" : "Show hint"}
                      aria-expanded={revealedHints.has(challenge.id)}
                      className="text-sm font-medium text-[var(--color-accent)] hover:underline"
                    >
                      {revealedHints.has(challenge.id) ? "Hide Hint" : "Show Hint"}
                    </button>
                    {revealedHints.has(challenge.id) && (
                      <p className="mt-2 rounded-lg bg-[var(--color-background)] p-3 text-sm text-[var(--color-text-secondary)]">
                        {challenge.hint}
                      </p>
                    )}
                  </div>

                  <div className="mt-3">
                    <button
                      onClick={() => toggleSolution(challenge.id)}
                      aria-label={revealedSolutions.has(challenge.id) ? "Hide optimized solution" : "Reveal optimized solution"}
                      aria-expanded={revealedSolutions.has(challenge.id)}
                      className={`rounded-md px-4 py-2 text-xs font-medium transition-colors ${
                        revealedSolutions.has(challenge.id)
                          ? "bg-emerald-600 text-white hover:bg-emerald-700"
                          : "bg-[var(--color-background)] text-emerald-500 border border-emerald-500/30 hover:bg-emerald-500/10"
                      }`}
                    >
                      {revealedSolutions.has(challenge.id) ? "Hide Solution" : "Reveal Optimized Solution"}
                    </button>

                    {revealedSolutions.has(challenge.id) && (
                      <div className="mt-3">
                        <h4 className="text-xs font-semibold text-emerald-500 mb-2">Optimized Query</h4>
                        <pre className="overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-emerald-700 dark:text-emerald-300">
                          <code>{challenge.optimizedQuery}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {filteredChallenges.length === 0 && (
              <div className="flex h-40 items-center justify-center rounded-xl border border-dashed border-[var(--color-border)]">
                <p className="text-sm text-[var(--color-text-muted)]">
                  No challenges match the selected tag.
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/*  EXPLAIN Visualizer Tab                                       */}
      {/* ============================================================ */}
      {activeTab === "explain" && (
        <div className="mt-6">
          {/* Intro */}
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 mb-6">
            <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
              How to Read EXPLAIN Plans
            </h2>
            <p className="mt-2 text-xs text-[var(--color-text-secondary)] leading-relaxed">
              PostgreSQL&apos;s EXPLAIN ANALYZE shows you exactly how the database executes a query.
              The plan is a tree of nodes — each node represents an operation (scan, join, sort, etc.).
              Data flows from leaf nodes up to the root. Click any node below to see detailed metrics.
            </p>
            <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-2 text-[10px]">
              <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                <span className="font-semibold text-[var(--color-text-primary)]">Cost</span>
                <p className="text-[var(--color-text-muted)]">Estimated effort in arbitrary units</p>
              </div>
              <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                <span className="font-semibold text-[var(--color-text-primary)]">Rows</span>
                <p className="text-[var(--color-text-muted)]">Number of rows output by the node</p>
              </div>
              <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                <span className="font-semibold text-[var(--color-text-primary)]">Time</span>
                <p className="text-[var(--color-text-muted)]">Actual wall-clock time in ms</p>
              </div>
              <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                <span className="font-semibold text-[var(--color-text-primary)]">Loops</span>
                <p className="text-[var(--color-text-muted)]">Times node was executed</p>
              </div>
            </div>
          </div>

          {/* Plan selector */}
          <div className="flex flex-wrap gap-2 mb-6">
            {EXAMPLE_PLANS.map((plan) => (
              <button
                key={plan.id}
                onClick={() => { setSelectedPlan(plan.id); setSelectedNode(null); }}
                aria-label={`View plan: ${plan.title}`}
                aria-pressed={selectedPlan === plan.id}
                className={`rounded-lg px-3 py-2 text-xs font-medium transition-colors ${
                  selectedPlan === plan.id
                    ? "bg-[var(--color-accent)] text-white"
                    : "bg-[var(--color-surface)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent)]/30"
                }`}
              >
                {plan.title}
              </button>
            ))}
          </div>

          {/* Active plan display */}
          <div className="grid gap-6 lg:grid-cols-[1fr_220px]">
            <div>
              {/* Query */}
              <div className="mb-4">
                <h3 className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-2">
                  Query
                </h3>
                <pre className="overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-blue-700 dark:text-blue-300">
                  <code>{activePlan.query}</code>
                </pre>
              </div>

              {/* Summary stats */}
              <div className="mb-4 flex items-center gap-4">
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2">
                  <span className="text-[10px] text-[var(--color-text-muted)]">Total Time</span>
                  <p className={`text-sm font-bold ${activePlan.totalTime > 500 ? "text-red-400" : activePlan.totalTime > 50 ? "text-amber-400" : "text-emerald-400"}`}>
                    {activePlan.totalTime.toFixed(1)}ms
                  </p>
                </div>
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2">
                  <span className="text-[10px] text-[var(--color-text-muted)]">Root Node</span>
                  <p className="text-sm font-bold text-[var(--color-text-primary)]">{activePlan.root.nodeType}</p>
                </div>
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2">
                  <span className="text-[10px] text-[var(--color-text-muted)]">Result Rows</span>
                  <p className="text-sm font-bold text-[var(--color-text-primary)]">
                    {(activePlan.root.actualRows ?? activePlan.root.rows).toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Plan tree */}
              <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] p-4">
                <h3 className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-3">
                  Execution Plan Tree
                </h3>
                <div className="space-y-1">
                  <PlanNodeCard
                    node={activePlan.root}
                    depth={0}
                    totalTime={activePlan.totalTime}
                    annotations={activePlan.annotations}
                    selectedNode={selectedNode}
                    onSelect={handleSelectNode}
                  />
                </div>
              </div>

              {/* Reading guide */}
              <div className="mt-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-semibold text-[var(--color-text-primary)] mb-2">
                  Reading This Plan
                </h3>
                <ul className="space-y-1.5 text-xs text-[var(--color-text-secondary)]">
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    <span>Data flows bottom-up: leaf nodes (scans) feed into parent nodes (joins, aggregates).</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    <span>The colored time bar shows what percentage of total time each node consumed.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    <span>Click a node to expand its detailed metrics: costs, filters, index conditions.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    <span>Look for red bars (hot spots) and Seq Scan on large tables — those are optimization targets.</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-4">
              <NodeTypeLegend />

              {/* Quick reference */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
                <h4 className="text-[10px] font-semibold uppercase tracking-wider text-[var(--color-text-muted)] mb-2">
                  Quick Reference
                </h4>
                <div className="space-y-2 text-[10px]">
                  <div>
                    <span className="font-semibold text-red-400">Seq Scan</span>
                    <p className="text-[var(--color-text-muted)]">Reads every row. Slow on large tables.</p>
                  </div>
                  <div>
                    <span className="font-semibold text-emerald-400">Index Scan</span>
                    <p className="text-[var(--color-text-muted)]">Uses B-tree to find specific rows. Fast.</p>
                  </div>
                  <div>
                    <span className="font-semibold text-blue-400">Hash Join</span>
                    <p className="text-[var(--color-text-muted)]">Builds hash table for efficient joining.</p>
                  </div>
                  <div>
                    <span className="font-semibold text-purple-400">Nested Loop</span>
                    <p className="text-[var(--color-text-muted)]">Best for small outer tables + indexed inner.</p>
                  </div>
                  <div>
                    <span className="font-semibold text-orange-400">Sort</span>
                    <p className="text-[var(--color-text-muted)]">Explicit sort step. Can be avoided with indexes.</p>
                  </div>
                  <div>
                    <span className="font-semibold text-amber-400">Bitmap Scan</span>
                    <p className="text-[var(--color-text-muted)]">Two-phase: build bitmap, then fetch rows.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/*  Concepts Tab                                                 */}
      {/* ============================================================ */}
      {activeTab === "concepts" && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {CONCEPTS.map((concept) => (
            <div
              key={concept.title}
              className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--color-accent)]/10 text-xs font-bold text-[var(--color-accent)]">
                  {concept.icon}
                </span>
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                  {concept.title}
                </h3>
              </div>

              <p className="mt-3 text-xs text-[var(--color-text-secondary)] leading-relaxed">
                {concept.description}
              </p>

              <ul className="mt-3 space-y-1.5">
                {concept.keyPoints.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    {point}
                  </li>
                ))}
              </ul>

              {concept.example && (
                <pre className="mt-3 overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-3 text-[10px] leading-relaxed text-blue-700 dark:text-blue-300">
                  <code>{concept.example}</code>
                </pre>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ============================================================ */}
      {/*  Before vs After Tab                                          */}
      {/* ============================================================ */}
      {activeTab === "compare" && (
        <div className="mt-6 space-y-4">
          <p className="text-sm text-[var(--color-text-secondary)]">
            Side-by-side comparisons of slow queries and their optimized versions, with execution plan
            annotations and performance metrics.
          </p>

          {BEFORE_AFTER_PAIRS.map((pair) => (
            <div
              key={pair.id}
              className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] overflow-hidden"
            >
              <button
                onClick={() => setExpandedPair(expandedPair === pair.id ? null : pair.id)}
                aria-label={`${pair.title}: ${pair.before.time} to ${pair.after.time}`}
                aria-expanded={expandedPair === pair.id}
                className="flex w-full items-center justify-between p-5 text-left"
              >
                <div>
                  <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">{pair.title}</h3>
                  <p className="mt-1 text-xs text-[var(--color-text-muted)]">{pair.description}</p>
                </div>
                <div className="flex items-center gap-3 shrink-0 ml-4">
                  <span className="rounded-md bg-red-500/10 px-2 py-1 text-[10px] font-bold text-red-400">
                    {pair.before.time}
                  </span>
                  <span className="text-xs text-[var(--color-text-muted)]">-&gt;</span>
                  <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-[10px] font-bold text-emerald-400">
                    {pair.after.time}
                  </span>
                  <svg
                    className={`h-4 w-4 text-[var(--color-text-muted)] transition-transform ${expandedPair === pair.id ? "rotate-180" : ""}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>

              {expandedPair === pair.id && (
                <div className="border-t border-[var(--color-border)] px-5 pb-5 pt-4">
                  <div className="grid gap-4 lg:grid-cols-2">
                    {/* Before */}
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-red-500" />
                        <h4 className="text-xs font-semibold text-red-500 uppercase tracking-wider">Before</h4>
                      </div>
                      <pre className="overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-red-700 dark:text-red-300">
                        <code>{pair.before.query}</code>
                      </pre>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                          <p className="text-[10px] text-[var(--color-text-muted)]">Execution Time</p>
                          <p className="text-xs font-bold text-red-400">{pair.before.time}</p>
                        </div>
                        <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                          <p className="text-[10px] text-[var(--color-text-muted)]">Rows Processed</p>
                          <p className="text-xs font-bold text-red-400">{pair.before.rows}</p>
                        </div>
                      </div>
                      <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                        <p className="text-[10px] text-[var(--color-text-muted)]">Execution Plan</p>
                        <p className="mt-0.5 text-xs font-mono text-[var(--color-text-secondary)]">{pair.before.plan}</p>
                      </div>
                    </div>

                    {/* After */}
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-emerald-500" />
                        <h4 className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">After</h4>
                      </div>
                      <pre className="overflow-x-auto rounded-lg bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-emerald-700 dark:text-emerald-300">
                        <code>{pair.after.query}</code>
                      </pre>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                          <p className="text-[10px] text-[var(--color-text-muted)]">Execution Time</p>
                          <p className="text-xs font-bold text-emerald-400">{pair.after.time}</p>
                        </div>
                        <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                          <p className="text-[10px] text-[var(--color-text-muted)]">Rows Processed</p>
                          <p className="text-xs font-bold text-emerald-400">{pair.after.rows}</p>
                        </div>
                      </div>
                      <div className="rounded-lg bg-[var(--color-background)] px-3 py-2">
                        <p className="text-[10px] text-[var(--color-text-muted)]">Execution Plan</p>
                        <p className="mt-0.5 text-xs font-mono text-[var(--color-text-secondary)]">{pair.after.plan}</p>
                      </div>
                    </div>
                  </div>

                  {/* Speedup callout */}
                  <div className="mt-4 flex items-center justify-center gap-2 rounded-lg bg-emerald-500/5 border border-emerald-500/10 px-4 py-3">
                    <span className="text-xs text-[var(--color-text-muted)]">Performance improvement:</span>
                    <span className="text-sm font-bold text-emerald-400">
                      {Math.round(
                        parseFloat(pair.before.time.replace(/,/g, "")) /
                          parseFloat(pair.after.time.replace(/,/g, ""))
                      )}x faster
                    </span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
