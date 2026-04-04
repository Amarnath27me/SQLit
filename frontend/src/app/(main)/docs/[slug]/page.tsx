"use client";

import { useParams } from "next/navigation";
import Link from "next/link";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface DocTopic {
  title: string;
  section: string;
  concept: string[];
  syntax: string;
  example: string;
  pitfalls: string[];
  tryItSlug: string;
  tryItLabel: string;
}

/* ------------------------------------------------------------------ */
/*  Ordered list of all slugs (drives prev / next navigation)          */
/* ------------------------------------------------------------------ */

const SLUG_ORDER: string[] = [
  // Fundamentals
  "select",
  "where",
  "operators",
  "order-by",
  "limit-offset",
  "distinct",
  // Aggregations
  "count",
  "sum-avg",
  "min-max",
  "group-by",
  "having",
  // Joins
  "inner-join",
  "left-join",
  "right-join",
  "full-join",
  "self-join",
  "cross-join",
  // Subqueries
  "scalar-subquery",
  "derived-tables",
  "correlated",
  "exists",
  // Window Functions
  "row-number",
  "rank-dense-rank",
  "lag-lead",
  "running-totals",
  "ntile",
  // Advanced
  "cte",
  "recursive-cte",
  "case",
  "union",
  "date-functions",
  "string-functions",
];

/* ------------------------------------------------------------------ */
/*  Content keyed by slug                                              */
/* ------------------------------------------------------------------ */

