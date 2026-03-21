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
