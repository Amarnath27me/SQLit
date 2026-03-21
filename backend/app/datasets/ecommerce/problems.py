"""
E-Commerce dataset practice problems.

40 progressive SQL problems covering fundamentals through advanced topics,
designed around a realistic e-commerce database schema.

Tables:
  - customers (id, first_name, last_name, email, phone, city, state, country, created_at)
  - categories (id, name, description)
  - products (id, name, category_id, price, cost, stock_quantity, created_at)
  - orders (id, customer_id, order_date, status, total_amount)
  - order_items (id, order_id, product_id, quantity, unit_price, discount)
  - payments (id, order_id, payment_date, amount, method, status)
  - reviews (id, product_id, customer_id, rating, comment, review_date)
  - shipping (id, order_id, shipping_date, delivery_date, carrier, tracking_number, status)
"""

PROBLEMS: list[dict] = [
    # =========================================================================
    # LEVEL 1 — FUNDAMENTALS (8 problems: ec-001 through ec-008)
    # =========================================================================
    {
        "id": "ec-001",
        "slug": "list-all-products",
        "title": "List All Products",
        "difficulty": "easy",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "The product catalog team needs a quick inventory snapshot. "
            "Write a query that retrieves the name and price of every product "
            "in the store, sorted alphabetically by product name."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price\n"
            "FROM products\n"
            "ORDER BY name;"
        ),
        "hints": [
            "You only need to query a single table for this one.",
            "Think about which columns the question asks you to return.",
            "Use ORDER BY to control the sort direction.",
            "SELECT name, price FROM products ORDER BY ...;",
        ],
        "explanation": (
            "1. SELECT the name and price columns from the products table.\n"
            "2. ORDER BY name sorts the results alphabetically (ascending is the default)."
        ),
        "approach": [
            "Identify the table that stores product information.",
            "Pick only the columns requested: name and price.",
            "Apply an ORDER BY on the name column for alphabetical sorting.",
        ],
        "common_mistakes": [
            "Selecting all columns with SELECT * instead of only name and price.",
            "Forgetting the ORDER BY clause, which means results come back in an undefined order.",
        ],
        "concept_tags": ["SELECT", "ORDER BY"],
    },
    {
        "id": "ec-002",
        "slug": "customers-from-specific-state",
        "title": "Customers from a Specific State",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The regional marketing team wants to send a targeted promotion to "
            "all customers located in California. Retrieve the first name, last name, "
            "and email of every customer whose state is 'CA'."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE state = 'CA';"
        ),
        "hints": [
            "You need to filter rows based on a column value.",
            "The WHERE clause lets you restrict which rows are returned.",
            "The state column stores two-letter abbreviations.",
            "WHERE state = 'CA' is the filter you need.",
        ],
        "explanation": (
            "1. SELECT the three requested columns from customers.\n"
            "2. WHERE state = 'CA' filters the result set to only California customers."
        ),
        "approach": [
            "Identify that the customers table holds location info.",
            "Use WHERE to filter on the state column.",
            "Return only the columns the marketing team needs.",
        ],
        "common_mistakes": [
            "Using LIKE '%CA%' which could match unintended values if state names were longer.",
            "Forgetting that string comparisons in SQL are case-sensitive in some configurations.",
        ],
        "concept_tags": ["SELECT", "WHERE", "string comparison"],
    },
    {
        "id": "ec-003",
        "slug": "high-value-completed-orders",
        "title": "High-Value Completed Orders",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The finance team is auditing large transactions. Find all orders "
            "with a total_amount greater than 500 that have a status of 'completed'. "
            "Return the order id, order_date, and total_amount."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id, order_date, total_amount\n"
            "FROM orders\n"
            "WHERE total_amount > 500\n"
            "  AND status = 'completed';"
        ),
        "hints": [
            "You need two conditions in your WHERE clause.",
            "Combine conditions with AND so both must be true.",
            "One condition is numeric (> 500), the other is a string match.",
            "WHERE total_amount > 500 AND status = 'completed'",
        ],
        "explanation": (
            "1. SELECT id, order_date, and total_amount from orders.\n"
            "2. WHERE total_amount > 500 keeps only high-value orders.\n"
            "3. AND status = 'completed' further narrows to completed ones."
        ),
        "approach": [
            "Identify that the orders table has both amount and status.",
            "Combine a numeric comparison with a string equality check using AND.",
            "Return only the requested columns.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, which returns orders matching either condition rather than both.",
            "Putting quotes around 500, treating it as a string instead of a number.",
            "Forgetting that status values are case-sensitive strings.",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "comparison operators"],
    },
    {
        "id": "ec-004",
        "slug": "products-in-price-range",
        "title": "Products in a Price Range",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "A buyer is looking for mid-range products priced between $25 and $100 "
            "(inclusive). List the product name, price, and stock_quantity, "
            "ordered from cheapest to most expensive."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price, stock_quantity\n"
            "FROM products\n"
            "WHERE price BETWEEN 25 AND 100\n"
            "ORDER BY price;"
        ),
        "hints": [
            "There is a SQL keyword designed for range checks.",
            "BETWEEN is inclusive on both ends.",
            "Remember to sort the results by price ascending.",
            "WHERE price BETWEEN 25 AND 100 ORDER BY price;",
        ],
        "explanation": (
            "1. SELECT name, price, and stock_quantity from products.\n"
            "2. WHERE price BETWEEN 25 AND 100 filters to the inclusive range.\n"
            "3. ORDER BY price sorts ascending (cheapest first)."
        ),
        "approach": [
            "Use the BETWEEN operator for an inclusive range filter.",
            "Add ORDER BY price for ascending sort.",
        ],
        "common_mistakes": [
            "Using price >= 25 AND price < 100, accidentally excluding the upper bound.",
            "Forgetting ORDER BY, returning results in arbitrary order.",
        ],
        "concept_tags": ["SELECT", "WHERE", "BETWEEN", "ORDER BY"],
    },
    {
        "id": "ec-005",
        "slug": "search-products-by-name",
        "title": "Search Products by Name",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "A customer support agent needs to look up products whose name "
            "contains the word 'Pro'. Return the product id, name, and price "
            "for all matching products."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT id, name, price\n"
            "FROM products\n"
            "WHERE name LIKE '%Pro%';"
        ),
        "hints": [
            "You need a pattern-matching operator, not exact equality.",
            "LIKE is the SQL operator for pattern matching.",
            "The % wildcard matches zero or more characters.",
            "Place % on both sides of 'Pro' to match anywhere in the string.",
        ],
        "explanation": (
            "1. SELECT id, name, and price from products.\n"
            "2. WHERE name LIKE '%Pro%' matches any product whose name "
            "contains the substring 'Pro' anywhere."
        ),
        "approach": [
            "Use LIKE with wildcard characters to do a substring search.",
            "Place % before and after the search term.",
        ],
        "common_mistakes": [
            "Using = instead of LIKE, which only matches exact values.",
            "Forgetting the wildcard on one side, e.g., LIKE 'Pro%' only matches names starting with 'Pro'.",
        ],
        "concept_tags": ["SELECT", "WHERE", "LIKE", "wildcards"],
    },
    {
        "id": "ec-006",
        "slug": "recent-orders-top-ten",
        "title": "Ten Most Recent Orders",
        "difficulty": "easy",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "The operations dashboard needs to show the ten most recent orders. "
            "Return the order id, customer_id, order_date, and total_amount, "
            "sorted with the newest orders first."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id, customer_id, order_date, total_amount\n"
            "FROM orders\n"
            "ORDER BY order_date DESC\n"
            "LIMIT 10;"
        ),
        "hints": [
            "You need to control both sorting direction and result count.",
            "ORDER BY with DESC gives newest-first sorting.",
            "LIMIT restricts how many rows are returned.",
            "Combine ORDER BY order_date DESC with LIMIT 10.",
        ],
        "explanation": (
            "1. SELECT the requested columns from orders.\n"
            "2. ORDER BY order_date DESC sorts newest first.\n"
            "3. LIMIT 10 returns only the top ten rows."
        ),
        "approach": [
            "Sort orders by date in descending order.",
            "Use LIMIT to cap the result set at 10 rows.",
        ],
        "common_mistakes": [
            "Forgetting DESC, which returns the oldest orders instead.",
            "Placing LIMIT before ORDER BY, which is a syntax error in PostgreSQL.",
        ],
        "concept_tags": ["SELECT", "ORDER BY", "DESC", "LIMIT"],
    },
    {
        "id": "ec-007",
        "slug": "unique-customer-cities",
        "title": "Unique Customer Cities",
        "difficulty": "easy",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "The business development team wants to know which cities the "
            "customer base spans. List all distinct cities from the customers "
            "table, sorted alphabetically."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT DISTINCT city\n"
            "FROM customers\n"
            "ORDER BY city;"
        ),
        "hints": [
            "Multiple customers may live in the same city.",
            "There is a keyword that removes duplicate values from results.",
            "DISTINCT is placed right after SELECT.",
            "SELECT DISTINCT city FROM customers ORDER BY city;",
        ],
        "explanation": (
            "1. SELECT DISTINCT city removes duplicate city values.\n"
            "2. ORDER BY city sorts alphabetically."
        ),
        "approach": [
            "Use DISTINCT to eliminate duplicate city entries.",
            "Sort the output alphabetically.",
        ],
        "common_mistakes": [
            "Omitting DISTINCT, which returns one row per customer instead of per city.",
            "Using GROUP BY city without an aggregate, which works but is less idiomatic for simple deduplication.",
        ],
        "concept_tags": ["SELECT", "DISTINCT", "ORDER BY"],
    },
    {
        "id": "ec-008",
        "slug": "orders-by-status",
        "title": "Orders by Status",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The fulfillment team needs to quickly find all orders that are either "
            "'pending' or 'processing'. Return the order id, customer_id, "
            "order_date, and status, ordered by order_date ascending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id, customer_id, order_date, status\n"
            "FROM orders\n"
            "WHERE status IN ('pending', 'processing')\n"
            "ORDER BY order_date;"
        ),
        "hints": [
            "You are filtering on a column that can match one of several values.",
            "The IN operator checks membership in a list.",
            "IN is cleaner than chaining multiple OR conditions.",
            "WHERE status IN ('pending', 'processing')",
        ],
        "explanation": (
            "1. SELECT the requested columns from orders.\n"
            "2. WHERE status IN ('pending', 'processing') matches either value.\n"
            "3. ORDER BY order_date returns rows in chronological order."
        ),
        "approach": [
            "Use the IN operator to match against a set of values.",
            "Sort by order_date ascending (the default).",
        ],
        "common_mistakes": [
            "Writing status = 'pending' OR 'processing', which is not valid SQL.",
            "Forgetting quotes around the string values inside IN.",
        ],
        "concept_tags": ["SELECT", "WHERE", "IN", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 2 — AGGREGATIONS (8 problems: ec-009 through ec-016)
    # =========================================================================
    {
        "id": "ec-009",
        "slug": "total-number-of-orders",
        "title": "Total Number of Orders",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Management wants a quick KPI check. Write a query that returns the "
            "total number of orders in the system."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT COUNT(*) AS total_orders\n"
            "FROM orders;"
        ),
        "hints": [
            "You need an aggregate function that counts rows.",
            "COUNT(*) counts all rows regardless of NULL values.",
            "Use an alias to give the result a meaningful column name.",
            "SELECT COUNT(*) AS total_orders FROM orders;",
        ],
        "explanation": (
            "1. COUNT(*) counts every row in the orders table.\n"
            "2. AS total_orders gives the output column a readable name."
        ),
        "approach": [
            "Use the COUNT aggregate function on the orders table.",
            "Alias the result for clarity.",
        ],
        "common_mistakes": [
            "Using COUNT(id) instead of COUNT(*) — both work here, but COUNT(*) is more conventional for total row counts.",
            "Forgetting the alias, which returns a column named 'count' that may confuse consumers.",
        ],
        "concept_tags": ["COUNT", "aggregate functions", "alias"],
    },
    {
        "id": "ec-010",
        "slug": "revenue-by-category",
        "title": "Total Revenue by Category",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The product analytics team wants to see total revenue broken down "
            "by product category. Calculate the sum of total_amount from orders "
            "grouped by category. Use order_items and products to link orders to "
            "categories. Return the category name and total revenue, sorted by "
            "revenue descending."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "SELECT c.name AS category, SUM(oi.quantity * oi.unit_price) AS total_revenue\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "JOIN categories c ON p.category_id = c.id\n"
            "GROUP BY c.name\n"
            "ORDER BY total_revenue DESC;"
        ),
        "hints": [
            "Revenue per line item is quantity times unit_price.",
            "You need to join order_items to products, then products to categories.",
            "Use GROUP BY on the category name to aggregate per category.",
            "SUM(oi.quantity * oi.unit_price) gives total revenue per group.",
        ],
        "explanation": (
            "1. JOIN order_items to products on product_id, then products to categories on category_id.\n"
            "2. For each line item, revenue = quantity * unit_price.\n"
            "3. GROUP BY c.name aggregates revenue per category.\n"
            "4. ORDER BY total_revenue DESC shows the highest-revenue category first."
        ),
        "approach": [
            "Link order_items -> products -> categories through foreign keys.",
            "Calculate line-item revenue as quantity * unit_price.",
            "Aggregate with SUM and group by category name.",
            "Sort descending to highlight top categories.",
        ],
        "common_mistakes": [
            "Using orders.total_amount instead of computing revenue from order_items, which double-counts if an order has items in multiple categories.",
            "Forgetting to GROUP BY, which causes an aggregation error.",
            "Not accounting for the discount column (acceptable here since the question asks for unit_price-based revenue).",
        ],
        "concept_tags": ["SUM", "GROUP BY", "JOIN", "ORDER BY"],
    },
    {
        "id": "ec-011",
        "slug": "average-order-value",
        "title": "Average Order Value",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The finance team monitors average order value (AOV) as a key metric. "
            "Calculate the average total_amount across all orders, rounded to two "
            "decimal places."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT ROUND(AVG(total_amount), 2) AS avg_order_value\n"
            "FROM orders;"
        ),
        "hints": [
            "There is an aggregate function specifically for averages.",
            "AVG computes the mean of a numeric column.",
            "Use ROUND to limit decimal places.",
            "ROUND(AVG(total_amount), 2) rounds to two decimals.",
        ],
        "explanation": (
            "1. AVG(total_amount) computes the arithmetic mean of all order totals.\n"
            "2. ROUND(..., 2) limits the result to two decimal places."
        ),
        "approach": [
            "Apply AVG to the total_amount column.",
            "Wrap in ROUND for a clean two-decimal result.",
        ],
        "common_mistakes": [
            "Forgetting ROUND, which may return many decimal places.",
            "Using SUM/COUNT manually instead of the built-in AVG function.",
        ],
        "concept_tags": ["AVG", "ROUND", "aggregate functions"],
    },
    {
        "id": "ec-012",
        "slug": "orders-per-customer",
        "title": "Orders Per Customer",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The customer success team wants to identify engagement levels. "
            "For each customer, count the number of orders they have placed. "
            "Return customer_id and order_count, sorted by order_count descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id, COUNT(*) AS order_count\n"
            "FROM orders\n"
            "GROUP BY customer_id\n"
            "ORDER BY order_count DESC;"
        ),
        "hints": [
            "You need to count rows per group, not overall.",
            "GROUP BY creates one group per customer_id.",
            "COUNT(*) within a GROUP BY counts rows in each group.",
            "Sort by the count descending to see the most active customers first.",
        ],
        "explanation": (
            "1. GROUP BY customer_id creates one group per customer.\n"
            "2. COUNT(*) counts the orders within each group.\n"
            "3. ORDER BY order_count DESC puts the most active customers first."
        ),
        "approach": [
            "Group the orders table by customer_id.",
            "Count rows per group.",
            "Sort by the count in descending order.",
        ],
        "common_mistakes": [
            "Selecting columns not in the GROUP BY or an aggregate, causing an error.",
            "Forgetting the GROUP BY clause entirely.",
        ],
        "concept_tags": ["COUNT", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "ec-013",
        "slug": "highest-and-lowest-priced-products",
        "title": "Highest and Lowest Priced Products",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The pricing analyst needs a quick snapshot of the product price "
            "range. Write a single query that returns the minimum price, maximum "
            "price, and the difference between them (as price_range)."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT MIN(price) AS min_price,\n"
            "       MAX(price) AS max_price,\n"
            "       MAX(price) - MIN(price) AS price_range\n"
            "FROM products;"
        ),
        "hints": [
            "MIN and MAX are aggregate functions that find extremes.",
            "You can use arithmetic on aggregate results in the SELECT list.",
            "No GROUP BY is needed when aggregating the entire table.",
            "MAX(price) - MIN(price) gives the range.",
        ],
        "explanation": (
            "1. MIN(price) finds the cheapest product's price.\n"
            "2. MAX(price) finds the most expensive.\n"
            "3. Subtracting them gives the price range.\n"
            "4. No GROUP BY is needed because we aggregate across all products."
        ),
        "approach": [
            "Use MIN and MAX on the price column.",
            "Subtract to compute the range in the same query.",
        ],
        "common_mistakes": [
            "Writing two separate queries instead of combining MIN and MAX in one SELECT.",
            "Adding an unnecessary GROUP BY, which would change the result.",
        ],
        "concept_tags": ["MIN", "MAX", "aggregate functions", "arithmetic"],
    },
    {
        "id": "ec-014",
        "slug": "categories-with-many-products",
        "title": "Categories with Many Products",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The inventory manager needs to identify product-heavy categories. "
            "Find all categories that have more than 5 products. Return the "
            "category_id, category name, and product count."
        ),
        "schema_hint": ["products", "categories"],
        "solution_query": (
            "SELECT c.id AS category_id, c.name, COUNT(p.id) AS product_count\n"
            "FROM categories c\n"
            "JOIN products p ON c.id = p.category_id\n"
            "GROUP BY c.id, c.name\n"
            "HAVING COUNT(p.id) > 5\n"
            "ORDER BY product_count DESC;"
        ),
        "hints": [
            "After grouping, you need to filter groups based on a count.",
            "HAVING filters groups after aggregation (WHERE filters rows before).",
            "Join categories to products to get category names with counts.",
            "HAVING COUNT(p.id) > 5 keeps only categories with more than 5 products.",
        ],
        "explanation": (
            "1. JOIN categories to products on category_id.\n"
            "2. GROUP BY c.id, c.name aggregates per category.\n"
            "3. COUNT(p.id) counts products per category.\n"
            "4. HAVING COUNT(p.id) > 5 filters out small categories."
        ),
        "approach": [
            "Join the two tables to get category names.",
            "Group by category and count products.",
            "Use HAVING to filter aggregated groups.",
        ],
        "common_mistakes": [
            "Using WHERE COUNT(p.id) > 5, which is invalid — WHERE cannot contain aggregates.",
            "Grouping only by c.id and forgetting c.name, which works in some databases but is bad practice.",
        ],
        "concept_tags": ["COUNT", "GROUP BY", "HAVING", "JOIN"],
    },
    {
        "id": "ec-015",
        "slug": "monthly-order-count",
        "title": "Monthly Order Count",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The operations team needs a monthly order trend report. Count the "
            "number of orders placed each month. Return the month (as YYYY-MM) "
            "and the order count, sorted chronologically."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,\n"
            "       COUNT(*) AS order_count\n"
            "FROM orders\n"
            "GROUP BY TO_CHAR(order_date, 'YYYY-MM')\n"
            "ORDER BY month;"
        ),
        "hints": [
            "You need to extract the year and month from a date column.",
            "PostgreSQL's TO_CHAR function can format dates as 'YYYY-MM'.",
            "Group by the formatted date string to aggregate per month.",
            "TO_CHAR(order_date, 'YYYY-MM') converts dates to year-month strings.",
        ],
        "explanation": (
            "1. TO_CHAR(order_date, 'YYYY-MM') extracts year-month as a string.\n"
            "2. GROUP BY that expression aggregates orders per month.\n"
            "3. COUNT(*) counts orders within each month.\n"
            "4. ORDER BY month sorts chronologically (YYYY-MM strings sort correctly)."
        ),
        "approach": [
            "Format the order_date to year-month granularity.",
            "Group and count by that formatted value.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Extracting only the month number, which loses year information and groups January 2023 with January 2024.",
            "Using DATE_TRUNC but forgetting it returns a full timestamp, not a clean YYYY-MM string.",
        ],
        "concept_tags": ["TO_CHAR", "GROUP BY", "COUNT", "date functions"],
    },
    {
        "id": "ec-016",
        "slug": "average-rating-per-product",
        "title": "Average Rating Per Product",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The product team wants to find well-reviewed products. Calculate the "
            "average rating for each product that has at least 3 reviews. Return "
            "the product_id, average rating (rounded to 1 decimal), and review "
            "count, sorted by average rating descending."
        ),
        "schema_hint": ["reviews"],
        "solution_query": (
            "SELECT product_id,\n"
            "       ROUND(AVG(rating), 1) AS avg_rating,\n"
            "       COUNT(*) AS review_count\n"
            "FROM reviews\n"
            "GROUP BY product_id\n"
            "HAVING COUNT(*) >= 3\n"
            "ORDER BY avg_rating DESC;"
        ),
        "hints": [
            "You need both AVG and COUNT in the same query.",
            "HAVING filters groups after aggregation — use it for the minimum review count.",
            "ROUND(AVG(rating), 1) gives one decimal place.",
            "GROUP BY product_id, then HAVING COUNT(*) >= 3.",
        ],
        "explanation": (
            "1. GROUP BY product_id creates one group per product.\n"
            "2. AVG(rating) calculates the mean rating per product.\n"
            "3. COUNT(*) counts reviews per product.\n"
            "4. HAVING COUNT(*) >= 3 filters out products with fewer than 3 reviews.\n"
            "5. ORDER BY avg_rating DESC shows the highest-rated products first."
        ),
        "approach": [
            "Group reviews by product_id.",
            "Compute both AVG(rating) and COUNT(*).",
            "Filter groups with HAVING for a minimum review threshold.",
            "Sort by average rating descending.",
        ],
        "common_mistakes": [
            "Using WHERE COUNT(*) >= 3 instead of HAVING.",
            "Forgetting ROUND, leading to overly precise decimal output.",
            "Filtering before grouping, which does not achieve the same result.",
        ],
        "concept_tags": ["AVG", "COUNT", "GROUP BY", "HAVING", "ROUND"],
    },

    # =========================================================================
    # LEVEL 3 — JOINS (8 problems: ec-017 through ec-024)
    # =========================================================================
    {
        "id": "ec-017",
        "slug": "order-details-with-customer-name",
        "title": "Order Details with Customer Name",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Customer service needs an order report that includes customer names. "
            "Write a query that returns the order id, order_date, total_amount, "
            "and the customer's full name (first_name || ' ' || last_name) for "
            "every order."
        ),
        "schema_hint": ["orders", "customers"],
        "solution_query": (
            "SELECT o.id AS order_id,\n"
            "       o.order_date,\n"
            "       o.total_amount,\n"
            "       c.first_name || ' ' || c.last_name AS customer_name\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.id;"
        ),
        "hints": [
            "You need data from two tables: orders and customers.",
            "JOIN connects tables using a shared key — customer_id.",
            "Use the || operator to concatenate strings in PostgreSQL.",
            "JOIN customers c ON o.customer_id = c.id links each order to its customer.",
        ],
        "explanation": (
            "1. JOIN orders with customers on the customer_id foreign key.\n"
            "2. SELECT columns from both tables.\n"
            "3. Concatenate first_name and last_name with || ' ' || for the full name."
        ),
        "approach": [
            "Identify the foreign key relationship between orders and customers.",
            "Use INNER JOIN to combine the tables.",
            "Concatenate name columns for a full name.",
        ],
        "common_mistakes": [
            "Forgetting the ON clause, which produces a cross join.",
            "Using CONCAT instead of || — both work in PostgreSQL, but || is more idiomatic.",
        ],
        "concept_tags": ["JOIN", "INNER JOIN", "string concatenation"],
    },
    {
        "id": "ec-018",
        "slug": "products-with-category-names",
        "title": "Products with Category Names",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The catalog page needs product listings with category labels. "
            "Return product name, price, stock_quantity, and category name "
            "for all products, sorted by category name then product name."
        ),
        "schema_hint": ["products", "categories"],
        "solution_query": (
            "SELECT p.name AS product_name,\n"
            "       p.price,\n"
            "       p.stock_quantity,\n"
            "       c.name AS category_name\n"
            "FROM products p\n"
            "JOIN categories c ON p.category_id = c.id\n"
            "ORDER BY c.name, p.name;"
        ),
        "hints": [
            "You need to join products to categories.",
            "The category_id in products references the id in categories.",
            "Use table aliases to keep the query concise.",
            "ORDER BY c.name, p.name sorts by category first, then product.",
        ],
        "explanation": (
            "1. JOIN products to categories on category_id.\n"
            "2. SELECT columns from both tables with clear aliases.\n"
            "3. ORDER BY category name first, then product name within each category."
        ),
        "approach": [
            "Join products and categories on the foreign key.",
            "Alias columns to avoid ambiguity (both tables have a 'name' column).",
            "Sort by category then product name.",
        ],
        "common_mistakes": [
            "Not aliasing the name columns, causing ambiguous column names.",
            "Using LEFT JOIN when INNER JOIN is sufficient (all products should have a category).",
        ],
        "concept_tags": ["JOIN", "INNER JOIN", "ORDER BY", "aliases"],
    },
    {
        "id": "ec-019",
        "slug": "customers-without-orders",
        "title": "Customers Who Never Ordered",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The re-engagement team wants to target customers who registered but "
            "have never placed an order. Find all customers with no matching "
            "orders. Return their id, first_name, last_name, and email."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.id, c.first_name, c.last_name, c.email\n"
            "FROM customers c\n"
            "LEFT JOIN orders o ON c.id = o.customer_id\n"
            "WHERE o.id IS NULL;"
        ),
        "hints": [
            "An INNER JOIN would exclude customers with no orders entirely.",
            "LEFT JOIN keeps all customers even if they have no matching orders.",
            "After a LEFT JOIN, unmatched rows have NULL in the right table's columns.",
            "Filter with WHERE o.id IS NULL to find customers with no orders.",
        ],
        "explanation": (
            "1. LEFT JOIN customers to orders keeps all customers.\n"
            "2. Customers with no orders have NULL in all orders columns.\n"
            "3. WHERE o.id IS NULL filters to only those unmatched customers."
        ),
        "approach": [
            "Use LEFT JOIN to preserve all customers.",
            "Filter for NULL in the orders side to find non-buyers.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which excludes the very customers you are looking for.",
            "Checking WHERE o.customer_id IS NULL instead of o.id — both work but o.id is clearer since customer_id is the join key.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join pattern"],
    },
    {
        "id": "ec-020",
        "slug": "order-items-full-details",
        "title": "Order Items with Full Details",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Build a detailed line-item report. For each order item, show the "
            "order id, product name, category name, quantity, unit_price, and "
            "line total (quantity * unit_price). Sort by order id, then product "
            "name."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "SELECT oi.order_id,\n"
            "       p.name AS product_name,\n"
            "       c.name AS category_name,\n"
            "       oi.quantity,\n"
            "       oi.unit_price,\n"
            "       oi.quantity * oi.unit_price AS line_total\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "JOIN categories c ON p.category_id = c.id\n"
            "ORDER BY oi.order_id, p.name;"
        ),
        "hints": [
            "This query requires joining three tables in a chain.",
            "order_items -> products -> categories follows the foreign key path.",
            "Compute the line total as a calculated column in the SELECT.",
            "Use two JOINs: one for products, one for categories.",
        ],
        "explanation": (
            "1. JOIN order_items to products on product_id.\n"
            "2. JOIN products to categories on category_id (chained join).\n"
            "3. Calculate line_total as quantity * unit_price.\n"
            "4. ORDER BY order_id, product_name for organized output."
        ),
        "approach": [
            "Chain joins through the foreign key relationships.",
            "Compute derived columns in the SELECT list.",
            "Sort by order_id first for grouping, then product_name.",
        ],
        "common_mistakes": [
            "Joining order_items directly to categories, which is not possible — products is the bridge.",
            "Forgetting to alias the name columns from products and categories.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "calculated columns"],
    },
    {
        "id": "ec-021",
        "slug": "orders-with-payment-and-shipping",
        "title": "Orders with Payment and Shipping Status",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The operations team needs a unified view of each order's payment "
            "and shipping status. For each order, show the order id, order_date, "
            "total_amount, payment method, payment status, shipping carrier, and "
            "shipping status. Include orders even if they have no shipping record yet."
        ),
        "schema_hint": ["orders", "payments", "shipping"],
        "solution_query": (
            "SELECT o.id AS order_id,\n"
            "       o.order_date,\n"
            "       o.total_amount,\n"
            "       pay.method AS payment_method,\n"
            "       pay.status AS payment_status,\n"
            "       s.carrier,\n"
            "       s.status AS shipping_status\n"
            "FROM orders o\n"
            "JOIN payments pay ON o.id = pay.order_id\n"
            "LEFT JOIN shipping s ON o.id = s.order_id\n"
            "ORDER BY o.order_date DESC;"
        ),
        "hints": [
            "You need to join three tables, but not all orders may have shipping records.",
            "Use INNER JOIN for payments (every paid order has a payment) and LEFT JOIN for shipping.",
            "LEFT JOIN preserves orders that have not shipped yet.",
            "Alias tables to keep column references clear.",
        ],
        "explanation": (
            "1. INNER JOIN payments to orders — assuming every order has a payment.\n"
            "2. LEFT JOIN shipping to orders — some orders may not have shipped.\n"
            "3. Shipping columns will be NULL for orders without a shipping record.\n"
            "4. ORDER BY order_date DESC shows most recent first."
        ),
        "approach": [
            "Determine which joins should be INNER vs LEFT based on data availability.",
            "Use INNER JOIN for required relationships (payments).",
            "Use LEFT JOIN for optional relationships (shipping).",
            "Alias columns that share names across tables (e.g., status).",
        ],
        "common_mistakes": [
            "Using INNER JOIN for shipping, which drops orders not yet shipped.",
            "Not aliasing the status column, causing ambiguity between payment and shipping status.",
            "Forgetting that an order could have multiple payments — this query assumes one payment per order.",
        ],
        "concept_tags": ["JOIN", "LEFT JOIN", "multi-table join", "aliases"],
    },
    {
        "id": "ec-022",
        "slug": "customer-order-summary",
        "title": "Customer Order Summary",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Create a customer-level summary showing each customer's name, total "
            "number of orders, and total amount spent. Include customers who have "
            "not placed any orders (show 0 for counts and amounts). Sort by total "
            "spent descending."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       COUNT(o.id) AS total_orders,\n"
            "       COALESCE(SUM(o.total_amount), 0) AS total_spent\n"
            "FROM customers c\n"
            "LEFT JOIN orders o ON c.id = o.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY total_spent DESC;"
        ),
        "hints": [
            "LEFT JOIN ensures customers with no orders still appear.",
            "COUNT(o.id) counts only non-NULL values, so it returns 0 for customers with no orders.",
            "SUM of NULL values returns NULL — use COALESCE to turn that into 0.",
            "Group by customer identifiers (id, first_name, last_name).",
        ],
        "explanation": (
            "1. LEFT JOIN customers to orders to keep all customers.\n"
            "2. GROUP BY customer fields to aggregate per customer.\n"
            "3. COUNT(o.id) correctly returns 0 for customers with no orders.\n"
            "4. COALESCE(SUM(o.total_amount), 0) handles the NULL sum case.\n"
            "5. ORDER BY total_spent DESC shows top spenders first."
        ),
        "approach": [
            "Use LEFT JOIN to include customers without orders.",
            "Group by customer and aggregate order data.",
            "Handle NULL aggregates with COALESCE.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which drops customers with no orders.",
            "Using COUNT(*) instead of COUNT(o.id), which counts 1 for customers with no orders.",
            "Forgetting COALESCE, leaving NULL instead of 0 for non-buying customers.",
        ],
        "concept_tags": ["LEFT JOIN", "GROUP BY", "COUNT", "SUM", "COALESCE"],
    },
    {
        "id": "ec-023",
        "slug": "products-never-reviewed",
        "title": "Products Never Reviewed",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The marketing team wants to encourage reviews for products that "
            "have none. Find all products that have never been reviewed. Return "
            "the product id, name, and price."
        ),
        "schema_hint": ["products", "reviews"],
        "solution_query": (
            "SELECT p.id, p.name, p.price\n"
            "FROM products p\n"
            "LEFT JOIN reviews r ON p.id = r.product_id\n"
            "WHERE r.id IS NULL\n"
            "ORDER BY p.name;"
        ),
        "hints": [
            "This is similar to finding customers who never ordered.",
            "LEFT JOIN preserves all products, even those without reviews.",
            "After the LEFT JOIN, unmatched products have NULL in review columns.",
            "Filter with WHERE r.id IS NULL to isolate unreviewed products.",
        ],
        "explanation": (
            "1. LEFT JOIN products to reviews keeps all products.\n"
            "2. Products with no reviews have NULL in all review columns.\n"
            "3. WHERE r.id IS NULL filters to only unreviewed products."
        ),
        "approach": [
            "Apply the anti-join pattern: LEFT JOIN + IS NULL.",
            "This is the same pattern as 'customers without orders'.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which excludes the products you are looking for.",
            "Using WHERE r.product_id IS NULL instead of r.id — both work but r.id is cleaner.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join pattern"],
    },
    {
        "id": "ec-024",
        "slug": "customers-who-reviewed-own-purchases",
        "title": "Customers Who Reviewed Their Purchases",
        "difficulty": "hard",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The data quality team wants to verify that reviews come from actual "
            "buyers. Find all reviews where the reviewer actually purchased the "
            "product. Return the customer's full name, product name, rating, and "
            "order_date. A customer purchased a product if they have an order "
            "containing that product in order_items."
        ),
        "schema_hint": ["reviews", "customers", "products", "orders", "order_items"],
        "solution_query": (
            "SELECT DISTINCT\n"
            "       c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       p.name AS product_name,\n"
            "       r.rating,\n"
            "       o.order_date\n"
            "FROM reviews r\n"
            "JOIN customers c ON r.customer_id = c.id\n"
            "JOIN products p ON r.product_id = p.id\n"
            "JOIN orders o ON o.customer_id = r.customer_id\n"
            "JOIN order_items oi ON oi.order_id = o.id AND oi.product_id = r.product_id\n"
            "ORDER BY customer_name, product_name;"
        ),
        "hints": [
            "You need to connect reviews to actual purchases through orders and order_items.",
            "The key condition is that the same customer_id and product_id appear in both reviews and order_items.",
            "Join orders on customer_id, then order_items on both order_id and product_id.",
            "Use DISTINCT to avoid duplicates if a customer bought the same product in multiple orders.",
        ],
        "explanation": (
            "1. Start from reviews and join customers and products for display names.\n"
            "2. Join orders on customer_id to find the reviewer's orders.\n"
            "3. Join order_items on both order_id and product_id to confirm the product was in that order.\n"
            "4. DISTINCT removes duplicates from multiple purchases of the same product."
        ),
        "approach": [
            "Trace the path: review -> customer's orders -> order_items containing the reviewed product.",
            "The critical join condition is matching both customer and product through orders/order_items.",
            "Use DISTINCT to handle edge cases.",
        ],
        "common_mistakes": [
            "Joining order_items only on product_id without going through orders, which matches other customers' purchases.",
            "Forgetting DISTINCT, leading to duplicate rows when a product was purchased multiple times.",
            "Missing the dual condition on the order_items join (both order_id and product_id).",
        ],
        "concept_tags": ["JOIN", "multi-table join", "DISTINCT", "complex join conditions"],
    },

    # =========================================================================
    # LEVEL 4 — SUBQUERIES (6 problems: ec-025 through ec-030)
    # =========================================================================
    {
        "id": "ec-025",
        "slug": "above-average-price-products",
        "title": "Products Priced Above Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "The pricing team wants to identify premium products. Find all "
            "products whose price is above the overall average product price. "
            "Return the product name, price, and the average price for reference."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name,\n"
            "       price,\n"
            "       (SELECT ROUND(AVG(price), 2) FROM products) AS avg_price\n"
            "FROM products\n"
            "WHERE price > (SELECT AVG(price) FROM products)\n"
            "ORDER BY price DESC;"
        ),
        "hints": [
            "You need to compare each product's price against the overall average.",
            "A subquery in the WHERE clause can compute the average dynamically.",
            "You cannot use AVG(price) directly in a WHERE clause without a subquery.",
            "Use a scalar subquery: WHERE price > (SELECT AVG(price) FROM products).",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(price) FROM products) computes the overall average.\n"
            "2. The outer WHERE clause filters products whose price exceeds that average.\n"
            "3. A second scalar subquery in SELECT displays the average for reference."
        ),
        "approach": [
            "Compute the average in a subquery.",
            "Compare each row's price against that average in WHERE.",
            "Optionally include the average as a column for context.",
        ],
        "common_mistakes": [
            "Trying to use WHERE price > AVG(price) without a subquery, which is a syntax error.",
            "Hardcoding the average value instead of computing it dynamically.",
        ],
        "concept_tags": ["subquery", "scalar subquery", "AVG", "WHERE"],
    },
    {
        "id": "ec-026",
        "slug": "customers-with-above-avg-spending",
        "title": "High-Spending Customers",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Identify VIP customers whose total spending exceeds the average "
            "customer's total spending. Return the customer's full name and "
            "their total spent. Use a subquery to compute the average total "
            "spending per customer."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       SUM(o.total_amount) AS total_spent\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING SUM(o.total_amount) > (\n"
            "    SELECT AVG(customer_total)\n"
            "    FROM (\n"
            "        SELECT SUM(total_amount) AS customer_total\n"
            "        FROM orders\n"
            "        GROUP BY customer_id\n"
            "    ) AS customer_totals\n"
            ")\n"
            "ORDER BY total_spent DESC;"
        ),
        "hints": [
            "First, you need each customer's total spending (GROUP BY + SUM).",
            "Then, you need the average of those totals — that is the average of an aggregate.",
            "A subquery in the FROM clause (derived table) can compute per-customer totals.",
            "Use that derived table inside another subquery to get the average, then compare in HAVING.",
        ],
        "explanation": (
            "1. The innermost subquery groups orders by customer_id and sums total_amount.\n"
            "2. The middle subquery computes the AVG of those per-customer totals.\n"
            "3. The outer query joins customers to orders, groups by customer, and uses HAVING to filter.\n"
            "4. Only customers whose total spending exceeds the average customer total are returned."
        ),
        "approach": [
            "Break the problem into layers: per-customer totals, average of those totals, then filter.",
            "Build from the inside out: first the derived table, then the average, then the main query.",
        ],
        "common_mistakes": [
            "Computing AVG(total_amount) directly, which gives the average per order, not per customer.",
            "Putting the subquery in WHERE instead of HAVING — you need to filter after GROUP BY.",
        ],
        "concept_tags": ["subquery", "derived table", "HAVING", "SUM", "AVG"],
    },
    {
        "id": "ec-027",
        "slug": "most-expensive-product-per-category",
        "title": "Most Expensive Product Per Category",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "For each category, find the product with the highest price. "
            "Return the category name, product name, and price. Use a "
            "correlated subquery to identify the max-priced product."
        ),
        "schema_hint": ["products", "categories"],
        "solution_query": (
            "SELECT c.name AS category_name,\n"
            "       p.name AS product_name,\n"
            "       p.price\n"
            "FROM products p\n"
            "JOIN categories c ON p.category_id = c.id\n"
            "WHERE p.price = (\n"
            "    SELECT MAX(p2.price)\n"
            "    FROM products p2\n"
            "    WHERE p2.category_id = p.category_id\n"
            ")\n"
            "ORDER BY p.price DESC;"
        ),
        "hints": [
            "A correlated subquery references a column from the outer query.",
            "For each product, check if its price equals the max price in its category.",
            "The inner query must filter on the same category_id as the outer row.",
            "WHERE p.price = (SELECT MAX(p2.price) FROM products p2 WHERE p2.category_id = p.category_id)",
        ],
        "explanation": (
            "1. For each row in the outer query, the correlated subquery finds the MAX price "
            "in the same category.\n"
            "2. The WHERE clause keeps only the product(s) matching that max price.\n"
            "3. If two products tie for the highest price, both appear."
        ),
        "approach": [
            "Use a correlated subquery that runs once per outer row.",
            "The subquery finds the max price within the same category.",
            "Compare the outer product's price to that max.",
        ],
        "common_mistakes": [
            "Writing a non-correlated subquery that finds the global max instead of per-category max.",
            "Forgetting that ties are possible — multiple products may share the max price.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "WHERE"],
    },
    {
        "id": "ec-028",
        "slug": "customers-who-ordered-every-category",
        "title": "Customers Who Ordered from Every Category",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Find customers who have purchased at least one product from every "
            "category. Return their full name and email. This requires checking "
            "that the count of distinct categories in a customer's orders equals "
            "the total number of categories."
        ),
        "schema_hint": ["customers", "orders", "order_items", "products", "categories"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       c.email\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "JOIN order_items oi ON o.id = oi.order_id\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "GROUP BY c.id, c.first_name, c.last_name, c.email\n"
            "HAVING COUNT(DISTINCT p.category_id) = (SELECT COUNT(*) FROM categories);"
        ),
        "hints": [
            "You need to count how many distinct categories each customer has ordered from.",
            "Compare that count to the total number of categories in the system.",
            "Join customers -> orders -> order_items -> products to reach category_id.",
            "HAVING COUNT(DISTINCT p.category_id) = (SELECT COUNT(*) FROM categories)",
        ],
        "explanation": (
            "1. Join the chain: customers -> orders -> order_items -> products.\n"
            "2. GROUP BY customer to aggregate.\n"
            "3. COUNT(DISTINCT p.category_id) counts unique categories per customer.\n"
            "4. The subquery (SELECT COUNT(*) FROM categories) gives the total category count.\n"
            "5. HAVING ensures only customers covering all categories are returned."
        ),
        "approach": [
            "Trace the join path from customers to category_id through orders and order_items.",
            "Count distinct categories per customer.",
            "Compare against the total category count using a subquery.",
        ],
        "common_mistakes": [
            "Using COUNT(p.category_id) without DISTINCT, which counts duplicate categories.",
            "Hardcoding the number of categories instead of using a subquery.",
            "Forgetting one of the intermediate joins in the chain.",
        ],
        "concept_tags": ["subquery", "COUNT DISTINCT", "HAVING", "multi-table join", "relational division"],
    },
    {
        "id": "ec-029",
        "slug": "products-ordered-but-not-reviewed",
        "title": "Products Ordered but Never Reviewed",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "The product team wants to solicit reviews for products that have "
            "been sold but never reviewed. Find products that appear in at least "
            "one order but have no reviews. Use EXISTS and NOT EXISTS."
        ),
        "schema_hint": ["products", "order_items", "reviews"],
        "solution_query": (
            "SELECT p.id, p.name, p.price\n"
            "FROM products p\n"
            "WHERE EXISTS (\n"
            "    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id\n"
            ")\n"
            "AND NOT EXISTS (\n"
            "    SELECT 1 FROM reviews r WHERE r.product_id = p.id\n"
            ")\n"
            "ORDER BY p.name;"
        ),
        "hints": [
            "EXISTS returns true if the subquery finds at least one matching row.",
            "NOT EXISTS returns true if the subquery finds no matching rows.",
            "Combine both to find products that are ordered (EXISTS) but not reviewed (NOT EXISTS).",
            "Each subquery is correlated — it references p.id from the outer query.",
        ],
        "explanation": (
            "1. EXISTS checks that at least one order_item row references this product.\n"
            "2. NOT EXISTS checks that no review row references this product.\n"
            "3. Both conditions must be true: ordered AND not reviewed."
        ),
        "approach": [
            "Use EXISTS for a positive existence check (has been ordered).",
            "Use NOT EXISTS for a negative existence check (never reviewed).",
            "Both are correlated subqueries referencing the outer product's id.",
        ],
        "common_mistakes": [
            "Using IN instead of EXISTS — both work but EXISTS is often more efficient for existence checks.",
            "Reversing the logic: NOT EXISTS for orders and EXISTS for reviews.",
        ],
        "concept_tags": ["EXISTS", "NOT EXISTS", "correlated subquery"],
    },
    {
        "id": "ec-030",
        "slug": "orders-above-customer-average",
        "title": "Orders Above Customer's Own Average",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "For each customer, find orders whose total_amount exceeds that "
            "specific customer's average order value. Return the customer's "
            "full name, order id, total_amount, and their personal average "
            "order value. This requires a correlated subquery."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       o.id AS order_id,\n"
            "       o.total_amount,\n"
            "       ROUND((\n"
            "           SELECT AVG(o2.total_amount)\n"
            "           FROM orders o2\n"
            "           WHERE o2.customer_id = o.customer_id\n"
            "       ), 2) AS customer_avg\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.id\n"
            "WHERE o.total_amount > (\n"
            "    SELECT AVG(o3.total_amount)\n"
            "    FROM orders o3\n"
            "    WHERE o3.customer_id = o.customer_id\n"
            ")\n"
            "ORDER BY customer_name, o.total_amount DESC;"
        ),
        "hints": [
            "Each customer has a different average — you need a per-customer comparison.",
            "A correlated subquery can compute the average for the current row's customer.",
            "The subquery must filter by the same customer_id as the outer row.",
            "Use the correlated subquery in both WHERE (for filtering) and SELECT (for display).",
        ],
        "explanation": (
            "1. For each order, the correlated subquery computes AVG(total_amount) for that customer.\n"
            "2. The WHERE clause keeps only orders exceeding their customer's average.\n"
            "3. A second correlated subquery in SELECT displays the average for reference.\n"
            "4. Results are sorted by customer name, then by amount descending."
        ),
        "approach": [
            "Write a correlated subquery that computes each customer's average order value.",
            "Use it in WHERE to filter, and in SELECT to display.",
            "The subquery runs for each outer row, filtering by customer_id.",
        ],
        "common_mistakes": [
            "Using the global average instead of a per-customer average.",
            "Forgetting that the subquery must be correlated (must reference the outer query's customer_id).",
            "Using HAVING instead of WHERE — HAVING is for grouped results, not row-level filtering.",
        ],
        "concept_tags": ["correlated subquery", "AVG", "scalar subquery"],
    },

    # =========================================================================
    # LEVEL 5 — WINDOW FUNCTIONS (5 problems: ec-031 through ec-035)
    # =========================================================================
    {
        "id": "ec-031",
        "slug": "rank-products-by-price",
        "title": "Rank Products by Price Within Category",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "The catalog team wants to rank products by price within each "
            "category. Return the category name, product name, price, and "
            "a rank (1 = most expensive). Use RANK() so ties share the same rank."
        ),
        "schema_hint": ["products", "categories"],
        "solution_query": (
            "SELECT c.name AS category_name,\n"
            "       p.name AS product_name,\n"
            "       p.price,\n"
            "       RANK() OVER (PARTITION BY c.id ORDER BY p.price DESC) AS price_rank\n"
            "FROM products p\n"
            "JOIN categories c ON p.category_id = c.id\n"
            "ORDER BY c.name, price_rank;"
        ),
        "hints": [
            "Window functions compute values across a set of rows without collapsing them.",
            "PARTITION BY divides rows into groups (like GROUP BY, but without aggregating).",
            "RANK() assigns a rank within each partition, with gaps after ties.",
            "RANK() OVER (PARTITION BY ... ORDER BY ...) is the syntax.",
        ],
        "explanation": (
            "1. PARTITION BY c.id creates a window per category.\n"
            "2. ORDER BY p.price DESC means rank 1 is the most expensive.\n"
            "3. RANK() assigns the same rank to tied prices and skips subsequent ranks.\n"
            "4. Unlike GROUP BY, window functions preserve individual rows."
        ),
        "approach": [
            "Join products to categories for the category name.",
            "Apply RANK() with PARTITION BY category and ORDER BY price descending.",
            "Sort the final output by category name and rank.",
        ],
        "common_mistakes": [
            "Using ROW_NUMBER instead of RANK, which does not handle ties correctly.",
            "Forgetting PARTITION BY, which ranks all products globally instead of per category.",
            "Using GROUP BY instead of window functions, which would collapse rows.",
        ],
        "concept_tags": ["RANK", "window functions", "PARTITION BY", "ORDER BY"],
    },
    {
        "id": "ec-032",
        "slug": "customer-order-sequence",
        "title": "Customer Order Sequence Numbers",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each customer, assign a sequence number to their orders in "
            "chronological order (1st order, 2nd order, etc.). Return "
            "customer_id, order_id, order_date, total_amount, and the "
            "order_sequence_number."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       id AS order_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       ROW_NUMBER() OVER (\n"
            "           PARTITION BY customer_id\n"
            "           ORDER BY order_date, id\n"
            "       ) AS order_sequence_number\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_sequence_number;"
        ),
        "hints": [
            "Each customer should get their own sequence starting from 1.",
            "ROW_NUMBER assigns a unique sequential integer to each row in a partition.",
            "PARTITION BY customer_id restarts the numbering for each customer.",
            "ORDER BY order_date within the window determines the sequence order.",
        ],
        "explanation": (
            "1. PARTITION BY customer_id creates a separate sequence for each customer.\n"
            "2. ORDER BY order_date, id orders by date, with id as a tiebreaker.\n"
            "3. ROW_NUMBER() assigns 1, 2, 3, ... within each partition.\n"
            "4. Unlike RANK(), ROW_NUMBER never produces ties."
        ),
        "approach": [
            "Use ROW_NUMBER for unique sequential numbering.",
            "Partition by customer to restart for each customer.",
            "Order by date to reflect chronological sequence.",
        ],
        "common_mistakes": [
            "Using RANK instead of ROW_NUMBER when you need unique sequential numbers.",
            "Not including a tiebreaker column in ORDER BY (two orders on the same date get non-deterministic numbers).",
        ],
        "concept_tags": ["ROW_NUMBER", "window functions", "PARTITION BY"],
    },
    {
        "id": "ec-033",
        "slug": "running-total-revenue",
        "title": "Running Total of Daily Revenue",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "The finance team needs a running total of daily revenue. First "
            "compute total revenue per day, then calculate a cumulative running "
            "total across days. Return the order_date, daily revenue, and "
            "running total."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT order_date,\n"
            "       SUM(total_amount) AS daily_revenue,\n"
            "       SUM(SUM(total_amount)) OVER (ORDER BY order_date) AS running_total\n"
            "FROM orders\n"
            "GROUP BY order_date\n"
            "ORDER BY order_date;"
        ),
        "hints": [
            "First aggregate daily revenue with GROUP BY order_date.",
            "Then apply a window function on top of the aggregated result.",
            "SUM() OVER (ORDER BY ...) computes a running total by default.",
            "You can nest an aggregate inside a window function: SUM(SUM(...)) OVER (...).",
        ],
        "explanation": (
            "1. GROUP BY order_date and SUM(total_amount) gives daily revenue.\n"
            "2. SUM(...) OVER (ORDER BY order_date) computes the cumulative sum.\n"
            "3. The default window frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, "
            "which creates a running total.\n"
            "4. SUM(SUM(total_amount)) nests the aggregate inside the window function."
        ),
        "approach": [
            "Aggregate to daily level first with GROUP BY.",
            "Apply a window SUM over the aggregated values, ordered by date.",
            "The nested SUM(SUM(...)) pattern allows combining GROUP BY with window functions.",
        ],
        "common_mistakes": [
            "Trying to use a CTE or subquery when the nested aggregate approach works directly.",
            "Forgetting GROUP BY, which would give a running total per order row, not per day.",
            "Adding ROWS BETWEEN when the default frame already provides the running total.",
        ],
        "concept_tags": ["window functions", "running total", "SUM OVER", "GROUP BY"],
    },
    {
        "id": "ec-034",
        "slug": "order-value-vs-previous",
        "title": "Compare Order Value to Previous Order",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each customer's orders, show how the order value compares to "
            "their previous order. Return customer_id, order_id, order_date, "
            "total_amount, the previous order's amount, and the difference. "
            "Use LAG to access the previous row."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       id AS order_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       LAG(total_amount) OVER (\n"
            "           PARTITION BY customer_id ORDER BY order_date, id\n"
            "       ) AS prev_order_amount,\n"
            "       total_amount - LAG(total_amount) OVER (\n"
            "           PARTITION BY customer_id ORDER BY order_date, id\n"
            "       ) AS amount_change\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_date;"
        ),
        "hints": [
            "LAG accesses a value from a previous row in the window.",
            "PARTITION BY customer_id so each customer's history is separate.",
            "The first order per customer will have NULL for LAG (no previous order).",
            "Subtract the LAG value from the current value to get the change.",
        ],
        "explanation": (
            "1. LAG(total_amount) OVER (...) gets the previous order's total for each customer.\n"
            "2. PARTITION BY customer_id ensures cross-customer comparisons don't happen.\n"
            "3. ORDER BY order_date, id defines 'previous' as the chronologically prior order.\n"
            "4. The difference is simply total_amount minus the LAG value.\n"
            "5. The first order per customer has NULL for both prev_order_amount and amount_change."
        ),
        "approach": [
            "Use LAG to access the previous row's value within a window.",
            "Partition by customer so each customer's order history is independent.",
            "Compute the difference as current minus previous.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, which would compare across different customers.",
            "Using LEAD instead of LAG (LEAD looks forward, LAG looks backward).",
            "Not handling the NULL first row (acceptable to leave as NULL).",
        ],
        "concept_tags": ["LAG", "window functions", "PARTITION BY"],
    },
    {
        "id": "ec-035",
        "slug": "dense-rank-customers-by-spending",
        "title": "Dense Rank Customers by Total Spending",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Rank all customers by their total spending using DENSE_RANK (no "
            "gaps in rankings). Return customer name, total spent, and their "
            "spending rank. Show only the top 10 spenders."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT customer_name, total_spent, spending_rank\n"
            "FROM (\n"
            "    SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "           SUM(o.total_amount) AS total_spent,\n"
            "           DENSE_RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS spending_rank\n"
            "    FROM customers c\n"
            "    JOIN orders o ON c.id = o.customer_id\n"
            "    GROUP BY c.id, c.first_name, c.last_name\n"
            ") ranked\n"
            "WHERE spending_rank <= 10\n"
            "ORDER BY spending_rank;"
        ),
        "hints": [
            "DENSE_RANK assigns consecutive ranks with no gaps, even with ties.",
            "You need to aggregate first (SUM), then rank.",
            "Window functions can reference aggregate results: DENSE_RANK() OVER (ORDER BY SUM(...)).",
            "Wrap in a subquery to filter by rank (WHERE cannot reference window functions directly).",
        ],
        "explanation": (
            "1. Join customers to orders and GROUP BY customer to get total_spent.\n"
            "2. DENSE_RANK() OVER (ORDER BY SUM(o.total_amount) DESC) ranks by spending.\n"
            "3. DENSE_RANK ensures no gaps: if two customers tie at rank 2, the next is rank 3.\n"
            "4. Wrap in a subquery to filter WHERE spending_rank <= 10."
        ),
        "approach": [
            "Aggregate customer spending with GROUP BY and SUM.",
            "Apply DENSE_RANK over the aggregated amount.",
            "Use a derived table to filter on the rank.",
        ],
        "common_mistakes": [
            "Using RANK instead of DENSE_RANK, which leaves gaps after ties.",
            "Trying to filter with WHERE spending_rank <= 10 in the inner query (window functions aren't available in WHERE).",
            "Using LIMIT 10, which might exclude tied customers at rank 10.",
        ],
        "concept_tags": ["DENSE_RANK", "window functions", "derived table", "SUM", "GROUP BY"],
    },

    # =========================================================================
    # LEVEL 6 — ADVANCED (5 problems: ec-036 through ec-040)
    # =========================================================================
    {
        "id": "ec-036",
        "slug": "monthly-revenue-with-cte",
        "title": "Monthly Revenue Report with CTE",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Build a monthly revenue report using a Common Table Expression. "
            "The CTE should compute monthly revenue and order count. The main "
            "query should return the month, revenue, order count, and the "
            "month-over-month revenue change."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH monthly_stats AS (\n"
            "    SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,\n"
            "           SUM(total_amount) AS revenue,\n"
            "           COUNT(*) AS order_count\n"
            "    FROM orders\n"
            "    GROUP BY TO_CHAR(order_date, 'YYYY-MM')\n"
            ")\n"
            "SELECT month,\n"
            "       revenue,\n"
            "       order_count,\n"
            "       revenue - LAG(revenue) OVER (ORDER BY month) AS revenue_change\n"
            "FROM monthly_stats\n"
            "ORDER BY month;"
        ),
        "hints": [
            "A CTE (WITH clause) lets you define a temporary named result set.",
            "Put the aggregation logic in the CTE, and the window function in the main query.",
            "LAG over the CTE's results gives you the previous month's revenue.",
            "WITH monthly_stats AS (...) SELECT ... FROM monthly_stats",
        ],
        "explanation": (
            "1. The CTE monthly_stats aggregates orders by month: revenue and count.\n"
            "2. The main query selects from the CTE and adds a window function.\n"
            "3. LAG(revenue) OVER (ORDER BY month) gets the previous month's revenue.\n"
            "4. Subtracting gives the month-over-month change."
        ),
        "approach": [
            "Encapsulate the monthly aggregation in a CTE for readability.",
            "Apply LAG in the main query to compute changes between rows.",
            "CTEs make complex queries easier to read and debug.",
        ],
        "common_mistakes": [
            "Writing everything in one query without a CTE, making it harder to understand.",
            "Forgetting to ORDER BY month inside the LAG window, which gives unpredictable results.",
            "Placing the window function inside the CTE where GROUP BY would conflict.",
        ],
        "concept_tags": ["CTE", "WITH", "LAG", "window functions", "TO_CHAR"],
    },
    {
        "id": "ec-037",
        "slug": "revenue-pivot-by-payment-method",
        "title": "Revenue Pivot by Payment Method",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Create a pivot report showing total revenue per month broken down "
            "by payment method. Each payment method should be its own column. "
            "Use CASE expressions inside SUM to achieve the pivot. Assume "
            "methods include 'credit_card', 'debit_card', 'paypal', and 'bank_transfer'."
        ),
        "schema_hint": ["orders", "payments"],
        "solution_query": (
            "SELECT TO_CHAR(o.order_date, 'YYYY-MM') AS month,\n"
            "       SUM(CASE WHEN p.method = 'credit_card' THEN p.amount ELSE 0 END) AS credit_card,\n"
            "       SUM(CASE WHEN p.method = 'debit_card' THEN p.amount ELSE 0 END) AS debit_card,\n"
            "       SUM(CASE WHEN p.method = 'paypal' THEN p.amount ELSE 0 END) AS paypal,\n"
            "       SUM(CASE WHEN p.method = 'bank_transfer' THEN p.amount ELSE 0 END) AS bank_transfer,\n"
            "       SUM(p.amount) AS total\n"
            "FROM orders o\n"
            "JOIN payments p ON o.id = p.order_id\n"
            "GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')\n"
            "ORDER BY month;"
        ),
        "hints": [
            "PostgreSQL does not have a built-in PIVOT operator; use CASE inside aggregates.",
            "SUM(CASE WHEN condition THEN value ELSE 0 END) selectively sums values.",
            "Each payment method becomes its own CASE expression wrapped in SUM.",
            "Group by month to get one row per month.",
        ],
        "explanation": (
            "1. JOIN orders to payments to connect dates with payment methods.\n"
            "2. GROUP BY month to aggregate per time period.\n"
            "3. Each SUM(CASE ...) column checks the payment method and sums only matching amounts.\n"
            "4. The total column sums all payments regardless of method."
        ),
        "approach": [
            "Use conditional aggregation (CASE inside SUM) to create a pivot table.",
            "One SUM(CASE ...) per payment method creates one column per method.",
            "Group by the month to produce one row per time period.",
        ],
        "common_mistakes": [
            "Forgetting the ELSE 0 in the CASE, which causes NULLs that break the SUM.",
            "Using FILTER (WHERE ...) syntax, which is PostgreSQL-specific and less portable.",
            "Grouping by order_date instead of the formatted month, creating one row per day.",
        ],
        "concept_tags": ["CASE", "conditional aggregation", "pivot", "SUM", "JOIN"],
    },
    {
        "id": "ec-038",
        "slug": "days-between-order-and-delivery",
        "title": "Average Delivery Time by Carrier",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "The logistics team wants to compare carrier performance. Calculate "
            "the average number of days between order_date and delivery_date for "
            "each carrier, but only for delivered shipments. Return the carrier, "
            "total delivered shipments, and average delivery days (rounded to 1 "
            "decimal)."
        ),
        "schema_hint": ["orders", "shipping"],
        "solution_query": (
            "SELECT s.carrier,\n"
            "       COUNT(*) AS delivered_shipments,\n"
            "       ROUND(AVG(s.delivery_date - o.order_date), 1) AS avg_delivery_days\n"
            "FROM shipping s\n"
            "JOIN orders o ON s.order_id = o.id\n"
            "WHERE s.status = 'delivered'\n"
            "  AND s.delivery_date IS NOT NULL\n"
            "GROUP BY s.carrier\n"
            "ORDER BY avg_delivery_days;"
        ),
        "hints": [
            "In PostgreSQL, subtracting two dates gives the number of days as an integer.",
            "Filter for delivered shipments before aggregating.",
            "Join shipping to orders to access the order_date.",
            "delivery_date - order_date gives days; use AVG to average across shipments.",
        ],
        "explanation": (
            "1. JOIN shipping to orders to get both order_date and delivery_date.\n"
            "2. WHERE filters to delivered shipments with a non-null delivery_date.\n"
            "3. delivery_date - order_date computes days between the two dates.\n"
            "4. AVG averages those day counts per carrier.\n"
            "5. ROUND(..., 1) limits to one decimal place."
        ),
        "approach": [
            "Use PostgreSQL's date subtraction to compute delivery time.",
            "Filter to completed deliveries.",
            "Aggregate by carrier with AVG.",
        ],
        "common_mistakes": [
            "Forgetting to filter for delivered status, including in-transit shipments.",
            "Using DATEDIFF (not a PostgreSQL function) instead of simple date subtraction.",
            "Not handling NULL delivery_date, which would produce NULL in the subtraction.",
        ],
        "concept_tags": ["date arithmetic", "AVG", "GROUP BY", "JOIN", "WHERE"],
    },
    {
        "id": "ec-039",
        "slug": "top-3-products-per-category",
        "title": "Top 3 Best-Selling Products Per Category",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Find the top 3 best-selling products (by total quantity sold) in "
            "each category. Return category name, product name, total quantity "
            "sold, and the rank within the category. Use a CTE with a window "
            "function, then filter to rank <= 3."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "WITH product_sales AS (\n"
            "    SELECT p.id AS product_id,\n"
            "           p.name AS product_name,\n"
            "           c.name AS category_name,\n"
            "           SUM(oi.quantity) AS total_qty_sold\n"
            "    FROM order_items oi\n"
            "    JOIN products p ON oi.product_id = p.id\n"
            "    JOIN categories c ON p.category_id = c.id\n"
            "    GROUP BY p.id, p.name, c.name\n"
            "),\n"
            "ranked AS (\n"
            "    SELECT category_name,\n"
            "           product_name,\n"
            "           total_qty_sold,\n"
            "           ROW_NUMBER() OVER (\n"
            "               PARTITION BY category_name ORDER BY total_qty_sold DESC\n"
            "           ) AS category_rank\n"
            "    FROM product_sales\n"
            ")\n"
            "SELECT category_name, product_name, total_qty_sold, category_rank\n"
            "FROM ranked\n"
            "WHERE category_rank <= 3\n"
            "ORDER BY category_name, category_rank;"
        ),
        "hints": [
            "This is a classic Top-N per group problem.",
            "First aggregate total quantity per product, then rank within each category.",
            "Use a CTE to separate the aggregation step from the ranking step.",
            "Filter on the rank in the final SELECT (you cannot use WHERE on window functions directly).",
        ],
        "explanation": (
            "1. CTE product_sales aggregates total quantity sold per product.\n"
            "2. CTE ranked applies ROW_NUMBER partitioned by category, ordered by quantity descending.\n"
            "3. The final query filters WHERE category_rank <= 3 to keep only the top 3.\n"
            "4. Two CTEs make the logic clear and maintainable."
        ),
        "approach": [
            "Break into steps: aggregate sales, rank within category, filter top N.",
            "Use multiple CTEs for clarity.",
            "ROW_NUMBER is preferred over RANK here to guarantee exactly 3 per category.",
        ],
        "common_mistakes": [
            "Using LIMIT 3, which limits the entire result set, not per category.",
            "Using RANK instead of ROW_NUMBER when you want exactly 3 (RANK may return more due to ties).",
            "Trying to filter the window function in the WHERE clause of the same query level.",
        ],
        "concept_tags": ["CTE", "ROW_NUMBER", "Top-N per group", "PARTITION BY", "SUM"],
    },
    {
        "id": "ec-040",
        "slug": "customer-cohort-first-purchase-analysis",
        "title": "Customer Cohort Analysis by First Purchase Month",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Group customers into cohorts based on the month of their first "
            "order. For each cohort, show the number of customers, total revenue "
            "from the cohort, and average revenue per customer. Use a CTE to "
            "find each customer's first order month."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "WITH first_orders AS (\n"
            "    SELECT customer_id,\n"
            "           TO_CHAR(MIN(order_date), 'YYYY-MM') AS cohort_month\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "cohort_revenue AS (\n"
            "    SELECT fo.cohort_month,\n"
            "           fo.customer_id,\n"
            "           SUM(o.total_amount) AS customer_revenue\n"
            "    FROM first_orders fo\n"
            "    JOIN orders o ON fo.customer_id = o.customer_id\n"
            "    GROUP BY fo.cohort_month, fo.customer_id\n"
            ")\n"
            "SELECT cohort_month,\n"
            "       COUNT(*) AS cohort_size,\n"
            "       ROUND(SUM(customer_revenue), 2) AS total_revenue,\n"
            "       ROUND(AVG(customer_revenue), 2) AS avg_revenue_per_customer\n"
            "FROM cohort_revenue\n"
            "GROUP BY cohort_month\n"
            "ORDER BY cohort_month;"
        ),
        "hints": [
            "A cohort is defined by when a customer first purchased — use MIN(order_date).",
            "First CTE: find each customer's earliest order month.",
            "Second CTE: join back to orders to calculate each customer's total lifetime revenue.",
            "Final query: aggregate by cohort_month to get cohort-level metrics.",
        ],
        "explanation": (
            "1. CTE first_orders finds each customer's first order month using MIN(order_date).\n"
            "2. CTE cohort_revenue joins back to all orders to compute total revenue per customer, "
            "tagged with their cohort month.\n"
            "3. The final query groups by cohort_month to produce cohort-level summaries.\n"
            "4. COUNT gives cohort size, SUM gives total revenue, AVG gives per-customer revenue."
        ),
        "approach": [
            "Define cohorts using each customer's first order month.",
            "Compute per-customer lifetime revenue.",
            "Aggregate to the cohort level for the final report.",
            "Multiple CTEs keep each step clean and testable.",
        ],
        "common_mistakes": [
            "Using created_at from the customers table instead of the first order_date (registration is not the same as first purchase).",
            "Computing revenue only from the first order, not the customer's entire lifetime.",
            "Forgetting to group by customer in the intermediate step before grouping by cohort.",
        ],
        "concept_tags": ["CTE", "cohort analysis", "MIN", "SUM", "AVG", "GROUP BY", "TO_CHAR"],
    },
    # =========================================================================
    # LEVEL 6 — EXTENDED PROBLEMS (60 problems: ec-041 through ec-100)
    # =========================================================================
    {
        "id": "ec-041",
        "slug": "count-customers-per-country",
        "title": "Count Customers per Country",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The international expansion team wants to know where the customer "
            "base is concentrated. Count the number of customers in each country "
            "and sort by count descending."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT country, COUNT(*) AS customer_count\n"
            "FROM customers\n"
            "GROUP BY country\n"
            "ORDER BY customer_count DESC;"
        ),
        "hints": [
            "You need to group rows by a column and count them.",
            "GROUP BY country will create one row per country.",
            "COUNT(*) counts all rows in each group.",
            "Add ORDER BY on the count column to sort descending.",
        ],
        "explanation": (
            "1. GROUP BY country creates one group per distinct country.\n"
            "2. COUNT(*) counts customers in each group.\n"
            "3. ORDER BY customer_count DESC shows the largest markets first."
        ),
        "approach": [
            "Identify the customers table has the country column.",
            "Use GROUP BY country with COUNT(*).",
            "Sort descending to see the biggest markets first.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY, which would just count all customers into one row.",
            "Using ORDER BY country instead of ORDER BY customer_count DESC.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "ec-042",
        "slug": "products-never-ordered",
        "title": "Products Never Ordered",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The inventory team wants to identify dead stock. Find all products "
            "that have never appeared in any order. Return the product name and price."
        ),
        "schema_hint": ["products", "order_items"],
        "solution_query": (
            "SELECT p.name, p.price\n"
            "FROM products p\n"
            "LEFT JOIN order_items oi ON p.id = oi.product_id\n"
            "WHERE oi.id IS NULL;"
        ),
        "hints": [
            "You need to find products with no matching order_items rows.",
            "A LEFT JOIN keeps all products even if they have no order items.",
            "After a LEFT JOIN, unmatched rows have NULL in the joined table's columns.",
            "Filter for rows where the joined table's column IS NULL.",
        ],
        "explanation": (
            "1. LEFT JOIN order_items onto products to keep all products.\n"
            "2. Products with no order items will have NULL for oi.id.\n"
            "3. WHERE oi.id IS NULL filters to only those unmatched products."
        ),
        "approach": [
            "Use a LEFT JOIN from products to order_items.",
            "Filter for NULLs in the order_items side to find products with no orders.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which would exclude the very products you want to find.",
            "Using WHERE oi.id = NULL instead of IS NULL.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "dead stock"],
    },
    {
        "id": "ec-043",
        "slug": "average-order-value-by-status",
        "title": "Average Order Value by Status",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Management wants a breakdown of the average order value for each "
            "order status. Return the status and the average total_amount, "
            "rounded to 2 decimal places, sorted by average descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT status, ROUND(AVG(total_amount), 2) AS avg_order_value\n"
            "FROM orders\n"
            "GROUP BY status\n"
            "ORDER BY avg_order_value DESC;"
        ),
        "hints": [
            "You need an aggregate function that computes the mean.",
            "AVG() calculates the average of a numeric column.",
            "ROUND(value, 2) limits to two decimal places.",
            "GROUP BY status produces one row per status value.",
        ],
        "explanation": (
            "1. GROUP BY status splits orders into groups by their status.\n"
            "2. AVG(total_amount) computes the mean order value per group.\n"
            "3. ROUND(..., 2) ensures clean two-decimal output."
        ),
        "approach": [
            "Group by the status column.",
            "Use AVG to compute the mean total_amount in each group.",
            "Round and sort for a clean report.",
        ],
        "common_mistakes": [
            "Forgetting ROUND, which can produce long decimal numbers.",
            "Not including GROUP BY, which would average across all orders.",
        ],
        "concept_tags": ["AVG", "ROUND", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "ec-044",
        "slug": "orders-with-customer-names",
        "title": "Orders with Customer Names",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The customer service team needs an order list that includes "
            "customer names. Join orders with customers to show the order id, "
            "order_date, total_amount, and the customer's first and last name. "
            "Sort by order_date descending."
        ),
        "schema_hint": ["orders", "customers"],
        "solution_query": (
            "SELECT o.id, o.order_date, o.total_amount,\n"
            "       c.first_name, c.last_name\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.id\n"
            "ORDER BY o.order_date DESC;"
        ),
        "hints": [
            "You need data from two tables: orders and customers.",
            "The foreign key customer_id in orders links to id in customers.",
            "Use JOIN (INNER JOIN) to combine the tables on that key.",
            "Alias tables with short names like o and c for readability.",
        ],
        "explanation": (
            "1. JOIN customers onto orders using the customer_id foreign key.\n"
            "2. Select columns from both tables.\n"
            "3. ORDER BY order_date DESC shows the most recent orders first."
        ),
        "approach": [
            "Identify the relationship: orders.customer_id = customers.id.",
            "Use an INNER JOIN to combine the data.",
            "Select the requested columns from both tables.",
        ],
        "common_mistakes": [
            "Joining on the wrong columns (e.g., o.id = c.id instead of o.customer_id = c.id).",
            "Forgetting to qualify column names with table aliases when both tables have an id column.",
        ],
        "concept_tags": ["JOIN", "INNER JOIN", "ORDER BY"],
    },
    {
        "id": "ec-045",
        "slug": "distinct-carriers",
        "title": "Distinct Shipping Carriers",
        "difficulty": "easy",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "The logistics team needs a list of all shipping carriers used. "
            "Return the distinct carrier names sorted alphabetically."
        ),
        "schema_hint": ["shipping"],
        "solution_query": (
            "SELECT DISTINCT carrier\n"
            "FROM shipping\n"
            "ORDER BY carrier;"
        ),
        "hints": [
            "You only need unique values, not every row.",
            "The DISTINCT keyword removes duplicate values.",
            "Apply it right after SELECT.",
            "SELECT DISTINCT carrier FROM shipping will give unique carriers.",
        ],
        "explanation": (
            "1. SELECT DISTINCT carrier returns each carrier name only once.\n"
            "2. ORDER BY carrier sorts them alphabetically."
        ),
        "approach": [
            "Use DISTINCT to de-duplicate carrier values.",
            "Sort alphabetically for a clean list.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT and getting duplicate carrier names.",
            "Using GROUP BY without an aggregate — it works but DISTINCT is more idiomatic here.",
        ],
        "concept_tags": ["SELECT", "DISTINCT", "ORDER BY"],
    },
    {
        "id": "ec-046",
        "slug": "total-revenue-per-category",
        "title": "Total Revenue per Product Category",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The finance team wants total revenue broken down by product category. "
            "Calculate the sum of (quantity * unit_price) from order_items, grouped "
            "by category name. Only include orders with status 'delivered'. "
            "Sort by total revenue descending."
        ),
        "schema_hint": ["order_items", "products", "categories", "orders"],
        "solution_query": (
            "SELECT cat.name AS category_name,\n"
            "       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue\n"
            "FROM order_items oi\n"
            "JOIN orders o ON oi.order_id = o.id\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "JOIN categories cat ON p.category_id = cat.id\n"
            "WHERE o.status = 'delivered'\n"
            "GROUP BY cat.name\n"
            "ORDER BY total_revenue DESC;"
        ),
        "hints": [
            "You need to join multiple tables to connect order_items to category names.",
            "The chain is: order_items -> products -> categories, and order_items -> orders for the status filter.",
            "Revenue per line item is quantity * unit_price.",
            "GROUP BY the category name and SUM the revenue.",
        ],
        "explanation": (
            "1. Join order_items to orders (for status filter), products, and categories.\n"
            "2. WHERE o.status = 'delivered' restricts to completed sales.\n"
            "3. SUM(oi.quantity * oi.unit_price) calculates revenue per category.\n"
            "4. GROUP BY cat.name aggregates at the category level."
        ),
        "approach": [
            "Chain joins: order_items -> orders, order_items -> products -> categories.",
            "Filter on order status before aggregating.",
            "Use SUM on the calculated line-item revenue.",
        ],
        "common_mistakes": [
            "Forgetting to join to orders, so the status filter cannot be applied.",
            "Using product price instead of order_item unit_price (they may differ).",
            "Not accounting for discounts if the question required net revenue.",
        ],
        "concept_tags": ["JOIN", "SUM", "GROUP BY", "multi-table join"],
    },
    {
        "id": "ec-047",
        "slug": "customers-with-multiple-orders",
        "title": "Customers with Multiple Orders",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Identify repeat buyers. Find customers who have placed more than "
            "one order. Return their customer id, first name, last name, and "
            "order count, sorted by order count descending."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.id, c.first_name, c.last_name,\n"
            "       COUNT(o.id) AS order_count\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(o.id) > 1\n"
            "ORDER BY order_count DESC;"
        ),
        "hints": [
            "You need to count orders per customer, then filter by count.",
            "JOIN customers to orders on the customer_id foreign key.",
            "HAVING lets you filter after GROUP BY (unlike WHERE which filters before).",
            "HAVING COUNT(o.id) > 1 keeps only customers with more than one order.",
        ],
        "explanation": (
            "1. JOIN customers to orders to pair each customer with their orders.\n"
            "2. GROUP BY customer to count orders per customer.\n"
            "3. HAVING COUNT(o.id) > 1 filters to repeat buyers only."
        ),
        "approach": [
            "Join the two tables on customer_id.",
            "Group by customer and count their orders.",
            "Use HAVING to filter groups with more than 1 order.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING to filter on the aggregate.",
            "Forgetting to GROUP BY, which would count all orders into one row.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT"],
    },
    {
        "id": "ec-048",
        "slug": "payment-method-distribution",
        "title": "Payment Method Distribution",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The payments team wants to see how payment methods are distributed. "
            "For each payment method, show the count of payments and the total "
            "amount collected where the payment status is 'completed'. Sort by "
            "total amount descending."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT method,\n"
            "       COUNT(*) AS payment_count,\n"
            "       ROUND(SUM(amount), 2) AS total_collected\n"
            "FROM payments\n"
            "WHERE status = 'completed'\n"
            "GROUP BY method\n"
            "ORDER BY total_collected DESC;"
        ),
        "hints": [
            "Filter for completed payments first, then aggregate.",
            "Use WHERE to filter rows before grouping.",
            "GROUP BY method to get one row per payment method.",
            "Use COUNT(*) and SUM(amount) for the metrics.",
        ],
        "explanation": (
            "1. WHERE status = 'completed' filters to successful payments.\n"
            "2. GROUP BY method aggregates by payment type.\n"
            "3. COUNT(*) and SUM(amount) give the requested metrics."
        ),
        "approach": [
            "Filter with WHERE before aggregating.",
            "Group by payment method.",
            "Calculate count and sum in the SELECT.",
        ],
        "common_mistakes": [
            "Putting the status filter in HAVING instead of WHERE — it works but is less efficient.",
            "Forgetting to filter by status and including pending/failed payments.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "SUM", "WHERE"],
    },
    {
        "id": "ec-049",
        "slug": "products-above-average-price",
        "title": "Products Above Average Price",
        "difficulty": "easy",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Find all products whose price is above the overall average product "
            "price. Return the product name, price, and category_id, sorted by "
            "price descending."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price, category_id\n"
            "FROM products\n"
            "WHERE price > (SELECT AVG(price) FROM products)\n"
            "ORDER BY price DESC;"
        ),
        "hints": [
            "You need to compare each product's price to the overall average.",
            "A subquery can compute the average price independently.",
            "Place the subquery in the WHERE clause as a scalar value.",
            "WHERE price > (SELECT AVG(price) FROM ...) compares each row to the average.",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(price) FROM products) calculates the overall average.\n"
            "2. The outer WHERE clause filters products whose price exceeds that average.\n"
            "3. ORDER BY price DESC shows the most expensive first."
        ),
        "approach": [
            "Use a scalar subquery to compute the average price.",
            "Compare each product's price to that average in WHERE.",
        ],
        "common_mistakes": [
            "Trying to use AVG(price) directly in WHERE without a subquery.",
            "Using HAVING instead of WHERE — HAVING is for filtering after GROUP BY.",
        ],
        "concept_tags": ["subquery", "AVG", "WHERE", "scalar subquery"],
    },
    {
        "id": "ec-050",
        "slug": "monthly-order-count",
        "title": "Monthly Order Count",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The operations team needs to see order volume trends. Count the "
            "number of orders placed each month. Return the month (as YYYY-MM) "
            "and the order count, sorted chronologically."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT strftime('%Y-%m', order_date) AS order_month,\n"
            "       COUNT(*) AS order_count\n"
            "FROM orders\n"
            "GROUP BY order_month\n"
            "ORDER BY order_month;"
        ),
        "hints": [
            "You need to extract the year and month from order_date.",
            "SQLite uses strftime() for date formatting.",
            "strftime('%Y-%m', date_column) extracts YYYY-MM.",
            "Group by the formatted month and count rows in each group.",
        ],
        "explanation": (
            "1. strftime('%Y-%m', order_date) extracts the year-month portion.\n"
            "2. GROUP BY order_month aggregates orders into monthly buckets.\n"
            "3. COUNT(*) counts orders in each month."
        ),
        "approach": [
            "Use strftime to format the date into year-month.",
            "Group by the formatted string and count.",
            "Sort chronologically by the same string.",
        ],
        "common_mistakes": [
            "Using non-SQLite date functions like MONTH() or DATE_FORMAT().",
            "Forgetting to sort, which may return months in arbitrary order.",
        ],
        "concept_tags": ["strftime", "GROUP BY", "COUNT", "date functions"],
    },
    {
        "id": "ec-051",
        "slug": "top-spending-customers",
        "title": "Top 10 Spending Customers",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Find the top 10 customers by total spending. Return their first name, "
            "last name, and total amount spent (sum of order total_amount), "
            "sorted by total spent descending. Only include non-cancelled orders."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       ROUND(SUM(o.total_amount), 2) AS total_spent\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "WHERE o.status != 'cancelled'\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY total_spent DESC\n"
            "LIMIT 10;"
        ),
        "hints": [
            "Join customers to orders and sum the order amounts per customer.",
            "Exclude cancelled orders with a WHERE filter.",
            "GROUP BY customer to aggregate their spending.",
            "Use LIMIT 10 to restrict to the top spenders.",
        ],
        "explanation": (
            "1. JOIN connects customers to their orders.\n"
            "2. WHERE filters out cancelled orders.\n"
            "3. GROUP BY customer aggregates total_amount into total_spent.\n"
            "4. ORDER BY DESC and LIMIT 10 returns the top spenders."
        ),
        "approach": [
            "Join customers to orders, filter out cancellations.",
            "Sum total_amount per customer.",
            "Sort descending and limit to 10.",
        ],
        "common_mistakes": [
            "Including cancelled orders in the total.",
            "Using LIMIT without ORDER BY, which gives arbitrary rows.",
        ],
        "concept_tags": ["JOIN", "SUM", "GROUP BY", "LIMIT", "ORDER BY"],
    },
    {
        "id": "ec-052",
        "slug": "order-items-with-discount",
        "title": "Order Items with Discounts Applied",
        "difficulty": "easy",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "Find all order items where a discount was applied (discount > 0). "
            "Return the order_id, product_id, quantity, unit_price, discount, "
            "and the net line total calculated as quantity * unit_price * (1 - discount). "
            "Sort by net line total descending."
        ),
        "schema_hint": ["order_items"],
        "solution_query": (
            "SELECT order_id, product_id, quantity, unit_price, discount,\n"
            "       ROUND(quantity * unit_price * (1 - discount), 2) AS net_line_total\n"
            "FROM order_items\n"
            "WHERE discount > 0\n"
            "ORDER BY net_line_total DESC;"
        ),
        "hints": [
            "Filter for rows where discount is greater than zero.",
            "Calculate the net total using the discount as a percentage.",
            "If discount is 0.1, the customer pays 90%, so multiply by (1 - discount).",
            "Use ROUND to keep the result to 2 decimal places.",
        ],
        "explanation": (
            "1. WHERE discount > 0 finds items with discounts.\n"
            "2. quantity * unit_price * (1 - discount) computes the net revenue.\n"
            "3. ROUND cleans up floating point results."
        ),
        "approach": [
            "Filter for discounted items.",
            "Compute the net line total with an arithmetic expression.",
            "Round and sort the results.",
        ],
        "common_mistakes": [
            "Subtracting the discount instead of multiplying by (1 - discount).",
            "Forgetting that discount is a decimal (e.g., 0.1 for 10%), not a dollar amount.",
        ],
        "concept_tags": ["SELECT", "WHERE", "arithmetic", "ROUND"],
    },
    {
        "id": "ec-053",
        "slug": "customers-no-reviews",
        "title": "Customers Who Never Left a Review",
        "difficulty": "easy",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "The marketing team wants to encourage reviews. Find customers who "
            "have never written a review. Return their first name, last name, "
            "and email, sorted by last name."
        ),
        "schema_hint": ["customers", "reviews"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE id NOT IN (SELECT DISTINCT customer_id FROM reviews)\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "You need to find customers absent from the reviews table.",
            "NOT IN with a subquery can check for absence.",
            "The subquery should return all customer_ids that appear in reviews.",
            "Alternatively, a LEFT JOIN with IS NULL works too.",
        ],
        "explanation": (
            "1. The subquery gets all customer_ids present in reviews.\n"
            "2. NOT IN excludes those customers from the outer query.\n"
            "3. The result is customers who have zero reviews."
        ),
        "approach": [
            "Use a subquery to get the set of customers who have reviewed.",
            "Exclude that set from the full customers table.",
        ],
        "common_mistakes": [
            "Using IN instead of NOT IN, which gives customers who HAVE reviewed.",
            "Not handling potential NULLs in NOT IN subqueries (less of an issue here since customer_id is NOT NULL in reviews).",
        ],
        "concept_tags": ["NOT IN", "subquery", "anti-join pattern"],
    },
    {
        "id": "ec-054",
        "slug": "average-shipping-days",
        "title": "Average Shipping Duration by Carrier",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Calculate the average number of days between shipping_date and "
            "delivery_date for each carrier. Only include shipments that have "
            "been delivered (delivery_date IS NOT NULL). Round to 1 decimal place "
            "and sort by average days ascending."
        ),
        "schema_hint": ["shipping"],
        "solution_query": (
            "SELECT carrier,\n"
            "       ROUND(AVG(julianday(delivery_date) - julianday(shipping_date)), 1) AS avg_days\n"
            "FROM shipping\n"
            "WHERE delivery_date IS NOT NULL\n"
            "GROUP BY carrier\n"
            "ORDER BY avg_days;"
        ),
        "hints": [
            "You need to compute the difference between two dates in days.",
            "SQLite's julianday() function converts dates to a numeric day value.",
            "Subtracting two julianday() values gives the number of days between them.",
            "Filter out rows where delivery_date is NULL before averaging.",
        ],
        "explanation": (
            "1. julianday(delivery_date) - julianday(shipping_date) gives days in transit.\n"
            "2. AVG computes the mean across all shipments for each carrier.\n"
            "3. WHERE delivery_date IS NOT NULL excludes undelivered packages."
        ),
        "approach": [
            "Use julianday() for date arithmetic in SQLite.",
            "Filter for delivered shipments.",
            "Group by carrier and average the day differences.",
        ],
        "common_mistakes": [
            "Using DATEDIFF which is not available in SQLite.",
            "Forgetting to exclude NULL delivery dates, which would produce NULL averages.",
        ],
        "concept_tags": ["julianday", "AVG", "GROUP BY", "date arithmetic"],
    },
    {
        "id": "ec-055",
        "slug": "revenue-with-and-without-discount",
        "title": "Revenue Impact of Discounts",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Compare gross revenue vs net revenue across all order items. "
            "Calculate the total gross revenue (quantity * unit_price), "
            "total net revenue (quantity * unit_price * (1 - discount)), "
            "and the total discount amount (gross - net). Return a single "
            "row with all three values rounded to 2 decimal places."
        ),
        "schema_hint": ["order_items"],
        "solution_query": (
            "SELECT ROUND(SUM(quantity * unit_price), 2) AS gross_revenue,\n"
            "       ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS net_revenue,\n"
            "       ROUND(SUM(quantity * unit_price) - SUM(quantity * unit_price * (1 - discount)), 2) AS total_discount\n"
            "FROM order_items;"
        ),
        "hints": [
            "This is an aggregation without GROUP BY — the entire table is one group.",
            "Gross revenue ignores discounts; net revenue applies them.",
            "The discount amount is the difference between gross and net.",
            "SUM across all rows to get totals.",
        ],
        "explanation": (
            "1. SUM(quantity * unit_price) computes gross revenue across all items.\n"
            "2. SUM(quantity * unit_price * (1 - discount)) computes net revenue.\n"
            "3. The difference is the total discount given."
        ),
        "approach": [
            "Use SUM with arithmetic expressions for each metric.",
            "No GROUP BY needed — we want a single summary row.",
            "Round all values for clean output.",
        ],
        "common_mistakes": [
            "Trying to compute discount as SUM(discount), which sums the percentages, not dollar amounts.",
            "Forgetting that discount is a fraction, not a dollar value.",
        ],
        "concept_tags": ["SUM", "arithmetic", "ROUND", "aggregate without GROUP BY"],
    },
    {
        "id": "ec-056",
        "slug": "rank-products-by-revenue",
        "title": "Rank Products by Revenue Within Category",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each product, calculate its total revenue from order_items "
            "(quantity * unit_price) and rank it within its category using "
            "RANK(). Return the category name, product name, total revenue "
            "(rounded to 2), and the rank. Order by category name, then rank."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "SELECT cat.name AS category_name,\n"
            "       p.name AS product_name,\n"
            "       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,\n"
            "       RANK() OVER (\n"
            "           PARTITION BY cat.name\n"
            "           ORDER BY SUM(oi.quantity * oi.unit_price) DESC\n"
            "       ) AS revenue_rank\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "JOIN categories cat ON p.category_id = cat.id\n"
            "GROUP BY cat.name, p.name\n"
            "ORDER BY cat.name, revenue_rank;"
        ),
        "hints": [
            "First aggregate revenue per product, then rank within each category.",
            "Window functions like RANK() can be used with GROUP BY in the same query.",
            "PARTITION BY category separates the ranking into per-category groups.",
            "The ORDER BY inside the window function determines the ranking order.",
        ],
        "explanation": (
            "1. JOIN links order_items to products and categories.\n"
            "2. GROUP BY cat.name, p.name aggregates revenue per product.\n"
            "3. RANK() OVER (PARTITION BY cat.name ORDER BY revenue DESC) ranks within each category.\n"
            "4. Products with tied revenue get the same rank."
        ),
        "approach": [
            "Join tables to get category names alongside order item data.",
            "Group by category and product to sum revenue.",
            "Apply RANK() partitioned by category.",
        ],
        "common_mistakes": [
            "Using ROW_NUMBER instead of RANK when ties should share the same rank.",
            "Forgetting GROUP BY — window functions work on the result set after grouping.",
            "Using PARTITION BY product instead of category.",
        ],
        "concept_tags": ["RANK", "PARTITION BY", "window functions", "GROUP BY", "JOIN"],
    },
    {
        "id": "ec-057",
        "slug": "running-total-of-payments",
        "title": "Running Total of Payments",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Create a running total of completed payments over time. For each "
            "completed payment, show the payment_date, amount, and a cumulative "
            "sum of amounts ordered by payment_date. Sort by payment_date."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT payment_date, amount,\n"
            "       SUM(amount) OVER (\n"
            "           ORDER BY payment_date\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS running_total\n"
            "FROM payments\n"
            "WHERE status = 'completed'\n"
            "ORDER BY payment_date;"
        ),
        "hints": [
            "A running total accumulates values as you move through rows.",
            "SUM() can be used as a window function with OVER().",
            "ORDER BY inside the OVER clause defines the accumulation order.",
            "The frame clause ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW gives a running total.",
        ],
        "explanation": (
            "1. WHERE status = 'completed' filters to successful payments.\n"
            "2. SUM(amount) OVER (ORDER BY payment_date ...) accumulates the total.\n"
            "3. The frame ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ensures "
            "each row includes all prior rows plus itself."
        ),
        "approach": [
            "Filter to completed payments.",
            "Use SUM as a window function with an ORDER BY clause.",
            "The default frame for ORDER BY is already a running total, but specifying it is clearer.",
        ],
        "common_mistakes": [
            "Using GROUP BY instead of a window function, which collapses rows.",
            "Forgetting the WHERE filter for completed payments.",
            "Not specifying the frame clause, relying on implicit behavior.",
        ],
        "concept_tags": ["window functions", "SUM OVER", "running total", "frame clause"],
    },
    {
        "id": "ec-058",
        "slug": "order-with-most-items",
        "title": "Orders with the Most Line Items",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Find the orders that have the most distinct products (line items). "
            "Return the order_id, the count of distinct products, and the "
            "order total_amount. Show only orders whose product count equals "
            "the maximum across all orders."
        ),
        "schema_hint": ["order_items", "orders"],
        "solution_query": (
            "SELECT oi.order_id,\n"
            "       COUNT(DISTINCT oi.product_id) AS product_count,\n"
            "       o.total_amount\n"
            "FROM order_items oi\n"
            "JOIN orders o ON oi.order_id = o.id\n"
            "GROUP BY oi.order_id, o.total_amount\n"
            "HAVING COUNT(DISTINCT oi.product_id) = (\n"
            "    SELECT MAX(cnt) FROM (\n"
            "        SELECT COUNT(DISTINCT product_id) AS cnt\n"
            "        FROM order_items\n"
            "        GROUP BY order_id\n"
            "    )\n"
            ");"
        ),
        "hints": [
            "First figure out how many distinct products each order has.",
            "Then find the maximum of that count across all orders.",
            "A subquery in HAVING can compare each group's count to the max.",
            "You need a nested subquery: inner one counts per order, outer one finds MAX.",
        ],
        "explanation": (
            "1. GROUP BY order_id and count distinct products per order.\n"
            "2. The nested subquery computes all per-order counts, then MAX finds the highest.\n"
            "3. HAVING filters to only orders matching that maximum count."
        ),
        "approach": [
            "Count distinct products per order.",
            "Use a subquery to find the maximum count.",
            "Filter with HAVING to keep only orders matching the max.",
        ],
        "common_mistakes": [
            "Using LIMIT 1 which misses ties — multiple orders could share the max.",
            "Counting rows instead of DISTINCT products (an order may have multiple rows for the same product).",
        ],
        "concept_tags": ["HAVING", "subquery", "COUNT DISTINCT", "MAX", "nested subquery"],
    },
    {
        "id": "ec-059",
        "slug": "customer-order-gap-analysis",
        "title": "Days Between Consecutive Customer Orders",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each customer who has placed at least 2 orders, calculate the "
            "number of days between each consecutive order using LAG(). Return "
            "the customer_id, order_date, previous_order_date, and days_gap. "
            "Exclude the first order per customer (where there is no previous). "
            "Sort by customer_id, then order_date."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id, order_date, previous_order_date,\n"
            "       CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER) AS days_gap\n"
            "FROM (\n"
            "    SELECT customer_id, order_date,\n"
            "           LAG(order_date) OVER (\n"
            "               PARTITION BY customer_id ORDER BY order_date\n"
            "           ) AS previous_order_date\n"
            "    FROM orders\n"
            ")\n"
            "WHERE previous_order_date IS NOT NULL\n"
            "ORDER BY customer_id, order_date;"
        ),
        "hints": [
            "LAG() lets you access a value from the previous row in a partition.",
            "Partition by customer_id so each customer's orders are independent.",
            "The first order per customer will have NULL for the LAG value.",
            "Use julianday() to compute the difference in days between dates.",
        ],
        "explanation": (
            "1. LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) "
            "gets the previous order date for each customer.\n"
            "2. The outer query filters out NULLs (first orders).\n"
            "3. julianday difference gives the gap in days."
        ),
        "approach": [
            "Use LAG window function partitioned by customer.",
            "Wrap in a subquery to filter out NULL previous dates.",
            "Compute the day gap using julianday().",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, which would compare across different customers.",
            "Not filtering out the NULL rows from the first order per customer.",
            "Using LEAD instead of LAG — LEAD looks forward, LAG looks backward.",
        ],
        "concept_tags": ["LAG", "window functions", "PARTITION BY", "julianday", "date arithmetic"],
    },
    {
        "id": "ec-060",
        "slug": "category-revenue-percentage",
        "title": "Category Share of Total Revenue",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Calculate each category's share of total revenue as a percentage. "
            "For each category, show the category name, category revenue "
            "(from order_items: quantity * unit_price), and the percentage of "
            "overall revenue that category represents. Round percentages to 1 "
            "decimal place. Sort by percentage descending."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "SELECT cat.name AS category_name,\n"
            "       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS category_revenue,\n"
            "       ROUND(\n"
            "           SUM(oi.quantity * oi.unit_price) * 100.0 /\n"
            "           SUM(SUM(oi.quantity * oi.unit_price)) OVER (),\n"
            "           1\n"
            "       ) AS revenue_pct\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "JOIN categories cat ON p.category_id = cat.id\n"
            "GROUP BY cat.name\n"
            "ORDER BY revenue_pct DESC;"
        ),
        "hints": [
            "You need each category's revenue AND the overall total in the same query.",
            "A window function with an empty OVER() clause computes across all rows.",
            "SUM(SUM(...)) OVER () — the inner SUM is the aggregate, the outer SUM is a window function over all groups.",
            "Divide category revenue by total revenue and multiply by 100 for a percentage.",
        ],
        "explanation": (
            "1. GROUP BY cat.name with SUM gives revenue per category.\n"
            "2. SUM(SUM(...)) OVER () computes the grand total across all category groups.\n"
            "3. Dividing category revenue by grand total * 100 gives the percentage."
        ),
        "approach": [
            "Aggregate revenue per category.",
            "Use a window function over the aggregated results to get the grand total.",
            "Compute the percentage from category revenue / grand total.",
        ],
        "common_mistakes": [
            "Using a subquery for the grand total when a window function is more elegant.",
            "Forgetting the * 100.0 (integer division would truncate to 0).",
            "Using PARTITION BY in the window function, which would give per-category totals (i.e., always 100%).",
        ],
        "concept_tags": ["window functions", "SUM OVER", "percentage", "GROUP BY"],
    },
    {
        "id": "ec-061",
        "slug": "products-with-reviews-and-rating",
        "title": "Products with Average Rating and Review Count",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Create a product report showing each product's name, price, number "
            "of reviews, and average rating. Include products with zero reviews "
            "(show 0 for count and NULL for average). Sort by average rating "
            "descending, with NULLs last."
        ),
        "schema_hint": ["products", "reviews"],
        "solution_query": (
            "SELECT p.name, p.price,\n"
            "       COUNT(r.id) AS review_count,\n"
            "       ROUND(AVG(r.rating), 2) AS avg_rating\n"
            "FROM products p\n"
            "LEFT JOIN reviews r ON p.id = r.product_id\n"
            "GROUP BY p.id, p.name, p.price\n"
            "ORDER BY avg_rating DESC NULLS LAST;"
        ),
        "hints": [
            "Use a LEFT JOIN to include products with no reviews.",
            "COUNT(r.id) will be 0 for products with no reviews (COUNT ignores NULLs).",
            "AVG(r.rating) will be NULL for products with no reviews.",
            "NULLS LAST in ORDER BY puts unreviewed products at the bottom.",
        ],
        "explanation": (
            "1. LEFT JOIN reviews ensures all products appear even without reviews.\n"
            "2. COUNT(r.id) counts only non-NULL review IDs (0 for no reviews).\n"
            "3. AVG(r.rating) computes the average, NULL when no reviews exist.\n"
            "4. NULLS LAST puts products without reviews at the end."
        ),
        "approach": [
            "Use LEFT JOIN from products to reviews.",
            "Aggregate with COUNT and AVG.",
            "Handle NULL ordering for unreviewed products.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which drops products with no reviews.",
            "Using COUNT(*) instead of COUNT(r.id) — COUNT(*) counts 1 for products with no reviews.",
            "Forgetting NULLS LAST, placing unreviewed products at the top.",
        ],
        "concept_tags": ["LEFT JOIN", "COUNT", "AVG", "NULLS LAST", "GROUP BY"],
    },
    {
        "id": "ec-062",
        "slug": "multi-payment-orders",
        "title": "Orders with Multiple Payments",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Some orders may have multiple payment attempts. Find orders that "
            "have more than one payment record. Return the order_id, number of "
            "payments, count of completed payments, and total amount of "
            "completed payments. Sort by number of payments descending."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT order_id,\n"
            "       COUNT(*) AS total_payments,\n"
            "       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_payments,\n"
            "       ROUND(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 2) AS completed_amount\n"
            "FROM payments\n"
            "GROUP BY order_id\n"
            "HAVING COUNT(*) > 1\n"
            "ORDER BY total_payments DESC;"
        ),
        "hints": [
            "Group payments by order_id and count them.",
            "HAVING filters groups after aggregation.",
            "Use CASE WHEN inside SUM to conditionally count or sum.",
            "CASE WHEN status = 'completed' THEN 1 ELSE 0 END counts completed ones.",
        ],
        "explanation": (
            "1. GROUP BY order_id to aggregate per order.\n"
            "2. COUNT(*) gives total payment attempts.\n"
            "3. SUM(CASE WHEN ...) selectively counts/sums completed payments.\n"
            "4. HAVING COUNT(*) > 1 filters to multi-payment orders."
        ),
        "approach": [
            "Group by order and count all payments.",
            "Use conditional aggregation (CASE inside SUM) for completed-only metrics.",
            "Filter with HAVING for multiple payments.",
        ],
        "common_mistakes": [
            "Using WHERE status = 'completed' which would exclude failed payment rows from the total count.",
            "Forgetting HAVING and returning all orders.",
        ],
        "concept_tags": ["CASE WHEN", "conditional aggregation", "HAVING", "GROUP BY"],
    },
    {
        "id": "ec-063",
        "slug": "self-referencing-customer-cities",
        "title": "Customers in the Same City",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Find pairs of customers who live in the same city. Return the "
            "first customer's name, the second customer's name, and the city. "
            "Avoid duplicate pairs (if A-B is shown, don't also show B-A) and "
            "don't pair a customer with themselves. Sort by city, then first "
            "customer's last name."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT c1.first_name || ' ' || c1.last_name AS customer_1,\n"
            "       c2.first_name || ' ' || c2.last_name AS customer_2,\n"
            "       c1.city\n"
            "FROM customers c1\n"
            "JOIN customers c2 ON c1.city = c2.city AND c1.id < c2.id\n"
            "ORDER BY c1.city, c1.last_name;"
        ),
        "hints": [
            "You need to join the customers table to itself (a self-join).",
            "Match on the same city to find customers sharing a location.",
            "To avoid duplicates, enforce an ordering condition like c1.id < c2.id.",
            "The < condition ensures each pair appears exactly once.",
        ],
        "explanation": (
            "1. Self-join customers c1 and c2 on matching city.\n"
            "2. c1.id < c2.id prevents duplicates and self-pairs.\n"
            "3. Concatenation (||) combines first and last name."
        ),
        "approach": [
            "Self-join the customers table on city.",
            "Use c1.id < c2.id to eliminate duplicates and self-pairs.",
            "Concatenate names for readable output.",
        ],
        "common_mistakes": [
            "Using c1.id != c2.id which still produces duplicate pairs (A-B and B-A).",
            "Forgetting the self-join condition, creating a Cartesian product.",
        ],
        "concept_tags": ["self-join", "JOIN", "string concatenation", "de-duplication"],
    },
    {
        "id": "ec-064",
        "slug": "first-order-per-customer",
        "title": "Each Customer's First Order",
        "difficulty": "medium",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "For each customer, find their first order. Return the customer's "
            "full name, the order_date of their first order, and the total_amount. "
            "Use a CTE with ROW_NUMBER to identify the earliest order per customer. "
            "Sort by order_date."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "WITH ranked_orders AS (\n"
            "    SELECT o.customer_id, o.order_date, o.total_amount,\n"
            "           ROW_NUMBER() OVER (\n"
            "               PARTITION BY o.customer_id ORDER BY o.order_date\n"
            "           ) AS rn\n"
            "    FROM orders o\n"
            ")\n"
            "SELECT c.first_name || ' ' || c.last_name AS full_name,\n"
            "       ro.order_date,\n"
            "       ro.total_amount\n"
            "FROM ranked_orders ro\n"
            "JOIN customers c ON ro.customer_id = c.id\n"
            "WHERE ro.rn = 1\n"
            "ORDER BY ro.order_date;"
        ),
        "hints": [
            "Use ROW_NUMBER() to assign a sequence number to each customer's orders.",
            "PARTITION BY customer_id and ORDER BY order_date gives row 1 as the earliest.",
            "A CTE makes the logic cleaner — compute ranks first, then filter.",
            "Filter WHERE rn = 1 to keep only the first order per customer.",
        ],
        "explanation": (
            "1. CTE ranked_orders assigns ROW_NUMBER partitioned by customer, ordered by date.\n"
            "2. WHERE rn = 1 filters to the earliest order per customer.\n"
            "3. JOIN to customers adds the customer name."
        ),
        "approach": [
            "Use a CTE with ROW_NUMBER to rank orders per customer.",
            "Filter for rank 1 in the outer query.",
            "Join to customers for the name.",
        ],
        "common_mistakes": [
            "Using MIN(order_date) with GROUP BY, which is simpler but requires a correlated subquery or extra join to get total_amount.",
            "Forgetting PARTITION BY, which would give only one global first order.",
        ],
        "concept_tags": ["CTE", "ROW_NUMBER", "PARTITION BY", "first-per-group"],
    },
    {
        "id": "ec-065",
        "slug": "product-profit-margin",
        "title": "Product Profit Margins",
        "difficulty": "medium",
        "category": "select",
        "dataset": "ecommerce",
        "description": (
            "Calculate the profit margin for each product as "
            "(price - cost) / price * 100. Return the product name, price, "
            "cost, and margin rounded to 1 decimal place. Sort by margin "
            "descending. Only include products with a positive margin."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price, cost,\n"
            "       ROUND((price - cost) * 100.0 / price, 1) AS margin_pct\n"
            "FROM products\n"
            "WHERE price > cost\n"
            "ORDER BY margin_pct DESC;"
        ),
        "hints": [
            "Profit margin is (price - cost) / price * 100.",
            "Use 100.0 (not 100) to force floating-point division.",
            "WHERE price > cost ensures a positive margin.",
            "ROUND to 1 decimal place for clean output.",
        ],
        "explanation": (
            "1. (price - cost) * 100.0 / price computes the margin percentage.\n"
            "2. WHERE price > cost filters out non-profitable products.\n"
            "3. ROUND(..., 1) limits to one decimal."
        ),
        "approach": [
            "Compute margin using arithmetic in the SELECT.",
            "Filter for positive margins.",
            "Round and sort for a clean report.",
        ],
        "common_mistakes": [
            "Using integer division (100 instead of 100.0), which truncates the result.",
            "Dividing by cost instead of price for the margin calculation.",
        ],
        "concept_tags": ["arithmetic", "ROUND", "WHERE", "calculated column"],
    },
    {
        "id": "ec-066",
        "slug": "orders-with-shipping-delay",
        "title": "Orders with Shipping Delays",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Find orders where shipping took longer than 5 days (from order_date "
            "to shipping_date). Return the order id, order_date, shipping_date, "
            "and the number of days delay. Sort by delay descending."
        ),
        "schema_hint": ["orders", "shipping"],
        "solution_query": (
            "SELECT o.id AS order_id, o.order_date, s.shipping_date,\n"
            "       CAST(julianday(s.shipping_date) - julianday(o.order_date) AS INTEGER) AS days_to_ship\n"
            "FROM orders o\n"
            "JOIN shipping s ON o.id = s.order_id\n"
            "WHERE julianday(s.shipping_date) - julianday(o.order_date) > 5\n"
            "ORDER BY days_to_ship DESC;"
        ),
        "hints": [
            "Join orders to shipping on order_id.",
            "Use julianday() to compute date differences in SQLite.",
            "Filter for differences greater than 5 days.",
            "CAST to INTEGER removes the decimal portion of day differences.",
        ],
        "explanation": (
            "1. JOIN orders to shipping on order_id.\n"
            "2. julianday difference computes days between order and ship date.\n"
            "3. WHERE filters for delays exceeding 5 days."
        ),
        "approach": [
            "Join the two tables on order_id.",
            "Compute date difference with julianday().",
            "Filter and sort by the delay.",
        ],
        "common_mistakes": [
            "Trying to subtract date strings directly without julianday().",
            "Confusing shipping_date with delivery_date.",
        ],
        "concept_tags": ["JOIN", "julianday", "date arithmetic", "CAST"],
    },
    {
        "id": "ec-067",
        "slug": "cumulative-revenue-by-month",
        "title": "Cumulative Monthly Revenue",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Show monthly revenue and a cumulative running total. For each month "
            "(YYYY-MM), display the monthly revenue from delivered orders and "
            "the cumulative revenue up to and including that month. Round to 2 "
            "decimal places. Sort chronologically."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT strftime('%Y-%m', order_date) AS month,\n"
            "       ROUND(SUM(total_amount), 2) AS monthly_revenue,\n"
            "       ROUND(SUM(SUM(total_amount)) OVER (\n"
            "           ORDER BY strftime('%Y-%m', order_date)\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS cumulative_revenue\n"
            "FROM orders\n"
            "WHERE status = 'delivered'\n"
            "GROUP BY strftime('%Y-%m', order_date)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "First aggregate revenue by month, then compute a running total over those aggregates.",
            "SUM(SUM(total_amount)) OVER () — inner SUM is the GROUP BY aggregate, outer SUM is a window function.",
            "ORDER BY inside the window function determines the accumulation order.",
            "Use strftime('%Y-%m', order_date) for month extraction in SQLite.",
        ],
        "explanation": (
            "1. GROUP BY month with SUM gives monthly revenue.\n"
            "2. SUM(...) OVER (ORDER BY month) computes the running total.\n"
            "3. The nested SUM(SUM(...)) pattern works because window functions "
            "operate after GROUP BY."
        ),
        "approach": [
            "Aggregate to monthly totals first.",
            "Apply a window function over the aggregated results.",
            "The frame clause ensures a proper running total.",
        ],
        "common_mistakes": [
            "Trying to use a window function without GROUP BY, which would give a running total per row, not per month.",
            "Forgetting the status filter for delivered orders.",
        ],
        "concept_tags": ["window functions", "running total", "SUM OVER", "strftime", "GROUP BY"],
    },
    {
        "id": "ec-068",
        "slug": "customers-who-bought-all-categories",
        "title": "Customers Who Bought from Every Category",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Find customers who have purchased products from every single "
            "product category. Return the customer's first name, last name, "
            "and the number of distinct categories they bought from. Sort by "
            "last name."
        ),
        "schema_hint": ["customers", "orders", "order_items", "products", "categories"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       COUNT(DISTINCT p.category_id) AS categories_bought\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "JOIN order_items oi ON o.id = oi.order_id\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(DISTINCT p.category_id) = (SELECT COUNT(*) FROM categories)\n"
            "ORDER BY c.last_name;"
        ),
        "hints": [
            "You need to count how many distinct categories each customer has bought from.",
            "Compare that count to the total number of categories in the categories table.",
            "Chain joins: customers -> orders -> order_items -> products to reach category_id.",
            "HAVING with a subquery can compare the per-customer count to the total category count.",
        ],
        "explanation": (
            "1. Join from customers through orders and order_items to products.\n"
            "2. COUNT(DISTINCT p.category_id) per customer gives categories covered.\n"
            "3. HAVING compares to (SELECT COUNT(*) FROM categories) — the total.\n"
            "4. Only customers matching all categories pass the filter."
        ),
        "approach": [
            "Chain joins to connect customers to product categories.",
            "Count distinct categories per customer.",
            "Use HAVING with a subquery to match the total category count.",
        ],
        "common_mistakes": [
            "Hardcoding the category count instead of using a subquery.",
            "Using COUNT(category_id) without DISTINCT, which overcounts.",
            "Forgetting a join in the chain and getting incorrect results.",
        ],
        "concept_tags": ["HAVING", "COUNT DISTINCT", "subquery", "relational division", "multi-table join"],
    },
    {
        "id": "ec-069",
        "slug": "moving-average-order-value",
        "title": "3-Month Moving Average of Order Value",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Calculate a 3-month moving average of monthly order value. For "
            "each month, show the monthly average order value and a moving "
            "average that includes the current month and the two preceding "
            "months. Round to 2 decimal places. Sort chronologically."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH monthly AS (\n"
            "    SELECT strftime('%Y-%m', order_date) AS month,\n"
            "           ROUND(AVG(total_amount), 2) AS avg_order_value\n"
            "    FROM orders\n"
            "    WHERE status != 'cancelled'\n"
            "    GROUP BY strftime('%Y-%m', order_date)\n"
            ")\n"
            "SELECT month, avg_order_value,\n"
            "       ROUND(AVG(avg_order_value) OVER (\n"
            "           ORDER BY month\n"
            "           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg_3m\n"
            "FROM monthly\n"
            "ORDER BY month;"
        ),
        "hints": [
            "First compute the monthly average order value in a CTE.",
            "Then apply a window function over those monthly values.",
            "The frame clause ROWS BETWEEN 2 PRECEDING AND CURRENT ROW gives a 3-row window.",
            "AVG as a window function computes the mean over the specified frame.",
        ],
        "explanation": (
            "1. CTE monthly computes average order value per month.\n"
            "2. AVG(...) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) "
            "computes the 3-month moving average.\n"
            "3. For the first two months, the window contains fewer than 3 rows, "
            "so the average is over 1 or 2 values."
        ),
        "approach": [
            "Use a CTE to pre-aggregate monthly averages.",
            "Apply a window function with a 3-row frame for the moving average.",
            "This two-step approach keeps the logic clean.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS, which behaves differently with date values.",
            "Trying to do everything in one query without a CTE, making it hard to read.",
            "Forgetting that the first months will have fewer than 3 preceding rows.",
        ],
        "concept_tags": ["CTE", "window functions", "moving average", "frame clause", "AVG OVER"],
    },
    {
        "id": "ec-070",
        "slug": "unpaid-delivered-orders",
        "title": "Delivered Orders Without Completed Payment",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Find orders that have been delivered but have no completed payment "
            "record. Return the order id, order_date, total_amount, and the "
            "customer's email. Sort by total_amount descending."
        ),
        "schema_hint": ["orders", "payments", "customers"],
        "solution_query": (
            "SELECT o.id AS order_id, o.order_date, o.total_amount, c.email\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.id\n"
            "LEFT JOIN payments p ON o.id = p.order_id AND p.status = 'completed'\n"
            "WHERE o.status = 'delivered'\n"
            "  AND p.id IS NULL\n"
            "ORDER BY o.total_amount DESC;"
        ),
        "hints": [
            "You need to find delivered orders that lack a completed payment.",
            "A LEFT JOIN to payments with IS NULL can find missing records.",
            "Put the payment status condition in the JOIN clause, not in WHERE.",
            "If the status filter is in WHERE, it would filter out NULLs and defeat the LEFT JOIN.",
        ],
        "explanation": (
            "1. LEFT JOIN payments with the completed status filter in the ON clause.\n"
            "2. WHERE p.id IS NULL finds orders with no matching completed payment.\n"
            "3. WHERE o.status = 'delivered' restricts to delivered orders.\n"
            "4. JOIN customers adds the email."
        ),
        "approach": [
            "Use a LEFT JOIN with the payment status condition in the ON clause.",
            "Check for NULL in the payments side to find missing completed payments.",
            "Join customers for the email address.",
        ],
        "common_mistakes": [
            "Putting p.status = 'completed' in the WHERE clause, which converts the LEFT JOIN to an INNER JOIN.",
            "Using NOT IN with a subquery that might contain NULLs.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join", "JOIN condition vs WHERE"],
    },
    # =========================================================================
    # EXTENDED SET — ec-071 through ec-105 (35 problems)
    # =========================================================================
    # --- 5 easy SELECT/WHERE problems (ec-071 to ec-075) ---
    {
        "id": "ec-071",
        "slug": "products-below-ten-dollars",
        "title": "Budget-Friendly Products Under $10",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The marketing team is creating a 'deals under $10' landing page. "
            "List the name and price of every product that costs less than 10 dollars, "
            "sorted from cheapest to most expensive."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price\n"
            "FROM products\n"
            "WHERE price < 10\n"
            "ORDER BY price;"
        ),
        "hints": [
            "You only need one table for this.",
            "Use a WHERE clause to filter by price.",
            "The comparison operator for 'less than' is <.",
            "SELECT name, price FROM products WHERE price < 10 ORDER BY price;",
        ],
        "explanation": (
            "1. SELECT name and price from the products table.\n"
            "2. WHERE price < 10 filters to only budget items.\n"
            "3. ORDER BY price sorts cheapest first."
        ),
        "approach": [
            "Query the products table.",
            "Filter with WHERE price < 10.",
            "Sort ascending by price.",
        ],
        "common_mistakes": [
            "Using <= 10 instead of < 10, which includes $10 items.",
            "Forgetting the ORDER BY clause.",
        ],
        "concept_tags": ["SELECT", "WHERE", "ORDER BY", "comparison operators"],
    },
    {
        "id": "ec-072",
        "slug": "recent-customers-this-year",
        "title": "Customers Who Joined This Year",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The growth team wants to know how many new customers signed up in 2024. "
            "Retrieve the first name, last name, and created_at for all customers "
            "whose account was created on or after '2024-01-01', ordered by signup date."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name, created_at\n"
            "FROM customers\n"
            "WHERE created_at >= '2024-01-01'\n"
            "ORDER BY created_at;"
        ),
        "hints": [
            "Filter customers by their created_at column.",
            "Use >= for 'on or after'.",
            "Date strings can be compared directly in SQLite.",
            "SELECT first_name, last_name, created_at FROM customers WHERE created_at >= '2024-01-01' ORDER BY created_at;",
        ],
        "explanation": (
            "1. SELECT the requested columns from customers.\n"
            "2. WHERE created_at >= '2024-01-01' filters to 2024 signups.\n"
            "3. ORDER BY created_at sorts chronologically."
        ),
        "approach": [
            "Identify the customers table and the created_at column.",
            "Apply a date comparison in the WHERE clause.",
            "Sort by signup date.",
        ],
        "common_mistakes": [
            "Using > instead of >= and missing customers who signed up exactly on Jan 1.",
            "Forgetting that SQLite stores dates as text and compares them lexicographically.",
        ],
        "concept_tags": ["SELECT", "WHERE", "date comparison", "ORDER BY"],
    },
    {
        "id": "ec-073",
        "slug": "out-of-stock-products",
        "title": "Out-of-Stock Products",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "The warehouse manager needs to know which products are completely sold out. "
            "List the product name and category_id for every product where stock_quantity "
            "is zero, sorted by name."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, category_id\n"
            "FROM products\n"
            "WHERE stock_quantity = 0\n"
            "ORDER BY name;"
        ),
        "hints": [
            "Only the products table is needed.",
            "Filter where stock_quantity equals zero.",
            "Remember to sort alphabetically by name.",
            "SELECT name, category_id FROM products WHERE stock_quantity = 0 ORDER BY name;",
        ],
        "explanation": (
            "1. SELECT name and category_id from products.\n"
            "2. WHERE stock_quantity = 0 isolates out-of-stock items.\n"
            "3. ORDER BY name for alphabetical output."
        ),
        "approach": [
            "Query products.",
            "Filter for zero stock.",
            "Sort by name.",
        ],
        "common_mistakes": [
            "Using stock_quantity IS NULL instead of = 0.",
            "Selecting all columns instead of just name and category_id.",
        ],
        "concept_tags": ["SELECT", "WHERE", "equality filter"],
    },
    {
        "id": "ec-074",
        "slug": "orders-with-specific-status",
        "title": "Pending and Processing Orders",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "Customer support needs a list of all orders that are still in progress. "
            "Retrieve the order id, customer_id, order_date, and status for orders "
            "whose status is either 'pending' or 'processing', sorted by order_date descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id, customer_id, order_date, status\n"
            "FROM orders\n"
            "WHERE status IN ('pending', 'processing')\n"
            "ORDER BY order_date DESC;"
        ),
        "hints": [
            "You only need the orders table.",
            "Use IN (...) to match multiple status values.",
            "DESC after ORDER BY sorts newest first.",
            "SELECT id, customer_id, order_date, status FROM orders WHERE status IN ('pending', 'processing') ORDER BY order_date DESC;",
        ],
        "explanation": (
            "1. SELECT the four requested columns from orders.\n"
            "2. WHERE status IN ('pending', 'processing') matches either value.\n"
            "3. ORDER BY order_date DESC puts most recent orders first."
        ),
        "approach": [
            "Query the orders table.",
            "Use IN to filter for multiple statuses.",
            "Sort descending by date.",
        ],
        "common_mistakes": [
            "Using OR without parentheses, which can cause logic errors.",
            "Forgetting DESC for newest-first ordering.",
        ],
        "concept_tags": ["SELECT", "WHERE", "IN", "ORDER BY DESC"],
    },
    {
        "id": "ec-075",
        "slug": "products-name-search",
        "title": "Search Products by Name Keyword",
        "difficulty": "easy",
        "category": "where",
        "dataset": "ecommerce",
        "description": (
            "A customer is searching for products related to 'Pro' in the store. "
            "Find all products whose name contains the word 'Pro' (case-insensitive). "
            "Return the product name, price, and stock_quantity, sorted by price descending."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price, stock_quantity\n"
            "FROM products\n"
            "WHERE name LIKE '%Pro%'\n"
            "ORDER BY price DESC;"
        ),
        "hints": [
            "Use the LIKE operator for partial string matching.",
            "Surround the search term with % wildcards.",
            "LIKE in SQLite is case-insensitive for ASCII characters by default.",
            "SELECT name, price, stock_quantity FROM products WHERE name LIKE '%Pro%' ORDER BY price DESC;",
        ],
        "explanation": (
            "1. SELECT the requested columns from products.\n"
            "2. WHERE name LIKE '%Pro%' finds names containing 'Pro' anywhere.\n"
            "3. ORDER BY price DESC puts the most expensive matches first."
        ),
        "approach": [
            "Use LIKE with wildcard characters for partial matching.",
            "Apply ORDER BY price DESC.",
        ],
        "common_mistakes": [
            "Forgetting the % wildcards around the search term.",
            "Using = instead of LIKE for partial matching.",
        ],
        "concept_tags": ["SELECT", "WHERE", "LIKE", "wildcards"],
    },
    # --- 5 medium aggregation problems (ec-076 to ec-080) ---
    {
        "id": "ec-076",
        "slug": "average-order-value-by-status",
        "title": "Average Order Value by Status",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "Finance wants to understand the average order value segmented by order status. "
            "For each distinct order status, calculate the average total_amount and the "
            "number of orders. Round the average to two decimal places and sort by average "
            "descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT status,\n"
            "       COUNT(*) AS order_count,\n"
            "       ROUND(AVG(total_amount), 2) AS avg_amount\n"
            "FROM orders\n"
            "GROUP BY status\n"
            "ORDER BY avg_amount DESC;"
        ),
        "hints": [
            "Group orders by their status column.",
            "Use AVG() for the average and COUNT(*) for the count.",
            "ROUND(value, 2) gives two decimal places.",
            "SELECT status, COUNT(*) AS order_count, ROUND(AVG(total_amount), 2) AS avg_amount FROM orders GROUP BY status ORDER BY avg_amount DESC;",
        ],
        "explanation": (
            "1. GROUP BY status creates one row per status.\n"
            "2. COUNT(*) counts orders in each group.\n"
            "3. AVG(total_amount) computes the mean, rounded to 2 decimals.\n"
            "4. ORDER BY avg_amount DESC shows the highest average first."
        ),
        "approach": [
            "Group by status.",
            "Apply COUNT and AVG aggregate functions.",
            "Round and sort.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY, which would aggregate all rows into one.",
            "Not rounding the average as requested.",
        ],
        "concept_tags": ["GROUP BY", "AVG", "COUNT", "ROUND", "ORDER BY"],
    },
    {
        "id": "ec-077",
        "slug": "top-five-customers-by-spend",
        "title": "Top 5 Customers by Total Spend",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The VIP program manager wants the top 5 customers ranked by total spending. "
            "Return customer_id and the sum of total_amount across all their orders. "
            "Only include customers with at least 2 orders. Sort by total spend descending "
            "and limit to 5."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       SUM(total_amount) AS total_spend\n"
            "FROM orders\n"
            "GROUP BY customer_id\n"
            "HAVING COUNT(*) >= 2\n"
            "ORDER BY total_spend DESC\n"
            "LIMIT 5;"
        ),
        "hints": [
            "Group orders by customer_id.",
            "Use SUM to total up each customer's orders.",
            "HAVING filters groups after aggregation.",
            "SELECT customer_id, SUM(total_amount) AS total_spend FROM orders GROUP BY customer_id HAVING COUNT(*) >= 2 ORDER BY total_spend DESC LIMIT 5;",
        ],
        "explanation": (
            "1. GROUP BY customer_id aggregates per customer.\n"
            "2. SUM(total_amount) computes total spend.\n"
            "3. HAVING COUNT(*) >= 2 removes single-order customers.\n"
            "4. ORDER BY + LIMIT 5 returns the top five."
        ),
        "approach": [
            "Aggregate orders by customer.",
            "Filter with HAVING for minimum order count.",
            "Sort and limit results.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING for the count filter.",
            "Forgetting LIMIT to restrict to 5 results.",
        ],
        "concept_tags": ["GROUP BY", "SUM", "HAVING", "LIMIT", "ORDER BY"],
    },
    {
        "id": "ec-078",
        "slug": "monthly-revenue-summary",
        "title": "Monthly Revenue Summary",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The CFO needs a month-by-month revenue report. For each month (formatted "
            "as YYYY-MM), compute the total revenue (sum of total_amount) and the number "
            "of orders. Only include months with revenue exceeding 500. Sort chronologically."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT strftime('%Y-%m', order_date) AS month,\n"
            "       COUNT(*) AS order_count,\n"
            "       SUM(total_amount) AS revenue\n"
            "FROM orders\n"
            "GROUP BY month\n"
            "HAVING revenue > 500\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Use strftime('%Y-%m', order_date) to extract year-month.",
            "Group by the formatted month.",
            "HAVING filters groups by aggregate values.",
            "SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS order_count, SUM(total_amount) AS revenue FROM orders GROUP BY month HAVING revenue > 500 ORDER BY month;",
        ],
        "explanation": (
            "1. strftime('%Y-%m', order_date) extracts the year-month.\n"
            "2. GROUP BY month aggregates per calendar month.\n"
            "3. SUM and COUNT provide the totals.\n"
            "4. HAVING revenue > 500 excludes low-revenue months."
        ),
        "approach": [
            "Format dates to year-month using strftime.",
            "Group and aggregate.",
            "Filter with HAVING and sort chronologically.",
        ],
        "common_mistakes": [
            "Using DATE() instead of strftime for month grouping.",
            "Putting the revenue filter in WHERE instead of HAVING.",
        ],
        "concept_tags": ["GROUP BY", "strftime", "SUM", "COUNT", "HAVING"],
    },
    {
        "id": "ec-079",
        "slug": "category-product-stats",
        "title": "Product Statistics per Category",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The product team wants a statistical overview by category. For each category_id, "
            "show the number of products, the minimum price, maximum price, and average price "
            "(rounded to 2 decimals). Sort by the number of products descending."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT category_id,\n"
            "       COUNT(*) AS product_count,\n"
            "       MIN(price) AS min_price,\n"
            "       MAX(price) AS max_price,\n"
            "       ROUND(AVG(price), 2) AS avg_price\n"
            "FROM products\n"
            "GROUP BY category_id\n"
            "ORDER BY product_count DESC;"
        ),
        "hints": [
            "Group by category_id.",
            "Use COUNT, MIN, MAX, and AVG aggregate functions.",
            "ROUND(AVG(price), 2) rounds to two decimal places.",
            "SELECT category_id, COUNT(*) AS product_count, MIN(price) AS min_price, MAX(price) AS max_price, ROUND(AVG(price), 2) AS avg_price FROM products GROUP BY category_id ORDER BY product_count DESC;",
        ],
        "explanation": (
            "1. GROUP BY category_id creates one row per category.\n"
            "2. COUNT, MIN, MAX, AVG provide the requested statistics.\n"
            "3. ORDER BY product_count DESC shows the largest categories first."
        ),
        "approach": [
            "Group products by category_id.",
            "Apply multiple aggregate functions.",
            "Sort by product count descending.",
        ],
        "common_mistakes": [
            "Forgetting to round the average.",
            "Using a non-aggregated column without grouping.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "MIN", "MAX", "AVG", "ROUND"],
    },
    {
        "id": "ec-080",
        "slug": "payment-method-breakdown",
        "title": "Payment Method Breakdown",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "ecommerce",
        "description": (
            "The finance team wants to know how revenue is distributed across payment methods. "
            "For each payment method, show the number of completed payments, the total amount, "
            "and the percentage of total revenue (rounded to 1 decimal). Sort by total amount "
            "descending."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT method,\n"
            "       COUNT(*) AS payment_count,\n"
            "       SUM(amount) AS total_amount,\n"
            "       ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM payments WHERE status = 'completed'), 1) AS pct_of_revenue\n"
            "FROM payments\n"
            "WHERE status = 'completed'\n"
            "GROUP BY method\n"
            "ORDER BY total_amount DESC;"
        ),
        "hints": [
            "Filter to completed payments first.",
            "Group by method and use SUM and COUNT.",
            "To get a percentage, divide each group's sum by the overall sum using a scalar subquery.",
            "SELECT method, COUNT(*) AS payment_count, SUM(amount) AS total_amount, ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM payments WHERE status = 'completed'), 1) AS pct_of_revenue FROM payments WHERE status = 'completed' GROUP BY method ORDER BY total_amount DESC;",
        ],
        "explanation": (
            "1. WHERE status = 'completed' filters to successful payments.\n"
            "2. GROUP BY method aggregates per payment method.\n"
            "3. A scalar subquery computes the overall total for percentage calculation.\n"
            "4. Multiply by 100.0 to get a percentage, then ROUND to 1 decimal."
        ),
        "approach": [
            "Filter completed payments.",
            "Group by method with COUNT and SUM.",
            "Use a subquery for the grand total to compute percentages.",
        ],
        "common_mistakes": [
            "Forgetting to filter by completed status in both the main query and the subquery.",
            "Integer division: use 100.0 instead of 100 for correct percentage.",
        ],
        "concept_tags": ["GROUP BY", "SUM", "COUNT", "ROUND", "scalar subquery", "percentage"],
    },
    # --- 5 medium join problems (ec-081 to ec-085) ---
    {
        "id": "ec-081",
        "slug": "customer-order-history",
        "title": "Customer Order History with Names",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The support team needs a readable order log. List each order's id, order_date, "
            "total_amount, and the customer's first and last name. Sort by order_date descending."
        ),
        "schema_hint": ["orders", "customers"],
        "solution_query": (
            "SELECT o.id, c.first_name, c.last_name, o.order_date, o.total_amount\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.id\n"
            "ORDER BY o.order_date DESC;"
        ),
        "hints": [
            "You need data from both orders and customers.",
            "Join on orders.customer_id = customers.id.",
            "Use table aliases to keep the query readable.",
            "SELECT o.id, c.first_name, c.last_name, o.order_date, o.total_amount FROM orders o JOIN customers c ON o.customer_id = c.id ORDER BY o.order_date DESC;",
        ],
        "explanation": (
            "1. JOIN orders to customers on the foreign key.\n"
            "2. SELECT columns from both tables.\n"
            "3. ORDER BY order_date DESC for newest first."
        ),
        "approach": [
            "Identify the relationship between orders and customers.",
            "Write an INNER JOIN on the foreign key.",
            "Select the required columns and sort.",
        ],
        "common_mistakes": [
            "Joining on the wrong column.",
            "Forgetting to qualify ambiguous column names with table aliases.",
        ],
        "concept_tags": ["JOIN", "table aliases", "ORDER BY"],
    },
    {
        "id": "ec-082",
        "slug": "order-items-with-product-names",
        "title": "Order Line Items with Product Details",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Build a detailed invoice view. For each order_item, show the order_id, "
            "product name, quantity, unit_price, discount, and the line total "
            "(quantity * unit_price - discount). Sort by order_id then product name."
        ),
        "schema_hint": ["order_items", "products"],
        "solution_query": (
            "SELECT oi.order_id,\n"
            "       p.name AS product_name,\n"
            "       oi.quantity,\n"
            "       oi.unit_price,\n"
            "       oi.discount,\n"
            "       (oi.quantity * oi.unit_price - oi.discount) AS line_total\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "ORDER BY oi.order_id, p.name;"
        ),
        "hints": [
            "Join order_items with products to get the product name.",
            "Compute the line total as quantity * unit_price - discount.",
            "Sort by order_id first, then product name.",
            "SELECT oi.order_id, p.name AS product_name, oi.quantity, oi.unit_price, oi.discount, (oi.quantity * oi.unit_price - oi.discount) AS line_total FROM order_items oi JOIN products p ON oi.product_id = p.id ORDER BY oi.order_id, p.name;",
        ],
        "explanation": (
            "1. JOIN order_items to products on product_id.\n"
            "2. Compute line_total as a calculated column.\n"
            "3. Sort by order_id and product name."
        ),
        "approach": [
            "Join order_items and products.",
            "Add a calculated column for line total.",
            "Sort by the composite key.",
        ],
        "common_mistakes": [
            "Forgetting to subtract the discount in the line total.",
            "Not aliasing the calculated column.",
        ],
        "concept_tags": ["JOIN", "calculated column", "ORDER BY", "arithmetic"],
    },
    {
        "id": "ec-083",
        "slug": "products-with-category-names",
        "title": "Product Catalog with Category Names",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The front-end team needs the product catalog with human-readable category names. "
            "Return product name, price, stock_quantity, and category name. Include products "
            "even if they have no assigned category. Sort by category name then product name."
        ),
        "schema_hint": ["products", "categories"],
        "solution_query": (
            "SELECT p.name AS product_name,\n"
            "       p.price,\n"
            "       p.stock_quantity,\n"
            "       c.name AS category_name\n"
            "FROM products p\n"
            "LEFT JOIN categories c ON p.category_id = c.id\n"
            "ORDER BY c.name, p.name;"
        ),
        "hints": [
            "Use LEFT JOIN to keep products without a category.",
            "Join products to categories on category_id.",
            "Sort by category name first, then product name.",
            "SELECT p.name AS product_name, p.price, p.stock_quantity, c.name AS category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id ORDER BY c.name, p.name;",
        ],
        "explanation": (
            "1. LEFT JOIN keeps all products, even those with NULL category_id.\n"
            "2. Products without a category will show NULL for category_name.\n"
            "3. ORDER BY c.name, p.name sorts by category then product."
        ),
        "approach": [
            "Use LEFT JOIN from products to categories.",
            "Select columns from both tables.",
            "Sort by category and product name.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which drops products without a category.",
            "Not aliasing the two 'name' columns, causing ambiguity.",
        ],
        "concept_tags": ["LEFT JOIN", "NULL handling", "column aliases"],
    },
    {
        "id": "ec-084",
        "slug": "orders-with-shipping-info",
        "title": "Orders with Shipping Status",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "Logistics needs a dashboard showing each order's shipping progress. "
            "Return order id, order_date, customer_id, shipping carrier, shipping status, "
            "and delivery_date. Include all orders even if shipping hasn't been created yet. "
            "Sort by order_date descending."
        ),
        "schema_hint": ["orders", "shipping"],
        "solution_query": (
            "SELECT o.id AS order_id,\n"
            "       o.order_date,\n"
            "       o.customer_id,\n"
            "       s.carrier,\n"
            "       s.status AS shipping_status,\n"
            "       s.delivery_date\n"
            "FROM orders o\n"
            "LEFT JOIN shipping s ON o.id = s.order_id\n"
            "ORDER BY o.order_date DESC;"
        ),
        "hints": [
            "Use LEFT JOIN to include orders without a shipping record.",
            "Join orders to shipping on order_id.",
            "Alias columns to avoid confusion between order status and shipping status.",
            "SELECT o.id AS order_id, o.order_date, o.customer_id, s.carrier, s.status AS shipping_status, s.delivery_date FROM orders o LEFT JOIN shipping s ON o.id = s.order_id ORDER BY o.order_date DESC;",
        ],
        "explanation": (
            "1. LEFT JOIN ensures orders without shipping records are included.\n"
            "2. Shipping columns will be NULL for orders not yet shipped.\n"
            "3. Alias s.status to avoid ambiguity with o.status."
        ),
        "approach": [
            "LEFT JOIN orders to shipping.",
            "Alias overlapping column names.",
            "Sort by order_date descending.",
        ],
        "common_mistakes": [
            "Using INNER JOIN and losing unshipped orders.",
            "Not aliasing the status columns from different tables.",
        ],
        "concept_tags": ["LEFT JOIN", "column aliases", "NULL", "ORDER BY"],
    },
    {
        "id": "ec-085",
        "slug": "reviews-with-product-and-customer",
        "title": "Detailed Review Report",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "ecommerce",
        "description": (
            "The product team wants a full review report. Show each review's rating, comment, "
            "review_date, the product name, and the reviewer's first and last name. "
            "Sort by review_date descending."
        ),
        "schema_hint": ["reviews", "products", "customers"],
        "solution_query": (
            "SELECT r.rating,\n"
            "       r.comment,\n"
            "       r.review_date,\n"
            "       p.name AS product_name,\n"
            "       c.first_name,\n"
            "       c.last_name\n"
            "FROM reviews r\n"
            "JOIN products p ON r.product_id = p.id\n"
            "JOIN customers c ON r.customer_id = c.id\n"
            "ORDER BY r.review_date DESC;"
        ),
        "hints": [
            "You need to join three tables: reviews, products, and customers.",
            "Join reviews to products on product_id and to customers on customer_id.",
            "Chain multiple JOINs one after another.",
            "SELECT r.rating, r.comment, r.review_date, p.name AS product_name, c.first_name, c.last_name FROM reviews r JOIN products p ON r.product_id = p.id JOIN customers c ON r.customer_id = c.id ORDER BY r.review_date DESC;",
        ],
        "explanation": (
            "1. JOIN reviews to products to get the product name.\n"
            "2. JOIN reviews to customers to get the reviewer's name.\n"
            "3. Sort by review_date descending."
        ),
        "approach": [
            "Start from reviews as the base table.",
            "Join to products and customers.",
            "Select the required columns and sort.",
        ],
        "common_mistakes": [
            "Forgetting one of the two joins.",
            "Joining on the wrong foreign key columns.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "ORDER BY"],
    },
    # --- 5 medium subquery problems (ec-086 to ec-090) ---
    {
        "id": "ec-086",
        "slug": "products-above-average-price",
        "title": "Products Priced Above Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "The pricing team wants to identify premium products. List the name and price "
            "of all products whose price is above the overall average product price. "
            "Sort by price descending."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price\n"
            "FROM products\n"
            "WHERE price > (SELECT AVG(price) FROM products)\n"
            "ORDER BY price DESC;"
        ),
        "hints": [
            "You need the average price of all products.",
            "Use a scalar subquery in the WHERE clause.",
            "The subquery computes AVG(price) from products.",
            "SELECT name, price FROM products WHERE price > (SELECT AVG(price) FROM products) ORDER BY price DESC;",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(price) FROM products) computes the global average.\n"
            "2. The outer query filters products with price above that average.\n"
            "3. Sort by price descending."
        ),
        "approach": [
            "Write a subquery for the average price.",
            "Use it in the WHERE clause of the main query.",
            "Sort results.",
        ],
        "common_mistakes": [
            "Trying to use AVG(price) directly in WHERE without a subquery.",
            "Using >= instead of > if the question says 'above'.",
        ],
        "concept_tags": ["subquery", "scalar subquery", "AVG", "WHERE"],
    },
    {
        "id": "ec-087",
        "slug": "customers-who-never-ordered",
        "title": "Customers Who Have Never Placed an Order",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Marketing wants to re-engage dormant users. Find all customers who have "
            "never placed an order. Return their first_name, last_name, and email. "
            "Sort by last_name, first_name."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE id NOT IN (SELECT DISTINCT customer_id FROM orders)\n"
            "ORDER BY last_name, first_name;"
        ),
        "hints": [
            "You need to find customers absent from the orders table.",
            "Use NOT IN with a subquery that selects customer_ids from orders.",
            "DISTINCT in the subquery is optional but can improve clarity.",
            "SELECT first_name, last_name, email FROM customers WHERE id NOT IN (SELECT DISTINCT customer_id FROM orders) ORDER BY last_name, first_name;",
        ],
        "explanation": (
            "1. The subquery gets all customer_ids that appear in orders.\n"
            "2. NOT IN excludes those customers from the result.\n"
            "3. Sort alphabetically by last name then first name."
        ),
        "approach": [
            "Subquery to get customer_ids from orders.",
            "Use NOT IN to find customers not in that set.",
            "Sort the result.",
        ],
        "common_mistakes": [
            "NOT IN can behave unexpectedly if the subquery returns NULLs.",
            "Forgetting to sort by both last_name and first_name.",
        ],
        "concept_tags": ["subquery", "NOT IN", "anti-pattern"],
    },
    {
        "id": "ec-088",
        "slug": "most-expensive-product-per-category",
        "title": "Most Expensive Product in Each Category",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "For each category, find the product with the highest price. Return the "
            "category_id, product name, and price. If there are ties, include all tied products. "
            "Sort by category_id."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT p.category_id, p.name, p.price\n"
            "FROM products p\n"
            "WHERE p.price = (\n"
            "    SELECT MAX(p2.price)\n"
            "    FROM products p2\n"
            "    WHERE p2.category_id = p.category_id\n"
            ")\n"
            "ORDER BY p.category_id;"
        ),
        "hints": [
            "You need the max price within each category.",
            "Use a correlated subquery that references the outer query's category_id.",
            "Compare each product's price to its category's max price.",
            "SELECT p.category_id, p.name, p.price FROM products p WHERE p.price = (SELECT MAX(p2.price) FROM products p2 WHERE p2.category_id = p.category_id) ORDER BY p.category_id;",
        ],
        "explanation": (
            "1. The correlated subquery finds the MAX price for the same category.\n"
            "2. The outer WHERE keeps only products matching that max.\n"
            "3. Ties are naturally included since all max-priced products match."
        ),
        "approach": [
            "Write a correlated subquery for MAX(price) per category.",
            "Filter the outer query to match that max.",
            "Sort by category_id.",
        ],
        "common_mistakes": [
            "Using a non-correlated subquery, which returns a single global max.",
            "Using LIMIT 1, which would not handle ties.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "per-group maximum"],
    },
    {
        "id": "ec-089",
        "slug": "orders-above-customer-average",
        "title": "Orders Exceeding Customer's Own Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "Find all orders where the total_amount exceeds the placing customer's "
            "average order total. Return order id, customer_id, total_amount, "
            "and the customer's average (rounded to 2 decimals). Sort by customer_id, then order id."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT o.id,\n"
            "       o.customer_id,\n"
            "       o.total_amount,\n"
            "       ROUND((SELECT AVG(o2.total_amount) FROM orders o2 WHERE o2.customer_id = o.customer_id), 2) AS customer_avg\n"
            "FROM orders o\n"
            "WHERE o.total_amount > (\n"
            "    SELECT AVG(o2.total_amount)\n"
            "    FROM orders o2\n"
            "    WHERE o2.customer_id = o.customer_id\n"
            ")\n"
            "ORDER BY o.customer_id, o.id;"
        ),
        "hints": [
            "Each customer has their own average; you need a correlated subquery.",
            "The subquery computes AVG(total_amount) for the same customer_id.",
            "You can also include the average as a column in the SELECT.",
            "Use a correlated subquery in both WHERE and SELECT.",
        ],
        "explanation": (
            "1. The correlated subquery computes each customer's average total.\n"
            "2. WHERE filters to orders above that personal average.\n"
            "3. The same subquery in SELECT displays the average for reference."
        ),
        "approach": [
            "Write a correlated subquery for per-customer average.",
            "Use it in WHERE to filter.",
            "Include it in SELECT for display.",
        ],
        "common_mistakes": [
            "Using a global average instead of a per-customer average.",
            "Forgetting to round the displayed average.",
        ],
        "concept_tags": ["correlated subquery", "AVG", "self-comparison"],
    },
    {
        "id": "ec-090",
        "slug": "products-never-reviewed",
        "title": "Products with No Reviews",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "ecommerce",
        "description": (
            "The product team wants to encourage reviews for products that have none. "
            "Find all products that have zero reviews. Return the product name, price, "
            "and stock_quantity. Sort by name."
        ),
        "schema_hint": ["products", "reviews"],
        "solution_query": (
            "SELECT name, price, stock_quantity\n"
            "FROM products\n"
            "WHERE id NOT IN (SELECT DISTINCT product_id FROM reviews)\n"
            "ORDER BY name;"
        ),
        "hints": [
            "You need to find products absent from the reviews table.",
            "Use NOT IN or NOT EXISTS with a subquery on reviews.",
            "The subquery selects product_ids from reviews.",
            "SELECT name, price, stock_quantity FROM products WHERE id NOT IN (SELECT DISTINCT product_id FROM reviews) ORDER BY name;",
        ],
        "explanation": (
            "1. The subquery finds all product_ids that have at least one review.\n"
            "2. NOT IN excludes those from the products result.\n"
            "3. Sort alphabetically by name."
        ),
        "approach": [
            "Subquery to find reviewed product_ids.",
            "Exclude them with NOT IN.",
            "Sort by name.",
        ],
        "common_mistakes": [
            "Using NOT IN when the subquery could return NULLs (safer to use NOT EXISTS).",
            "Joining instead of using a subquery, then forgetting to filter properly.",
        ],
        "concept_tags": ["subquery", "NOT IN", "anti-join"],
    },
    # --- 5 hard window function problems (ec-091 to ec-095) ---
    {
        "id": "ec-091",
        "slug": "rank-products-by-price-in-category",
        "title": "Rank Products by Price Within Category",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each product, show its name, category_id, price, and its rank within "
            "its category based on price (most expensive = rank 1). Use RANK() so tied "
            "prices share the same rank. Sort by category_id, then rank."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name,\n"
            "       category_id,\n"
            "       price,\n"
            "       RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank\n"
            "FROM products\n"
            "ORDER BY category_id, price_rank;"
        ),
        "hints": [
            "Use a window function with PARTITION BY category_id.",
            "RANK() assigns the same rank to ties and skips the next rank.",
            "ORDER BY price DESC inside the OVER clause ranks most expensive first.",
            "SELECT name, category_id, price, RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank FROM products ORDER BY category_id, price_rank;",
        ],
        "explanation": (
            "1. PARTITION BY category_id restarts ranking for each category.\n"
            "2. ORDER BY price DESC ranks highest price as 1.\n"
            "3. RANK() handles ties by assigning the same rank.\n"
            "4. Outer ORDER BY sorts by category then rank."
        ),
        "approach": [
            "Use RANK() with PARTITION BY and ORDER BY.",
            "Place the window function in the SELECT clause.",
            "Add an outer ORDER BY for the final sort.",
        ],
        "common_mistakes": [
            "Using ROW_NUMBER() instead of RANK(), which doesn't handle ties.",
            "Forgetting PARTITION BY, which ranks across all categories.",
        ],
        "concept_tags": ["RANK", "window function", "PARTITION BY", "ORDER BY"],
    },
    {
        "id": "ec-092",
        "slug": "running-total-of-order-amounts",
        "title": "Running Total of Daily Order Revenue",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Produce a daily revenue report with a running total. For each order_date, "
            "show the date, the daily revenue (sum of total_amount), and the cumulative "
            "running total across all dates. Sort by order_date."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT order_date,\n"
            "       SUM(total_amount) AS daily_revenue,\n"
            "       SUM(SUM(total_amount)) OVER (ORDER BY order_date) AS running_total\n"
            "FROM orders\n"
            "GROUP BY order_date\n"
            "ORDER BY order_date;"
        ),
        "hints": [
            "First aggregate daily revenue with GROUP BY order_date.",
            "Then apply a window function over the grouped result.",
            "SUM(...) OVER (ORDER BY order_date) computes a running total.",
            "You can nest SUM inside a window SUM: SUM(SUM(total_amount)) OVER (...).",
        ],
        "explanation": (
            "1. GROUP BY order_date computes daily revenue.\n"
            "2. SUM(SUM(total_amount)) OVER (ORDER BY order_date) runs a cumulative sum.\n"
            "3. The inner SUM is the aggregate; the outer SUM OVER is the window function."
        ),
        "approach": [
            "Aggregate daily with GROUP BY.",
            "Apply a cumulative SUM window function.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Trying to use a window function without GROUP BY, getting per-order rows.",
            "Forgetting that the default window frame for ORDER BY is UNBOUNDED PRECEDING to CURRENT ROW.",
        ],
        "concept_tags": ["window function", "SUM OVER", "running total", "GROUP BY"],
    },
    {
        "id": "ec-093",
        "slug": "customer-order-sequence-number",
        "title": "Customer Order Sequence Number",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "For each order, show the order id, customer_id, order_date, total_amount, "
            "and the sequence number of that order for the customer (1st order, 2nd order, etc.). "
            "Also show the previous order's total_amount using LAG. Sort by customer_id, "
            "then sequence number."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id,\n"
            "       customer_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_seq,\n"
            "       LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_amount\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_seq;"
        ),
        "hints": [
            "Use ROW_NUMBER() partitioned by customer_id.",
            "LAG(column) accesses the previous row's value.",
            "Both window functions share the same PARTITION BY and ORDER BY.",
            "SELECT id, customer_id, order_date, total_amount, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_seq, LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_amount FROM orders ORDER BY customer_id, order_seq;",
        ],
        "explanation": (
            "1. ROW_NUMBER() assigns a sequential number per customer.\n"
            "2. LAG(total_amount) gets the previous order's amount (NULL for the first).\n"
            "3. Both are partitioned by customer_id and ordered by order_date."
        ),
        "approach": [
            "Use ROW_NUMBER for sequencing.",
            "Use LAG for previous row access.",
            "Partition both by customer_id.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, which sequences across all customers.",
            "Confusing LAG (previous) with LEAD (next).",
        ],
        "concept_tags": ["ROW_NUMBER", "LAG", "window function", "PARTITION BY"],
    },
    {
        "id": "ec-094",
        "slug": "top-product-per-category-dense-rank",
        "title": "Top 3 Products per Category by Revenue",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Find the top 3 products by total revenue in each category. Revenue is "
            "calculated from order_items (quantity * unit_price - discount). Use DENSE_RANK "
            "to rank and filter to rank <= 3. Show category_id, product name, total revenue, "
            "and rank. Sort by category_id, then rank."
        ),
        "schema_hint": ["order_items", "products"],
        "solution_query": (
            "SELECT category_id, product_name, total_revenue, rnk\n"
            "FROM (\n"
            "    SELECT p.category_id,\n"
            "           p.name AS product_name,\n"
            "           SUM(oi.quantity * oi.unit_price - oi.discount) AS total_revenue,\n"
            "           DENSE_RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity * oi.unit_price - oi.discount) DESC) AS rnk\n"
            "    FROM order_items oi\n"
            "    JOIN products p ON oi.product_id = p.id\n"
            "    GROUP BY p.category_id, p.id, p.name\n"
            ") sub\n"
            "WHERE rnk <= 3\n"
            "ORDER BY category_id, rnk;"
        ),
        "hints": [
            "First compute total revenue per product using SUM on order_items.",
            "Use DENSE_RANK() with PARTITION BY category_id.",
            "Wrap it in a subquery to filter WHERE rnk <= 3.",
            "DENSE_RANK preserves consecutive ranks even with ties.",
        ],
        "explanation": (
            "1. Join order_items to products for category info.\n"
            "2. GROUP BY product to compute total revenue.\n"
            "3. DENSE_RANK partitioned by category ranks products.\n"
            "4. Outer query filters to top 3."
        ),
        "approach": [
            "Compute per-product revenue with GROUP BY.",
            "Apply DENSE_RANK in a subquery.",
            "Filter to rank <= 3 in the outer query.",
        ],
        "common_mistakes": [
            "Using RANK() instead of DENSE_RANK(), which can skip ranks.",
            "Trying to filter by rank in the WHERE of the same query (window functions can't be in WHERE).",
        ],
        "concept_tags": ["DENSE_RANK", "window function", "top-N per group", "subquery"],
    },
    {
        "id": "ec-095",
        "slug": "moving-average-order-amount",
        "title": "7-Day Moving Average of Order Amounts",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "ecommerce",
        "description": (
            "Compute a 7-day moving average of daily order revenue. For each date, show "
            "the order_date, daily revenue, and the average of the current day plus the "
            "6 preceding days. Round to 2 decimal places. Sort by order_date."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT order_date,\n"
            "       SUM(total_amount) AS daily_revenue,\n"
            "       ROUND(AVG(SUM(total_amount)) OVER (\n"
            "           ORDER BY order_date\n"
            "           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg_7d\n"
            "FROM orders\n"
            "GROUP BY order_date\n"
            "ORDER BY order_date;"
        ),
        "hints": [
            "First aggregate daily revenue with GROUP BY.",
            "Use AVG as a window function with a frame clause.",
            "ROWS BETWEEN 6 PRECEDING AND CURRENT ROW gives a 7-day window.",
            "Nest SUM inside AVG OVER for the moving average of daily totals.",
        ],
        "explanation": (
            "1. GROUP BY order_date produces one row per day.\n"
            "2. AVG(...) OVER (... ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) computes the moving average.\n"
            "3. The frame includes the current row plus 6 prior rows.\n"
            "4. Round to 2 decimal places."
        ),
        "approach": [
            "Aggregate daily revenue.",
            "Apply AVG window function with explicit frame.",
            "Round and sort.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS, which behaves differently with date gaps.",
            "Setting the frame to 7 PRECEDING instead of 6, which gives an 8-day window.",
        ],
        "concept_tags": ["window function", "moving average", "frame clause", "ROWS BETWEEN"],
    },
    # --- 5 hard CTE problems (ec-096 to ec-100) ---
    {
        "id": "ec-096",
        "slug": "customer-lifetime-value-tiers",
        "title": "Customer Lifetime Value Tiers",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Classify customers into lifetime value tiers. First compute each customer's "
            "total spend. Then assign: 'Platinum' if spend >= 1000, 'Gold' if >= 500, "
            "'Silver' if >= 100, else 'Bronze'. Return first_name, last_name, total_spend, "
            "and tier. Sort by total_spend descending."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "WITH customer_spend AS (\n"
            "    SELECT customer_id, SUM(total_amount) AS total_spend\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT c.first_name,\n"
            "       c.last_name,\n"
            "       cs.total_spend,\n"
            "       CASE\n"
            "           WHEN cs.total_spend >= 1000 THEN 'Platinum'\n"
            "           WHEN cs.total_spend >= 500 THEN 'Gold'\n"
            "           WHEN cs.total_spend >= 100 THEN 'Silver'\n"
            "           ELSE 'Bronze'\n"
            "       END AS tier\n"
            "FROM customer_spend cs\n"
            "JOIN customers c ON cs.customer_id = c.id\n"
            "ORDER BY cs.total_spend DESC;"
        ),
        "hints": [
            "Use a CTE to compute total spend per customer first.",
            "Join the CTE to customers for names.",
            "Use CASE WHEN for tier classification.",
            "Order CASE conditions from highest to lowest threshold.",
        ],
        "explanation": (
            "1. CTE customer_spend aggregates total spend per customer.\n"
            "2. Join to customers for name columns.\n"
            "3. CASE assigns tiers based on spend thresholds.\n"
            "4. Sort by total_spend descending."
        ),
        "approach": [
            "CTE for aggregation.",
            "JOIN for customer details.",
            "CASE for tier assignment.",
        ],
        "common_mistakes": [
            "Wrong order in CASE conditions (must go from highest threshold down).",
            "Forgetting customers with no orders (they won't appear in the CTE).",
        ],
        "concept_tags": ["CTE", "CASE", "GROUP BY", "JOIN"],
    },
    {
        "id": "ec-097",
        "slug": "repeat-purchase-rate",
        "title": "Repeat Purchase Rate by Month",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Calculate the repeat purchase rate for each month. A 'repeat purchaser' "
            "is a customer who placed more than one order that month. For each month "
            "(YYYY-MM), show total unique customers, repeat customers, and the repeat "
            "rate as a percentage (rounded to 1 decimal). Sort by month."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH monthly_orders AS (\n"
            "    SELECT strftime('%Y-%m', order_date) AS month,\n"
            "           customer_id,\n"
            "           COUNT(*) AS order_count\n"
            "    FROM orders\n"
            "    GROUP BY month, customer_id\n"
            ")\n"
            "SELECT month,\n"
            "       COUNT(*) AS total_customers,\n"
            "       SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,\n"
            "       ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS repeat_rate_pct\n"
            "FROM monthly_orders\n"
            "GROUP BY month\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Use a CTE to count orders per customer per month.",
            "In the main query, count total vs repeat customers.",
            "A CASE expression can flag repeat customers (order_count > 1).",
            "Divide repeat by total and multiply by 100 for percentage.",
        ],
        "explanation": (
            "1. CTE counts orders per customer per month.\n"
            "2. Main query counts total customers and those with > 1 order.\n"
            "3. Repeat rate = repeat / total * 100."
        ),
        "approach": [
            "CTE for per-customer monthly order count.",
            "Aggregate to monthly level with conditional counting.",
            "Compute percentage.",
        ],
        "common_mistakes": [
            "Integer division when computing percentages (use 100.0).",
            "Counting orders instead of distinct customers.",
        ],
        "concept_tags": ["CTE", "CASE", "conditional aggregation", "percentage"],
    },
    {
        "id": "ec-098",
        "slug": "product-profit-margin-ranking",
        "title": "Product Profit Margin Ranking",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Rank products by their profit margin. Use a CTE to compute margin as "
            "(price - cost) / price * 100 for each product. Then show product name, "
            "price, cost, margin (rounded to 2 decimals), and the rank (highest margin = 1). "
            "Only include products where cost is not NULL. Sort by rank."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "WITH margins AS (\n"
            "    SELECT name,\n"
            "           price,\n"
            "           cost,\n"
            "           ROUND((price - cost) * 100.0 / price, 2) AS margin_pct\n"
            "    FROM products\n"
            "    WHERE cost IS NOT NULL AND price > 0\n"
            ")\n"
            "SELECT name,\n"
            "       price,\n"
            "       cost,\n"
            "       margin_pct,\n"
            "       RANK() OVER (ORDER BY margin_pct DESC) AS margin_rank\n"
            "FROM margins\n"
            "ORDER BY margin_rank;"
        ),
        "hints": [
            "Compute margin in a CTE to keep the main query clean.",
            "Filter out NULL costs in the CTE.",
            "Use RANK() in the main query to rank by margin.",
            "Guard against division by zero by filtering price > 0.",
        ],
        "explanation": (
            "1. CTE computes margin_pct and filters nulls.\n"
            "2. Main query applies RANK by margin descending.\n"
            "3. Sort by rank for final output."
        ),
        "approach": [
            "CTE for margin calculation and filtering.",
            "Window function for ranking.",
            "Sort by rank.",
        ],
        "common_mistakes": [
            "Division by zero if price is 0.",
            "Forgetting to handle NULL cost values.",
        ],
        "concept_tags": ["CTE", "RANK", "calculated column", "NULL handling"],
    },
    {
        "id": "ec-099",
        "slug": "order-fulfillment-pipeline",
        "title": "Order Fulfillment Pipeline Report",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Build a pipeline report showing each order's journey. Use CTEs to gather: "
            "(1) order info with customer name, (2) payment status, (3) shipping status. "
            "Combine them to show order id, customer name, order status, payment status "
            "(or 'unpaid'), shipping status (or 'not shipped'), and delivery_date. "
            "Sort by order_date descending."
        ),
        "schema_hint": ["orders", "customers", "payments", "shipping"],
        "solution_query": (
            "WITH order_info AS (\n"
            "    SELECT o.id AS order_id,\n"
            "           o.order_date,\n"
            "           o.status AS order_status,\n"
            "           c.first_name || ' ' || c.last_name AS customer_name\n"
            "    FROM orders o\n"
            "    JOIN customers c ON o.customer_id = c.id\n"
            "),\n"
            "payment_info AS (\n"
            "    SELECT order_id,\n"
            "           status AS payment_status\n"
            "    FROM payments\n"
            "),\n"
            "shipping_info AS (\n"
            "    SELECT order_id,\n"
            "           status AS shipping_status,\n"
            "           delivery_date\n"
            "    FROM shipping\n"
            ")\n"
            "SELECT oi.order_id,\n"
            "       oi.customer_name,\n"
            "       oi.order_status,\n"
            "       COALESCE(pi.payment_status, 'unpaid') AS payment_status,\n"
            "       COALESCE(si.shipping_status, 'not shipped') AS shipping_status,\n"
            "       si.delivery_date\n"
            "FROM order_info oi\n"
            "LEFT JOIN payment_info pi ON oi.order_id = pi.order_id\n"
            "LEFT JOIN shipping_info si ON oi.order_id = si.order_id\n"
            "ORDER BY oi.order_date DESC;"
        ),
        "hints": [
            "Use multiple CTEs, separated by commas.",
            "LEFT JOIN to preserve orders without payments or shipping.",
            "COALESCE replaces NULL with a default string.",
            "String concatenation in SQLite uses ||.",
        ],
        "explanation": (
            "1. CTE order_info joins orders and customers.\n"
            "2. CTE payment_info extracts payment status.\n"
            "3. CTE shipping_info extracts shipping status and delivery date.\n"
            "4. Main query LEFT JOINs all three, using COALESCE for defaults."
        ),
        "approach": [
            "Break the problem into logical CTEs.",
            "Use LEFT JOINs to handle missing data.",
            "COALESCE for friendly defaults.",
        ],
        "common_mistakes": [
            "Using INNER JOIN and losing orders without payment or shipping.",
            "Forgetting to handle multiple payments per order (if applicable).",
        ],
        "concept_tags": ["CTE", "multiple CTEs", "LEFT JOIN", "COALESCE"],
    },
    {
        "id": "ec-100",
        "slug": "month-over-month-growth",
        "title": "Month-over-Month Revenue Growth Rate",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "ecommerce",
        "description": (
            "Calculate the month-over-month revenue growth rate. Use a CTE for monthly "
            "revenue, then use LAG to get the previous month's revenue. Compute growth "
            "as (current - previous) / previous * 100, rounded to 2 decimals. "
            "Sort by month."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH monthly_rev AS (\n"
            "    SELECT strftime('%Y-%m', order_date) AS month,\n"
            "           SUM(total_amount) AS revenue\n"
            "    FROM orders\n"
            "    GROUP BY month\n"
            ")\n"
            "SELECT month,\n"
            "       revenue,\n"
            "       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,\n"
            "       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0\n"
            "             / LAG(revenue) OVER (ORDER BY month), 2) AS growth_pct\n"
            "FROM monthly_rev\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Use a CTE to compute monthly revenue first.",
            "LAG(revenue) OVER (ORDER BY month) gets the prior month's value.",
            "Growth = (current - previous) / previous * 100.",
            "The first month will have NULL growth since there's no prior month.",
        ],
        "explanation": (
            "1. CTE aggregates revenue by month.\n"
            "2. LAG provides the previous month's revenue.\n"
            "3. Growth formula computes percentage change.\n"
            "4. First month has NULL growth (no predecessor)."
        ),
        "approach": [
            "CTE for monthly aggregation.",
            "LAG window function for previous value.",
            "Arithmetic for growth rate.",
        ],
        "common_mistakes": [
            "Division by zero if previous month's revenue is 0.",
            "Using LEAD instead of LAG.",
        ],
        "concept_tags": ["CTE", "LAG", "window function", "growth rate"],
    },
    # --- 5 hard advanced problems (ec-101 to ec-105) ---
    {
        "id": "ec-101",
        "slug": "rfm-segmentation",
        "title": "RFM Customer Segmentation",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Perform RFM (Recency, Frequency, Monetary) analysis. For each customer, compute: "
            "Recency = days since their last order (from '2025-01-01'), Frequency = number "
            "of orders, Monetary = total spend. Then assign each metric a score 1-3 using "
            "NTILE(3). Return customer_id, recency_days, frequency, monetary, and their "
            "three scores. Sort by monetary descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH rfm AS (\n"
            "    SELECT customer_id,\n"
            "           CAST(julianday('2025-01-01') - julianday(MAX(order_date)) AS INTEGER) AS recency_days,\n"
            "           COUNT(*) AS frequency,\n"
            "           SUM(total_amount) AS monetary\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT customer_id,\n"
            "       recency_days,\n"
            "       frequency,\n"
            "       monetary,\n"
            "       NTILE(3) OVER (ORDER BY recency_days DESC) AS recency_score,\n"
            "       NTILE(3) OVER (ORDER BY frequency) AS frequency_score,\n"
            "       NTILE(3) OVER (ORDER BY monetary) AS monetary_score\n"
            "FROM rfm\n"
            "ORDER BY monetary DESC;"
        ),
        "hints": [
            "Use julianday to compute days between dates.",
            "A CTE can compute the raw RFM values.",
            "NTILE(3) splits rows into 3 roughly equal groups.",
            "For recency, lower days = more recent = higher score, so order DESC.",
        ],
        "explanation": (
            "1. CTE computes recency (days since last order), frequency, and monetary.\n"
            "2. NTILE(3) assigns scores 1-3 for each metric.\n"
            "3. Recency is ordered DESC so recent customers get higher scores.\n"
            "4. Sort by monetary descending."
        ),
        "approach": [
            "CTE for raw RFM computation.",
            "NTILE for scoring.",
            "Careful ordering for each metric.",
        ],
        "common_mistakes": [
            "Getting recency score direction wrong (lower days should be higher score).",
            "Using RANK instead of NTILE for equal-sized groups.",
        ],
        "concept_tags": ["CTE", "NTILE", "window function", "RFM", "julianday"],
    },
    {
        "id": "ec-102",
        "slug": "market-basket-co-purchase",
        "title": "Market Basket: Frequently Co-Purchased Products",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Find pairs of products that are frequently bought together in the same order. "
            "For each pair, count how many orders contain both products. Only include pairs "
            "appearing in at least 2 orders. Show product_a name, product_b name, and "
            "co_purchase_count. Avoid duplicate pairs (A,B and B,A). Sort by count descending."
        ),
        "schema_hint": ["order_items", "products"],
        "solution_query": (
            "WITH item_pairs AS (\n"
            "    SELECT oi1.order_id,\n"
            "           oi1.product_id AS product_a_id,\n"
            "           oi2.product_id AS product_b_id\n"
            "    FROM order_items oi1\n"
            "    JOIN order_items oi2\n"
            "        ON oi1.order_id = oi2.order_id\n"
            "        AND oi1.product_id < oi2.product_id\n"
            ")\n"
            "SELECT p1.name AS product_a,\n"
            "       p2.name AS product_b,\n"
            "       COUNT(DISTINCT ip.order_id) AS co_purchase_count\n"
            "FROM item_pairs ip\n"
            "JOIN products p1 ON ip.product_a_id = p1.id\n"
            "JOIN products p2 ON ip.product_b_id = p2.id\n"
            "GROUP BY ip.product_a_id, ip.product_b_id\n"
            "HAVING co_purchase_count >= 2\n"
            "ORDER BY co_purchase_count DESC;"
        ),
        "hints": [
            "Self-join order_items to itself on order_id.",
            "Use product_id < product_id to avoid duplicate pairs and self-pairs.",
            "Count distinct orders for each pair.",
            "HAVING filters to pairs with at least 2 co-occurrences.",
        ],
        "explanation": (
            "1. Self-join order_items on order_id with < to get unique pairs.\n"
            "2. Count distinct orders per pair.\n"
            "3. HAVING >= 2 filters rare co-purchases.\n"
            "4. Join products for names."
        ),
        "approach": [
            "Self-join for pairs with < to deduplicate.",
            "Count co-occurrences.",
            "Filter and join for names.",
        ],
        "common_mistakes": [
            "Using != instead of < which creates duplicate pairs (A,B and B,A).",
            "Forgetting COUNT DISTINCT when an order could have multiple line items for the same product.",
        ],
        "concept_tags": ["self-join", "market basket", "CTE", "HAVING", "deduplication"],
    },
    {
        "id": "ec-103",
        "slug": "cohort-retention-analysis",
        "title": "Monthly Cohort Retention Analysis",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Perform a cohort retention analysis. Define each customer's cohort as the month "
            "of their first order. For each cohort month and subsequent order month, count "
            "distinct customers. Show cohort_month, order_month, months_since_first (0, 1, 2...), "
            "and customer_count. Sort by cohort_month, then months_since_first."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH first_order AS (\n"
            "    SELECT customer_id,\n"
            "           strftime('%Y-%m', MIN(order_date)) AS cohort_month\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "order_months AS (\n"
            "    SELECT customer_id,\n"
            "           strftime('%Y-%m', order_date) AS order_month\n"
            "    FROM orders\n"
            "    GROUP BY customer_id, strftime('%Y-%m', order_date)\n"
            ")\n"
            "SELECT fo.cohort_month,\n"
            "       om.order_month,\n"
            "       CAST((strftime('%Y', om.order_month || '-01') - strftime('%Y', fo.cohort_month || '-01')) * 12\n"
            "            + strftime('%m', om.order_month || '-01') - strftime('%m', fo.cohort_month || '-01') AS INTEGER) AS months_since_first,\n"
            "       COUNT(DISTINCT fo.customer_id) AS customer_count\n"
            "FROM first_order fo\n"
            "JOIN order_months om ON fo.customer_id = om.customer_id\n"
            "GROUP BY fo.cohort_month, om.order_month\n"
            "ORDER BY fo.cohort_month, months_since_first;"
        ),
        "hints": [
            "First CTE: find each customer's first order month (cohort).",
            "Second CTE: get distinct order months per customer.",
            "Join and compute month difference between order month and cohort.",
            "Group by cohort_month and order_month to count customers.",
        ],
        "explanation": (
            "1. first_order CTE finds each customer's cohort month.\n"
            "2. order_months CTE extracts distinct months per customer.\n"
            "3. Join them to pair each customer's activity with their cohort.\n"
            "4. Compute months_since_first using year/month arithmetic.\n"
            "5. COUNT DISTINCT per cohort and order month."
        ),
        "approach": [
            "CTE for cohort assignment.",
            "CTE for monthly activity.",
            "Join and compute time difference.",
            "Group and count.",
        ],
        "common_mistakes": [
            "Incorrect month difference calculation.",
            "Not deduplicating customers per month before counting.",
        ],
        "concept_tags": ["CTE", "cohort analysis", "retention", "date arithmetic"],
    },
    {
        "id": "ec-104",
        "slug": "inventory-reorder-alert",
        "title": "Inventory Reorder Alert with Sales Velocity",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Create an inventory alert system. Compute each product's average daily sales "
            "quantity over the last 30 days (from '2025-01-01'). Then estimate days until "
            "stockout as stock_quantity / avg_daily_sales. Flag products where days_until_stockout "
            "< 14 as 'REORDER'. Show product name, stock_quantity, avg_daily_sales (rounded to 2), "
            "days_until_stockout (rounded to 0), and the flag. Sort by days_until_stockout."
        ),
        "schema_hint": ["products", "order_items", "orders"],
        "solution_query": (
            "WITH recent_sales AS (\n"
            "    SELECT oi.product_id,\n"
            "           SUM(oi.quantity) AS total_sold\n"
            "    FROM order_items oi\n"
            "    JOIN orders o ON oi.order_id = o.id\n"
            "    WHERE o.order_date >= date('2025-01-01', '-30 days')\n"
            "      AND o.order_date <= '2025-01-01'\n"
            "    GROUP BY oi.product_id\n"
            "),\n"
            "velocity AS (\n"
            "    SELECT product_id,\n"
            "           total_sold,\n"
            "           ROUND(total_sold * 1.0 / 30, 2) AS avg_daily_sales\n"
            "    FROM recent_sales\n"
            ")\n"
            "SELECT p.name,\n"
            "       p.stock_quantity,\n"
            "       v.avg_daily_sales,\n"
            "       ROUND(p.stock_quantity * 1.0 / v.avg_daily_sales, 0) AS days_until_stockout,\n"
            "       CASE WHEN p.stock_quantity * 1.0 / v.avg_daily_sales < 14 THEN 'REORDER' ELSE 'OK' END AS flag\n"
            "FROM products p\n"
            "JOIN velocity v ON p.id = v.product_id\n"
            "WHERE v.avg_daily_sales > 0\n"
            "ORDER BY days_until_stockout;"
        ),
        "hints": [
            "Use a CTE to compute total quantity sold in the last 30 days per product.",
            "Divide by 30 for average daily sales.",
            "Days until stockout = stock / daily sales.",
            "Use CASE to flag items needing reorder.",
        ],
        "explanation": (
            "1. recent_sales CTE sums quantity sold in the 30-day window.\n"
            "2. velocity CTE computes daily average.\n"
            "3. Main query computes days until stockout and flags items.\n"
            "4. Filter out zero-velocity products to avoid division by zero."
        ),
        "approach": [
            "CTE for recent sales aggregation.",
            "CTE for daily velocity.",
            "Main query for stockout estimation and flagging.",
        ],
        "common_mistakes": [
            "Division by zero when avg_daily_sales is 0.",
            "Integer division without multiplying by 1.0.",
        ],
        "concept_tags": ["CTE", "CASE", "date arithmetic", "business logic", "inventory"],
    },
    {
        "id": "ec-105",
        "slug": "customer-churn-prediction",
        "title": "Customer Churn Risk Scoring",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "ecommerce",
        "description": (
            "Build a churn risk report. For each customer, compute: days since last order "
            "(from '2025-01-01'), total orders, average order value, and days between their "
            "first and last order. Assign risk: 'High' if no order in 90+ days, 'Medium' "
            "if 60-89 days, 'Low' otherwise. Show customer_id, first_name, last_name, "
            "total_orders, avg_order_value (rounded to 2), days_since_last_order, and risk_level. "
            "Sort by days_since_last_order descending."
        ),
        "schema_hint": ["orders", "customers"],
        "solution_query": (
            "WITH customer_metrics AS (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS total_orders,\n"
            "           ROUND(AVG(total_amount), 2) AS avg_order_value,\n"
            "           CAST(julianday('2025-01-01') - julianday(MAX(order_date)) AS INTEGER) AS days_since_last_order,\n"
            "           CAST(julianday(MAX(order_date)) - julianday(MIN(order_date)) AS INTEGER) AS customer_tenure_days\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT cm.customer_id,\n"
            "       c.first_name,\n"
            "       c.last_name,\n"
            "       cm.total_orders,\n"
            "       cm.avg_order_value,\n"
            "       cm.days_since_last_order,\n"
            "       CASE\n"
            "           WHEN cm.days_since_last_order >= 90 THEN 'High'\n"
            "           WHEN cm.days_since_last_order >= 60 THEN 'Medium'\n"
            "           ELSE 'Low'\n"
            "       END AS risk_level\n"
            "FROM customer_metrics cm\n"
            "JOIN customers c ON cm.customer_id = c.id\n"
            "ORDER BY cm.days_since_last_order DESC;"
        ),
        "hints": [
            "Use a CTE to compute all per-customer metrics.",
            "julianday gives a numeric day count for date arithmetic.",
            "CASE WHEN handles the risk classification.",
            "Join to customers for name columns.",
        ],
        "explanation": (
            "1. CTE computes order count, average value, recency, and tenure per customer.\n"
            "2. Main query joins to customers for names.\n"
            "3. CASE assigns risk based on days_since_last_order thresholds.\n"
            "4. Sort by recency descending to show highest risk first."
        ),
        "approach": [
            "CTE for customer-level metrics.",
            "JOIN for customer names.",
            "CASE for risk classification.",
            "Sort by recency.",
        ],
        "common_mistakes": [
            "Forgetting to handle customers with only one order (tenure = 0 days).",
            "Incorrect CASE ordering — conditions must go from highest to lowest.",
        ],
        "concept_tags": ["CTE", "CASE", "julianday", "churn analysis", "business logic"],
    },

    # =========================================================================
    # INTERVIEW PROBLEMS — EASY (12 problems: interview-ecom-001 to 012)
    # =========================================================================
    {
        "id": "interview-ecom-001",
        "slug": "int-ecom-count-delivered-orders",
        "title": "Count Delivered Orders",
        "difficulty": "easy",
        "category": "Interview — Aggregation",
        "dataset": "ecommerce",
        "description": (
            "The logistics team wants to know how many orders have been successfully "
            "delivered. Write a query that returns the total number of orders with "
            "a status of 'delivered'."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT COUNT(*) AS delivered_count\n"
            "FROM orders\n"
            "WHERE status = 'delivered';"
        ),
        "hints": [
            "Filter rows before counting them.",
            "Use WHERE to restrict to delivered orders.",
            "COUNT(*) counts all rows that pass the filter.",
        ],
        "explanation": (
            "1. WHERE status = 'delivered' filters to only delivered orders.\n"
            "2. COUNT(*) counts those filtered rows."
        ),
        "approach": [
            "Apply a WHERE filter for the delivered status.",
            "Use COUNT(*) to get the total.",
        ],
        "common_mistakes": [
            "Forgetting the WHERE clause and counting all orders.",
            "Using COUNT(status) instead of COUNT(*) — both work but COUNT(*) is conventional.",
        ],
        "concept_tags": ["COUNT", "WHERE", "filtering"],
    },
    {
        "id": "interview-ecom-002",
        "slug": "int-ecom-null-phone-customers",
        "title": "Customers with Missing Phone Numbers",
        "difficulty": "easy",
        "category": "Interview — NULL Handling",
        "dataset": "ecommerce",
        "description": (
            "The data quality team needs to identify customers with incomplete "
            "profiles. Find all customers whose phone number is missing (NULL). "
            "Return their id, first_name, last_name, and email."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT id, first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE phone IS NULL;"
        ),
        "hints": [
            "NULL is not a value — you cannot compare it with =.",
            "Use IS NULL to test for missing values.",
            "WHERE phone IS NULL finds rows with no phone number.",
        ],
        "explanation": (
            "1. WHERE phone IS NULL correctly identifies rows where phone is missing.\n"
            "2. Using = NULL would not work because NULL is not equal to anything, including itself."
        ),
        "approach": [
            "Use IS NULL to check for missing phone values.",
            "Select only the columns requested.",
        ],
        "common_mistakes": [
            "Writing WHERE phone = NULL, which always evaluates to UNKNOWN and returns no rows.",
            "Using WHERE phone = '' which checks for empty strings, not NULL.",
        ],
        "concept_tags": ["IS NULL", "WHERE", "NULL handling"],
    },
    {
        "id": "interview-ecom-003",
        "slug": "int-ecom-coalesce-phone-fallback",
        "title": "Customer Contact with COALESCE Fallback",
        "difficulty": "easy",
        "category": "Interview — COALESCE",
        "dataset": "ecommerce",
        "description": (
            "Build a customer contact list where every row has a usable contact "
            "value. Return the customer's first_name, last_name, and a column "
            "called contact_info that shows the phone number if available, "
            "otherwise shows the email address."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name,\n"
            "       COALESCE(phone, email) AS contact_info\n"
            "FROM customers;"
        ),
        "hints": [
            "COALESCE returns the first non-NULL argument.",
            "If phone is NULL, COALESCE will fall back to email.",
            "COALESCE(phone, email) gives phone when available, email otherwise.",
        ],
        "explanation": (
            "1. COALESCE(phone, email) evaluates phone first.\n"
            "2. If phone is NULL, it returns email instead.\n"
            "3. This ensures every row has a contact value."
        ),
        "approach": [
            "Use COALESCE to provide a fallback value for NULL phone numbers.",
            "Alias the result column as contact_info.",
        ],
        "common_mistakes": [
            "Using IFNULL instead of COALESCE — IFNULL works in SQLite but COALESCE is standard SQL.",
            "Reversing the argument order, which would show email for everyone who has one.",
        ],
        "concept_tags": ["COALESCE", "NULL handling", "SELECT"],
    },
    {
        "id": "interview-ecom-004",
        "slug": "int-ecom-case-order-size-label",
        "title": "Classify Orders by Size",
        "difficulty": "easy",
        "category": "Interview — CASE",
        "dataset": "ecommerce",
        "description": (
            "The analytics team wants to segment orders by value. Write a query "
            "that returns the order id, total_amount, and a new column called "
            "order_size that labels orders as 'Small' (under 50), 'Medium' "
            "(50 to 200 inclusive), or 'Large' (over 200)."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id,\n"
            "       total_amount,\n"
            "       CASE\n"
            "           WHEN total_amount < 50 THEN 'Small'\n"
            "           WHEN total_amount <= 200 THEN 'Medium'\n"
            "           ELSE 'Large'\n"
            "       END AS order_size\n"
            "FROM orders;"
        ),
        "hints": [
            "CASE WHEN lets you create conditional labels.",
            "Order the WHEN conditions from smallest to largest.",
            "ELSE handles all remaining values.",
        ],
        "explanation": (
            "1. CASE evaluates conditions in order.\n"
            "2. The first WHEN catches orders under 50.\n"
            "3. The second catches 50-200 (because < 50 was already handled).\n"
            "4. ELSE catches everything over 200."
        ),
        "approach": [
            "Use CASE WHEN for conditional classification.",
            "Order conditions so they are mutually exclusive.",
            "Use ELSE for the final bucket.",
        ],
        "common_mistakes": [
            "Overlapping ranges, e.g., <= 50 and >= 50, counting 50 in two buckets.",
            "Forgetting the ELSE clause, which results in NULL for unmatched rows.",
        ],
        "concept_tags": ["CASE", "conditional logic", "SELECT"],
    },
    {
        "id": "interview-ecom-005",
        "slug": "int-ecom-extract-order-year",
        "title": "Extract Year from Order Dates",
        "difficulty": "easy",
        "category": "Interview — Date Functions",
        "dataset": "ecommerce",
        "description": (
            "The reporting team needs order counts broken down by year. Write a "
            "query that extracts the year from order_date and counts the number of "
            "orders per year. Return the year and order_count, sorted by year."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT strftime('%Y', order_date) AS order_year,\n"
            "       COUNT(*) AS order_count\n"
            "FROM orders\n"
            "GROUP BY strftime('%Y', order_date)\n"
            "ORDER BY order_year;"
        ),
        "hints": [
            "SQLite uses strftime for date extraction.",
            "strftime('%Y', date_column) extracts the four-digit year.",
            "Group by the extracted year to count per year.",
        ],
        "explanation": (
            "1. strftime('%Y', order_date) extracts the year as a string.\n"
            "2. GROUP BY that expression aggregates orders per year.\n"
            "3. COUNT(*) counts orders within each year group."
        ),
        "approach": [
            "Use strftime to extract the year component.",
            "Group by the extracted year and count.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Using YEAR() which is not a SQLite function.",
            "Grouping by order_date directly, which groups by exact date instead of year.",
        ],
        "concept_tags": ["strftime", "GROUP BY", "COUNT", "date extraction"],
    },
    {
        "id": "interview-ecom-006",
        "slug": "int-ecom-uppercase-product-names",
        "title": "Uppercase Product Names",
        "difficulty": "easy",
        "category": "Interview — String Functions",
        "dataset": "ecommerce",
        "description": (
            "The export team needs product names in uppercase for a data feed. "
            "Write a query that returns the product id, the original name, and "
            "the name converted to uppercase (as upper_name). Also include the "
            "length of each product name (as name_length). Sort by name_length "
            "descending."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT id,\n"
            "       name,\n"
            "       UPPER(name) AS upper_name,\n"
            "       LENGTH(name) AS name_length\n"
            "FROM products\n"
            "ORDER BY name_length DESC;"
        ),
        "hints": [
            "UPPER() converts a string to uppercase.",
            "LENGTH() returns the number of characters in a string.",
            "You can use multiple string functions in the same SELECT.",
        ],
        "explanation": (
            "1. UPPER(name) converts the product name to uppercase.\n"
            "2. LENGTH(name) counts the characters in the name.\n"
            "3. ORDER BY name_length DESC shows the longest names first."
        ),
        "approach": [
            "Use UPPER for case conversion.",
            "Use LENGTH for character counting.",
            "Sort by the computed length.",
        ],
        "common_mistakes": [
            "Using LEN() instead of LENGTH() — SQLite uses LENGTH.",
            "Forgetting to alias the computed columns.",
        ],
        "concept_tags": ["UPPER", "LENGTH", "string functions", "SELECT"],
    },
    {
        "id": "interview-ecom-007",
        "slug": "int-ecom-union-cancelled-returned",
        "title": "Combine Cancelled and Returned Orders",
        "difficulty": "easy",
        "category": "Interview — UNION",
        "dataset": "ecommerce",
        "description": (
            "The loss prevention team needs a combined list of problematic orders. "
            "Write a query that returns all cancelled orders and all returned orders "
            "as a single result set. Include the order id, customer_id, order_date, "
            "status, and total_amount. Use UNION ALL to preserve duplicates."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT id, customer_id, order_date, status, total_amount\n"
            "FROM orders\n"
            "WHERE status = 'cancelled'\n"
            "UNION ALL\n"
            "SELECT id, customer_id, order_date, status, total_amount\n"
            "FROM orders\n"
            "WHERE status = 'returned'\n"
            "ORDER BY order_date DESC;"
        ),
        "hints": [
            "UNION ALL combines two result sets without removing duplicates.",
            "Both SELECT statements must have the same number and type of columns.",
            "An ORDER BY at the end sorts the combined result.",
        ],
        "explanation": (
            "1. First SELECT gets cancelled orders.\n"
            "2. UNION ALL appends returned orders.\n"
            "3. ORDER BY sorts the combined result by date.\n"
            "Note: This could also be done with WHERE status IN ('cancelled', 'returned'), "
            "but the problem specifically asks to demonstrate UNION ALL."
        ),
        "approach": [
            "Write two separate SELECT queries for each status.",
            "Combine them with UNION ALL.",
            "Apply ORDER BY to the final result.",
        ],
        "common_mistakes": [
            "Using UNION instead of UNION ALL — UNION removes duplicates, which adds overhead.",
            "Mismatching column counts or types between the two SELECTs.",
        ],
        "concept_tags": ["UNION ALL", "UNION", "set operations"],
    },
    {
        "id": "interview-ecom-008",
        "slug": "int-ecom-exists-customers-with-reviews",
        "title": "Customers Who Have Written Reviews",
        "difficulty": "easy",
        "category": "Interview — EXISTS",
        "dataset": "ecommerce",
        "description": (
            "Find all customers who have written at least one review. Use EXISTS "
            "to check for the presence of reviews. Return the customer id, "
            "first_name, and last_name."
        ),
        "schema_hint": ["customers", "reviews"],
        "solution_query": (
            "SELECT c.id, c.first_name, c.last_name\n"
            "FROM customers c\n"
            "WHERE EXISTS (\n"
            "    SELECT 1\n"
            "    FROM reviews r\n"
            "    WHERE r.customer_id = c.id\n"
            ");"
        ),
        "hints": [
            "EXISTS returns TRUE if the subquery returns at least one row.",
            "The subquery must be correlated — it references the outer table.",
            "SELECT 1 is conventional inside EXISTS since the actual values don't matter.",
        ],
        "explanation": (
            "1. For each customer, the EXISTS subquery checks if any reviews exist.\n"
            "2. The correlation is r.customer_id = c.id.\n"
            "3. If at least one review exists, the customer is included."
        ),
        "approach": [
            "Use a correlated subquery inside EXISTS.",
            "Reference the outer customer in the subquery's WHERE clause.",
        ],
        "common_mistakes": [
            "Forgetting the correlation (WHERE r.customer_id = c.id), making it a non-correlated subquery.",
            "Using SELECT * instead of SELECT 1 — both work but SELECT 1 is more conventional.",
        ],
        "concept_tags": ["EXISTS", "correlated subquery", "semi-join"],
    },
    {
        "id": "interview-ecom-009",
        "slug": "int-ecom-conditional-count-order-status",
        "title": "Count Orders by Status Category",
        "difficulty": "easy",
        "category": "Interview — Conditional Aggregation",
        "dataset": "ecommerce",
        "description": (
            "Write a single query that returns the total number of orders, the "
            "count of completed orders (status = 'delivered'), and the count of "
            "problematic orders (status IN ('cancelled', 'returned'))."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT COUNT(*) AS total_orders,\n"
            "       SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS completed_orders,\n"
            "       SUM(CASE WHEN status IN ('cancelled', 'returned') THEN 1 ELSE 0 END) AS problematic_orders\n"
            "FROM orders;"
        ),
        "hints": [
            "You can use CASE inside an aggregate function.",
            "SUM(CASE WHEN ... THEN 1 ELSE 0 END) counts rows matching a condition.",
            "No GROUP BY needed — you are aggregating the entire table.",
        ],
        "explanation": (
            "1. COUNT(*) counts all orders.\n"
            "2. SUM(CASE WHEN status = 'delivered' ...) counts only delivered orders.\n"
            "3. SUM(CASE WHEN status IN (...) ...) counts cancelled and returned orders."
        ),
        "approach": [
            "Use conditional aggregation with CASE inside SUM.",
            "Each SUM/CASE pair counts a different subset.",
        ],
        "common_mistakes": [
            "Writing separate queries for each count instead of combining them.",
            "Forgetting ELSE 0, which results in NULL instead of 0 for non-matching rows.",
        ],
        "concept_tags": ["CASE", "SUM", "conditional aggregation"],
    },
    {
        "id": "interview-ecom-010",
        "slug": "int-ecom-distinct-states-with-counts",
        "title": "Customer Count by State",
        "difficulty": "easy",
        "category": "Interview — GROUP BY",
        "dataset": "ecommerce",
        "description": (
            "The expansion team wants to see customer distribution across states. "
            "Return each state and the number of customers in that state, but only "
            "include states that have at least 2 customers. Sort by customer count "
            "descending."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT state, COUNT(*) AS customer_count\n"
            "FROM customers\n"
            "GROUP BY state\n"
            "HAVING COUNT(*) >= 2\n"
            "ORDER BY customer_count DESC;"
        ),
        "hints": [
            "GROUP BY state creates one group per state.",
            "HAVING filters groups after aggregation.",
            "HAVING COUNT(*) >= 2 keeps only states with multiple customers.",
        ],
        "explanation": (
            "1. GROUP BY state aggregates customers per state.\n"
            "2. COUNT(*) counts customers in each state.\n"
            "3. HAVING COUNT(*) >= 2 filters out states with only one customer.\n"
            "4. ORDER BY customer_count DESC shows the most populated states first."
        ),
        "approach": [
            "Group by state and count.",
            "Use HAVING to filter groups by count.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING for the count filter.",
            "Using HAVING with the alias (customer_count) — SQLite supports this but it is not portable.",
        ],
        "concept_tags": ["GROUP BY", "HAVING", "COUNT", "ORDER BY"],
    },
    {
        "id": "interview-ecom-011",
        "slug": "int-ecom-second-highest-price",
        "title": "Second Most Expensive Product",
        "difficulty": "easy",
        "category": "Interview — Subquery",
        "dataset": "ecommerce",
        "description": (
            "Find the product with the second highest price. Return its name and "
            "price. If there are ties for the highest price, the second highest "
            "should be the next distinct price below the maximum."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT name, price\n"
            "FROM products\n"
            "WHERE price = (\n"
            "    SELECT MAX(price)\n"
            "    FROM products\n"
            "    WHERE price < (SELECT MAX(price) FROM products)\n"
            ");"
        ),
        "hints": [
            "First find the maximum price, then find the max price below that.",
            "Use a nested subquery to find the second-highest distinct price.",
            "The inner subquery gets MAX(price), the outer subquery gets MAX(price) below that.",
        ],
        "explanation": (
            "1. The innermost query finds the absolute maximum price.\n"
            "2. The middle query finds the maximum price that is strictly less than the max.\n"
            "3. The outer query returns all products at that second-highest price."
        ),
        "approach": [
            "Use nested subqueries to find the second-highest distinct price.",
            "Return all products at that price level.",
        ],
        "common_mistakes": [
            "Using LIMIT 1 OFFSET 1 without handling ties correctly.",
            "Not considering that multiple products could share the second-highest price.",
        ],
        "concept_tags": ["subquery", "MAX", "nested queries"],
    },
    {
        "id": "interview-ecom-012",
        "slug": "int-ecom-total-discount-per-order",
        "title": "Total Discount Amount Per Order",
        "difficulty": "easy",
        "category": "Interview — Aggregation",
        "dataset": "ecommerce",
        "description": (
            "Calculate the total discount given on each order. The discount on each "
            "line item is quantity * unit_price * discount (where discount is a "
            "decimal fraction). Return order_id and total_discount_amount, only "
            "for orders where the total discount exceeds 10. Sort by "
            "total_discount_amount descending."
        ),
        "schema_hint": ["order_items"],
        "solution_query": (
            "SELECT order_id,\n"
            "       ROUND(SUM(quantity * unit_price * discount), 2) AS total_discount_amount\n"
            "FROM order_items\n"
            "GROUP BY order_id\n"
            "HAVING SUM(quantity * unit_price * discount) > 10\n"
            "ORDER BY total_discount_amount DESC;"
        ),
        "hints": [
            "Discount per line item = quantity * unit_price * discount.",
            "SUM the discount across all items in each order.",
            "Use HAVING to filter orders with total discount > 10.",
        ],
        "explanation": (
            "1. For each line item, the discount amount is quantity * unit_price * discount.\n"
            "2. SUM aggregates the discount across all items per order.\n"
            "3. HAVING filters to orders with significant discounts.\n"
            "4. ROUND ensures clean decimal output."
        ),
        "approach": [
            "Calculate line-item discount as quantity * unit_price * discount.",
            "Group by order_id and sum the discounts.",
            "Filter with HAVING and sort descending.",
        ],
        "common_mistakes": [
            "Treating the discount column as a flat dollar amount instead of a fraction.",
            "Forgetting GROUP BY and getting a single total across all orders.",
        ],
        "concept_tags": ["SUM", "GROUP BY", "HAVING", "ROUND", "calculated columns"],
    },

    # =========================================================================
    # INTERVIEW PROBLEMS — MEDIUM (13 problems: interview-ecom-013 to 025)
    # =========================================================================
    {
        "id": "interview-ecom-013",
        "slug": "int-ecom-revenue-per-customer-with-name",
        "title": "Total Revenue Per Customer with Name",
        "difficulty": "medium",
        "category": "Interview — JOIN + Aggregation",
        "dataset": "ecommerce",
        "description": (
            "Calculate the total revenue generated by each customer. Join orders "
            "with customers to show the customer's full name (first_name || ' ' || "
            "last_name), their total number of orders, and their total spending. "
            "Only include customers who have spent more than 500 in total. Sort "
            "by total spending descending."
        ),
        "schema_hint": ["customers", "orders"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       COUNT(o.id) AS total_orders,\n"
            "       ROUND(SUM(o.total_amount), 2) AS total_spending\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING SUM(o.total_amount) > 500\n"
            "ORDER BY total_spending DESC;"
        ),
        "hints": [
            "Join customers to orders on customer_id.",
            "Group by customer to aggregate their orders.",
            "Use HAVING to filter by total spending.",
            "Concatenate first and last name for the full name.",
        ],
        "explanation": (
            "1. JOIN customers to orders on the foreign key.\n"
            "2. GROUP BY customer aggregates all their orders.\n"
            "3. COUNT(o.id) counts orders, SUM(o.total_amount) totals spending.\n"
            "4. HAVING SUM(o.total_amount) > 500 filters low-spending customers."
        ),
        "approach": [
            "Join the two tables on customer_id.",
            "Group by customer identifiers.",
            "Aggregate with COUNT and SUM.",
            "Filter groups with HAVING.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING for the spending filter.",
            "Not including all non-aggregated columns in GROUP BY.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "SUM", "COUNT"],
    },
    {
        "id": "interview-ecom-014",
        "slug": "int-ecom-subquery-above-avg-spending",
        "title": "Customers Spending Above Average",
        "difficulty": "medium",
        "category": "Interview — Subquery in WHERE",
        "dataset": "ecommerce",
        "description": (
            "Find customers whose total spending exceeds the average total spending "
            "across all customers. Return customer_id, total_spending, and the "
            "overall average spending. Sort by total_spending descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       SUM(total_amount) AS total_spending,\n"
            "       (SELECT ROUND(AVG(customer_total), 2)\n"
            "        FROM (SELECT SUM(total_amount) AS customer_total\n"
            "              FROM orders GROUP BY customer_id)) AS avg_spending\n"
            "FROM orders\n"
            "GROUP BY customer_id\n"
            "HAVING SUM(total_amount) > (\n"
            "    SELECT AVG(customer_total)\n"
            "    FROM (SELECT SUM(total_amount) AS customer_total\n"
            "          FROM orders GROUP BY customer_id)\n"
            ")\n"
            "ORDER BY total_spending DESC;"
        ),
        "hints": [
            "First calculate total spending per customer, then find the average of those totals.",
            "Use a subquery in HAVING to compare against the average.",
            "The average of per-customer totals requires a nested subquery.",
        ],
        "explanation": (
            "1. The outer query groups orders by customer and sums their spending.\n"
            "2. The HAVING subquery calculates the average of per-customer totals.\n"
            "3. Only customers whose total exceeds that average are returned.\n"
            "4. The scalar subquery in SELECT shows the average for context."
        ),
        "approach": [
            "Group by customer_id and sum total_amount.",
            "Build a subquery that computes per-customer totals and averages them.",
            "Use HAVING to compare each customer's total to the average.",
        ],
        "common_mistakes": [
            "Using AVG(total_amount) directly, which averages individual orders, not per-customer totals.",
            "Forgetting that the average needs to be computed from grouped totals.",
        ],
        "concept_tags": ["subquery", "HAVING", "AVG", "GROUP BY", "nested queries"],
    },
    {
        "id": "interview-ecom-015",
        "slug": "int-ecom-correlated-latest-order-per-customer",
        "title": "Each Customer's Most Recent Order Amount",
        "difficulty": "medium",
        "category": "Interview — Correlated Subquery",
        "dataset": "ecommerce",
        "description": (
            "For each customer, find the total_amount of their most recent order. "
            "Use a correlated subquery to match each customer to their latest order. "
            "Return customer_id, order_date, and total_amount."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT o.customer_id, o.order_date, o.total_amount\n"
            "FROM orders o\n"
            "WHERE o.order_date = (\n"
            "    SELECT MAX(o2.order_date)\n"
            "    FROM orders o2\n"
            "    WHERE o2.customer_id = o.customer_id\n"
            ");"
        ),
        "hints": [
            "A correlated subquery references the outer query's current row.",
            "For each row, find the MAX order_date for that customer.",
            "Compare the row's order_date to the max for its customer.",
        ],
        "explanation": (
            "1. For each order row, the subquery finds the maximum order_date for that customer.\n"
            "2. The WHERE clause keeps only the row(s) matching that max date.\n"
            "3. This gives the most recent order per customer."
        ),
        "approach": [
            "Write a correlated subquery that finds MAX(order_date) per customer.",
            "Match the outer row's date to the subquery result.",
        ],
        "common_mistakes": [
            "Forgetting the correlation (o2.customer_id = o.customer_id), which would return the global max date.",
            "Not handling ties — if a customer has two orders on the same max date, both are returned.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "per-group filtering"],
    },
    {
        "id": "interview-ecom-016",
        "slug": "int-ecom-case-aggregation-rating-breakdown",
        "title": "Product Rating Breakdown with CASE",
        "difficulty": "medium",
        "category": "Interview — CASE with Aggregation",
        "dataset": "ecommerce",
        "description": (
            "For each product, calculate the number of positive reviews (rating >= 4), "
            "neutral reviews (rating = 3), and negative reviews (rating <= 2). "
            "Return product_id and the three counts. Only include products with at "
            "least 2 reviews total."
        ),
        "schema_hint": ["reviews"],
        "solution_query": (
            "SELECT product_id,\n"
            "       SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) AS positive_reviews,\n"
            "       SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END) AS neutral_reviews,\n"
            "       SUM(CASE WHEN rating <= 2 THEN 1 ELSE 0 END) AS negative_reviews\n"
            "FROM reviews\n"
            "GROUP BY product_id\n"
            "HAVING COUNT(*) >= 2\n"
            "ORDER BY product_id;"
        ),
        "hints": [
            "Use CASE inside SUM for conditional counting.",
            "Each CASE expression handles one rating bucket.",
            "HAVING COUNT(*) >= 2 filters to products with enough reviews.",
        ],
        "explanation": (
            "1. Each SUM(CASE ...) counts reviews in a specific rating range.\n"
            "2. GROUP BY product_id aggregates per product.\n"
            "3. HAVING ensures minimum review count.\n"
            "4. This is a pivoting technique — turning row values into columns."
        ),
        "approach": [
            "Create three CASE expressions for positive, neutral, and negative.",
            "Wrap each in SUM for counting.",
            "Group by product and filter with HAVING.",
        ],
        "common_mistakes": [
            "Overlapping CASE conditions (e.g., >= 3 and <= 3 both matching rating = 3).",
            "Forgetting ELSE 0, causing NULL instead of 0.",
        ],
        "concept_tags": ["CASE", "SUM", "conditional aggregation", "pivoting"],
    },
    {
        "id": "interview-ecom-017",
        "slug": "int-ecom-date-diff-shipping-days",
        "title": "Average Days to Ship by Status",
        "difficulty": "medium",
        "category": "Interview — Date Arithmetic",
        "dataset": "ecommerce",
        "description": (
            "Calculate the average number of days between order_date and "
            "shipping_date for each order status. Only consider orders that have "
            "a shipping record. Return the order status, average days to ship "
            "(rounded to 1 decimal), and the count of orders."
        ),
        "schema_hint": ["orders", "shipping"],
        "solution_query": (
            "SELECT o.status,\n"
            "       ROUND(AVG(julianday(s.shipping_date) - julianday(o.order_date)), 1) AS avg_days_to_ship,\n"
            "       COUNT(*) AS order_count\n"
            "FROM orders o\n"
            "JOIN shipping s ON o.id = s.order_id\n"
            "GROUP BY o.status\n"
            "ORDER BY avg_days_to_ship;"
        ),
        "hints": [
            "julianday() converts a date to a numeric day value in SQLite.",
            "Subtracting two julianday values gives the difference in days.",
            "Join orders to shipping to get both dates.",
        ],
        "explanation": (
            "1. JOIN orders to shipping on order_id.\n"
            "2. julianday(shipping_date) - julianday(order_date) gives days between.\n"
            "3. AVG computes the mean per status group.\n"
            "4. ROUND(..., 1) limits to one decimal place."
        ),
        "approach": [
            "Join orders and shipping tables.",
            "Use julianday for date arithmetic.",
            "Group by status and compute AVG.",
        ],
        "common_mistakes": [
            "Using DATEDIFF which is not a SQLite function.",
            "Subtracting date strings directly without julianday conversion.",
        ],
        "concept_tags": ["julianday", "date arithmetic", "AVG", "JOIN", "GROUP BY"],
    },
    {
        "id": "interview-ecom-018",
        "slug": "int-ecom-self-join-same-category-products",
        "title": "Product Pairs in the Same Category",
        "difficulty": "medium",
        "category": "Interview — Self Join",
        "dataset": "ecommerce",
        "description": (
            "Find all pairs of products that belong to the same category. Return "
            "the category_id, the name of the first product (product_a), and the "
            "name of the second product (product_b). Avoid duplicate pairs by "
            "ensuring the first product's id is less than the second's."
        ),
        "schema_hint": ["products"],
        "solution_query": (
            "SELECT p1.category_id,\n"
            "       p1.name AS product_a,\n"
            "       p2.name AS product_b\n"
            "FROM products p1\n"
            "JOIN products p2 ON p1.category_id = p2.category_id\n"
            "                 AND p1.id < p2.id\n"
            "ORDER BY p1.category_id, p1.name;"
        ),
        "hints": [
            "A self-join joins a table to itself.",
            "Use two different aliases for the same table.",
            "p1.id < p2.id ensures each pair appears only once.",
        ],
        "explanation": (
            "1. Self-join products to itself on matching category_id.\n"
            "2. The condition p1.id < p2.id prevents (A,B) and (B,A) duplicates.\n"
            "3. It also prevents pairing a product with itself (p1.id != p2.id)."
        ),
        "approach": [
            "Join the products table to itself using different aliases.",
            "Match on category_id for same-category products.",
            "Use id inequality to deduplicate pairs.",
        ],
        "common_mistakes": [
            "Using p1.id != p2.id which still produces duplicate pairs (A,B) and (B,A).",
            "Forgetting the category_id join condition, producing cross-category pairs.",
        ],
        "concept_tags": ["self-join", "JOIN", "deduplication"],
    },
    {
        "id": "interview-ecom-019",
        "slug": "int-ecom-anti-join-unshipped-orders",
        "title": "Orders That Were Never Shipped",
        "difficulty": "medium",
        "category": "Interview — Anti-Join",
        "dataset": "ecommerce",
        "description": (
            "Find all orders that have no corresponding shipping record. "
            "Return the order id, customer_id, order_date, status, and "
            "total_amount. Sort by order_date descending."
        ),
        "schema_hint": ["orders", "shipping"],
        "solution_query": (
            "SELECT o.id, o.customer_id, o.order_date, o.status, o.total_amount\n"
            "FROM orders o\n"
            "LEFT JOIN shipping s ON o.id = s.order_id\n"
            "WHERE s.id IS NULL\n"
            "ORDER BY o.order_date DESC;"
        ),
        "hints": [
            "A LEFT JOIN keeps all rows from the left table.",
            "Rows with no match in shipping will have NULL in all shipping columns.",
            "Filter for s.id IS NULL to find unshipped orders.",
        ],
        "explanation": (
            "1. LEFT JOIN preserves all orders, even those without shipping records.\n"
            "2. WHERE s.id IS NULL filters to only unmatched orders.\n"
            "3. This is the classic anti-join pattern."
        ),
        "approach": [
            "Use LEFT JOIN from orders to shipping.",
            "Filter for NULL on the shipping side.",
            "Sort by date descending.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which would exclude the very orders you want to find.",
            "Checking s.order_id IS NULL instead of s.id — the join key might seem NULL for a different reason.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join"],
    },
    {
        "id": "interview-ecom-020",
        "slug": "int-ecom-pivot-payment-method-revenue",
        "title": "Revenue Pivot by Payment Method Per Month",
        "difficulty": "medium",
        "category": "Interview — Pivoting with CASE",
        "dataset": "ecommerce",
        "description": (
            "Create a monthly revenue breakdown by payment method. For each month "
            "(YYYY-MM format), show separate columns for credit_card, debit_card, "
            "paypal, and bank_transfer revenue. Sort chronologically."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT strftime('%Y-%m', payment_date) AS month,\n"
            "       ROUND(SUM(CASE WHEN method = 'credit_card' THEN amount ELSE 0 END), 2) AS credit_card,\n"
            "       ROUND(SUM(CASE WHEN method = 'debit_card' THEN amount ELSE 0 END), 2) AS debit_card,\n"
            "       ROUND(SUM(CASE WHEN method = 'paypal' THEN amount ELSE 0 END), 2) AS paypal,\n"
            "       ROUND(SUM(CASE WHEN method = 'bank_transfer' THEN amount ELSE 0 END), 2) AS bank_transfer\n"
            "FROM payments\n"
            "WHERE status = 'completed'\n"
            "GROUP BY strftime('%Y-%m', payment_date)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Use CASE inside SUM to route amounts to different columns.",
            "Each payment method gets its own SUM(CASE ...) expression.",
            "Group by month to get monthly totals.",
        ],
        "explanation": (
            "1. strftime('%Y-%m', payment_date) extracts the year-month.\n"
            "2. Each SUM(CASE ...) accumulates revenue for one payment method.\n"
            "3. This effectively pivots rows into columns.\n"
            "4. Only completed payments are counted."
        ),
        "approach": [
            "Extract month from payment_date.",
            "Create a SUM(CASE ...) for each payment method.",
            "Group by month and sort chronologically.",
        ],
        "common_mistakes": [
            "Forgetting to filter for completed payments, including failed/refunded amounts.",
            "Missing the ELSE 0 which would cause NULL in months with no transactions for a method.",
        ],
        "concept_tags": ["CASE", "SUM", "pivoting", "strftime", "GROUP BY"],
    },
    {
        "id": "interview-ecom-021",
        "slug": "int-ecom-cumulative-customer-spending",
        "title": "Cumulative Spending Per Customer",
        "difficulty": "medium",
        "category": "Interview — Cumulative Sum",
        "dataset": "ecommerce",
        "description": (
            "For each customer's orders, calculate a running total of their "
            "spending over time. Return customer_id, order_date, total_amount, "
            "and cumulative_spending (the sum of all their orders up to and "
            "including the current one). Sort by customer_id, then order_date."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       SUM(total_amount) OVER (\n"
            "           PARTITION BY customer_id\n"
            "           ORDER BY order_date\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS cumulative_spending\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_date;"
        ),
        "hints": [
            "A cumulative sum uses a window function with a running frame.",
            "PARTITION BY customer_id resets the sum for each customer.",
            "ORDER BY order_date inside the window defines the running order.",
        ],
        "explanation": (
            "1. SUM(total_amount) OVER(...) computes a running sum.\n"
            "2. PARTITION BY customer_id resets the sum per customer.\n"
            "3. ORDER BY order_date with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW "
            "accumulates from the first order to the current one."
        ),
        "approach": [
            "Use SUM as a window function with PARTITION BY and ORDER BY.",
            "Define the frame as ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, which computes a cumulative sum across all customers.",
            "Using GROUP BY instead of a window function, which collapses rows.",
        ],
        "concept_tags": ["window function", "SUM OVER", "cumulative sum", "PARTITION BY"],
    },
    {
        "id": "interview-ecom-022",
        "slug": "int-ecom-from-subquery-top-category",
        "title": "Top-Selling Category by Quantity",
        "difficulty": "medium",
        "category": "Interview — Subquery in FROM",
        "dataset": "ecommerce",
        "description": (
            "Find the product category with the highest total quantity sold. "
            "Use a subquery in the FROM clause to first calculate total quantity "
            "per category, then select the top one. Return category name and "
            "total_quantity."
        ),
        "schema_hint": ["order_items", "products", "categories"],
        "solution_query": (
            "SELECT category_name, total_quantity\n"
            "FROM (\n"
            "    SELECT c.name AS category_name,\n"
            "           SUM(oi.quantity) AS total_quantity\n"
            "    FROM order_items oi\n"
            "    JOIN products p ON oi.product_id = p.id\n"
            "    JOIN categories c ON p.category_id = c.id\n"
            "    GROUP BY c.name\n"
            "    ORDER BY total_quantity DESC\n"
            "    LIMIT 1\n"
            ") sub;"
        ),
        "hints": [
            "A subquery in FROM (derived table) acts like a temporary table.",
            "First aggregate quantity by category inside the subquery.",
            "Then select from it with LIMIT 1 for the top category.",
        ],
        "explanation": (
            "1. The inner subquery joins order_items -> products -> categories.\n"
            "2. It groups by category and sums quantity.\n"
            "3. ORDER BY total_quantity DESC LIMIT 1 picks the highest.\n"
            "4. The outer query simply selects from this derived table."
        ),
        "approach": [
            "Write the aggregation query as a derived table (subquery in FROM).",
            "Apply ORDER BY and LIMIT inside the subquery.",
            "Select from the derived table.",
        ],
        "common_mistakes": [
            "Forgetting to alias the subquery (required in most SQL dialects).",
            "Not joining through products to reach categories.",
        ],
        "concept_tags": ["derived table", "subquery in FROM", "JOIN", "LIMIT"],
    },
    {
        "id": "interview-ecom-023",
        "slug": "int-ecom-percentage-of-total-revenue",
        "title": "Each Product's Share of Total Revenue",
        "difficulty": "medium",
        "category": "Interview — Percentage Calculation",
        "dataset": "ecommerce",
        "description": (
            "Calculate each product's share of total revenue as a percentage. "
            "Return the product name, its revenue (quantity * unit_price), and "
            "its percentage of overall revenue (rounded to 2 decimal places). "
            "Sort by revenue_pct descending."
        ),
        "schema_hint": ["order_items", "products"],
        "solution_query": (
            "SELECT p.name,\n"
            "       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS product_revenue,\n"
            "       ROUND(\n"
            "           SUM(oi.quantity * oi.unit_price) * 100.0 /\n"
            "           (SELECT SUM(quantity * unit_price) FROM order_items),\n"
            "           2\n"
            "       ) AS revenue_pct\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.id\n"
            "GROUP BY p.id, p.name\n"
            "ORDER BY revenue_pct DESC;"
        ),
        "hints": [
            "Use a scalar subquery to get total revenue across all products.",
            "Divide each product's revenue by the total and multiply by 100.",
            "Multiply by 100.0 (not 100) to force floating-point division.",
        ],
        "explanation": (
            "1. SUM(oi.quantity * oi.unit_price) computes each product's revenue.\n"
            "2. The scalar subquery gets the overall total revenue.\n"
            "3. Dividing and multiplying by 100.0 gives the percentage.\n"
            "4. ROUND(..., 2) formats to two decimal places."
        ),
        "approach": [
            "Aggregate revenue per product.",
            "Use a scalar subquery for the grand total.",
            "Compute percentage with floating-point division.",
        ],
        "common_mistakes": [
            "Integer division (100 instead of 100.0) which truncates the result to 0.",
            "Forgetting the scalar subquery and trying to mix aggregate levels.",
        ],
        "concept_tags": ["scalar subquery", "percentage", "SUM", "GROUP BY"],
    },
    {
        "id": "interview-ecom-024",
        "slug": "int-ecom-customers-multiple-payment-methods",
        "title": "Customers Using Multiple Payment Methods",
        "difficulty": "medium",
        "category": "Interview — Multi-table JOIN + DISTINCT",
        "dataset": "ecommerce",
        "description": (
            "Find customers who have used more than one distinct payment method "
            "across all their orders. Return the customer's full name, the number "
            "of distinct payment methods they've used, and their total spending. "
            "Sort by distinct_methods descending."
        ),
        "schema_hint": ["customers", "orders", "payments"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS customer_name,\n"
            "       COUNT(DISTINCT pay.method) AS distinct_methods,\n"
            "       ROUND(SUM(DISTINCT pay.amount), 2) AS total_spending\n"
            "FROM customers c\n"
            "JOIN orders o ON c.id = o.customer_id\n"
            "JOIN payments pay ON o.id = pay.order_id\n"
            "WHERE pay.status = 'completed'\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(DISTINCT pay.method) > 1\n"
            "ORDER BY distinct_methods DESC;"
        ),
        "hints": [
            "COUNT(DISTINCT method) counts unique payment methods per customer.",
            "You need to join customers -> orders -> payments.",
            "HAVING COUNT(DISTINCT ...) > 1 filters for multiple methods.",
        ],
        "explanation": (
            "1. Three-table join: customers -> orders -> payments.\n"
            "2. COUNT(DISTINCT pay.method) counts unique methods per customer.\n"
            "3. HAVING filters to customers with more than one method.\n"
            "4. Only completed payments are considered."
        ),
        "approach": [
            "Chain joins from customers to orders to payments.",
            "Use COUNT(DISTINCT) on the method column.",
            "Filter with HAVING for more than one method.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT inside COUNT, counting total payments instead of unique methods.",
            "Not filtering for completed payments, including failed ones.",
        ],
        "concept_tags": ["COUNT DISTINCT", "HAVING", "multi-table JOIN"],
    },
    {
        "id": "interview-ecom-025",
        "slug": "int-ecom-moving-avg-3-order",
        "title": "3-Order Moving Average Per Customer",
        "difficulty": "medium",
        "category": "Interview — Moving Average",
        "dataset": "ecommerce",
        "description": (
            "Calculate a 3-order moving average of total_amount for each customer. "
            "The moving average should include the current order and the two preceding "
            "orders (by date). Return customer_id, order_date, total_amount, and "
            "moving_avg_3 (rounded to 2 decimal places)."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       ROUND(AVG(total_amount) OVER (\n"
            "           PARTITION BY customer_id\n"
            "           ORDER BY order_date\n"
            "           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg_3\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_date;"
        ),
        "hints": [
            "Use AVG as a window function with a frame clause.",
            "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW defines a 3-row window.",
            "PARTITION BY customer_id resets the window per customer.",
        ],
        "explanation": (
            "1. AVG(total_amount) OVER(...) computes the average within the window frame.\n"
            "2. ROWS BETWEEN 2 PRECEDING AND CURRENT ROW includes up to 3 rows.\n"
            "3. For the first order, only 1 row is in the window; for the second, 2 rows.\n"
            "4. PARTITION BY customer_id isolates each customer's calculations."
        ),
        "approach": [
            "Use AVG as a window function.",
            "Define the frame as 2 PRECEDING to CURRENT ROW.",
            "Partition by customer_id.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS, which handles ties differently.",
            "Forgetting PARTITION BY, computing the moving average across all customers.",
        ],
        "concept_tags": ["window function", "AVG OVER", "moving average", "ROWS BETWEEN"],
    },

    # =========================================================================
    # INTERVIEW PROBLEMS — HARD (10 problems: interview-ecom-026 to 035)
    # =========================================================================
    {
        "id": "interview-ecom-026",
        "slug": "int-ecom-rank-customers-by-order-value",
        "title": "Rank Customers by Order Value with RANK and DENSE_RANK",
        "difficulty": "hard",
        "category": "Interview — Window Functions",
        "dataset": "ecommerce",
        "description": (
            "For each order, rank customers by total_amount using both RANK() and "
            "DENSE_RANK(). Return customer_id, order_date, total_amount, the RANK "
            "value, and the DENSE_RANK value. Order by total_amount descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       RANK() OVER (ORDER BY total_amount DESC) AS rank_val,\n"
            "       DENSE_RANK() OVER (ORDER BY total_amount DESC) AS dense_rank_val\n"
            "FROM orders\n"
            "ORDER BY total_amount DESC;"
        ),
        "hints": [
            "RANK() and DENSE_RANK() are window functions that assign rankings.",
            "RANK() leaves gaps after ties; DENSE_RANK() does not.",
            "Both use OVER (ORDER BY ...) to define the ranking order.",
        ],
        "explanation": (
            "1. RANK() assigns ranks with gaps — if two rows tie for rank 1, the next rank is 3.\n"
            "2. DENSE_RANK() assigns ranks without gaps — the next rank after a tie for 1 is 2.\n"
            "3. Both are ordered by total_amount DESC for highest-first ranking."
        ),
        "approach": [
            "Use RANK() OVER (ORDER BY total_amount DESC).",
            "Use DENSE_RANK() OVER (ORDER BY total_amount DESC).",
            "Compare the two rankings side by side.",
        ],
        "common_mistakes": [
            "Confusing RANK, DENSE_RANK, and ROW_NUMBER behavior with ties.",
            "Forgetting the OVER clause, which causes a syntax error.",
        ],
        "concept_tags": ["RANK", "DENSE_RANK", "window function"],
    },
    {
        "id": "interview-ecom-027",
        "slug": "int-ecom-row-number-dedup",
        "title": "Deduplicate Reviews with ROW_NUMBER",
        "difficulty": "hard",
        "category": "Interview — ROW_NUMBER",
        "dataset": "ecommerce",
        "description": (
            "Some customers may have left multiple reviews for the same product. "
            "For each customer-product pair, keep only the most recent review. "
            "Return the review id, product_id, customer_id, rating, and review_date."
        ),
        "schema_hint": ["reviews"],
        "solution_query": (
            "SELECT id, product_id, customer_id, rating, review_date\n"
            "FROM (\n"
            "    SELECT *,\n"
            "           ROW_NUMBER() OVER (\n"
            "               PARTITION BY customer_id, product_id\n"
            "               ORDER BY review_date DESC\n"
            "           ) AS rn\n"
            "    FROM reviews\n"
            ") sub\n"
            "WHERE rn = 1;"
        ),
        "hints": [
            "ROW_NUMBER assigns a unique sequential number within each partition.",
            "PARTITION BY customer_id, product_id creates groups for each customer-product pair.",
            "ORDER BY review_date DESC makes the most recent review row number 1.",
            "Filter for rn = 1 to keep only the latest review per pair.",
        ],
        "explanation": (
            "1. ROW_NUMBER() assigns 1 to the most recent review per customer-product pair.\n"
            "2. The subquery assigns row numbers to all reviews.\n"
            "3. The outer WHERE rn = 1 keeps only the latest review per pair.\n"
            "4. This is a standard deduplication pattern."
        ),
        "approach": [
            "Use ROW_NUMBER with PARTITION BY on the deduplication keys.",
            "Order by review_date DESC within each partition.",
            "Wrap in a subquery and filter for rn = 1.",
        ],
        "common_mistakes": [
            "Trying to filter ROW_NUMBER in the same SELECT (window functions cannot appear in WHERE).",
            "Using RANK instead of ROW_NUMBER, which assigns the same rank to ties.",
        ],
        "concept_tags": ["ROW_NUMBER", "window function", "deduplication"],
    },
    {
        "id": "interview-ecom-028",
        "slug": "int-ecom-lag-lead-order-comparison",
        "title": "Compare Each Order to Previous and Next",
        "difficulty": "hard",
        "category": "Interview — LAG/LEAD",
        "dataset": "ecommerce",
        "description": (
            "For each customer's orders (ordered by date), show the current "
            "order's total_amount alongside the previous order's amount and the "
            "next order's amount. Also compute the change from the previous order. "
            "Return customer_id, order_date, total_amount, prev_amount, "
            "next_amount, and amount_change."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       order_date,\n"
            "       total_amount,\n"
            "       LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount,\n"
            "       LEAD(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_amount,\n"
            "       total_amount - LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS amount_change\n"
            "FROM orders\n"
            "ORDER BY customer_id, order_date;"
        ),
        "hints": [
            "LAG(column) accesses the previous row's value.",
            "LEAD(column) accesses the next row's value.",
            "Both need PARTITION BY customer_id and ORDER BY order_date.",
            "The first order has NULL for LAG, the last has NULL for LEAD.",
        ],
        "explanation": (
            "1. LAG(total_amount) gets the previous order's amount per customer.\n"
            "2. LEAD(total_amount) gets the next order's amount.\n"
            "3. Subtracting LAG from current gives the change.\n"
            "4. NULL appears for the first/last orders where no previous/next exists."
        ),
        "approach": [
            "Use LAG for previous row access.",
            "Use LEAD for next row access.",
            "Compute the difference for amount_change.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, which compares across different customers.",
            "Not handling the NULL case for the first/last orders.",
        ],
        "concept_tags": ["LAG", "LEAD", "window function", "PARTITION BY"],
    },
    {
        "id": "interview-ecom-029",
        "slug": "int-ecom-ntile-quartiles",
        "title": "Assign Customers to Spending Quartiles",
        "difficulty": "hard",
        "category": "Interview — NTILE",
        "dataset": "ecommerce",
        "description": (
            "Divide customers into four equal-sized spending tiers based on their "
            "total order spending. Return customer_id, total_spending, and "
            "spending_quartile (1 = lowest, 4 = highest). Sort by total_spending "
            "descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "SELECT customer_id,\n"
            "       total_spending,\n"
            "       NTILE(4) OVER (ORDER BY total_spending) AS spending_quartile\n"
            "FROM (\n"
            "    SELECT customer_id, SUM(total_amount) AS total_spending\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            ") customer_totals\n"
            "ORDER BY total_spending DESC;"
        ),
        "hints": [
            "NTILE(4) divides rows into 4 approximately equal groups.",
            "First aggregate spending per customer, then apply NTILE.",
            "ORDER BY total_spending inside NTILE defines the quartile order.",
        ],
        "explanation": (
            "1. The subquery calculates total spending per customer.\n"
            "2. NTILE(4) divides customers into 4 groups ordered by spending.\n"
            "3. Quartile 1 = lowest spenders, Quartile 4 = highest.\n"
            "4. The outer ORDER BY sorts the final output by spending."
        ),
        "approach": [
            "Aggregate spending per customer in a subquery.",
            "Apply NTILE(4) ordered by spending.",
            "Sort the output descending.",
        ],
        "common_mistakes": [
            "Applying NTILE to individual orders instead of per-customer totals.",
            "Misunderstanding NTILE ordering — ascending puts low spenders in quartile 1.",
        ],
        "concept_tags": ["NTILE", "window function", "quartiles", "derived table"],
    },
    {
        "id": "interview-ecom-030",
        "slug": "int-ecom-cte-multi-step-rfm",
        "title": "Multi-Step CTE: Customer Value Tiers",
        "difficulty": "hard",
        "category": "Interview — Complex CTE",
        "dataset": "ecommerce",
        "description": (
            "Build a customer value analysis using multiple CTEs. Step 1: Calculate "
            "each customer's total orders and total spending. Step 2: Compute the "
            "overall average orders and average spending. Step 3: Classify each "
            "customer as 'High Value' (above average in both metrics), 'Medium Value' "
            "(above average in one metric), or 'Low Value' (below average in both). "
            "Return customer_id, total_orders, total_spending, and value_tier."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH customer_stats AS (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS total_orders,\n"
            "           ROUND(SUM(total_amount), 2) AS total_spending\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "averages AS (\n"
            "    SELECT AVG(total_orders) AS avg_orders,\n"
            "           AVG(total_spending) AS avg_spending\n"
            "    FROM customer_stats\n"
            ")\n"
            "SELECT cs.customer_id,\n"
            "       cs.total_orders,\n"
            "       cs.total_spending,\n"
            "       CASE\n"
            "           WHEN cs.total_orders > a.avg_orders AND cs.total_spending > a.avg_spending THEN 'High Value'\n"
            "           WHEN cs.total_orders > a.avg_orders OR cs.total_spending > a.avg_spending THEN 'Medium Value'\n"
            "           ELSE 'Low Value'\n"
            "       END AS value_tier\n"
            "FROM customer_stats cs\n"
            "CROSS JOIN averages a\n"
            "ORDER BY cs.total_spending DESC;"
        ),
        "hints": [
            "Use multiple CTEs separated by commas.",
            "The first CTE aggregates per customer, the second computes averages.",
            "CROSS JOIN brings in the single-row averages for comparison.",
            "CASE with AND/OR classifies into three tiers.",
        ],
        "explanation": (
            "1. customer_stats CTE: computes orders and spending per customer.\n"
            "2. averages CTE: computes the average of those metrics.\n"
            "3. Main query: CROSS JOINs stats with averages (single row) and classifies.\n"
            "4. CASE logic: AND for High, OR for Medium, ELSE for Low."
        ),
        "approach": [
            "Break the problem into logical steps using CTEs.",
            "CTE 1: Per-customer aggregation.",
            "CTE 2: Compute averages from CTE 1.",
            "Main query: Classify with CASE.",
        ],
        "common_mistakes": [
            "Trying to compute averages from the original orders table instead of per-customer totals.",
            "Forgetting the CROSS JOIN for the averages row.",
            "Incorrect CASE logic — AND vs OR matters for the tier definitions.",
        ],
        "concept_tags": ["CTE", "CASE", "CROSS JOIN", "multi-step analysis"],
    },
    {
        "id": "interview-ecom-031",
        "slug": "int-ecom-gap-analysis-order-dates",
        "title": "Order Date Gap Analysis",
        "difficulty": "hard",
        "category": "Interview — Gap Analysis",
        "dataset": "ecommerce",
        "description": (
            "Find gaps in daily order activity. Identify dates where no orders "
            "were placed but the previous and next dates had orders. Use a CTE to "
            "generate the range of dates, then find missing ones. Return the gap "
            "date, the last date with an order before the gap, and the first date "
            "with an order after the gap."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH order_dates AS (\n"
            "    SELECT DISTINCT DATE(order_date) AS order_day\n"
            "    FROM orders\n"
            "),\n"
            "date_with_next AS (\n"
            "    SELECT order_day,\n"
            "           LEAD(order_day) OVER (ORDER BY order_day) AS next_order_day\n"
            "    FROM order_dates\n"
            ")\n"
            "SELECT order_day AS last_order_before_gap,\n"
            "       next_order_day AS first_order_after_gap,\n"
            "       CAST(julianday(next_order_day) - julianday(order_day) AS INTEGER) AS gap_days\n"
            "FROM date_with_next\n"
            "WHERE julianday(next_order_day) - julianday(order_day) > 1\n"
            "ORDER BY order_day;"
        ),
        "hints": [
            "First get distinct order dates.",
            "Use LEAD to pair each date with the next order date.",
            "A gap exists when the next date is more than 1 day away.",
            "julianday difference gives the gap size.",
        ],
        "explanation": (
            "1. order_dates CTE: gets distinct dates with orders.\n"
            "2. date_with_next CTE: pairs each date with the next using LEAD.\n"
            "3. Main query: filters for pairs more than 1 day apart.\n"
            "4. The gap_days column shows how many days were missed."
        ),
        "approach": [
            "Extract distinct order dates.",
            "Use LEAD to find the next order date.",
            "Filter where the gap is more than 1 day.",
            "Compute gap size with julianday arithmetic.",
        ],
        "common_mistakes": [
            "Not using DISTINCT on order dates, causing false gaps from missing times.",
            "Forgetting to handle the last date (LEAD returns NULL).",
        ],
        "concept_tags": ["LEAD", "CTE", "gap analysis", "julianday", "date arithmetic"],
    },
    {
        "id": "interview-ecom-032",
        "slug": "int-ecom-cohort-monthly-retention",
        "title": "Monthly Cohort Retention Rate",
        "difficulty": "hard",
        "category": "Interview — Cohort Analysis",
        "dataset": "ecommerce",
        "description": (
            "Calculate monthly retention rates for customer cohorts. A cohort is "
            "defined by the month of a customer's first order. For each cohort, "
            "determine what percentage of customers placed an order in subsequent "
            "months (month 0, 1, 2, etc.). Return cohort_month, months_since_first, "
            "active_customers, and retention_pct."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH first_orders AS (\n"
            "    SELECT customer_id,\n"
            "           strftime('%Y-%m', MIN(order_date)) AS cohort_month\n"
            "    FROM orders\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "cohort_size AS (\n"
            "    SELECT cohort_month, COUNT(*) AS total_customers\n"
            "    FROM first_orders\n"
            "    GROUP BY cohort_month\n"
            "),\n"
            "monthly_activity AS (\n"
            "    SELECT fo.cohort_month,\n"
            "           CAST(\n"
            "               (julianday(strftime('%Y-%m', o.order_date) || '-01') -\n"
            "                julianday(fo.cohort_month || '-01')) / 30\n"
            "           AS INTEGER) AS months_since_first,\n"
            "           COUNT(DISTINCT o.customer_id) AS active_customers\n"
            "    FROM orders o\n"
            "    JOIN first_orders fo ON o.customer_id = fo.customer_id\n"
            "    GROUP BY fo.cohort_month, months_since_first\n"
            ")\n"
            "SELECT ma.cohort_month,\n"
            "       ma.months_since_first,\n"
            "       ma.active_customers,\n"
            "       ROUND(ma.active_customers * 100.0 / cs.total_customers, 1) AS retention_pct\n"
            "FROM monthly_activity ma\n"
            "JOIN cohort_size cs ON ma.cohort_month = cs.cohort_month\n"
            "ORDER BY ma.cohort_month, ma.months_since_first;"
        ),
        "hints": [
            "First identify each customer's cohort (month of first order).",
            "Then count how many cohort members are active in each subsequent month.",
            "Divide active count by cohort size for retention rate.",
            "Use multiple CTEs to break this into manageable steps.",
        ],
        "explanation": (
            "1. first_orders CTE: finds each customer's first order month.\n"
            "2. cohort_size CTE: counts customers per cohort.\n"
            "3. monthly_activity CTE: counts distinct active customers per cohort per month.\n"
            "4. Main query: computes retention_pct as active/total * 100."
        ),
        "approach": [
            "CTE 1: Determine each customer's cohort month.",
            "CTE 2: Count cohort sizes.",
            "CTE 3: Count active customers per cohort-month pair.",
            "Main query: Compute retention percentage.",
        ],
        "common_mistakes": [
            "Not using COUNT(DISTINCT customer_id) which could double-count customers with multiple orders in a month.",
            "Incorrect month difference calculation.",
            "Forgetting to handle cohort_size join.",
        ],
        "concept_tags": ["CTE", "cohort analysis", "retention", "COUNT DISTINCT", "date arithmetic"],
    },
    {
        "id": "interview-ecom-033",
        "slug": "int-ecom-session-order-streaks",
        "title": "Customer Consecutive Order Month Streaks",
        "difficulty": "hard",
        "category": "Interview — Session/Streak Analysis",
        "dataset": "ecommerce",
        "description": (
            "Find the longest streak of consecutive months in which each customer "
            "placed at least one order. A streak breaks when a customer has no "
            "orders in a month. Return customer_id and their longest_streak (in "
            "months). Sort by longest_streak descending."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH monthly_orders AS (\n"
            "    SELECT DISTINCT customer_id,\n"
            "           strftime('%Y-%m', order_date) AS order_month\n"
            "    FROM orders\n"
            "),\n"
            "numbered AS (\n"
            "    SELECT customer_id,\n"
            "           order_month,\n"
            "           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_month) AS rn\n"
            "    FROM monthly_orders\n"
            "),\n"
            "streaks AS (\n"
            "    SELECT customer_id,\n"
            "           order_month,\n"
            "           DATE(order_month || '-01', '-' || rn || ' months') AS streak_group\n"
            "    FROM numbered\n"
            ")\n"
            "SELECT customer_id,\n"
            "       MAX(streak_length) AS longest_streak\n"
            "FROM (\n"
            "    SELECT customer_id,\n"
            "           streak_group,\n"
            "           COUNT(*) AS streak_length\n"
            "    FROM streaks\n"
            "    GROUP BY customer_id, streak_group\n"
            ")\n"
            "GROUP BY customer_id\n"
            "ORDER BY longest_streak DESC;"
        ),
        "hints": [
            "First get distinct months per customer.",
            "Use ROW_NUMBER to number each month sequentially.",
            "Subtracting the row number from the month creates a constant for consecutive months.",
            "Group by that constant to identify streaks.",
        ],
        "explanation": (
            "1. monthly_orders: gets distinct months per customer.\n"
            "2. numbered: assigns sequential ROW_NUMBER per customer.\n"
            "3. streaks: subtracts rn months from each month — consecutive months produce the same value.\n"
            "4. Group by streak_group and count to get streak lengths.\n"
            "5. MAX per customer gives the longest streak."
        ),
        "approach": [
            "Deduplicate to distinct customer-month pairs.",
            "Number them sequentially with ROW_NUMBER.",
            "Use the row-number subtraction trick to identify consecutive groups.",
            "Count per group and take the max.",
        ],
        "common_mistakes": [
            "Not deduplicating months first (a customer with 3 orders in one month is still one month).",
            "Incorrect date subtraction for the streak grouping constant.",
        ],
        "concept_tags": ["ROW_NUMBER", "CTE", "streak analysis", "gaps and islands"],
    },
    {
        "id": "interview-ecom-034",
        "slug": "int-ecom-complex-business-logic-refund-analysis",
        "title": "Refund Rate and Revenue Impact Analysis",
        "difficulty": "hard",
        "category": "Interview — Complex Business Logic",
        "dataset": "ecommerce",
        "description": (
            "Analyze the refund impact on each product category. For each category, "
            "calculate: total orders, refunded orders (payment status = 'refunded'), "
            "refund rate (as percentage), gross revenue (all orders), refunded revenue, "
            "and net revenue. Sort by refund_rate descending."
        ),
        "schema_hint": ["order_items", "products", "categories", "orders", "payments"],
        "solution_query": (
            "WITH order_category AS (\n"
            "    SELECT DISTINCT oi.order_id,\n"
            "           c.name AS category_name,\n"
            "           SUM(oi.quantity * oi.unit_price) AS order_category_revenue\n"
            "    FROM order_items oi\n"
            "    JOIN products p ON oi.product_id = p.id\n"
            "    JOIN categories c ON p.category_id = c.id\n"
            "    GROUP BY oi.order_id, c.name\n"
            "),\n"
            "order_payment_status AS (\n"
            "    SELECT oc.order_id,\n"
            "           oc.category_name,\n"
            "           oc.order_category_revenue,\n"
            "           CASE WHEN pay.status = 'refunded' THEN 1 ELSE 0 END AS is_refunded\n"
            "    FROM order_category oc\n"
            "    JOIN payments pay ON oc.order_id = pay.order_id\n"
            ")\n"
            "SELECT category_name,\n"
            "       COUNT(*) AS total_orders,\n"
            "       SUM(is_refunded) AS refunded_orders,\n"
            "       ROUND(SUM(is_refunded) * 100.0 / COUNT(*), 1) AS refund_rate,\n"
            "       ROUND(SUM(order_category_revenue), 2) AS gross_revenue,\n"
            "       ROUND(SUM(CASE WHEN is_refunded = 1 THEN order_category_revenue ELSE 0 END), 2) AS refunded_revenue,\n"
            "       ROUND(SUM(order_category_revenue) - SUM(CASE WHEN is_refunded = 1 THEN order_category_revenue ELSE 0 END), 2) AS net_revenue\n"
            "FROM order_payment_status\n"
            "GROUP BY category_name\n"
            "ORDER BY refund_rate DESC;"
        ),
        "hints": [
            "Use CTEs to break this into steps: map orders to categories, then to payment status.",
            "A refunded order has payment status = 'refunded'.",
            "Refund rate = refunded orders / total orders * 100.",
            "Net revenue = gross revenue - refunded revenue.",
        ],
        "explanation": (
            "1. order_category CTE: computes revenue per order per category.\n"
            "2. order_payment_status CTE: flags each order as refunded or not.\n"
            "3. Main query: aggregates per category with conditional sums.\n"
            "4. Refund rate and net revenue are computed from the aggregated values."
        ),
        "approach": [
            "CTE 1: Link orders to categories with per-category revenue.",
            "CTE 2: Join to payments and flag refunded orders.",
            "Main query: Aggregate and compute all metrics.",
        ],
        "common_mistakes": [
            "Not grouping by category in the order_category CTE, misallocating revenue.",
            "Mixing up payment status with order status.",
            "Integer division in refund rate calculation.",
        ],
        "concept_tags": ["CTE", "CASE", "conditional aggregation", "business logic", "multi-table JOIN"],
    },
    {
        "id": "interview-ecom-035",
        "slug": "int-ecom-recursive-cte-category-hierarchy",
        "title": "Recursive CTE: Order Value Tiers with Running Stats",
        "difficulty": "hard",
        "category": "Interview — Recursive CTE",
        "dataset": "ecommerce",
        "description": (
            "Use a recursive CTE to generate order value ranges (buckets) from 0 "
            "to 1000 in steps of 100 (0-99, 100-199, ..., 900-999, 1000+). For each "
            "bucket, count the number of orders and calculate the total revenue. "
            "Return bucket_start, bucket_end, order_count, and total_revenue."
        ),
        "schema_hint": ["orders"],
        "solution_query": (
            "WITH RECURSIVE buckets AS (\n"
            "    SELECT 0 AS bucket_start\n"
            "    UNION ALL\n"
            "    SELECT bucket_start + 100\n"
            "    FROM buckets\n"
            "    WHERE bucket_start < 1000\n"
            "),\n"
            "bucket_ranges AS (\n"
            "    SELECT bucket_start,\n"
            "           CASE WHEN bucket_start = 1000 THEN 999999\n"
            "                ELSE bucket_start + 99\n"
            "           END AS bucket_end\n"
            "    FROM buckets\n"
            ")\n"
            "SELECT br.bucket_start,\n"
            "       br.bucket_end,\n"
            "       COUNT(o.id) AS order_count,\n"
            "       COALESCE(ROUND(SUM(o.total_amount), 2), 0) AS total_revenue\n"
            "FROM bucket_ranges br\n"
            "LEFT JOIN orders o ON o.total_amount >= br.bucket_start\n"
            "                   AND o.total_amount <= br.bucket_end\n"
            "GROUP BY br.bucket_start, br.bucket_end\n"
            "ORDER BY br.bucket_start;"
        ),
        "hints": [
            "A recursive CTE has a base case (SELECT 0) and a recursive step (+ 100).",
            "The recursion terminates when bucket_start reaches 1000.",
            "LEFT JOIN orders to buckets so empty buckets still appear.",
            "The last bucket (1000+) needs special handling for the upper bound.",
        ],
        "explanation": (
            "1. Recursive CTE generates bucket_start values: 0, 100, 200, ..., 1000.\n"
            "2. bucket_ranges adds the end value (start + 99, or 999999 for the last bucket).\n"
            "3. LEFT JOIN matches orders to their respective buckets.\n"
            "4. GROUP BY bucket produces counts and revenue per bucket.\n"
            "5. COALESCE handles empty buckets (no orders)."
        ),
        "approach": [
            "Use a recursive CTE to generate bucket boundaries.",
            "Add a second CTE for bucket end values.",
            "LEFT JOIN orders to buckets on range matching.",
            "Aggregate per bucket.",
        ],
        "common_mistakes": [
            "Forgetting the termination condition, causing infinite recursion.",
            "Using INNER JOIN which drops empty buckets.",
            "Off-by-one errors in bucket boundaries.",
        ],
        "concept_tags": ["recursive CTE", "LEFT JOIN", "COALESCE", "bucketing", "histogram"],
    },
]