const DOCS: Record<string, DocTopic> = {
  /* ================================================================ */
  /*  FUNDAMENTALS                                                     */
  /* ================================================================ */

  select: {
    title: "SELECT Statements",
    section: "Fundamentals",
    concept: [
      "The SELECT statement is the cornerstone of SQL. Every time you want to read data from a database you will write a SELECT. At its simplest it retrieves one or more columns from a single table, but it can also compute expressions, call functions, and combine data from many sources.",
      "A basic SELECT has two required parts: the column list (what you want) and the FROM clause (where to get it). You can select all columns with the asterisk (*) shorthand, but in production code it is best practice to list columns explicitly so your queries remain predictable when the schema changes.",
      "SELECT also supports computed columns and literal values. You can perform arithmetic, concatenate strings, and apply built-in functions directly in the column list, giving each result an alias for clarity.",
    ],
    syntax: `-- Select specific columns
SELECT column1, column2
FROM table_name;

-- Select all columns
SELECT * FROM table_name;

-- Computed columns with aliases
SELECT
  first_name,
  last_name,
  unit_price * quantity AS line_total
FROM order_items;`,
    example: `-- List every product with its computed sale price (10% off)
SELECT
  product_id,
  name,
  price,
  ROUND(price * 0.90, 2) AS sale_price
FROM products;

-- Combine first and last name for customer display
SELECT
  customer_id,
  first_name || ' ' || last_name AS full_name,
  email
FROM customers;`,
    pitfalls: [
      "Avoid SELECT * in application code — it fetches unnecessary data and breaks when columns are added or removed.",
      "Remember that column aliases defined in SELECT cannot be used in the WHERE clause of the same query; the alias is resolved after filtering.",
      "When mixing aggregate functions with non-aggregated columns you must add GROUP BY — otherwise the query will error.",
    ],
    tryItSlug: "list-all-products",
    tryItLabel: "Practice SELECT basics",
  },

  where: {
    title: "WHERE Clause",
    section: "Fundamentals",
    concept: [
      "The WHERE clause filters rows before they appear in your result set. It evaluates a Boolean expression for every row in the source table and only keeps rows where the expression is true. This is the primary mechanism for narrowing down large datasets to exactly the records you need.",
      "Conditions in WHERE can use comparison operators (=, <>, <, >, <=, >=), pattern matching (LIKE, ILIKE), range checks (BETWEEN), set membership (IN), and NULL checks (IS NULL, IS NOT NULL). You can combine multiple conditions with AND and OR, and negate them with NOT.",
      "Because WHERE runs before GROUP BY and before SELECT aliases are resolved, it operates on raw table columns and cannot reference aggregates or column aliases. If you need to filter grouped results, use HAVING instead.",
    ],
    syntax: `-- Basic comparison
SELECT * FROM orders
WHERE status = 'shipped';

-- Multiple conditions
SELECT * FROM products
WHERE price >= 10
  AND price <= 100
  AND category = 'Electronics';

-- Pattern matching & NULL check
SELECT * FROM customers
WHERE email LIKE '%@gmail.com'
  AND phone IS NOT NULL;`,
    example: `-- Find high-value orders placed in the last 30 days
SELECT
  order_id,
  customer_id,
  total_amount,
  order_date
FROM orders
WHERE total_amount > 500
  AND order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Products that are either on sale or in a specific category
SELECT name, price, category
FROM products
WHERE category IN ('Books', 'Music')
   OR price < 5.00;`,
    pitfalls: [
      "Use IS NULL / IS NOT NULL instead of = NULL. Comparing with = NULL always returns unknown, not true or false.",
      "Be careful with OR precedence — wrap OR groups in parentheses when combining with AND to avoid unexpected results.",
      "LIKE patterns are case-sensitive in many databases. Use ILIKE (PostgreSQL) or LOWER() for case-insensitive matching.",
    ],
    tryItSlug: "customers-from-specific-state",
    tryItLabel: "Practice WHERE filtering",
  },

  operators: {
    title: "Operators",
    section: "Fundamentals",
    concept: [
      "SQL operators let you build rich conditions beyond simple equality checks. Logical operators AND, OR, and NOT combine or negate conditions. AND requires both sides to be true, OR requires at least one, and NOT flips the truth value. Proper use of parentheses is essential when mixing AND and OR because AND has higher precedence.",
      "The IN operator checks whether a value exists in a list or subquery result set — it is a clean alternative to writing many OR conditions. BETWEEN provides inclusive range checks and works with numbers, dates, and strings. LIKE enables pattern matching with % (any sequence of characters) and _ (single character) as wildcards.",
      "Understanding operator precedence prevents subtle bugs. SQL evaluates NOT first, then AND, then OR. When in doubt, add parentheses to make intent explicit. This is especially important in WHERE clauses with mixed logic.",
    ],
    syntax: `-- IN operator
SELECT * FROM products
WHERE category IN ('Electronics', 'Books', 'Games');

-- BETWEEN (inclusive on both ends)
SELECT * FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31';

-- LIKE with wildcards
SELECT * FROM customers
WHERE last_name LIKE 'Sm%';     -- starts with 'Sm'

-- NOT combined with IN
SELECT * FROM products
WHERE category NOT IN ('Archived', 'Draft');`,
    example: `-- Find customers whose name starts with 'J' and live in
-- New York or California, with orders over $100
SELECT
  c.first_name,
  c.last_name,
  c.state,
  o.total_amount
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE c.first_name LIKE 'J%'
  AND c.state IN ('NY', 'CA')
  AND o.total_amount > 100;

-- Products priced between $20 and $50,
-- excluding the 'Clearance' category
SELECT name, price, category
FROM products
WHERE price BETWEEN 20 AND 50
  AND category <> 'Clearance';`,
    pitfalls: [
      "BETWEEN is inclusive on both ends. BETWEEN 1 AND 10 includes 1 and 10. This catches many people off guard with date ranges.",
      "IN with a NULL in the list can produce unexpected results — NULL IN (1, 2, NULL) is unknown, not true.",
      "LIKE '%term%' cannot use a regular index and forces a full table scan. For large tables consider full-text search.",
    ],
    tryItSlug: "products-in-price-range",
    tryItLabel: "Practice operators and conditions",
  },

  "order-by": {
    title: "ORDER BY",
    section: "Fundamentals",
    concept: [
      "Without ORDER BY, SQL does not guarantee any particular row order. The database engine is free to return rows in whatever sequence is most efficient. If your application relies on a specific order — most recent first, alphabetical, lowest price — you must specify ORDER BY explicitly.",
      "You can sort by one or more columns or expressions. Each sort key can be ASC (ascending, the default) or DESC (descending). When you sort by multiple columns, the database orders by the first key and uses subsequent keys only to break ties.",
      "ORDER BY is one of the last clauses evaluated in query processing. This means you can reference column aliases from the SELECT list, ordinal positions (ORDER BY 1), and even expressions that do not appear in SELECT. However, using ordinal positions is discouraged because it makes queries fragile when columns are reordered.",
    ],
    syntax: `-- Single column, descending
SELECT * FROM products
ORDER BY price DESC;

-- Multiple columns
SELECT * FROM orders
ORDER BY customer_id ASC, order_date DESC;

-- Using a SELECT alias
SELECT
  name,
  price * quantity AS line_total
FROM order_items
ORDER BY line_total DESC;`,
    example: `-- Top 10 most expensive products
SELECT name, price, category
FROM products
ORDER BY price DESC
LIMIT 10;

-- Customer orders sorted by date, then amount
SELECT
  c.first_name || ' ' || c.last_name AS customer,
  o.order_date,
  o.total_amount
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC, o.total_amount DESC;`,
    pitfalls: [
      "NULL values sort differently across databases. In PostgreSQL NULLs come last for ASC; in MySQL they come first. Use NULLS FIRST / NULLS LAST to be explicit.",
      "ORDER BY with large result sets can be expensive — make sure to combine with LIMIT when you only need the top N rows.",
      "Avoid ORDER BY 1, 2 in production queries — positional references break silently when someone adds a column.",
    ],
    tryItSlug: "recent-orders-top-ten",
    tryItLabel: "Practice ORDER BY sorting",
  },

  "limit-offset": {
    title: "LIMIT & OFFSET",
    section: "Fundamentals",
    concept: [
      "LIMIT restricts the number of rows returned by a query, and OFFSET skips a specified number of rows before starting to return results. Together they enable pagination — showing results page by page — which is essential for any user-facing application that deals with large datasets.",
      "LIMIT is applied after ORDER BY, so you can reliably fetch the top-N or bottom-N rows. OFFSET tells the database how many rows to skip. For example, page 3 with 20 rows per page uses LIMIT 20 OFFSET 40. Note that the SQL standard uses FETCH FIRST N ROWS ONLY as an alternative syntax, but LIMIT/OFFSET is universally supported.",
      "While convenient, OFFSET-based pagination has a performance drawback: the database must still read and discard all the offset rows. For deep pagination (e.g., page 5000) consider keyset pagination — filtering by the last-seen value of the ORDER BY column — which is much more efficient.",
    ],
    syntax: `-- Return only 10 rows
SELECT * FROM products
ORDER BY price DESC
LIMIT 10;

-- Skip first 20 rows, return next 10 (page 3)
SELECT * FROM products
ORDER BY price DESC
LIMIT 10 OFFSET 20;

-- SQL standard alternative
SELECT * FROM products
ORDER BY price DESC
FETCH FIRST 10 ROWS ONLY;`,
    example: `-- Page 2 of orders (10 per page), most recent first
SELECT
  order_id,
  customer_id,
  total_amount,
  order_date
FROM orders
ORDER BY order_date DESC
LIMIT 10 OFFSET 10;

-- Keyset pagination (more efficient for deep pages)
SELECT order_id, order_date, total_amount
FROM orders
WHERE order_date < '2024-06-15'  -- last seen value
ORDER BY order_date DESC
LIMIT 10;`,
    pitfalls: [
      "Always use ORDER BY with LIMIT. Without it the rows you get back are non-deterministic and may change between executions.",
      "Large OFFSET values degrade performance because the database still processes all skipped rows. Use keyset/cursor pagination for deep pages.",
      "If two rows share the same ORDER BY value, LIMIT may return different subsets between runs. Add a tiebreaker column (e.g., primary key) to make results deterministic.",
    ],
    tryItSlug: "recent-orders-top-ten",
    tryItLabel: "Practice LIMIT & OFFSET",
  },

  distinct: {
    title: "DISTINCT",
    section: "Fundamentals",
    concept: [
      "DISTINCT removes duplicate rows from the result set. When you SELECT DISTINCT, the database compares all selected columns across every row and collapses identical rows into one. It is a simple, powerful way to answer questions like \"which categories exist?\" or \"which cities have customers?\".",
      "DISTINCT operates on the entire selected row, not just one column. If you SELECT DISTINCT city, state, the combination of city and state must be unique — the same city in two different states will produce two rows. For counting unique values within aggregations, use COUNT(DISTINCT column) instead.",
      "Be mindful that DISTINCT requires a sort or hash operation to identify duplicates, which adds processing cost. If you find yourself applying DISTINCT to fix a query that returns too many rows, the root cause is often a missing or incorrect JOIN condition rather than a genuine need for deduplication.",
    ],
    syntax: `-- Unique values from one column
SELECT DISTINCT category FROM products;

-- Unique combinations
SELECT DISTINCT city, state FROM customers;

-- Count distinct values
SELECT COUNT(DISTINCT customer_id) AS unique_buyers
FROM orders;`,
    example: `-- Find all unique product categories in the catalog
SELECT DISTINCT category
FROM products
ORDER BY category;

-- How many distinct customers ordered each month?
SELECT
  DATE_TRUNC('month', order_date) AS month,
  COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;`,
    pitfalls: [
      "DISTINCT on many columns can be slow — the database must compare every column for every row pair. Consider whether GROUP BY achieves the same result more efficiently.",
      "If your DISTINCT query unexpectedly returns duplicates, check whether you are selecting columns with invisible differences like trailing spaces or different cases.",
      "DISTINCT and GROUP BY often produce the same output, but GROUP BY allows aggregate functions while DISTINCT does not.",
    ],
    tryItSlug: "unique-customer-cities",
    tryItLabel: "Practice DISTINCT queries",
  },

  /* ================================================================ */
  /*  AGGREGATIONS                                                     */
  /* ================================================================ */

  count: {
    title: "COUNT",
    section: "Aggregations",
    concept: [
      "COUNT is the most frequently used aggregate function. COUNT(*) counts every row in the group, including rows with NULL values. COUNT(column) counts only non-NULL values in that column. COUNT(DISTINCT column) counts unique non-NULL values. Understanding these three variants is essential for accurate reporting.",
      "COUNT is often combined with GROUP BY to produce per-group tallies — for example, the number of orders per customer or the number of products per category. Without GROUP BY, COUNT collapses the entire table into a single summary row.",
      "Because COUNT(*) includes NULLs and COUNT(column) excludes them, the two can return different numbers for the same table. This difference is not a bug; it is a tool. When you specifically want to know how many rows have a value in a nullable column, COUNT(column) is the right choice.",
    ],
    syntax: `-- Count all rows
SELECT COUNT(*) FROM orders;

-- Count non-NULL values
SELECT COUNT(phone) FROM customers;

-- Count distinct values
SELECT COUNT(DISTINCT category) FROM products;

-- Count per group
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;`,
    example: `-- How many orders has each customer placed?
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer,
  COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY order_count DESC;

-- Monthly order volume
SELECT
  DATE_TRUNC('month', order_date) AS month,
  COUNT(*) AS total_orders,
  COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;`,
    pitfalls: [
      "COUNT(*) vs COUNT(column): they are NOT interchangeable. COUNT(*) counts all rows; COUNT(column) ignores NULLs. Pick the one that matches your intent.",
      "When using LEFT JOIN with COUNT, count the right-side column (e.g., COUNT(o.order_id)) not COUNT(*) — otherwise customers with zero orders will show a count of 1.",
      "COUNT(DISTINCT ...) can be slow on very large tables. Approximate alternatives like HyperLogLog are available in some databases.",
    ],
    tryItSlug: "total-number-of-orders",
    tryItLabel: "Practice COUNT queries",
  },

  "sum-avg": {
    title: "SUM & AVG",
    section: "Aggregations",
    concept: [
      "SUM adds up all non-NULL values in a numeric column, while AVG computes the arithmetic mean. These two aggregates are the workhorses of financial and analytical reporting — revenue totals, average order values, cost summaries, and more.",
      "Both functions ignore NULL values. This means AVG divides by the number of non-NULL values, not the total row count. If you need NULLs to count as zero in your average, wrap the column in COALESCE(column, 0) before aggregating. SUM of an all-NULL group returns NULL, not zero — use COALESCE(SUM(column), 0) to guard against this.",
      "SUM and AVG can operate on expressions, not just raw columns. You can compute SUM(unit_price * quantity) directly in the aggregate call. Combined with GROUP BY, they let you build rich summary reports at any level of granularity — per customer, per month, per product category, and so on.",
    ],
    syntax: `-- Total and average for the whole table
SELECT
  SUM(total_amount)  AS revenue,
  AVG(total_amount)  AS avg_order_value
FROM orders;

-- Per-group aggregation
SELECT
  category,
  SUM(price) AS total_value,
  AVG(price) AS avg_price
FROM products
GROUP BY category;

-- Aggregating an expression
SELECT SUM(unit_price * quantity) AS gross_revenue
FROM order_items;`,
    example: `-- Revenue and average order value by month
SELECT
  DATE_TRUNC('month', order_date) AS month,
  SUM(total_amount)               AS monthly_revenue,
  AVG(total_amount)               AS avg_order_value,
  COUNT(*)                        AS order_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Average spend per customer (only customers with orders)
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer,
  SUM(o.total_amount)  AS lifetime_spend,
  AVG(o.total_amount)  AS avg_order
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_spend DESC
LIMIT 10;`,
    pitfalls: [
      "SUM of an all-NULL group returns NULL, not 0. Use COALESCE(SUM(col), 0) when you need a guaranteed numeric result.",
      "AVG ignores NULLs, which can skew results. If NULL means 'zero' in your domain, wrap with COALESCE before averaging.",
      "Watch for integer division. In some databases AVG of an integer column truncates to integer. Cast to NUMERIC or DECIMAL for accurate averages.",
    ],
    tryItSlug: "average-order-value",
    tryItLabel: "Practice SUM & AVG queries",
  },

  "min-max": {
    title: "MIN & MAX",
    section: "Aggregations",
    concept: [
      "MIN returns the smallest value and MAX returns the largest value in a group. These functions work on numbers, strings (alphabetical comparison), dates, and any other sortable type. They are indispensable for finding extremes: the cheapest product, the latest order date, the first customer signup.",
      "Like other aggregate functions, MIN and MAX ignore NULL values. If every value in the group is NULL, they return NULL. They can be used with or without GROUP BY — without it, they scan the entire table and return a single row.",
      "MIN and MAX are often efficient because the database can use an index on the target column to find the answer without scanning every row. This makes queries like \"what is the most recent order date?\" very fast when order_date is indexed.",
    ],
    syntax: `-- Global min and max
SELECT
  MIN(price) AS cheapest,
  MAX(price) AS most_expensive
FROM products;

-- Per-group min and max
SELECT
  category,
  MIN(price) AS lowest_price,
  MAX(price) AS highest_price
FROM products
GROUP BY category;

-- With dates
SELECT
  MIN(order_date) AS first_order,
  MAX(order_date) AS latest_order
FROM orders;`,
    example: `-- Price range and count per category
SELECT
  category,
  COUNT(*)     AS product_count,
  MIN(price)   AS min_price,
  MAX(price)   AS max_price,
  MAX(price) - MIN(price) AS price_spread
FROM products
GROUP BY category
ORDER BY price_spread DESC;

-- Each customer's first and most recent order
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer,
  MIN(o.order_date) AS first_order,
  MAX(o.order_date) AS latest_order,
  MAX(o.order_date) - MIN(o.order_date) AS customer_lifetime
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY customer_lifetime DESC;`,
    pitfalls: [
      "MIN/MAX on strings use alphabetical order, which may not match your expectations for mixed-case or locale-sensitive data.",
      "If you want the entire row with the minimum or maximum value (not just the value itself), you need a subquery or window function — not just MIN/MAX in SELECT.",
      "MIN and MAX return NULL if the group is empty. Guard against this with COALESCE when feeding results into further calculations.",
    ],
    tryItSlug: "highest-and-lowest-priced-products",
    tryItLabel: "Practice MIN & MAX queries",
  },

  "group-by": {
    title: "GROUP BY",
    section: "Aggregations",
    concept: [
      "GROUP BY divides rows into groups that share the same values in one or more columns. Once grouped, each group is collapsed into a single summary row by applying aggregate functions like COUNT, SUM, AVG, MIN, or MAX. This is how you answer questions like \"total revenue per category\" or \"average order value per customer\".",
      "Every non-aggregated column in your SELECT list must appear in the GROUP BY clause. This rule ensures that each output row maps to exactly one group. Violating it produces an error in standard SQL (though MySQL historically allowed it, leading to nondeterministic results).",
      "GROUP BY is evaluated after WHERE but before HAVING and SELECT. This means WHERE filters individual rows before grouping, and HAVING filters the resulting groups. Understanding this order of operations is key to writing correct aggregation queries.",
    ],
    syntax: `-- Group by a single column
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category;

-- Group by multiple columns
SELECT
  category,
  status,
  COUNT(*) AS cnt
FROM products
GROUP BY category, status;

-- Group by expression
SELECT
  DATE_TRUNC('month', order_date) AS month,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);`,
    example: `-- Revenue breakdown by product category
SELECT
  p.category,
  COUNT(DISTINCT o.order_id) AS orders,
  SUM(oi.quantity)            AS units_sold,
  SUM(oi.unit_price * oi.quantity) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
GROUP BY p.category
ORDER BY revenue DESC;

-- Average order value by customer state
SELECT
  c.state,
  COUNT(o.order_id)   AS order_count,
  AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.state
ORDER BY avg_order_value DESC;`,
    pitfalls: [
      "Every non-aggregated column in SELECT must be in GROUP BY. Forgetting one column causes an error (or worse, undefined behavior in MySQL's permissive mode).",
      "GROUP BY happens before SELECT aliases are available. In standard SQL you cannot write GROUP BY alias_name — repeat the expression or use a subquery.",
      "Grouping by high-cardinality columns (e.g., a unique ID) gives you one row per value, defeating the purpose of aggregation.",
    ],
    tryItSlug: "revenue-by-category",
    tryItLabel: "Practice GROUP BY queries",
  },

  having: {
    title: "HAVING",
    section: "Aggregations",
    concept: [
      "HAVING filters groups after aggregation, whereas WHERE filters individual rows before aggregation. This distinction is critical: if you need to exclude groups based on an aggregate value (e.g., only categories with more than 10 products), you must use HAVING because the aggregate does not exist at the WHERE stage.",
      "HAVING can reference any aggregate expression, even ones not in the SELECT list. For example, you can write HAVING COUNT(*) > 5 without including COUNT(*) in your output columns. You can also combine multiple aggregate conditions with AND and OR.",
      "A common pattern is WHERE + GROUP BY + HAVING used together: WHERE narrows the raw data, GROUP BY organizes it, and HAVING prunes the groups. Think of it as two stages of filtering with aggregation in between.",
    ],
    syntax: `-- Filter groups by aggregate value
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;

-- Multiple aggregate conditions
SELECT customer_id,
       COUNT(*) AS order_count,
       SUM(total_amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 3
   AND SUM(total_amount) > 500;`,
    example: `-- Categories with average product price over $50
SELECT
  category,
  COUNT(*)   AS product_count,
  AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50
ORDER BY avg_price DESC;

-- Customers who placed at least 5 orders totaling over $1000
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer,
  COUNT(o.order_id)   AS orders,
  SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) >= 5
   AND SUM(o.total_amount) > 1000
ORDER BY total_spent DESC;`,
    pitfalls: [
      "Do not put row-level conditions in HAVING — use WHERE instead. Putting them in HAVING works but forces the database to aggregate first, wasting resources.",
      "HAVING without GROUP BY is valid but rare; it treats the entire table as one group and filters based on the overall aggregate.",
      "You cannot reference SELECT aliases in HAVING in standard SQL. Repeat the aggregate expression or wrap the query in a subquery.",
    ],
    tryItSlug: "customers-with-multiple-orders",
    tryItLabel: "Practice HAVING queries",
  },

  /* ================================================================ */
  /*  JOINS                                                            */
  /* ================================================================ */

  "inner-join": {
    title: "INNER JOIN",
    section: "Joins",
    concept: [
      "INNER JOIN combines rows from two tables where the join condition is true. If a row in either table has no match in the other, it is excluded from the result. This makes INNER JOIN the most restrictive join type — you only get rows that exist in both tables.",
      "The join condition is specified with ON followed by a Boolean expression, most commonly an equality between a foreign key and a primary key. You can join on multiple conditions using AND, and you can chain multiple INNER JOINs to bring in data from three or more tables.",
      "INNER JOIN is the default join type — writing just JOIN without a prefix means INNER JOIN. It is the most commonly used join in practice because most queries need rows that have matching records on both sides (e.g., orders and their customers, products and their categories).",
    ],
    syntax: `-- Basic inner join
SELECT o.order_id, c.first_name, c.last_name
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id;

-- Multi-table join
SELECT
  o.order_id,
  c.first_name,
  p.name AS product
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON oi.order_id = o.order_id
INNER JOIN products p ON p.product_id = oi.product_id;`,
    example: `-- Order details with customer and product info
SELECT
  o.order_id,
  o.order_date,
  c.first_name || ' ' || c.last_name AS customer,
  p.name AS product,
  oi.quantity,
  oi.unit_price,
  oi.quantity * oi.unit_price AS line_total
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON oi.order_id = o.order_id
INNER JOIN products p ON p.product_id = oi.product_id
ORDER BY o.order_date DESC;`,
    pitfalls: [
      "If the join condition is wrong or missing, you get a Cartesian product (every row paired with every other row). Always double-check your ON clause.",
      "INNER JOIN excludes rows with no match. If you need all customers including those without orders, use LEFT JOIN instead.",
      "Joining on non-indexed columns can be very slow on large tables. Ensure foreign key columns are indexed.",
    ],
    tryItSlug: "order-details-with-customer-name",
    tryItLabel: "Practice INNER JOIN queries",
  },

  "left-join": {
    title: "LEFT JOIN",
    section: "Joins",
    concept: [
      "LEFT JOIN (or LEFT OUTER JOIN) returns all rows from the left table and the matching rows from the right table. When a left-side row has no match on the right, the right-side columns are filled with NULL. This makes LEFT JOIN ideal for answering questions like \"all customers and their orders, including customers who have never ordered\".",
      "The \"left\" and \"right\" refer to the order in which tables appear in the query: the table before LEFT JOIN is the left table, and the table after it is the right table. The left table is preserved in full; the right table contributes only matching rows.",
      "LEFT JOIN is one of the most commonly used join types in reporting and analytics because it prevents data loss. When you INNER JOIN on a nullable foreign key, rows with NULL foreign keys disappear silently. LEFT JOIN keeps them visible, with NULL in the joined columns, so you can detect and handle missing relationships.",
    ],
    syntax: `-- Basic left join
SELECT c.customer_id, c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;

-- Finding rows with NO match (anti-join pattern)
SELECT c.customer_id, c.first_name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;`,
    example: `-- All customers with their order count (including zero-order customers)
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer,
  COUNT(o.order_id) AS order_count,
  COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- Products that have never been ordered
SELECT p.product_id, p.name, p.category
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.order_item_id IS NULL
ORDER BY p.name;`,
    pitfalls: [
      "When using LEFT JOIN with COUNT, count a column from the right table (e.g., COUNT(o.order_id)), not COUNT(*). COUNT(*) counts the row itself and will return 1 even for non-matching rows.",
      "Placing a filter on the right table in WHERE effectively converts a LEFT JOIN to an INNER JOIN. Move the condition to the ON clause instead to preserve all left-side rows.",
      "Be mindful of NULLs in aggregations after LEFT JOIN. Use COALESCE to convert NULLs to sensible defaults like 0.",
    ],
    tryItSlug: "customers-without-orders",
    tryItLabel: "Practice LEFT JOIN queries",
  },

  "right-join": {
    title: "RIGHT JOIN",
    section: "Joins",
    concept: [
      "RIGHT JOIN (or RIGHT OUTER JOIN) is the mirror image of LEFT JOIN. It returns all rows from the right table and matching rows from the left table. When a right-side row has no match on the left, the left-side columns are filled with NULL.",
      "In practice, RIGHT JOIN is rarely used because any RIGHT JOIN can be rewritten as a LEFT JOIN by swapping the table order. Most developers prefer LEFT JOIN for consistency and readability. However, understanding RIGHT JOIN is important for reading legacy code and passing SQL certification exams.",
      "The choice between LEFT and RIGHT JOIN is purely a matter of which table you want to preserve in full. If you are starting from orders and want to include all products, you could write products RIGHT JOIN orders or orders LEFT JOIN products — the result is the same.",
    ],
    syntax: `-- Basic right join
SELECT o.order_id, o.order_date, c.first_name
FROM orders o
RIGHT JOIN customers c ON c.customer_id = o.customer_id;

-- Equivalent left join (preferred style)
SELECT o.order_id, o.order_date, c.first_name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;`,
    example: `-- All products with their sales data (even unsold ones)
-- Written as RIGHT JOIN for illustration
SELECT
  oi.order_id,
  oi.quantity,
  p.product_id,
  p.name AS product_name,
  p.category
FROM order_items oi
RIGHT JOIN products p ON p.product_id = oi.product_id
ORDER BY p.name;

-- Equivalent LEFT JOIN (preferred)
SELECT
  oi.order_id,
  oi.quantity,
  p.product_id,
  p.name AS product_name,
  p.category
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
ORDER BY p.name;`,
    pitfalls: [
      "RIGHT JOIN is functionally identical to LEFT JOIN with swapped tables. Prefer LEFT JOIN for consistency across your codebase.",
      "Mixing LEFT and RIGHT JOINs in the same query makes it very hard to reason about which rows are preserved. Stick to one direction.",
      "Like LEFT JOIN, placing a filter on the non-preserved table in WHERE converts it to an INNER JOIN. Use the ON clause for such filters.",
    ],
    tryItSlug: "orders-with-payment-and-shipping",
    tryItLabel: "Practice RIGHT JOIN queries",
  },

  "full-join": {
    title: "FULL OUTER JOIN",
    section: "Joins",
    concept: [
      "FULL OUTER JOIN returns all rows from both tables. When a row from either side has no match, the other side's columns are filled with NULL. It is the union of LEFT JOIN and RIGHT JOIN — no row from either table is ever lost.",
      "FULL OUTER JOIN is useful for reconciliation and comparison tasks: finding records that exist in one table but not the other, merging data from two sources that may have partial overlap, or building complete reports where both sides matter equally.",
      "Note that SQLite does not support FULL OUTER JOIN natively. In SQLite you can emulate it with a LEFT JOIN combined with a UNION ALL of a RIGHT JOIN (or a second LEFT JOIN with swapped tables). Most other major databases (PostgreSQL, MySQL 8+, SQL Server, Oracle) support it directly.",
    ],
    syntax: `-- Basic full outer join
SELECT
  c.customer_id AS customer_cid,
  c.first_name,
  o.order_id,
  o.total_amount
FROM customers c
FULL OUTER JOIN orders o ON o.customer_id = c.customer_id;

-- Find unmatched rows on either side
SELECT c.customer_id, o.order_id
FROM customers c
FULL OUTER JOIN orders o ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
   OR o.order_id IS NULL;`,
    example: `-- Reconcile products catalog with inventory records
-- (find products missing inventory and inventory for unknown products)
SELECT
  p.product_id   AS catalog_id,
  p.name         AS catalog_name,
  i.product_id   AS inventory_pid,
  i.quantity_on_hand
FROM products p
FULL OUTER JOIN inventory i ON i.product_id = p.product_id
WHERE p.product_id IS NULL   -- in inventory but not in catalog
   OR i.product_id IS NULL;  -- in catalog but no inventory record`,
    pitfalls: [
      "FULL OUTER JOIN can produce many NULLs. Be prepared to handle them with COALESCE in downstream calculations.",
      "Not all databases support FULL OUTER JOIN. SQLite requires a UNION ALL workaround. Always check your target database's compatibility.",
      "FULL OUTER JOIN results can be large. If you only need unmatched rows from one side, a LEFT JOIN with IS NULL filter is more efficient.",
    ],
    tryItSlug: "order-items-full-details",
    tryItLabel: "Practice FULL OUTER JOIN queries",
  },

  "self-join": {
    title: "Self Join",
    section: "Joins",
    concept: [
      "A self join is when a table is joined to itself. This is accomplished by listing the same table twice in the FROM clause with different aliases. Self joins are essential for comparing rows within the same table — for example, finding employees and their managers when both are stored in an employees table.",
      "The most common use case is hierarchical data. An employees table often has a manager_id column that references another row in the same table. By self-joining employees AS e with employees AS m on e.manager_id = m.employee_id, you can display each employee alongside their manager's name.",
      "Self joins can also compare rows for analytical purposes: finding products in the same category, customers in the same city, or orders placed on the same date. The key is that the two aliases represent different roles of the same underlying table.",
    ],
    syntax: `-- Basic self join with aliases
SELECT
  e.name   AS employee,
  m.name   AS manager
FROM employees e
LEFT JOIN employees m ON m.employee_id = e.manager_id;

-- Find pairs within the same group
SELECT
  a.name AS product_a,
  b.name AS product_b,
  a.category
FROM products a
JOIN products b
  ON a.category = b.category
  AND a.product_id < b.product_id;`,
    example: `-- Customers in the same city (find potential referral pairs)
SELECT
  a.first_name || ' ' || a.last_name AS customer_a,
  b.first_name || ' ' || b.last_name AS customer_b,
  a.city
FROM customers a
JOIN customers b
  ON a.city = b.city
  AND a.customer_id < b.customer_id
ORDER BY a.city;

-- Products cheaper than others in the same category
SELECT
  cheap.name  AS budget_product,
  cheap.price AS budget_price,
  pricey.name AS premium_product,
  pricey.price AS premium_price,
  cheap.category
FROM products cheap
JOIN products pricey
  ON cheap.category = pricey.category
  AND cheap.price < pricey.price
ORDER BY cheap.category, cheap.price;`,
    pitfalls: [
      "Always use table aliases to avoid ambiguity. Without aliases, the database cannot tell which instance of the table you are referencing.",
      "Self joins can generate duplicate pairs (A-B and B-A). Use an inequality condition like a.id < b.id to get each pair only once.",
      "Self joins on large tables can be expensive because you are effectively doubling the data to scan. Index the join columns.",
    ],
    tryItSlug: "self-referencing-customer-cities",
    tryItLabel: "Practice self join queries",
  },

  "cross-join": {
    title: "CROSS JOIN",
    section: "Joins",
    concept: [
      "CROSS JOIN produces the Cartesian product of two tables: every row from the first table paired with every row from the second. If table A has 100 rows and table B has 50, the result has 5,000 rows. There is no ON clause because every possible combination is returned.",
      "While CROSS JOIN can produce massive result sets, it has legitimate uses. It is commonly used to generate combinations — for example, pairing every product with every store location to create a price matrix, or crossing a calendar table with a list of metrics to ensure every date has a row.",
      "CROSS JOIN is also useful with small lookup tables. If you have a table of status codes (5 rows) and want to count occurrences of each status per month, you can CROSS JOIN the status table with a month series and then LEFT JOIN the actual data, ensuring zero-count rows appear in your report.",
    ],
    syntax: `-- Explicit cross join
SELECT p.name, s.size_label
FROM products p
CROSS JOIN sizes s;

-- Implicit cross join (comma syntax — same result)
SELECT p.name, s.size_label
FROM products p, sizes s;

-- Cross join with a VALUES list
SELECT p.name, v.color
FROM products p
CROSS JOIN (VALUES ('Red'), ('Blue'), ('Green')) AS v(color);`,
    example: `-- Generate a matrix of all products and all months in 2024
-- for a sales report that shows zero where there are no sales
SELECT
  p.product_id,
  p.name,
  months.m AS report_month,
  COALESCE(SUM(oi.quantity), 0) AS units_sold
FROM products p
CROSS JOIN generate_series(
  '2024-01-01'::date,
  '2024-12-01'::date,
  '1 month'::interval
) AS months(m)
LEFT JOIN order_items oi
  ON oi.product_id = p.product_id
LEFT JOIN orders o
  ON o.order_id = oi.order_id
  AND DATE_TRUNC('month', o.order_date) = months.m
GROUP BY p.product_id, p.name, months.m
ORDER BY p.name, months.m;`,
    pitfalls: [
      "CROSS JOIN with two large tables produces an enormous result. A 10,000-row table crossed with another 10,000-row table yields 100 million rows.",
      "An accidental CROSS JOIN (forgetting the ON clause in an INNER JOIN) is one of the most common SQL bugs. Always verify your join conditions.",
      "The comma-separated FROM syntax (FROM a, b) is an implicit CROSS JOIN. Be careful when listing multiple tables — add WHERE conditions to avoid unintended Cartesian products.",
    ],
    tryItSlug: "products-with-category-names",
    tryItLabel: "Practice CROSS JOIN queries",
  },

  /* ================================================================ */
  /*  SUBQUERIES                                                       */
  /* ================================================================ */

  "scalar-subquery": {
    title: "Scalar Subqueries",
    section: "Subqueries",
    concept: [
      "A scalar subquery is a subquery that returns exactly one row and one column — a single value. It can be used anywhere a single value is expected: in SELECT, WHERE, HAVING, or even in an expression. Scalar subqueries are enclosed in parentheses and executed for each row of the outer query (unless the optimizer can flatten them).",
      "Common use cases include comparing each row against a global value (e.g., the average price), computing a derived column from a related table, or providing a default when no match exists. Because a scalar subquery must return exactly one value, it will error if it returns multiple rows.",
      "Scalar subqueries in the SELECT list are convenient but can have performance implications. If the subquery is executed once per outer row, it creates an implicit nested loop. In many cases, a JOIN or a window function is a more efficient alternative.",
    ],
    syntax: `-- Scalar subquery in WHERE
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Scalar subquery in SELECT
SELECT
  name,
  price,
  price - (SELECT AVG(price) FROM products) AS diff_from_avg
FROM products;

-- Scalar subquery as a computed value
SELECT
  order_id,
  total_amount,
  total_amount / (SELECT MAX(total_amount) FROM orders) AS pct_of_max
FROM orders;`,
    example: `-- Products priced above the average for their category
SELECT p.name, p.price, p.category
FROM products p
WHERE p.price > (
  SELECT AVG(p2.price)
  FROM products p2
  WHERE p2.category = p.category
);

-- Each order compared to the overall average
SELECT
  o.order_id,
  o.order_date,
  o.total_amount,
  ROUND(o.total_amount - (
    SELECT AVG(total_amount) FROM orders
  ), 2) AS above_below_avg
FROM orders o
ORDER BY above_below_avg DESC;`,
    pitfalls: [
      "A scalar subquery MUST return at most one row. If it returns multiple rows, the query fails with an error. Add LIMIT 1 or ensure your WHERE is restrictive enough.",
      "Scalar subqueries in SELECT can be slow because they may execute once per row. Consider rewriting as a JOIN or CTE for better performance.",
      "Be careful with NULL: if the scalar subquery returns NULL, comparisons with it yield UNKNOWN, which may silently exclude rows.",
    ],
    tryItSlug: "above-average-price-products",
    tryItLabel: "Practice scalar subqueries",
  },

  "derived-tables": {
    title: "Derived Tables",
    section: "Subqueries",
    concept: [
      "A derived table is a subquery in the FROM clause that acts as a virtual table for the outer query. It must be enclosed in parentheses and given an alias. The outer query can select from the derived table just like any regular table, joining it, filtering it, and aggregating it.",
      "Derived tables are useful when you need to pre-aggregate, pre-filter, or reshape data before joining it with other tables. For example, you might compute per-customer order totals in a derived table and then join that with the customer table to add demographic information.",
      "Derived tables have the same capabilities as CTEs (Common Table Expressions) but are inline and scoped to a single use. If you need to reference the same subquery multiple times, a CTE is cleaner. For single-use intermediate results, derived tables are perfectly fine.",
    ],
    syntax: `-- Basic derived table
SELECT dt.category, dt.avg_price
FROM (
  SELECT category, AVG(price) AS avg_price
  FROM products
  GROUP BY category
) AS dt
WHERE dt.avg_price > 50;

-- Joining a derived table with a regular table
SELECT c.first_name, ot.order_count, ot.total_spent
FROM customers c
JOIN (
  SELECT customer_id,
         COUNT(*) AS order_count,
         SUM(total_amount) AS total_spent
  FROM orders
  GROUP BY customer_id
) AS ot ON ot.customer_id = c.customer_id;`,
    example: `-- Top 5 categories by revenue, with product count
SELECT
  cs.category,
  cs.revenue,
  cs.units_sold,
  pc.product_count
FROM (
  SELECT
    p.category,
    SUM(oi.unit_price * oi.quantity) AS revenue,
    SUM(oi.quantity) AS units_sold
  FROM order_items oi
  JOIN products p ON p.product_id = oi.product_id
  GROUP BY p.category
) AS cs
JOIN (
  SELECT category, COUNT(*) AS product_count
  FROM products
  GROUP BY category
) AS pc ON pc.category = cs.category
ORDER BY cs.revenue DESC
LIMIT 5;`,
    pitfalls: [
      "A derived table MUST have an alias. Forgetting the AS alias causes a syntax error.",
      "You cannot reference a derived table more than once in the same query. If you need to, use a CTE instead.",
      "Deeply nested derived tables become hard to read. Extract them into CTEs for better readability when nesting exceeds two levels.",
    ],
    tryItSlug: "customers-with-above-avg-spending",
    tryItLabel: "Practice derived tables",
  },

  correlated: {
    title: "Correlated Subqueries",
    section: "Subqueries",
    concept: [
      "A correlated subquery references columns from the outer query, creating a dependency between the inner and outer queries. Unlike a regular subquery that runs once, a correlated subquery is conceptually re-evaluated for every row in the outer query. This makes it powerful but potentially expensive.",
      "Correlated subqueries are essential when the inner query's logic depends on the current outer row. Common patterns include finding the most recent order per customer, comparing each row to its group average, or checking existence of related records. The EXISTS operator frequently uses correlated subqueries.",
      "Modern database optimizers can often transform correlated subqueries into joins or semi-joins internally, so the actual execution may be more efficient than the conceptual row-by-row model suggests. However, complex correlated subqueries can still be performance bottlenecks on large datasets.",
    ],
    syntax: `-- Correlated subquery in WHERE
SELECT p.name, p.price, p.category
FROM products p
WHERE p.price = (
  SELECT MAX(p2.price)
  FROM products p2
  WHERE p2.category = p.category
);

-- Correlated subquery in SELECT
SELECT
  c.first_name,
  c.last_name,
  (SELECT COUNT(*)
   FROM orders o
   WHERE o.customer_id = c.customer_id
  ) AS order_count
FROM customers c;`,
    example: `-- Most expensive product in each category
SELECT p.name, p.price, p.category
FROM products p
WHERE p.price = (
  SELECT MAX(p2.price)
  FROM products p2
  WHERE p2.category = p.category
)
ORDER BY p.category;

-- Customers whose latest order is over $200
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer
FROM customers c
WHERE (
  SELECT o.total_amount
  FROM orders o
  WHERE o.customer_id = c.customer_id
  ORDER BY o.order_date DESC
  LIMIT 1
) > 200;`,
    pitfalls: [
      "Correlated subqueries run (conceptually) once per outer row, which can be very slow on large tables. Test performance and consider rewriting as a JOIN.",
      "If the correlated subquery returns no rows, it yields NULL. This can cause unexpected filtering behavior in WHERE.",
      "Aliasing is critical in correlated subqueries. Without clear aliases the inner and outer column references become ambiguous.",
    ],
    tryItSlug: "most-expensive-product-per-category",
    tryItLabel: "Practice correlated subqueries",
  },

  exists: {
    title: "EXISTS & NOT EXISTS",
    section: "Subqueries",
    concept: [
      "EXISTS tests whether a subquery returns at least one row. It returns TRUE if the subquery has results and FALSE if it is empty. The subquery is typically correlated — it references the outer query's current row. EXISTS does not care about the actual values returned, only whether any row exists.",
      "NOT EXISTS is the negation: it returns TRUE when the subquery produces no rows. This is the standard way to find records with no matching counterpart — customers who have never ordered, products never sold, categories with no active items. It is generally more readable and often more efficient than LEFT JOIN ... IS NULL patterns.",
      "One key advantage of EXISTS over IN is its handling of NULLs. IN can produce unexpected results when the subquery returns NULL values, because NULL comparisons yield UNKNOWN. EXISTS avoids this entirely since it only checks for row existence, not value equality.",
    ],
    syntax: `-- EXISTS: customers who have placed at least one order
SELECT c.customer_id, c.first_name
FROM customers c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
);

-- NOT EXISTS: customers who have never ordered
SELECT c.customer_id, c.first_name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
);`,
    example: `-- Products that have been ordered at least once
SELECT p.product_id, p.name, p.category
FROM products p
WHERE EXISTS (
  SELECT 1
  FROM order_items oi
  WHERE oi.product_id = p.product_id
)
ORDER BY p.name;

-- Categories where every product costs more than $20
SELECT DISTINCT p.category
FROM products p
WHERE NOT EXISTS (
  SELECT 1
  FROM products p2
  WHERE p2.category = p.category
    AND p2.price <= 20
);`,
    pitfalls: [
      "SELECT 1 in the EXISTS subquery is a convention. The actual select list does not matter — EXISTS only checks row existence. SELECT * works too but SELECT 1 makes intent clearer.",
      "EXISTS generally outperforms IN for large subquery results because the database can stop as soon as the first matching row is found.",
      "Forgetting the correlation (WHERE inner.col = outer.col) makes EXISTS always return TRUE for non-empty tables, which is almost certainly a bug.",
    ],
    tryItSlug: "products-ordered-but-not-reviewed",
    tryItLabel: "Practice EXISTS queries",
  },

  /* ================================================================ */
  /*  WINDOW FUNCTIONS                                                 */
  /* ================================================================ */

  "row-number": {
    title: "ROW_NUMBER",
    section: "Window Functions",
    concept: [
      "ROW_NUMBER() assigns a unique sequential integer to each row within its partition, starting at 1. The assignment is based on the ORDER BY specified in the OVER clause. Unlike RANK, ROW_NUMBER never produces ties — even if two rows have identical ORDER BY values, they get different numbers (though the order between them is nondeterministic).",
      "ROW_NUMBER is one of the most versatile window functions. Its most common use is the \"top-N per group\" pattern: partition by a grouping column, order by a ranking criterion, and then filter for row_number = 1 (or <= N). This is the standard way to get the most recent order per customer, the highest-paid employee per department, etc.",
      "Because window functions are evaluated after WHERE and GROUP BY but before ORDER BY and LIMIT, you cannot filter on ROW_NUMBER directly in WHERE. Instead, wrap the query in a subquery or CTE and filter in the outer query.",
    ],
    syntax: `-- Basic row number
SELECT
  ROW_NUMBER() OVER (ORDER BY price DESC) AS rank,
  name,
  price
FROM products;

-- Row number within partitions
SELECT
  ROW_NUMBER() OVER (
    PARTITION BY category
    ORDER BY price DESC
  ) AS category_rank,
  category,
  name,
  price
FROM products;`,
    example: `-- Most recent order per customer (top-1 per group)
SELECT customer_id, order_id, order_date, total_amount
FROM (
  SELECT
    o.*,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY order_date DESC
    ) AS rn
  FROM orders o
) ranked
WHERE rn = 1
ORDER BY customer_id;

-- Top 3 best-selling products per category
SELECT category, name, units_sold
FROM (
  SELECT
    p.category,
    p.name,
    SUM(oi.quantity) AS units_sold,
    ROW_NUMBER() OVER (
      PARTITION BY p.category
      ORDER BY SUM(oi.quantity) DESC
    ) AS rn
  FROM products p
  JOIN order_items oi ON oi.product_id = p.product_id
  GROUP BY p.category, p.name
) ranked
WHERE rn <= 3
ORDER BY category, rn;`,
    pitfalls: [
      "ROW_NUMBER with ties is nondeterministic — add a tiebreaker column (like a primary key) to the ORDER BY for reproducible results.",
      "You cannot use ROW_NUMBER() in WHERE directly. Wrap in a subquery or CTE: SELECT * FROM (SELECT ..., ROW_NUMBER() ...) WHERE rn = 1.",
      "Forgetting PARTITION BY gives you a global row number instead of per-group, which is a common mistake when writing top-N-per-group queries.",
    ],
    tryItSlug: "customer-order-sequence",
    tryItLabel: "Practice ROW_NUMBER queries",
  },

  "rank-dense-rank": {
    title: "RANK & DENSE_RANK",
    section: "Window Functions",
    concept: [
      "RANK() and DENSE_RANK() assign rank numbers to rows within a partition, but unlike ROW_NUMBER they handle ties. When two rows have equal ORDER BY values, RANK gives them the same rank number and then skips the next rank(s). DENSE_RANK also gives tied rows the same number but does not skip — the next distinct value gets the very next integer.",
      "For example, if three products are tied for 2nd place: RANK assigns 2, 2, 2, 5 (skipping 3 and 4), while DENSE_RANK assigns 2, 2, 2, 3 (no gaps). Choose RANK when you want traditional competition-style ranking and DENSE_RANK when you want contiguous rank numbers regardless of ties.",
      "These functions are commonly used in leaderboards, grading systems, and percentile calculations. Like ROW_NUMBER, they require an OVER clause with ORDER BY and an optional PARTITION BY. They cannot be filtered directly in WHERE — use a subquery or CTE.",
    ],
    syntax: `-- RANK (gaps after ties)
SELECT
  name,
  price,
  RANK() OVER (ORDER BY price DESC) AS price_rank
FROM products;

-- DENSE_RANK (no gaps)
SELECT
  name,
  price,
  DENSE_RANK() OVER (ORDER BY price DESC) AS price_drank
FROM products;

-- Both for comparison
SELECT
  name, price,
  RANK() OVER (ORDER BY price DESC) AS rank,
  DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rank
FROM products;`,
    example: `-- Rank customers by total spending (with ties)
SELECT
  c.first_name || ' ' || c.last_name AS customer,
  SUM(o.total_amount) AS total_spent,
  RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS spend_rank,
  DENSE_RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS spend_dense_rank
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY spend_rank;

-- Top-ranked product per category using DENSE_RANK
SELECT category, name, price
FROM (
  SELECT
    category, name, price,
    DENSE_RANK() OVER (
      PARTITION BY category ORDER BY price DESC
    ) AS dr
  FROM products
) ranked
WHERE dr = 1;`,
    pitfalls: [
      "RANK produces gaps after ties (1, 2, 2, 4). If contiguous numbering matters for your use case, use DENSE_RANK instead.",
      "DENSE_RANK with many tied values can make the maximum rank misleadingly low. Verify whether your business logic needs RANK or DENSE_RANK semantics.",
      "Like ROW_NUMBER, RANK and DENSE_RANK cannot be filtered in WHERE. Wrap in a subquery or CTE to filter by rank value.",
    ],
    tryItSlug: "rank-products-by-price",
    tryItLabel: "Practice RANK & DENSE_RANK queries",
  },

  "lag-lead": {
    title: "LAG & LEAD",
    section: "Window Functions",
    concept: [
      "LAG accesses a value from a previous row in the partition, and LEAD accesses a value from a subsequent row, both relative to the current row according to the ORDER BY in the OVER clause. They take three arguments: the column to read, the offset (defaulting to 1), and an optional default value when there is no previous/next row.",
      "These functions are invaluable for time-series analysis and change detection. With LAG you can calculate day-over-day changes, month-over-month growth rates, and gaps between events. With LEAD you can look ahead to compute time-to-next-event or identify upcoming changes.",
      "LAG and LEAD are evaluated based on the window ordering, not the final query ORDER BY. Make sure the OVER clause's ORDER BY matches the chronological or logical sequence you intend. PARTITION BY is optional: use it when you need to compare within groups (e.g., per customer, per product) rather than globally.",
    ],
    syntax: `-- LAG: previous row's value
SELECT
  order_date,
  total_amount,
  LAG(total_amount) OVER (ORDER BY order_date) AS prev_amount
FROM orders;

-- LEAD: next row's value with default
SELECT
  order_date,
  total_amount,
  LEAD(total_amount, 1, 0) OVER (ORDER BY order_date) AS next_amount
FROM orders;

-- With partition
SELECT
  customer_id,
  order_date,
  total_amount,
  LAG(order_date) OVER (
    PARTITION BY customer_id ORDER BY order_date
  ) AS prev_order_date
FROM orders;`,
    example: `-- Month-over-month revenue change
SELECT
  month,
  revenue,
  LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
  ROUND(
    (revenue - LAG(revenue) OVER (ORDER BY month))
    / LAG(revenue) OVER (ORDER BY month) * 100, 1
  ) AS growth_pct
FROM (
  SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(total_amount) AS revenue
  FROM orders
  GROUP BY DATE_TRUNC('month', order_date)
) monthly;

-- Days between consecutive orders per customer
SELECT
  customer_id,
  order_date,
  order_date - LAG(order_date) OVER (
    PARTITION BY customer_id ORDER BY order_date
  ) AS days_since_last_order
FROM orders
ORDER BY customer_id, order_date;`,
    pitfalls: [
      "The first row in a partition has no LAG value (returns NULL). The last row has no LEAD value. Provide a default third argument or use COALESCE to handle these edge cases.",
      "LAG/LEAD offsets must be non-negative. Use LAG for lookback and LEAD for lookahead — do not try negative offsets.",
      "Dividing by LAG() for growth rates can cause division-by-zero if the previous value is 0. Guard with NULLIF or CASE.",
    ],
    tryItSlug: "order-value-vs-previous",
    tryItLabel: "Practice LAG & LEAD queries",
  },

  "running-totals": {
    title: "Running Totals",
    section: "Window Functions",
    concept: [
      "A running total (cumulative sum) adds up values row by row as you move through an ordered set. In SQL, you create running totals with SUM() as a window function combined with an ORDER BY clause in the OVER frame. The default frame when ORDER BY is present is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, which gives you the cumulative sum from the first row up to the current row.",
      "Running totals are fundamental in financial analysis (cumulative revenue, running balances), inventory management (running stock levels), and progress tracking. You can also compute running averages, running counts, and running min/max using the same windowing technique with different aggregate functions.",
      "The frame specification controls exactly which rows contribute to each calculation. ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW counts physical rows, while RANGE treats rows with equal ORDER BY values as a group. For most running total use cases, ROWS gives the most intuitive behavior.",
    ],
    syntax: `-- Running total
SELECT
  order_date,
  total_amount,
  SUM(total_amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM orders;

-- Running average (moving window: last 7 rows)
SELECT
  order_date,
  total_amount,
  AVG(total_amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7_avg
FROM orders;`,
    example: `-- Cumulative revenue by day
SELECT
  order_date,
  daily_revenue,
  SUM(daily_revenue) OVER (
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS cumulative_revenue
FROM (
  SELECT
    order_date,
    SUM(total_amount) AS daily_revenue
  FROM orders
  GROUP BY order_date
) daily
ORDER BY order_date;

-- Running total per customer to track loyalty milestones
SELECT
  customer_id,
  order_date,
  total_amount,
  SUM(total_amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS lifetime_spend
FROM orders
ORDER BY customer_id, order_date;`,
    pitfalls: [
      "RANGE vs ROWS: if multiple rows share the same ORDER BY value, RANGE includes all tied rows in the frame, while ROWS processes them one at a time. This can produce different running totals.",
      "Forgetting ORDER BY in the OVER clause makes SUM() compute the total of the entire partition for every row — not a running total.",
      "Ensure your ORDER BY produces a deterministic order. Ties cause the running total to depend on the physical row order, which is non-deterministic.",
    ],
    tryItSlug: "running-total-revenue",
    tryItLabel: "Practice running totals",
  },

  ntile: {
    title: "NTILE",
    section: "Window Functions",
    concept: [
      "NTILE(n) divides the ordered rows in a partition into n approximately equal groups (buckets) and assigns each row a bucket number from 1 to n. If the rows do not divide evenly, the earlier buckets get one extra row. NTILE is commonly used for percentile analysis, quartile assignments, and distributing work evenly.",
      "For example, NTILE(4) creates quartiles: the top 25% of rows get bucket 1, the next 25% get bucket 2, and so on. NTILE(100) creates percentiles. This is useful for segmenting customers by spend level, products by popularity, or students by grade ranges.",
      "NTILE works within PARTITION BY boundaries, so you can compute percentiles within each category, region, or time period independently. The ORDER BY in the OVER clause determines how rows are ranked before being divided into buckets.",
    ],
    syntax: `-- Quartiles (4 buckets)
SELECT
  name,
  price,
  NTILE(4) OVER (ORDER BY price) AS price_quartile
FROM products;

-- Deciles within each category
SELECT
  category,
  name,
  price,
  NTILE(10) OVER (
    PARTITION BY category ORDER BY price
  ) AS price_decile
FROM products;`,
    example: `-- Segment customers into spending tiers (quartiles)
SELECT
  customer,
  total_spent,
  CASE spend_quartile
    WHEN 1 THEN 'Bronze'
    WHEN 2 THEN 'Silver'
    WHEN 3 THEN 'Gold'
    WHEN 4 THEN 'Platinum'
  END AS tier
FROM (
  SELECT
    c.first_name || ' ' || c.last_name AS customer,
    SUM(o.total_amount) AS total_spent,
    NTILE(4) OVER (ORDER BY SUM(o.total_amount)) AS spend_quartile
  FROM customers c
  JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.first_name, c.last_name
) tiers
ORDER BY total_spent DESC;

-- Products in the top 10% by sales volume
SELECT name, units_sold
FROM (
  SELECT
    p.name,
    SUM(oi.quantity) AS units_sold,
    NTILE(10) OVER (ORDER BY SUM(oi.quantity) DESC) AS decile
  FROM products p
  JOIN order_items oi ON oi.product_id = p.product_id
  GROUP BY p.product_id, p.name
) ranked
WHERE decile = 1;`,
    pitfalls: [
      "NTILE distributes rows as evenly as possible, but uneven division means some buckets have one more row than others. Do not assume exact equality.",
      "NTILE assigns bucket numbers based on row position, not value ranges. Two very different values can end up in the same bucket if they are adjacent in order.",
      "For true percentile values (not bucket numbers), use PERCENT_RANK() or CUME_DIST() instead of NTILE(100).",
    ],
    tryItSlug: "ntile-balance-quartiles",
    tryItLabel: "Practice NTILE queries",
  },

  /* ================================================================ */
  /*  ADVANCED                                                         */
  /* ================================================================ */

  cte: {
    title: "Common Table Expressions",
    section: "Advanced",
    concept: [
      "A Common Table Expression (CTE) is a named, temporary result set defined at the top of a query using the WITH keyword. It exists only for the duration of that single query and can be referenced like a table in the main SELECT, INSERT, UPDATE, or DELETE statement that follows.",
      "CTEs improve readability by breaking complex queries into named, logical steps. Instead of deeply nested subqueries, you define each intermediate result as a CTE with a meaningful name and then compose them in the final query. This makes queries significantly easier to write, debug, and maintain.",
      "Multiple CTEs can be defined in a single WITH clause, separated by commas. Later CTEs can reference earlier ones, enabling step-by-step data transformations. CTEs are not materialized by default in most databases (they are inlined like views), but PostgreSQL offers MATERIALIZED / NOT MATERIALIZED hints for controlling this behavior.",
    ],
    syntax: `-- Single CTE
WITH active_customers AS (
  SELECT customer_id, first_name, last_name
  FROM customers
  WHERE status = 'active'
)
SELECT * FROM active_customers;

-- Multiple CTEs
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(total_amount) AS revenue
  FROM orders
  GROUP BY DATE_TRUNC('month', order_date)
),
avg_revenue AS (
  SELECT AVG(revenue) AS avg_rev
  FROM monthly_revenue
)
SELECT
  mr.month,
  mr.revenue,
  ar.avg_rev,
  mr.revenue - ar.avg_rev AS diff
FROM monthly_revenue mr
CROSS JOIN avg_revenue ar
ORDER BY mr.month;`,
    example: `-- Multi-step analysis: top customers and their favorite categories
WITH customer_spend AS (
  SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer,
    SUM(o.total_amount) AS total_spent,
    COUNT(o.order_id) AS order_count
  FROM customers c
  JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.first_name, c.last_name
),
top_customers AS (
  SELECT * FROM customer_spend
  WHERE total_spent > 1000
),
customer_categories AS (
  SELECT
    o.customer_id,
    p.category,
    SUM(oi.quantity) AS items_bought,
    ROW_NUMBER() OVER (
      PARTITION BY o.customer_id
      ORDER BY SUM(oi.quantity) DESC
    ) AS rn
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  JOIN products p ON p.product_id = oi.product_id
  GROUP BY o.customer_id, p.category
)
SELECT
  tc.customer,
  tc.total_spent,
  tc.order_count,
  cc.category AS favorite_category,
  cc.items_bought
FROM top_customers tc
JOIN customer_categories cc
  ON cc.customer_id = tc.customer_id AND cc.rn = 1
ORDER BY tc.total_spent DESC;`,
    pitfalls: [
      "CTEs are not automatically materialized. If a CTE is referenced multiple times and is expensive to compute, it may run multiple times. Check your database's behavior or use MATERIALIZED hints.",
      "CTEs cannot be indexed. If you need indexed intermediate results, consider a temporary table instead.",
      "Do not overuse CTEs for trivial transformations — they add visual overhead without benefit if the logic is simple enough for a single query.",
    ],
    tryItSlug: "first-order-per-customer",
    tryItLabel: "Practice CTE queries",
  },

  "recursive-cte": {
    title: "Recursive CTEs",
    section: "Advanced",
    concept: [
      "A recursive CTE is a CTE that references itself, enabling iterative processing of hierarchical or graph-structured data. It consists of two parts: the anchor member (the starting point, a non-recursive query) and the recursive member (a query that references the CTE itself and extends the result set iteratively). The recursion stops when the recursive member produces no new rows.",
      "Recursive CTEs are the standard SQL mechanism for traversing trees and graphs: organizational hierarchies (employees and managers), category trees, bill-of-materials structures, flight route networks, and more. Each iteration adds one level of depth to the traversal.",
      "Safety is important with recursive CTEs because an incorrect termination condition leads to infinite recursion. Most databases impose a default recursion limit (e.g., 100 iterations in PostgreSQL, configurable with SET max_recursive_iterations). Always include a WHERE condition in the recursive member that ensures progress toward termination.",
    ],
    syntax: `-- Basic recursive CTE structure
WITH RECURSIVE cte_name AS (
  -- Anchor member: starting rows
  SELECT id, parent_id, name, 1 AS depth
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive member: extend from previous iteration
  SELECT c.id, c.parent_id, c.name, cte.depth + 1
  FROM categories c
  JOIN cte_name cte ON cte.id = c.parent_id
)
SELECT * FROM cte_name;

-- Generate a series of numbers
WITH RECURSIVE nums AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 100
)
SELECT n FROM nums;`,
    example: `-- Employee hierarchy with full management chain
WITH RECURSIVE org_chart AS (
  -- Anchor: top-level managers (no manager_id)
  SELECT
    employee_id,
    name,
    manager_id,
    name AS management_chain,
    0 AS depth
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive: each employee joined to their manager
  SELECT
    e.employee_id,
    e.name,
    e.manager_id,
    oc.management_chain || ' > ' || e.name,
    oc.depth + 1
  FROM employees e
  JOIN org_chart oc ON oc.employee_id = e.manager_id
)
SELECT
  employee_id,
  name,
  depth,
  management_chain
FROM org_chart
ORDER BY management_chain;`,
    pitfalls: [
      "Infinite recursion occurs if the recursive member does not converge. Always include a termination condition (e.g., WHERE depth < 20 or a join that eventually matches no rows).",
      "UNION ALL is typically used in recursive CTEs. UNION (with deduplication) can work but adds overhead and changes semantics. Only use UNION if you need cycle detection.",
      "Recursive CTEs on large graphs can be memory-intensive. For very deep or wide hierarchies, consider limiting depth or paginating the traversal.",
    ],
    tryItSlug: "int-ecom-recursive-cte-category-hierarchy",
    tryItLabel: "Practice recursive CTE queries",
  },

  case: {
    title: "CASE Expressions",
    section: "Advanced",
    concept: [
      "CASE is SQL's conditional expression, similar to if-else in programming languages. It evaluates conditions in order and returns the value associated with the first true condition. If no condition matches and there is no ELSE, it returns NULL. CASE can be used in SELECT, WHERE, ORDER BY, GROUP BY, and even inside aggregate functions.",
      "There are two forms: the searched CASE (CASE WHEN condition THEN result) which evaluates arbitrary Boolean expressions, and the simple CASE (CASE expression WHEN value THEN result) which compares a single expression against multiple values. The searched form is more flexible and more commonly used.",
      "CASE is extremely useful for data transformation, categorization, and conditional aggregation. You can create labeled buckets (price tiers, age groups), pivot data with conditional SUM, customize sort orders, and handle NULL values — all without leaving SQL.",
    ],
    syntax: `-- Searched CASE
SELECT
  name,
  price,
  CASE
    WHEN price < 10 THEN 'Budget'
    WHEN price < 50 THEN 'Mid-Range'
    WHEN price < 100 THEN 'Premium'
    ELSE 'Luxury'
  END AS price_tier
FROM products;

-- Simple CASE
SELECT
  order_id,
  status,
  CASE status
    WHEN 'pending'   THEN 'Awaiting Processing'
    WHEN 'shipped'   THEN 'In Transit'
    WHEN 'delivered'  THEN 'Completed'
    ELSE 'Unknown'
  END AS status_label
FROM orders;`,
    example: `-- Conditional aggregation: revenue by price tier
SELECT
  CASE
    WHEN p.price < 25  THEN 'Under $25'
    WHEN p.price < 100 THEN '$25-$99'
    ELSE '$100+'
  END AS price_tier,
  COUNT(DISTINCT p.product_id)       AS products,
  SUM(oi.quantity)                   AS units_sold,
  SUM(oi.unit_price * oi.quantity)   AS revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY
  CASE
    WHEN p.price < 25  THEN 'Under $25'
    WHEN p.price < 100 THEN '$25-$99'
    ELSE '$100+'
  END
ORDER BY revenue DESC;

-- Pivot-style report using CASE inside SUM
SELECT
  DATE_TRUNC('month', order_date) AS month,
  SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END) AS delivered_rev,
  SUM(CASE WHEN status = 'pending'   THEN total_amount ELSE 0 END) AS pending_rev,
  SUM(CASE WHEN status = 'cancelled' THEN total_amount ELSE 0 END) AS cancelled_rev
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;`,
    pitfalls: [
      "CASE evaluates conditions top-to-bottom and returns the first match. Order your WHEN clauses from most specific to least specific.",
      "Forgetting the ELSE clause causes unmatched rows to return NULL, which can break downstream calculations. Always include ELSE unless you intentionally want NULL.",
      "When using CASE in GROUP BY, you must repeat the entire CASE expression — you cannot reference the SELECT alias.",
    ],
    tryItSlug: "multi-payment-orders",
    tryItLabel: "Practice CASE expressions",
  },

  union: {
    title: "UNION & INTERSECT",
    section: "Advanced",
    concept: [
      "UNION combines the result sets of two or more SELECT statements into one, removing duplicate rows. UNION ALL does the same but keeps duplicates and is faster because it skips the deduplication step. Both require that the SELECT statements have the same number of columns with compatible data types.",
      "INTERSECT returns only rows that appear in both result sets, and EXCEPT (or MINUS in Oracle) returns rows from the first set that do not appear in the second. Together with UNION, these set operations provide powerful ways to combine, compare, and contrast data from different sources or different conditions.",
      "Column names in the result come from the first SELECT statement. ORDER BY applies to the combined result and must reference columns from the first SELECT or use positional notation. Each individual SELECT can have its own WHERE, JOIN, and GROUP BY logic.",
    ],
    syntax: `-- UNION (removes duplicates)
SELECT name, email FROM customers
UNION
SELECT name, email FROM newsletter_subscribers;

-- UNION ALL (keeps duplicates, faster)
SELECT product_id, 'ordered' AS source FROM order_items
UNION ALL
SELECT product_id, 'wishlisted' FROM wishlists;

-- INTERSECT
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM reviews;

-- EXCEPT
SELECT customer_id FROM customers
EXCEPT
SELECT customer_id FROM orders;`,
    example: `-- Combined activity feed: orders and reviews, sorted by date
SELECT
  'order' AS activity_type,
  customer_id,
  order_date AS activity_date,
  'Placed order #' || order_id AS description
FROM orders

UNION ALL

SELECT
  'review' AS activity_type,
  customer_id,
  review_date AS activity_date,
  'Reviewed ' || product_name AS description
FROM reviews

ORDER BY activity_date DESC
LIMIT 50;

-- Customers who ordered but never reviewed
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE c.customer_id IN (
  SELECT customer_id FROM orders
  EXCEPT
  SELECT customer_id FROM reviews
);`,
    pitfalls: [
      "UNION removes duplicates (like DISTINCT), which requires sorting and comparison. Use UNION ALL when you know there are no duplicates or when duplicates are acceptable — it is significantly faster.",
      "All SELECTs in a UNION must have the same number of columns with compatible types. Mismatched columns cause a syntax error.",
      "ORDER BY at the end of a UNION applies to the entire combined result, not to individual SELECTs. To order individual parts, use a subquery.",
    ],
    tryItSlug: "union-deposits-and-payments",
    tryItLabel: "Practice UNION & INTERSECT queries",
  },

  "date-functions": {
    title: "Date Functions",
    section: "Advanced",
    concept: [
      "Date and time functions let you extract parts of dates, perform date arithmetic, format dates for display, and generate date series. They are essential for time-based reporting: grouping by month, calculating durations, filtering by date ranges, and computing age or tenure.",
      "Common extraction functions include EXTRACT(part FROM date) which pulls out the year, month, day, hour, etc., and DATE_TRUNC(part, date) which rounds a timestamp down to a specified precision. For example, DATE_TRUNC('month', order_date) converts any date in January 2024 to 2024-01-01, making it perfect for monthly aggregation.",
      "Date arithmetic varies by database. PostgreSQL supports interval arithmetic (date + INTERVAL '30 days'), while MySQL uses DATE_ADD and DATE_SUB. AGE() computes the difference between dates as an interval. CURRENT_DATE and NOW() provide the current date and timestamp. Understanding your database's date functions is crucial for writing portable queries.",
    ],
    syntax: `-- Extract parts
SELECT
  EXTRACT(YEAR FROM order_date)  AS year,
  EXTRACT(MONTH FROM order_date) AS month,
  EXTRACT(DOW FROM order_date)   AS day_of_week
FROM orders;

-- Truncate to precision
SELECT
  DATE_TRUNC('month', order_date) AS month,
  COUNT(*) AS order_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Date arithmetic
SELECT
  order_date,
  order_date + INTERVAL '30 days' AS due_date,
  CURRENT_DATE - order_date AS days_ago
FROM orders;`,
    example: `-- Monthly revenue trend with year-over-year comparison
SELECT
  DATE_TRUNC('month', order_date) AS month,
  EXTRACT(YEAR FROM order_date) AS year,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY
  DATE_TRUNC('month', order_date),
  EXTRACT(YEAR FROM order_date)
ORDER BY month;

-- Average days between first and second order per customer
SELECT
  AVG(days_to_second) AS avg_days_to_repeat
FROM (
  SELECT
    customer_id,
    order_date - LAG(order_date) OVER (
      PARTITION BY customer_id ORDER BY order_date
    ) AS days_to_second,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id ORDER BY order_date
    ) AS order_num
  FROM orders
) t
WHERE order_num = 2;`,
    pitfalls: [
      "Date function names differ across databases. PostgreSQL uses DATE_TRUNC; MySQL uses DATE_FORMAT and YEAR()/MONTH(). Write database-specific code or use an abstraction layer.",
      "Timestamps include time components. Comparing a timestamp to a date may miss same-day records. Use DATE_TRUNC or cast to DATE for accurate date-only comparisons.",
      "Time zones matter. CURRENT_TIMESTAMP and NOW() return different results depending on the session timezone. Use AT TIME ZONE or store timestamps in UTC.",
    ],
    tryItSlug: "average-shipping-days",
    tryItLabel: "Practice date function queries",
  },

  "string-functions": {
    title: "String Functions",
    section: "Advanced",
    concept: [
      "String functions manipulate text data: extracting substrings, changing case, trimming whitespace, searching for patterns, and concatenating values. In data-heavy applications, string functions are essential for cleaning data, formatting output, parsing semi-structured text, and building dynamic values.",
      "Common functions include UPPER/LOWER for case conversion, TRIM/LTRIM/RTRIM for whitespace removal, SUBSTRING for extracting parts of a string, LENGTH for character count, REPLACE for substitution, and CONCAT or || for joining strings together. POSITION (or STRPOS) finds the location of a substring within a string.",
      "Regular expression functions like REGEXP_MATCHES (PostgreSQL) or REGEXP_LIKE (Oracle/MySQL) provide powerful pattern matching beyond what LIKE can do. However, regex in SQL can be slow on large datasets because it typically cannot use indexes. Use it for data cleaning and validation rather than high-volume filtering.",
    ],
    syntax: `-- Case conversion and trimming
SELECT
  UPPER(first_name) AS upper_name,
  LOWER(email) AS lower_email,
  TRIM(address) AS clean_address
FROM customers;

-- Substring and length
SELECT
  name,
  SUBSTRING(name FROM 1 FOR 10) AS short_name,
  LENGTH(name) AS name_length
FROM products;

-- Concatenation and replacement
SELECT
  CONCAT(first_name, ' ', last_name) AS full_name,
  REPLACE(phone, '-', '') AS clean_phone
FROM customers;`,
    example: `-- Clean and standardize customer email domains
SELECT
  email,
  LOWER(SUBSTRING(email FROM POSITION('@' IN email) + 1)) AS domain,
  COUNT(*) AS customer_count
FROM customers
GROUP BY
  email,
  LOWER(SUBSTRING(email FROM POSITION('@' IN email) + 1))
ORDER BY customer_count DESC;

-- Search products with flexible name matching
SELECT
  product_id,
  name,
  category,
  price
FROM products
WHERE LOWER(name) LIKE '%' || LOWER('wireless') || '%'
   OR LOWER(category) LIKE '%' || LOWER('wireless') || '%'
ORDER BY name;

-- Format order summary with string building
SELECT
  o.order_id,
  'Order #' || o.order_id || ' - ' ||
    TO_CHAR(o.order_date, 'Mon DD, YYYY') || ' - $' ||
    TO_CHAR(o.total_amount, 'FM999,999.00') AS order_summary
FROM orders o
ORDER BY o.order_date DESC
LIMIT 10;`,
    pitfalls: [
      "String function names vary widely across databases. PostgreSQL uses || for concatenation; MySQL uses CONCAT(); SQL Server uses +. Check your database's documentation.",
      "LIKE and string comparisons may be case-sensitive depending on the database and collation. Use LOWER() or ILIKE (PostgreSQL) for case-insensitive searches.",
      "String operations on large tables are slow because they typically cannot use indexes. For full-text search on large datasets, use dedicated full-text search features like tsvector/tsquery in PostgreSQL.",
    ],
    tryItSlug: "int-ecom-uppercase-product-names",
    tryItLabel: "Practice string function queries",
  },
};

/* ------------------------------------------------------------------ */
/*  Helper: tiny chevron arrow                                         */
/* ------------------------------------------------------------------ */

function ChevronRight({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      className={className ?? "h-3.5 w-3.5"}
    >
      <path
        fillRule="evenodd"
        d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function ArrowLeft({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      className={className ?? "h-4 w-4"}
    >
      <path
        fillRule="evenodd"
        d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
        clipRule="evenodd"
      />
    </svg>
  );
}

/* ------------------------------------------------------------------ */
/*  Page component                                                     */
/* ------------------------------------------------------------------ */

export default function DocTopicPage() {
  const params = useParams();
  const slug = params.slug as string;

  const doc = DOCS[slug];

  /* ----- Not found ----- */
  if (!doc) {
    return (
      <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-16 text-center">
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Topic Not Found
        </h1>
        <p className="mt-2 text-sm text-[var(--color-text-muted)]">
          The documentation page for &ldquo;{slug}&rdquo; does not exist.
        </p>
        <Link
          href="/docs"
          className="mt-6 inline-flex items-center gap-1.5 text-sm font-medium text-[var(--color-accent)] hover:underline"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Documentation
        </Link>
      </div>
    );
  }

  /* ----- Prev / Next ----- */
  const currentIndex = SLUG_ORDER.indexOf(slug);
  const prevSlug = currentIndex > 0 ? SLUG_ORDER[currentIndex - 1] : null;
  const nextSlug =
    currentIndex < SLUG_ORDER.length - 1 ? SLUG_ORDER[currentIndex + 1] : null;
  const prevDoc = prevSlug ? DOCS[prevSlug] : null;
  const nextDoc = nextSlug ? DOCS[nextSlug] : null;

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* ---- Back link ---- */}
      <Link
        href="/docs"
        className="inline-flex items-center gap-1.5 text-sm text-[var(--color-text-muted)] transition-colors hover:text-[var(--color-accent)]"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Documentation
      </Link>

      {/* ---- Breadcrumb ---- */}
      <div className="mt-4 flex items-center gap-1 text-xs text-[var(--color-text-muted)]">
        <Link href="/docs" className="hover:text-[var(--color-accent)]">
          Docs
        </Link>
        <ChevronRight />
        <span>{doc.section}</span>
        <ChevronRight />
        <span className="text-[var(--color-text-secondary)]">{doc.title}</span>
      </div>

      {/* ---- Title ---- */}
      <h1 className="mt-4 text-2xl font-bold text-[var(--color-text-primary)]">
        {doc.title}
      </h1>
      <span className="mt-1 inline-block rounded-full bg-[var(--color-surface)] px-2.5 py-0.5 text-xs font-medium text-[var(--color-text-muted)] ring-1 ring-[var(--color-border)]">
        {doc.section}
      </span>

      {/* ---- Concept ---- */}
      <section className="mt-8">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Concept
        </h2>
        <div className="mt-3 space-y-4">
          {doc.concept.map((p, i) => (
            <p
              key={i}
              className="text-sm leading-relaxed text-[var(--color-text-secondary)]"
            >
              {p}
            </p>
          ))}
        </div>
      </section>

      {/* ---- Syntax ---- */}
      <section className="mt-10">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Syntax
        </h2>
        <pre className="mt-3 overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-[13px] leading-relaxed text-[var(--color-text-primary)]">
          <code>{doc.syntax}</code>
        </pre>
      </section>

      {/* ---- Practical Example ---- */}
      <section className="mt-10">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Practical Example
        </h2>
        <p className="mt-1 text-xs text-[var(--color-text-muted)]">
          Using the ecommerce schema (customers, orders, order_items, products)
        </p>
        <pre className="mt-3 overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-[13px] leading-relaxed text-[var(--color-text-primary)]">
          <code>{doc.example}</code>
        </pre>
      </section>

      {/* ---- Pitfalls & Tips ---- */}
      <section className="mt-10">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Common Pitfalls &amp; Tips
        </h2>
        <ul className="mt-3 space-y-3">
          {doc.pitfalls.map((tip, i) => (
            <li
              key={i}
              className="flex gap-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-3 text-sm leading-relaxed text-[var(--color-text-secondary)]"
            >
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[var(--color-accent)] text-xs font-bold text-white">
                {i + 1}
              </span>
              <span>{tip}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* ---- Try It ---- */}
      <section className="mt-10">
        <Link
          href={`/practice/${doc.tryItSlug}`}
          className="inline-flex items-center gap-2 rounded-lg bg-[var(--color-accent)] px-5 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90"
        >
          {doc.tryItLabel}
          <ChevronRight className="h-4 w-4" />
        </Link>
      </section>

      {/* ---- Prev / Next nav ---- */}
      <nav className="mt-12 flex items-stretch gap-4 border-t border-[var(--color-border)] pt-6">
        {prevDoc && prevSlug ? (
          <Link
            href={`/docs/${prevSlug}`}
            className="group flex flex-1 flex-col rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 transition-all hover:border-[var(--color-accent)]"
          >
            <span className="text-xs text-[var(--color-text-muted)]">
              Previous
            </span>
            <span className="mt-1 text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
              {prevDoc.title}
            </span>
          </Link>
        ) : (
          <div className="flex-1" />
        )}

        {nextDoc && nextSlug ? (
          <Link
            href={`/docs/${nextSlug}`}
            className="group flex flex-1 flex-col items-end rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-right transition-all hover:border-[var(--color-accent)]"
          >
            <span className="text-xs text-[var(--color-text-muted)]">Next</span>
            <span className="mt-1 text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
              {nextDoc.title}
            </span>
          </Link>
        ) : (
          <div className="flex-1" />
        )}
      </nav>
    </div>
  );
}
