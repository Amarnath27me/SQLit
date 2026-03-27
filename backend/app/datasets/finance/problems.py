"""
Finance dataset practice problems.

40 progressive SQL problems covering fundamentals through advanced topics,
designed around a realistic banking/finance database schema.

Tables:
  - customers (id, first_name, last_name, email, phone, date_of_birth, city, state, country, created_at)
  - accounts (id, customer_id, account_type, balance, currency, opened_at, status)
  - transactions (id, account_id, transaction_date, type, amount, balance_after, description, reference_number)
  - cards (id, account_id, card_number, card_type, expiry_date, status, credit_limit, issued_at)
  - loans (id, customer_id, loan_type, principal, interest_rate, term_months, start_date, status)
  - payments (id, loan_id, payment_date, amount, principal_paid, interest_paid, remaining_balance)
  - branches (id, name, city, state, manager_name, opened_at)
"""

PROBLEMS: list[dict] = [
    # =========================================================================
    # LEVEL 1 — FUNDAMENTALS (8 problems: fi-001 through fi-008)
    # =========================================================================
    {
        "id": "fi-001",
        "slug": "list-all-branches",
        "title": "List All Branches",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The operations team needs an overview of the bank's branch network. "
            "Write a query that returns the name and city of every branch, "
            "sorted alphabetically by branch name."
        ),
        "schema_hint": ["branches"],
        "solution_query": (
            "SELECT name, city\n"
            "FROM branches\n"
            "ORDER BY name;"
        ),
        "hints": [
            "You only need to query a single table for this one.",
            "Think about which columns the question asks you to return.",
            "Use ORDER BY to control the sort direction.",
            "SELECT name, city FROM branches ORDER BY ...;",
        ],
        "explanation": (
            "1. SELECT the name and city columns from the branches table.\n"
            "2. ORDER BY name sorts the results alphabetically (ascending is the default)."
        ),
        "approach": [
            "Identify the table that stores branch information.",
            "Pick only the columns requested: name and city.",
            "Apply an ORDER BY on the name column for alphabetical sorting.",
        ],
        "common_mistakes": [
            "Selecting all columns with SELECT * instead of only name and city.",
            "Forgetting the ORDER BY clause, which means results come back in an undefined order.",
        ],
        "concept_tags": ["SELECT", "ORDER BY"],
    },
    {
        "id": "fi-002",
        "slug": "customers-in-california",
        "title": "Customers in California",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "The compliance team needs to audit all customers located in California. "
            "Retrieve the first name, last name, and email of every customer "
            "whose state is 'CA'."
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
            "Return only the columns the compliance team needs.",
        ],
        "common_mistakes": [
            "Using LIKE '%CA%' which could match unintended values.",
            "Forgetting that string comparisons in SQL are case-sensitive in some configurations.",
        ],
        "concept_tags": ["SELECT", "WHERE", "string comparison"],
    },
    {
        "id": "fi-003",
        "slug": "high-balance-active-accounts",
        "title": "High-Balance Active Accounts",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "The wealth management team wants to identify high-value clients. "
            "Find all accounts with a balance greater than 50000 that have a status "
            "of 'active'. Return the account id, account_type, and balance."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, account_type, balance\n"
            "FROM accounts\n"
            "WHERE balance > 50000\n"
            "  AND status = 'active';"
        ),
        "hints": [
            "You need two conditions in your WHERE clause.",
            "Combine conditions with AND so both must be true.",
            "One condition is numeric (> 50000), the other is a string match.",
            "WHERE balance > 50000 AND status = 'active'",
        ],
        "explanation": (
            "1. SELECT id, account_type, and balance from accounts.\n"
            "2. WHERE balance > 50000 keeps only high-value accounts.\n"
            "3. AND status = 'active' further narrows to active ones."
        ),
        "approach": [
            "Identify that the accounts table has both balance and status.",
            "Combine a numeric comparison with a string equality check using AND.",
            "Return only the requested columns.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, which returns accounts matching either condition rather than both.",
            "Putting quotes around 50000, treating it as a string instead of a number.",
            "Forgetting that status values are case-sensitive strings.",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "comparison operators"],
    },
    {
        "id": "fi-004",
        "slug": "accounts-by-type",
        "title": "Accounts by Type",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "The product team wants to see all checking and savings accounts. "
            "Return the id, customer_id, account_type, and balance for accounts "
            "whose type is either 'checking' or 'savings', ordered by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, account_type, balance\n"
            "FROM accounts\n"
            "WHERE account_type IN ('checking', 'savings')\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "You are filtering on a column that can match one of several values.",
            "The IN operator checks membership in a list.",
            "IN is cleaner than chaining multiple OR conditions.",
            "WHERE account_type IN ('checking', 'savings')",
        ],
        "explanation": (
            "1. SELECT the requested columns from accounts.\n"
            "2. WHERE account_type IN ('checking', 'savings') matches either value.\n"
            "3. ORDER BY balance DESC returns highest balances first."
        ),
        "approach": [
            "Use the IN operator to match against a set of values.",
            "Sort by balance in descending order.",
        ],
        "common_mistakes": [
            "Writing account_type = 'checking' OR 'savings', which is not valid SQL.",
            "Forgetting quotes around the string values inside IN.",
        ],
        "concept_tags": ["SELECT", "WHERE", "IN", "ORDER BY"],
    },
    {
        "id": "fi-005",
        "slug": "search-transactions-by-description",
        "title": "Search Transactions by Description",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "An auditor needs to find all transactions whose description contains "
            "the word 'ATM'. Return the transaction id, transaction_date, type, "
            "amount, and description for all matching transactions."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT id, transaction_date, type, amount, description\n"
            "FROM transactions\n"
            "WHERE description LIKE '%ATM%';"
        ),
        "hints": [
            "You need a pattern-matching operator, not exact equality.",
            "LIKE is the SQL operator for pattern matching.",
            "The % wildcard matches zero or more characters.",
            "Place % on both sides of 'ATM' to match anywhere in the string.",
        ],
        "explanation": (
            "1. SELECT the requested columns from transactions.\n"
            "2. WHERE description LIKE '%ATM%' matches any transaction whose "
            "description contains the substring 'ATM' anywhere."
        ),
        "approach": [
            "Use LIKE with wildcard characters to do a substring search.",
            "Place % before and after the search term.",
        ],
        "common_mistakes": [
            "Using = instead of LIKE, which only matches exact values.",
            "Forgetting the wildcard on one side, e.g., LIKE 'ATM%' only matches descriptions starting with 'ATM'.",
        ],
        "concept_tags": ["SELECT", "WHERE", "LIKE", "wildcards"],
    },
    {
        "id": "fi-006",
        "slug": "recent-transactions-top-ten",
        "title": "Ten Most Recent Transactions",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The fraud monitoring dashboard needs to show the ten most recent "
            "transactions. Return the id, account_id, transaction_date, type, "
            "and amount, sorted with the newest transactions first."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT id, account_id, transaction_date, type, amount\n"
            "FROM transactions\n"
            "ORDER BY transaction_date DESC\n"
            "LIMIT 10;"
        ),
        "hints": [
            "You need to control both sorting direction and result count.",
            "ORDER BY with DESC gives newest-first sorting.",
            "LIMIT restricts how many rows are returned.",
            "Combine ORDER BY transaction_date DESC with LIMIT 10.",
        ],
        "explanation": (
            "1. SELECT the requested columns from transactions.\n"
            "2. ORDER BY transaction_date DESC sorts newest first.\n"
            "3. LIMIT 10 returns only the top ten rows."
        ),
        "approach": [
            "Sort transactions by date in descending order.",
            "Use LIMIT to cap the result set at 10 rows.",
        ],
        "common_mistakes": [
            "Forgetting DESC, which returns the oldest transactions instead.",
            "Placing LIMIT before ORDER BY, which is a syntax error.",
        ],
        "concept_tags": ["SELECT", "ORDER BY", "DESC", "LIMIT"],
    },
    {
        "id": "fi-007",
        "slug": "unique-customer-cities",
        "title": "Unique Customer Cities",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The expansion planning team wants to know which cities the bank's "
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
        "id": "fi-008",
        "slug": "customers-without-phone",
        "title": "Customers Without a Phone Number",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "The customer outreach team needs to identify customers with missing "
            "phone numbers so they can request updates. Return the id, first_name, "
            "last_name, and email for all customers where phone is NULL."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT id, first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE phone IS NULL;"
        ),
        "hints": [
            "NULL values cannot be found with = or !=.",
            "SQL has a special operator for checking NULL values.",
            "IS NULL checks whether a value is missing.",
            "WHERE phone IS NULL",
        ],
        "explanation": (
            "1. SELECT the requested columns from customers.\n"
            "2. WHERE phone IS NULL filters for rows where the phone is missing.\n"
            "3. You must use IS NULL, not = NULL, because NULL is not equal to anything."
        ),
        "approach": [
            "Use IS NULL to filter for missing phone numbers.",
            "Return only the columns needed by the outreach team.",
        ],
        "common_mistakes": [
            "Using WHERE phone = NULL, which never matches because NULL is not equal to itself.",
            "Using WHERE phone = '' which checks for empty strings, not NULL.",
        ],
        "concept_tags": ["SELECT", "WHERE", "IS NULL", "NULL handling"],
    },

    # =========================================================================
    # LEVEL 2 — AGGREGATIONS (8 problems: fi-009 through fi-016)
    # =========================================================================
    {
        "id": "fi-009",
        "slug": "total-number-of-accounts",
        "title": "Total Number of Accounts",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "Management wants a quick KPI check. Write a query that returns "
            "the total number of accounts in the system."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT COUNT(*) AS total_accounts\n"
            "FROM accounts;"
        ),
        "hints": [
            "You need an aggregate function that counts rows.",
            "COUNT(*) counts all rows regardless of NULL values.",
            "Use an alias to give the result a meaningful column name.",
            "SELECT COUNT(*) AS total_accounts FROM accounts;",
        ],
        "explanation": (
            "1. COUNT(*) counts every row in the accounts table.\n"
            "2. AS total_accounts gives the output column a readable name."
        ),
        "approach": [
            "Use the COUNT aggregate function on the accounts table.",
            "Alias the result for clarity.",
        ],
        "common_mistakes": [
            "Using COUNT(id) instead of COUNT(*) — both work here, but COUNT(*) is more conventional for total row counts.",
            "Forgetting the alias, which returns a column named 'count' that may confuse consumers.",
        ],
        "concept_tags": ["COUNT", "aggregate functions", "alias"],
    },
    {
        "id": "fi-010",
        "slug": "total-balance-by-account-type",
        "title": "Total Balance by Account Type",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The finance team wants to see total deposits broken down by account "
            "type. Calculate the sum of balance for each account_type. Return the "
            "account_type and total_balance, sorted by total_balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT account_type, SUM(balance) AS total_balance\n"
            "FROM accounts\n"
            "GROUP BY account_type\n"
            "ORDER BY total_balance DESC;"
        ),
        "hints": [
            "SUM adds up all values in a numeric column.",
            "GROUP BY creates one group per account_type.",
            "Use ORDER BY on the aggregate result to sort.",
            "SUM(balance) gives total balance per group.",
        ],
        "explanation": (
            "1. GROUP BY account_type creates one group per type.\n"
            "2. SUM(balance) totals the balance within each group.\n"
            "3. ORDER BY total_balance DESC shows the highest totals first."
        ),
        "approach": [
            "Group the accounts table by account_type.",
            "Aggregate with SUM on the balance column.",
            "Sort descending to highlight top account types.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY, which causes an aggregation error.",
            "Not aliasing the SUM column, making results harder to read.",
        ],
        "concept_tags": ["SUM", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "fi-011",
        "slug": "average-loan-principal",
        "title": "Average Loan Principal",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The risk team monitors average loan sizes. Calculate the average "
            "principal across all loans, rounded to two decimal places."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT ROUND(AVG(principal), 2) AS avg_principal\n"
            "FROM loans;"
        ),
        "hints": [
            "There is an aggregate function specifically for averages.",
            "AVG computes the mean of a numeric column.",
            "Use ROUND to limit decimal places.",
            "ROUND(AVG(principal), 2) rounds to two decimals.",
        ],
        "explanation": (
            "1. AVG(principal) computes the arithmetic mean of all loan principals.\n"
            "2. ROUND(..., 2) limits the result to two decimal places."
        ),
        "approach": [
            "Apply AVG to the principal column.",
            "Wrap in ROUND for a clean two-decimal result.",
        ],
        "common_mistakes": [
            "Forgetting ROUND, which may return many decimal places.",
            "Using SUM/COUNT manually instead of the built-in AVG function.",
        ],
        "concept_tags": ["AVG", "ROUND", "aggregate functions"],
    },
    {
        "id": "fi-012",
        "slug": "transactions-per-account",
        "title": "Transactions Per Account",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The analytics team wants to measure account activity. For each "
            "account, count the number of transactions. Return account_id and "
            "tx_count, sorted by tx_count descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id, COUNT(*) AS tx_count\n"
            "FROM transactions\n"
            "GROUP BY account_id\n"
            "ORDER BY tx_count DESC;"
        ),
        "hints": [
            "You need to count rows per group, not overall.",
            "GROUP BY creates one group per account_id.",
            "COUNT(*) within a GROUP BY counts rows in each group.",
            "Sort by the count descending to see the most active accounts first.",
        ],
        "explanation": (
            "1. GROUP BY account_id creates one group per account.\n"
            "2. COUNT(*) counts the transactions within each group.\n"
            "3. ORDER BY tx_count DESC puts the most active accounts first."
        ),
        "approach": [
            "Group the transactions table by account_id.",
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
        "id": "fi-013",
        "slug": "min-max-loan-interest-rate",
        "title": "Minimum and Maximum Loan Interest Rates",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The product pricing analyst needs a quick snapshot of the interest "
            "rate range. Write a single query that returns the minimum interest_rate, "
            "maximum interest_rate, and the difference between them (as rate_spread)."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT MIN(interest_rate) AS min_rate,\n"
            "       MAX(interest_rate) AS max_rate,\n"
            "       MAX(interest_rate) - MIN(interest_rate) AS rate_spread\n"
            "FROM loans;"
        ),
        "hints": [
            "MIN and MAX are aggregate functions that find extremes.",
            "You can use arithmetic on aggregate results in the SELECT list.",
            "No GROUP BY is needed when aggregating the entire table.",
            "MAX(interest_rate) - MIN(interest_rate) gives the spread.",
        ],
        "explanation": (
            "1. MIN(interest_rate) finds the lowest rate.\n"
            "2. MAX(interest_rate) finds the highest.\n"
            "3. Subtracting them gives the rate spread.\n"
            "4. No GROUP BY is needed because we aggregate across all loans."
        ),
        "approach": [
            "Use MIN and MAX on the interest_rate column.",
            "Subtract to compute the spread in the same query.",
        ],
        "common_mistakes": [
            "Writing two separate queries instead of combining MIN and MAX in one SELECT.",
            "Adding an unnecessary GROUP BY, which would change the result.",
        ],
        "concept_tags": ["MIN", "MAX", "aggregate functions", "arithmetic"],
    },
    {
        "id": "fi-014",
        "slug": "account-types-with-many-accounts",
        "title": "Account Types with Many Accounts",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The product team wants to find account types that have more than "
            "100 accounts. Return the account_type and account_count for each "
            "qualifying type, sorted by account_count descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT account_type, COUNT(*) AS account_count\n"
            "FROM accounts\n"
            "GROUP BY account_type\n"
            "HAVING COUNT(*) > 100\n"
            "ORDER BY account_count DESC;"
        ),
        "hints": [
            "First group and count, then filter the groups.",
            "WHERE filters rows before grouping; HAVING filters after.",
            "HAVING is the clause that filters on aggregate results.",
            "HAVING COUNT(*) > 100 keeps only groups exceeding the threshold.",
        ],
        "explanation": (
            "1. GROUP BY account_type groups rows by type.\n"
            "2. COUNT(*) counts accounts per type.\n"
            "3. HAVING COUNT(*) > 100 filters out types with 100 or fewer.\n"
            "4. ORDER BY account_count DESC shows the largest types first."
        ),
        "approach": [
            "Group by account_type and count rows per group.",
            "Use HAVING to filter groups by their aggregate count.",
            "Sort the surviving groups by count descending.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING to filter on the count, which causes a syntax error.",
            "Referencing the alias account_count in the HAVING clause, which some databases do not support.",
        ],
        "concept_tags": ["COUNT", "GROUP BY", "HAVING", "ORDER BY"],
    },
    {
        "id": "fi-015",
        "slug": "monthly-transaction-volume",
        "title": "Monthly Transaction Volume",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The reporting team needs monthly transaction statistics. For each "
            "month (formatted as YYYY-MM), return the number of transactions and "
            "the total transaction amount. Sort by month ascending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT SUBSTR(transaction_date, 1, 7) AS month,\n"
            "       COUNT(*) AS tx_count,\n"
            "       ROUND(SUM(amount), 2) AS total_amount\n"
            "FROM transactions\n"
            "GROUP BY SUBSTR(transaction_date, 1, 7)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "The transaction_date is stored as text in YYYY-MM-DD format.",
            "You can extract the year-month portion using SUBSTR or strftime.",
            "SUBSTR(transaction_date, 1, 7) extracts the first 7 characters.",
            "Group by the extracted month to aggregate per month.",
        ],
        "explanation": (
            "1. SUBSTR(transaction_date, 1, 7) extracts the YYYY-MM portion.\n"
            "2. GROUP BY this expression creates one group per month.\n"
            "3. COUNT(*) and SUM(amount) aggregate within each month.\n"
            "4. ORDER BY month sorts chronologically."
        ),
        "approach": [
            "Extract the year-month from the date string.",
            "Group by the extracted value.",
            "Apply COUNT and SUM aggregates.",
            "Sort by month ascending.",
        ],
        "common_mistakes": [
            "Forgetting to group by the same expression used in SELECT.",
            "Using strftime without realizing the date is stored as text.",
        ],
        "concept_tags": ["SUBSTR", "GROUP BY", "COUNT", "SUM", "date manipulation"],
    },
    {
        "id": "fi-016",
        "slug": "average-balance-by-status",
        "title": "Average Account Balance by Status",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "Management wants to compare average account balances across account "
            "statuses (active, closed, frozen). Return the status, the count of "
            "accounts, and the average balance rounded to two decimal places. "
            "Sort by average balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT status,\n"
            "       COUNT(*) AS account_count,\n"
            "       ROUND(AVG(balance), 2) AS avg_balance\n"
            "FROM accounts\n"
            "GROUP BY status\n"
            "ORDER BY avg_balance DESC;"
        ),
        "hints": [
            "You need to group by status and compute two aggregates.",
            "COUNT(*) gives the number of accounts per status.",
            "AVG(balance) gives the average balance per status.",
            "ROUND the average to 2 decimal places for readability.",
        ],
        "explanation": (
            "1. GROUP BY status creates one group per account status.\n"
            "2. COUNT(*) counts accounts in each group.\n"
            "3. AVG(balance) computes the mean balance per group.\n"
            "4. ROUND(..., 2) formats the average to two decimal places."
        ),
        "approach": [
            "Group accounts by their status.",
            "Apply COUNT and AVG aggregates.",
            "Round the average and sort descending.",
        ],
        "common_mistakes": [
            "Forgetting ROUND, resulting in many decimal places.",
            "Not including both COUNT and AVG as requested.",
        ],
        "concept_tags": ["AVG", "COUNT", "GROUP BY", "ROUND", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 3 — JOINS (8 problems: fi-017 through fi-024)
    # =========================================================================
    {
        "id": "fi-017",
        "slug": "customer-account-list",
        "title": "Customer Account List",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The relationship management team needs a combined view of customers "
            "and their accounts. Return the customer's first_name, last_name, "
            "account_type, and balance for every account. Sort by last_name, "
            "then first_name."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, a.account_type, a.balance\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "ORDER BY c.last_name, c.first_name;"
        ),
        "hints": [
            "You need data from two tables: customers and accounts.",
            "JOIN connects tables using a shared key.",
            "The foreign key is accounts.customer_id referencing customers.id.",
            "Use table aliases (c, a) to keep the query concise.",
        ],
        "explanation": (
            "1. JOIN customers and accounts on the customer_id foreign key.\n"
            "2. SELECT the requested columns from both tables.\n"
            "3. ORDER BY last_name, first_name sorts alphabetically."
        ),
        "approach": [
            "Identify the foreign key relationship between customers and accounts.",
            "Use an INNER JOIN to combine matching rows.",
            "Select only the requested columns.",
            "Sort by last name then first name.",
        ],
        "common_mistakes": [
            "Forgetting the ON clause, which produces a cross join.",
            "Not using table aliases, making the query harder to read with ambiguous column names.",
        ],
        "concept_tags": ["JOIN", "INNER JOIN", "foreign key", "ORDER BY"],
    },
    {
        "id": "fi-018",
        "slug": "customers-with-no-accounts",
        "title": "Customers with No Accounts",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The sales team wants to reach out to registered customers who have "
            "not yet opened any account. Return the first_name, last_name, and "
            "email of customers who have zero accounts."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, c.email\n"
            "FROM customers c\n"
            "LEFT JOIN accounts a ON c.id = a.customer_id\n"
            "WHERE a.id IS NULL;"
        ),
        "hints": [
            "An INNER JOIN would exclude customers with no accounts.",
            "LEFT JOIN keeps all customers even without matching accounts.",
            "When there is no match, the joined columns are NULL.",
            "Filter for NULL on the accounts side to find unmatched customers.",
        ],
        "explanation": (
            "1. LEFT JOIN keeps all customers, filling account columns with NULL when there is no match.\n"
            "2. WHERE a.id IS NULL filters to only those customers with no accounts."
        ),
        "approach": [
            "Use LEFT JOIN to include all customers.",
            "Filter where the account id is NULL to find those without accounts.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which excludes the customers we want to find.",
            "Checking for NULL on the wrong column.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join pattern"],
    },
    {
        "id": "fi-019",
        "slug": "transaction-details-with-customer",
        "title": "Transaction Details with Customer Info",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The compliance team needs a report linking transactions to customers. "
            "For each transaction, return the customer's first_name, last_name, "
            "the account_type, transaction_date, type, and amount. Show only "
            "transactions from 2024. Sort by transaction_date descending."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, a.account_type,\n"
            "       t.transaction_date, t.type, t.amount\n"
            "FROM transactions t\n"
            "JOIN accounts a ON t.account_id = a.id\n"
            "JOIN customers c ON a.customer_id = c.id\n"
            "WHERE t.transaction_date >= '2024-01-01'\n"
            "  AND t.transaction_date < '2025-01-01'\n"
            "ORDER BY t.transaction_date DESC;"
        ),
        "hints": [
            "You need to chain two JOINs: transactions -> accounts -> customers.",
            "Filter dates using comparison operators on the text date.",
            "Use >= start and < end for a clean date range.",
            "Sort by transaction_date descending for most recent first.",
        ],
        "explanation": (
            "1. JOIN transactions to accounts on account_id.\n"
            "2. JOIN accounts to customers on customer_id.\n"
            "3. WHERE filters to the year 2024 using date range comparisons.\n"
            "4. ORDER BY transaction_date DESC shows newest first."
        ),
        "approach": [
            "Chain JOINs from transactions through accounts to customers.",
            "Apply a date range filter for 2024.",
            "Select only the requested columns and sort.",
        ],
        "common_mistakes": [
            "Forgetting one of the two JOINs needed to reach customer data.",
            "Using LIKE '2024%' which works but is less efficient than range comparison.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "WHERE", "date filtering", "ORDER BY"],
    },
    {
        "id": "fi-020",
        "slug": "cards-with-account-info",
        "title": "Cards with Account Information",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card services team needs a list of all active cards along with "
            "the associated account type and current balance. Return card_number, "
            "card_type, account_type, and balance. Only include cards with status "
            "'active'."
        ),
        "schema_hint": ["cards", "accounts"],
        "solution_query": (
            "SELECT cd.card_number, cd.card_type, a.account_type, a.balance\n"
            "FROM cards cd\n"
            "JOIN accounts a ON cd.account_id = a.id\n"
            "WHERE cd.status = 'active';"
        ),
        "hints": [
            "Join cards to accounts using the account_id foreign key.",
            "Filter on the card status, not the account status.",
            "Use table aliases to distinguish columns from each table.",
            "WHERE cd.status = 'active' filters for active cards.",
        ],
        "explanation": (
            "1. JOIN cards to accounts on account_id.\n"
            "2. WHERE cd.status = 'active' keeps only active cards.\n"
            "3. SELECT the requested columns from both tables."
        ),
        "approach": [
            "Identify the relationship between cards and accounts.",
            "Join on the foreign key and filter for active cards.",
            "Return only the needed columns.",
        ],
        "common_mistakes": [
            "Filtering on account status instead of card status.",
            "Forgetting the JOIN, which prevents access to account columns.",
        ],
        "concept_tags": ["JOIN", "WHERE", "foreign key"],
    },
    {
        "id": "fi-021",
        "slug": "loan-payments-with-customer",
        "title": "Loan Payments with Customer Names",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The collections team needs a report of loan payments with customer "
            "details. Return first_name, last_name, loan_type, payment_date, "
            "amount, and remaining_balance. Sort by payment_date descending."
        ),
        "schema_hint": ["customers", "loans", "payments"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, l.loan_type,\n"
            "       p.payment_date, p.amount, p.remaining_balance\n"
            "FROM payments p\n"
            "JOIN loans l ON p.loan_id = l.id\n"
            "JOIN customers c ON l.customer_id = c.id\n"
            "ORDER BY p.payment_date DESC;"
        ),
        "hints": [
            "You need to chain two JOINs: payments -> loans -> customers.",
            "payments.loan_id connects to loans.id.",
            "loans.customer_id connects to customers.id.",
            "Sort by payment_date descending for most recent payments first.",
        ],
        "explanation": (
            "1. JOIN payments to loans on loan_id.\n"
            "2. JOIN loans to customers on customer_id.\n"
            "3. SELECT the requested columns from all three tables.\n"
            "4. ORDER BY payment_date DESC shows the most recent payments first."
        ),
        "approach": [
            "Chain JOINs from payments through loans to customers.",
            "Select only the requested columns.",
            "Sort by payment date descending.",
        ],
        "common_mistakes": [
            "Joining payments directly to customers, which has no direct foreign key.",
            "Forgetting one of the two required JOINs.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "ORDER BY"],
    },
    {
        "id": "fi-022",
        "slug": "total-balance-per-customer",
        "title": "Total Balance Per Customer",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The wealth report needs the total balance across all accounts for "
            "each customer. Return first_name, last_name, and total_balance "
            "(sum of all account balances). Only include customers with active "
            "accounts. Sort by total_balance descending. Limit to top 20."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       SUM(a.balance) AS total_balance\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "WHERE a.status = 'active'\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY total_balance DESC\n"
            "LIMIT 20;"
        ),
        "hints": [
            "Join customers to accounts and filter for active accounts.",
            "Use SUM to aggregate balances per customer.",
            "GROUP BY the customer's identifying columns.",
            "LIMIT 20 caps the results to the top 20.",
        ],
        "explanation": (
            "1. JOIN customers to accounts on customer_id.\n"
            "2. WHERE a.status = 'active' filters out closed/frozen accounts.\n"
            "3. GROUP BY c.id aggregates all account balances per customer.\n"
            "4. SUM(a.balance) gives the total balance.\n"
            "5. ORDER BY total_balance DESC and LIMIT 20 give the top 20."
        ),
        "approach": [
            "Join and filter for active accounts.",
            "Group by customer and sum their balances.",
            "Sort and limit the result set.",
        ],
        "common_mistakes": [
            "Forgetting to filter for active accounts only.",
            "Not grouping by customer, which sums across all customers.",
            "Forgetting LIMIT to restrict to top 20.",
        ],
        "concept_tags": ["JOIN", "SUM", "GROUP BY", "WHERE", "LIMIT", "ORDER BY"],
    },
    {
        "id": "fi-023",
        "slug": "accounts-with-card-count",
        "title": "Accounts with Card Count",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card operations team wants to know how many cards are linked to "
            "each account. Return account id, account_type, balance, and the "
            "number of cards (card_count). Include accounts that have zero cards. "
            "Sort by card_count descending."
        ),
        "schema_hint": ["accounts", "cards"],
        "solution_query": (
            "SELECT a.id, a.account_type, a.balance,\n"
            "       COUNT(cd.id) AS card_count\n"
            "FROM accounts a\n"
            "LEFT JOIN cards cd ON a.id = cd.account_id\n"
            "GROUP BY a.id, a.account_type, a.balance\n"
            "ORDER BY card_count DESC;"
        ),
        "hints": [
            "You need to include accounts even if they have no cards.",
            "LEFT JOIN ensures all accounts appear in the result.",
            "COUNT(cd.id) counts only non-NULL matches (i.e., actual cards).",
            "Group by account columns to get one row per account.",
        ],
        "explanation": (
            "1. LEFT JOIN accounts to cards to include all accounts.\n"
            "2. COUNT(cd.id) counts cards per account (0 for unmatched).\n"
            "3. GROUP BY a.id creates one row per account.\n"
            "4. ORDER BY card_count DESC shows accounts with the most cards first."
        ),
        "approach": [
            "Use LEFT JOIN to include accounts without cards.",
            "Count card ids (not *) to correctly count 0 for unmatched accounts.",
            "Group by account and sort.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which excludes accounts with no cards.",
            "Using COUNT(*) instead of COUNT(cd.id), which counts 1 for accounts with no cards.",
        ],
        "concept_tags": ["LEFT JOIN", "COUNT", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "fi-024",
        "slug": "branch-customer-overlap",
        "title": "Customers in Branch Cities",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The marketing team wants to find customers who live in the same city "
            "as a bank branch. Return the customer's first_name, last_name, city, "
            "and the branch name. Sort by city, then last_name."
        ),
        "schema_hint": ["customers", "branches"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, c.city, b.name AS branch_name\n"
            "FROM customers c\n"
            "JOIN branches b ON c.city = b.city\n"
            "ORDER BY c.city, c.last_name;"
        ),
        "hints": [
            "This join is not on a foreign key — it matches on the city column.",
            "Both customers and branches have a city column.",
            "JOIN on c.city = b.city finds customers in branch cities.",
            "Sort by city first, then last_name.",
        ],
        "explanation": (
            "1. JOIN customers to branches on the city column.\n"
            "2. This is a non-foreign-key join matching by shared city values.\n"
            "3. SELECT the requested columns from both tables.\n"
            "4. ORDER BY city, last_name sorts the results."
        ),
        "approach": [
            "Identify that both tables share a city column.",
            "Join on city to find the overlap.",
            "Sort by city and last name.",
        ],
        "common_mistakes": [
            "Assuming a foreign key exists between customers and branches.",
            "Forgetting that one customer could match multiple branches in the same city.",
        ],
        "concept_tags": ["JOIN", "non-key join", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 4 — SUBQUERIES (6 problems: fi-025 through fi-030)
    # =========================================================================
    {
        "id": "fi-025",
        "slug": "above-average-balance-accounts",
        "title": "Accounts with Above-Average Balance",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The premium services team wants to identify accounts whose balance "
            "exceeds the overall average balance. Return the id, account_type, "
            "and balance of these accounts, sorted by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, account_type, balance\n"
            "FROM accounts\n"
            "WHERE balance > (SELECT AVG(balance) FROM accounts)\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "You need to compare each account's balance to the overall average.",
            "A subquery can compute the average in the WHERE clause.",
            "The subquery runs once and returns a single value.",
            "WHERE balance > (SELECT AVG(balance) FROM accounts)",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(balance) FROM accounts) computes the overall average.\n"
            "2. The outer query filters accounts whose balance exceeds that average.\n"
            "3. ORDER BY balance DESC shows the highest balances first."
        ),
        "approach": [
            "Write a subquery to compute the overall average balance.",
            "Use it in the WHERE clause to filter accounts.",
            "Sort by balance descending.",
        ],
        "common_mistakes": [
            "Trying to use AVG in WHERE directly without a subquery.",
            "Using HAVING instead of WHERE (HAVING is for group-level filtering).",
        ],
        "concept_tags": ["subquery", "scalar subquery", "AVG", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-026",
        "slug": "customers-with-multiple-account-types",
        "title": "Customers with Multiple Account Types",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The cross-selling team wants to find customers who have more than "
            "one type of account (e.g., both checking and savings). Return "
            "customer_id, first_name, last_name, and the number of distinct "
            "account types they hold. Sort by the count descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name,\n"
            "       COUNT(DISTINCT a.account_type) AS type_count\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(DISTINCT a.account_type) > 1\n"
            "ORDER BY type_count DESC;"
        ),
        "hints": [
            "COUNT(DISTINCT account_type) counts unique account types per customer.",
            "Join customers to accounts to access both names and types.",
            "Use HAVING to filter after grouping.",
            "HAVING COUNT(DISTINCT a.account_type) > 1 keeps only multi-type customers.",
        ],
        "explanation": (
            "1. JOIN customers to accounts.\n"
            "2. GROUP BY customer to aggregate account types.\n"
            "3. COUNT(DISTINCT a.account_type) counts unique types per customer.\n"
            "4. HAVING filters to customers with more than one type."
        ),
        "approach": [
            "Join customers and accounts.",
            "Group by customer and count distinct account types.",
            "Filter with HAVING for counts greater than 1.",
        ],
        "common_mistakes": [
            "Using COUNT(account_type) without DISTINCT, which counts total accounts not types.",
            "Using WHERE instead of HAVING to filter on an aggregate.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT"],
    },
    {
        "id": "fi-027",
        "slug": "largest-transaction-per-account",
        "title": "Largest Transaction Per Account",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "For each account, find the single largest transaction by amount. "
            "Return account_id, transaction_date, type, and amount for each "
            "account's maximum transaction. Sort by amount descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT t.account_id, t.transaction_date, t.type, t.amount\n"
            "FROM transactions t\n"
            "WHERE t.amount = (\n"
            "    SELECT MAX(t2.amount)\n"
            "    FROM transactions t2\n"
            "    WHERE t2.account_id = t.account_id\n"
            ")\n"
            "ORDER BY t.amount DESC;"
        ),
        "hints": [
            "You need a correlated subquery that finds the MAX for each account.",
            "The subquery references the outer query's account_id.",
            "For each row, the subquery checks if its amount equals the max for that account.",
            "A correlated subquery runs once per row of the outer query.",
        ],
        "explanation": (
            "1. The correlated subquery finds MAX(amount) for each account.\n"
            "2. The outer WHERE keeps only rows matching their account's max.\n"
            "3. ORDER BY amount DESC shows the largest transactions first.\n"
            "4. Note: ties are possible if two transactions have the same max amount."
        ),
        "approach": [
            "Write a correlated subquery to find the max amount per account.",
            "Match each transaction's amount against its account's max.",
            "Sort by amount descending.",
        ],
        "common_mistakes": [
            "Using a non-correlated subquery which returns a single global max.",
            "Forgetting that ties may produce multiple rows per account.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "WHERE"],
    },
    {
        "id": "fi-028",
        "slug": "customers-with-defaulted-loans",
        "title": "Customers with Defaulted Loans",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The risk management team needs a list of customers who have at least "
            "one defaulted loan. Return the customer's id, first_name, last_name, "
            "and email. Use a subquery with EXISTS."
        ),
        "schema_hint": ["customers", "loans"],
        "solution_query": (
            "SELECT c.id, c.first_name, c.last_name, c.email\n"
            "FROM customers c\n"
            "WHERE EXISTS (\n"
            "    SELECT 1 FROM loans l\n"
            "    WHERE l.customer_id = c.id\n"
            "      AND l.status = 'defaulted'\n"
            ");"
        ),
        "hints": [
            "EXISTS checks whether a subquery returns any rows.",
            "The subquery is correlated — it references the outer customer.",
            "SELECT 1 is a convention; EXISTS only cares about row existence.",
            "Filter loans by status = 'defaulted' inside the subquery.",
        ],
        "explanation": (
            "1. For each customer, the EXISTS subquery checks for defaulted loans.\n"
            "2. If any defaulted loan exists for that customer, the row is included.\n"
            "3. EXISTS is efficient because it stops as soon as one match is found."
        ),
        "approach": [
            "Use EXISTS with a correlated subquery.",
            "Filter loans by customer_id and defaulted status.",
            "Return customer details for matches.",
        ],
        "common_mistakes": [
            "Using IN instead of EXISTS — both work but EXISTS is more idiomatic for existence checks.",
            "Forgetting to correlate the subquery to the outer customer.",
        ],
        "concept_tags": ["EXISTS", "correlated subquery", "WHERE"],
    },
    {
        "id": "fi-029",
        "slug": "accounts-with-no-transactions",
        "title": "Accounts with No Transactions",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The account review team wants to identify dormant accounts that have "
            "never had a transaction. Return the account id, customer_id, "
            "account_type, and opened_at. Use NOT EXISTS."
        ),
        "schema_hint": ["accounts", "transactions"],
        "solution_query": (
            "SELECT a.id, a.customer_id, a.account_type, a.opened_at\n"
            "FROM accounts a\n"
            "WHERE NOT EXISTS (\n"
            "    SELECT 1 FROM transactions t\n"
            "    WHERE t.account_id = a.id\n"
            ");"
        ),
        "hints": [
            "NOT EXISTS is the opposite of EXISTS — it returns rows with no matches.",
            "The subquery checks for any transactions linked to each account.",
            "If no transaction exists, the account is included in the result.",
            "This is equivalent to a LEFT JOIN / IS NULL pattern.",
        ],
        "explanation": (
            "1. For each account, NOT EXISTS checks that no transactions reference it.\n"
            "2. Accounts without any matching transactions are returned.\n"
            "3. This pattern is called an anti-join."
        ),
        "approach": [
            "Use NOT EXISTS with a correlated subquery on transactions.",
            "The subquery correlates on account_id.",
            "Return the account details for unmatched accounts.",
        ],
        "common_mistakes": [
            "Using NOT IN which can behave unexpectedly with NULLs.",
            "Forgetting the correlation, which would check for any transactions globally.",
        ],
        "concept_tags": ["NOT EXISTS", "correlated subquery", "anti-join"],
    },
    {
        "id": "fi-030",
        "slug": "loans-above-type-average",
        "title": "Loans Above Their Type Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The analytics team wants to find loans whose principal exceeds the "
            "average principal for their specific loan type. Return the loan id, "
            "loan_type, principal, and interest_rate. Sort by principal descending."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT l.id, l.loan_type, l.principal, l.interest_rate\n"
            "FROM loans l\n"
            "WHERE l.principal > (\n"
            "    SELECT AVG(l2.principal)\n"
            "    FROM loans l2\n"
            "    WHERE l2.loan_type = l.loan_type\n"
            ")\n"
            "ORDER BY l.principal DESC;"
        ),
        "hints": [
            "Each loan type has its own average — you need a correlated subquery.",
            "The subquery computes AVG(principal) for the same loan_type.",
            "Compare each loan's principal against its type's average.",
            "This is a correlated subquery because it references the outer query's loan_type.",
        ],
        "explanation": (
            "1. The correlated subquery computes AVG(principal) for the same loan_type.\n"
            "2. The outer query keeps only loans exceeding their type's average.\n"
            "3. ORDER BY principal DESC shows the largest loans first."
        ),
        "approach": [
            "Write a correlated subquery to find the average principal per type.",
            "Compare each loan against its type's average.",
            "Sort by principal descending.",
        ],
        "common_mistakes": [
            "Using a global average instead of a per-type average.",
            "Forgetting the correlation on loan_type.",
        ],
        "concept_tags": ["correlated subquery", "AVG", "WHERE", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 5 — WINDOW FUNCTIONS (5 problems: fi-031 through fi-035)
    # =========================================================================
    {
        "id": "fi-031",
        "slug": "rank-accounts-by-balance",
        "title": "Rank Accounts by Balance Within Type",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The analytics team wants to rank accounts by balance within each "
            "account type. Return account id, account_type, balance, and a "
            "rank column. Use RANK() partitioned by account_type, ordered by "
            "balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, account_type, balance,\n"
            "       RANK() OVER (PARTITION BY account_type ORDER BY balance DESC) AS balance_rank\n"
            "FROM accounts;"
        ),
        "hints": [
            "RANK() assigns a ranking within a partition.",
            "PARTITION BY divides rows into groups (like GROUP BY but without collapsing).",
            "ORDER BY inside the OVER clause determines the ranking order.",
            "RANK() leaves gaps after ties (1, 2, 2, 4).",
        ],
        "explanation": (
            "1. PARTITION BY account_type creates separate ranking groups per type.\n"
            "2. ORDER BY balance DESC ranks highest balances first.\n"
            "3. RANK() assigns the position, leaving gaps for ties.\n"
            "4. Unlike GROUP BY, window functions do not collapse rows."
        ),
        "approach": [
            "Use the RANK() window function.",
            "Partition by account_type to rank within each type.",
            "Order by balance descending within the window.",
        ],
        "common_mistakes": [
            "Confusing RANK() with ROW_NUMBER() — RANK() has gaps for ties.",
            "Forgetting PARTITION BY, which ranks across all accounts globally.",
            "Putting ORDER BY outside the OVER clause instead of inside.",
        ],
        "concept_tags": ["RANK", "OVER", "PARTITION BY", "window functions"],
    },
    {
        "id": "fi-032",
        "slug": "running-balance-per-account",
        "title": "Running Transaction Total Per Account",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The audit team needs a running total of transaction amounts for "
            "each account, ordered by transaction date. Return account_id, "
            "transaction_date, amount, and running_total. Limit to account_id = 1 "
            "for readability."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id, transaction_date, amount,\n"
            "       SUM(amount) OVER (\n"
            "           PARTITION BY account_id\n"
            "           ORDER BY transaction_date\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS running_total\n"
            "FROM transactions\n"
            "WHERE account_id = 1\n"
            "ORDER BY transaction_date;"
        ),
        "hints": [
            "A running total is a cumulative SUM using a window function.",
            "SUM() OVER(...) computes the sum within a window frame.",
            "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW defines the running window.",
            "PARTITION BY ensures the running total resets per account.",
        ],
        "explanation": (
            "1. SUM(amount) OVER(...) computes a running total.\n"
            "2. PARTITION BY account_id resets the total for each account.\n"
            "3. ORDER BY transaction_date ensures chronological accumulation.\n"
            "4. ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW includes all prior rows."
        ),
        "approach": [
            "Use SUM() as a window function with a frame clause.",
            "Partition by account and order by date.",
            "Filter to a single account for clarity.",
        ],
        "common_mistakes": [
            "Omitting the frame clause, which may use a default RANGE frame and give unexpected results with ties.",
            "Forgetting PARTITION BY, which creates one running total across all accounts.",
        ],
        "concept_tags": ["SUM", "window function", "ROWS BETWEEN", "running total"],
    },
    {
        "id": "fi-033",
        "slug": "row-number-for-deduplication",
        "title": "Identify Duplicate Customer Emails",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The data quality team needs to find duplicate customer emails. "
            "Use ROW_NUMBER() partitioned by email and ordered by created_at to "
            "assign a sequence number. Return only rows where the row number is "
            "greater than 1 (i.e., the duplicates). Show id, first_name, "
            "last_name, email, and the row number."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT id, first_name, last_name, email, rn\n"
            "FROM (\n"
            "    SELECT id, first_name, last_name, email, created_at,\n"
            "           ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn\n"
            "    FROM customers\n"
            ") sub\n"
            "WHERE rn > 1;"
        ),
        "hints": [
            "ROW_NUMBER() assigns a unique number within each partition.",
            "PARTITION BY email groups rows with the same email.",
            "The first occurrence (rn = 1) is the original; rn > 1 are duplicates.",
            "You need a subquery because you cannot filter on window functions in WHERE directly.",
        ],
        "explanation": (
            "1. ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) numbers each email occurrence.\n"
            "2. The subquery computes the row numbers.\n"
            "3. The outer WHERE rn > 1 filters to only the duplicate entries.\n"
            "4. This is a common deduplication pattern."
        ),
        "approach": [
            "Use ROW_NUMBER() partitioned by email.",
            "Wrap in a subquery to filter on the row number.",
            "Keep only rows where rn > 1.",
        ],
        "common_mistakes": [
            "Trying to use ROW_NUMBER() directly in a WHERE clause, which is not allowed.",
            "Using RANK() instead of ROW_NUMBER() — RANK() can assign the same number to ties.",
        ],
        "concept_tags": ["ROW_NUMBER", "PARTITION BY", "subquery", "deduplication"],
    },
    {
        "id": "fi-034",
        "slug": "lag-previous-transaction",
        "title": "Previous Transaction Amount",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The fraud detection team wants to compare each transaction to the "
            "previous one on the same account. For account_id = 1, return "
            "transaction_date, amount, the previous transaction amount "
            "(prev_amount using LAG), and the difference. Order by date."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT transaction_date, amount,\n"
            "       LAG(amount) OVER (ORDER BY transaction_date) AS prev_amount,\n"
            "       amount - LAG(amount) OVER (ORDER BY transaction_date) AS amount_change\n"
            "FROM transactions\n"
            "WHERE account_id = 1\n"
            "ORDER BY transaction_date;"
        ),
        "hints": [
            "LAG() accesses a value from the previous row in the window.",
            "LAG(amount) returns the amount from the row before the current one.",
            "The first row will have NULL for prev_amount since there is no previous row.",
            "You can compute the difference as amount - LAG(amount).",
        ],
        "explanation": (
            "1. LAG(amount) OVER (ORDER BY transaction_date) gets the previous row's amount.\n"
            "2. The difference shows how much the amount changed between transactions.\n"
            "3. The first row has NULL for prev_amount because there is no prior row.\n"
            "4. Filtering to account_id = 1 focuses on a single account's history."
        ),
        "approach": [
            "Use LAG() to access the previous row's amount.",
            "Compute the difference between current and previous amounts.",
            "Filter to a single account and order by date.",
        ],
        "common_mistakes": [
            "Confusing LAG (previous row) with LEAD (next row).",
            "Forgetting to handle the NULL in the first row.",
            "Not ordering the window correctly, which gives a random 'previous' row.",
        ],
        "concept_tags": ["LAG", "window function", "OVER", "ORDER BY"],
    },
    {
        "id": "fi-035",
        "slug": "ntile-balance-quartiles",
        "title": "Account Balance Quartiles",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The analytics team wants to segment accounts into four balance "
            "quartiles. Use NTILE(4) to assign each account to a quartile based "
            "on balance. Return id, account_type, balance, and quartile. "
            "Only include active accounts. Order by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, account_type, balance,\n"
            "       NTILE(4) OVER (ORDER BY balance DESC) AS quartile\n"
            "FROM accounts\n"
            "WHERE status = 'active'\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "NTILE(4) divides the result set into 4 roughly equal groups.",
            "The OVER clause with ORDER BY determines the distribution order.",
            "Quartile 1 contains the highest balances when ordered DESC.",
            "Filter for active accounts with a WHERE clause before the window function.",
        ],
        "explanation": (
            "1. WHERE status = 'active' filters to active accounts.\n"
            "2. NTILE(4) OVER (ORDER BY balance DESC) assigns quartile numbers 1-4.\n"
            "3. Quartile 1 has the highest balances, quartile 4 the lowest.\n"
            "4. NTILE distributes rows as evenly as possible."
        ),
        "approach": [
            "Filter for active accounts.",
            "Apply NTILE(4) with ORDER BY balance DESC.",
            "The result gives each account a quartile assignment.",
        ],
        "common_mistakes": [
            "Forgetting the WHERE filter, which includes closed/frozen accounts.",
            "Using NTILE without ORDER BY, which assigns quartiles in arbitrary order.",
            "Confusing NTILE with PERCENTILE functions.",
        ],
        "concept_tags": ["NTILE", "window function", "OVER", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 6 — ADVANCED (5 problems: fi-036 through fi-040)
    # =========================================================================
    {
        "id": "fi-036",
        "slug": "customer-summary-cte",
        "title": "Customer Financial Summary with CTE",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Build a comprehensive customer financial summary using a CTE. First, "
            "compute the total balance across all accounts for each customer. "
            "Then, in the main query, join with customers to return first_name, "
            "last_name, total_balance, and the number of accounts. Only include "
            "customers with total_balance > 10000. Sort by total_balance descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "WITH customer_totals AS (\n"
            "    SELECT customer_id,\n"
            "           SUM(balance) AS total_balance,\n"
            "           COUNT(*) AS account_count\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       ct.total_balance, ct.account_count\n"
            "FROM customer_totals ct\n"
            "JOIN customers c ON ct.customer_id = c.id\n"
            "WHERE ct.total_balance > 10000\n"
            "ORDER BY ct.total_balance DESC;"
        ),
        "hints": [
            "A CTE (WITH clause) lets you define a temporary named result set.",
            "Compute the aggregates in the CTE, then join in the main query.",
            "The CTE groups accounts by customer_id with SUM and COUNT.",
            "The main query joins the CTE to customers for name information.",
        ],
        "explanation": (
            "1. The CTE customer_totals aggregates account data per customer.\n"
            "2. The main query joins to customers for name columns.\n"
            "3. WHERE total_balance > 10000 filters to high-value customers.\n"
            "4. CTEs improve readability by separating the aggregation step."
        ),
        "approach": [
            "Define a CTE that groups accounts by customer_id.",
            "Join the CTE to customers in the main query.",
            "Filter and sort the results.",
        ],
        "common_mistakes": [
            "Trying to do everything in a single query without a CTE, reducing readability.",
            "Forgetting to join the CTE back to the customers table for names.",
            "Placing the WHERE filter inside the CTE instead of the main query.",
        ],
        "concept_tags": ["CTE", "WITH", "JOIN", "SUM", "GROUP BY"],
    },
    {
        "id": "fi-037",
        "slug": "monthly-deposit-vs-withdrawal",
        "title": "Monthly Deposits vs Withdrawals",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The treasury team needs a monthly comparison of total deposits vs "
            "total withdrawals. For each month (YYYY-MM), compute total_deposits "
            "and total_withdrawals using conditional aggregation. Also compute "
            "net_flow (deposits minus withdrawals). Sort by month."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT SUBSTR(transaction_date, 1, 7) AS month,\n"
            "       SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) AS total_deposits,\n"
            "       SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS total_withdrawals,\n"
            "       SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END)\n"
            "         - SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS net_flow\n"
            "FROM transactions\n"
            "GROUP BY SUBSTR(transaction_date, 1, 7)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Conditional aggregation uses CASE inside SUM.",
            "SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) sums only deposits.",
            "Subtract withdrawals from deposits to get net flow.",
            "Group by the year-month extracted from transaction_date.",
        ],
        "explanation": (
            "1. SUBSTR extracts the YYYY-MM portion from transaction_date.\n"
            "2. Conditional SUM with CASE WHEN separates deposits from withdrawals.\n"
            "3. net_flow is the difference between the two sums.\n"
            "4. GROUP BY month and ORDER BY month gives a chronological report."
        ),
        "approach": [
            "Extract year-month from the date.",
            "Use conditional aggregation (CASE WHEN inside SUM) for each type.",
            "Compute net flow as the difference.",
            "Group and sort by month.",
        ],
        "common_mistakes": [
            "Using separate queries for deposits and withdrawals instead of conditional aggregation.",
            "Forgetting the ELSE 0 in CASE, which would produce NULL for non-matching rows.",
            "Not grouping by the extracted month.",
        ],
        "concept_tags": ["CASE WHEN", "conditional aggregation", "SUM", "GROUP BY", "SUBSTR"],
    },
    {
        "id": "fi-038",
        "slug": "loan-payment-coverage",
        "title": "Loan Payment Coverage Ratio",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The collections team needs to know what percentage of each loan's "
            "principal has been paid off. For each loan, compute total_paid "
            "(sum of principal_paid from payments), the original principal, and "
            "the coverage_ratio (total_paid / principal * 100, rounded to 1 "
            "decimal). Include loan_type and status. Sort by coverage_ratio "
            "descending."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.id AS loan_id, l.loan_type, l.principal, l.status,\n"
            "       COALESCE(SUM(p.principal_paid), 0) AS total_paid,\n"
            "       ROUND(COALESCE(SUM(p.principal_paid), 0) / l.principal * 100, 1) AS coverage_ratio\n"
            "FROM loans l\n"
            "LEFT JOIN payments p ON l.id = p.loan_id\n"
            "GROUP BY l.id, l.loan_type, l.principal, l.status\n"
            "ORDER BY coverage_ratio DESC;"
        ),
        "hints": [
            "Use LEFT JOIN to include loans with no payments (coverage = 0).",
            "SUM(principal_paid) gives the total principal repaid per loan.",
            "COALESCE handles NULLs from unmatched LEFT JOINs.",
            "Divide total_paid by principal and multiply by 100 for percentage.",
        ],
        "explanation": (
            "1. LEFT JOIN ensures loans without payments show coverage of 0.\n"
            "2. SUM(p.principal_paid) aggregates payments per loan.\n"
            "3. COALESCE(..., 0) converts NULL sums to 0.\n"
            "4. The ratio formula gives the percentage of principal repaid."
        ),
        "approach": [
            "Left join loans to payments.",
            "Group by loan and sum the principal_paid.",
            "Compute the ratio and handle NULLs with COALESCE.",
            "Sort by coverage ratio descending.",
        ],
        "common_mistakes": [
            "Using INNER JOIN, which drops loans without any payments.",
            "Dividing by zero if principal could be 0 (unlikely but possible).",
            "Forgetting COALESCE, resulting in NULL ratios for loans without payments.",
        ],
        "concept_tags": ["LEFT JOIN", "SUM", "COALESCE", "ROUND", "GROUP BY", "arithmetic"],
    },
    {
        "id": "fi-039",
        "slug": "multi-cte-risk-report",
        "title": "Multi-CTE Risk Report",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Build a risk report using multiple CTEs. CTE 1: customer_balances "
            "computes total_balance per customer from accounts. CTE 2: "
            "customer_loans computes total loan principal per customer from loans. "
            "Main query: join both CTEs to customers and show first_name, "
            "last_name, total_balance, total_principal, and a debt_to_asset_ratio "
            "(total_principal / total_balance, rounded to 2 decimals). Only "
            "include customers with total_balance > 0. Sort by ratio descending. "
            "Limit to 20."
        ),
        "schema_hint": ["customers", "accounts", "loans"],
        "solution_query": (
            "WITH customer_balances AS (\n"
            "    SELECT customer_id, SUM(balance) AS total_balance\n"
            "    FROM accounts\n"
            "    WHERE status = 'active'\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "customer_loans AS (\n"
            "    SELECT customer_id, SUM(principal) AS total_principal\n"
            "    FROM loans\n"
            "    WHERE status = 'active'\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       cb.total_balance,\n"
            "       COALESCE(cl.total_principal, 0) AS total_principal,\n"
            "       ROUND(COALESCE(cl.total_principal, 0) * 1.0 / cb.total_balance, 2) AS debt_to_asset_ratio\n"
            "FROM customer_balances cb\n"
            "JOIN customers c ON cb.customer_id = c.id\n"
            "LEFT JOIN customer_loans cl ON cb.customer_id = cl.customer_id\n"
            "WHERE cb.total_balance > 0\n"
            "ORDER BY debt_to_asset_ratio DESC\n"
            "LIMIT 20;"
        ),
        "hints": [
            "Define two CTEs separated by a comma after the WITH keyword.",
            "CTE 1 aggregates account balances, CTE 2 aggregates loan principals.",
            "Use LEFT JOIN for loans since not every customer has a loan.",
            "COALESCE handles NULL totals for customers without loans.",
        ],
        "explanation": (
            "1. CTE customer_balances sums active account balances per customer.\n"
            "2. CTE customer_loans sums active loan principals per customer.\n"
            "3. The main query joins both CTEs to customers.\n"
            "4. LEFT JOIN ensures customers without loans are included.\n"
            "5. The ratio shows how leveraged each customer is."
        ),
        "approach": [
            "Create two CTEs for balances and loans respectively.",
            "Join both to the customers table.",
            "Compute the ratio and filter/sort the results.",
        ],
        "common_mistakes": [
            "Forgetting the comma between CTEs.",
            "Using INNER JOIN for loans, excluding customers without loans.",
            "Division by zero when total_balance is 0.",
        ],
        "concept_tags": ["CTE", "multiple CTEs", "JOIN", "LEFT JOIN", "COALESCE", "ROUND"],
    },
    {
        "id": "fi-040",
        "slug": "detect-suspicious-transactions",
        "title": "Detect Suspicious Transaction Patterns",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The fraud team wants to find transactions whose amount is more "
            "than 1.5 times the average for their transaction type. Use a CTE to "
            "compute the average amount per type. Then join to flag "
            "above-average transactions. Return the transaction id, account_id, "
            "type, amount, and the type average (type_avg, rounded to 2 decimals). "
            "Sort by amount descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH type_stats AS (\n"
            "    SELECT type,\n"
            "           AVG(amount) AS type_avg\n"
            "    FROM transactions\n"
            "    GROUP BY type\n"
            ")\n"
            "SELECT t.id, t.account_id, t.type, t.amount,\n"
            "       ROUND(ts.type_avg, 2) AS type_avg\n"
            "FROM transactions t\n"
            "JOIN type_stats ts ON t.type = ts.type\n"
            "WHERE t.amount > 1.5 * ts.type_avg\n"
            "ORDER BY t.amount DESC;"
        ),
        "hints": [
            "Use a CTE to compute the average amount per transaction type.",
            "Join the CTE back to the transactions table on type.",
            "Filter where amount > 1.5 * type_avg.",
            "ROUND the average to 2 decimal places.",
        ],
        "explanation": (
            "1. The CTE computes the average amount for each transaction type.\n"
            "2. The main query joins transactions to the stats CTE.\n"
            "3. WHERE filters for transactions exceeding 1.5x the type average.\n"
            "4. This flags unusually large transactions relative to their type."
        ),
        "approach": [
            "Compute per-type average in a CTE.",
            "Join transactions to the stats CTE.",
            "Filter for amounts exceeding 1.5x the type average.",
            "Sort by amount descending to show the most suspicious first.",
        ],
        "common_mistakes": [
            "Comparing to the global average instead of per-type average.",
            "Forgetting the JOIN between the CTE and transactions table.",
            "Using the wrong multiplier or comparison direction.",
        ],
        "concept_tags": ["CTE", "AVG", "JOIN", "outlier detection"],
    },

    # =========================================================================
    # LEVEL 7 — JOINS & AGGREGATION MIX (fi-041 through fi-055)
    # =========================================================================
    {
        "id": "fi-041",
        "slug": "branch-account-count",
        "title": "Number of Customers Per Branch City",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The branch planning team wants to know how many customers live in "
            "each city that has a branch. Return the branch name, city, and the "
            "count of customers in that city. Sort by customer count descending."
        ),
        "schema_hint": ["branches", "customers"],
        "solution_query": (
            "SELECT b.name AS branch_name, b.city,\n"
            "       COUNT(c.id) AS customer_count\n"
            "FROM branches b\n"
            "LEFT JOIN customers c ON b.city = c.city\n"
            "GROUP BY b.name, b.city\n"
            "ORDER BY customer_count DESC;"
        ),
        "hints": [
            "You need to match customers to branches by city.",
            "Use LEFT JOIN so branches with zero customers still appear.",
            "COUNT(c.id) counts only matched customers (NULLs are not counted).",
            "Group by branch name and city to get one row per branch.",
        ],
        "explanation": (
            "1. LEFT JOIN branches to customers on city to include all branches.\n"
            "2. GROUP BY branch creates one row per branch.\n"
            "3. COUNT(c.id) counts customers, returning 0 for unmatched branches."
        ),
        "approach": [
            "Join branches to customers on city.",
            "Group by branch and count customer ids.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops branches with no customers in their city.",
            "Using COUNT(*) which counts 1 even for branches with no matching customers.",
        ],
        "concept_tags": ["LEFT JOIN", "COUNT", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "fi-042",
        "slug": "customers-with-checking-and-savings",
        "title": "Customers with Both Checking and Savings",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The product team wants to identify customers who hold both a checking "
            "and a savings account. Return customer_id, first_name, and last_name. "
            "Sort by last_name."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name\n"
            "FROM customers c\n"
            "JOIN accounts a1 ON c.id = a1.customer_id AND a1.account_type = 'checking'\n"
            "JOIN accounts a2 ON c.id = a2.customer_id AND a2.account_type = 'savings'\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY c.last_name;"
        ),
        "hints": [
            "You need to verify two conditions on the same table for the same customer.",
            "One approach is to join the accounts table twice with different filters.",
            "Each join filters for a specific account type.",
            "GROUP BY eliminates duplicates if a customer has multiple checking or savings accounts.",
        ],
        "explanation": (
            "1. Join accounts twice: once for checking, once for savings.\n"
            "2. Only customers appearing in both joins survive the INNER JOINs.\n"
            "3. GROUP BY removes duplicates from multiple accounts of the same type."
        ),
        "approach": [
            "Self-join the accounts table with different type filters.",
            "Customers matching both joins have both account types.",
            "Group to deduplicate and sort by name.",
        ],
        "common_mistakes": [
            "Using OR in a single join, which finds customers with either type.",
            "Forgetting GROUP BY, which can produce duplicate rows.",
        ],
        "concept_tags": ["self-join", "JOIN", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "fi-043",
        "slug": "average-transaction-amount-per-customer",
        "title": "Average Transaction Amount Per Customer",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The analytics team wants to know the average transaction amount for "
            "each customer. Return first_name, last_name, and avg_tx_amount "
            "(rounded to 2 decimal places). Only include customers who have at "
            "least 5 transactions. Sort by avg_tx_amount descending."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       ROUND(AVG(t.amount), 2) AS avg_tx_amount\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(t.id) >= 5\n"
            "ORDER BY avg_tx_amount DESC;"
        ),
        "hints": [
            "You need to chain joins: customers -> accounts -> transactions.",
            "AVG(t.amount) computes the mean transaction amount per group.",
            "Use HAVING to filter groups by transaction count.",
            "Remember to GROUP BY customer identifying columns.",
        ],
        "explanation": (
            "1. Chain JOINs from customers through accounts to transactions.\n"
            "2. GROUP BY customer to aggregate all their transactions.\n"
            "3. HAVING COUNT(t.id) >= 5 filters to active customers.\n"
            "4. AVG and ROUND produce the desired metric."
        ),
        "approach": [
            "Join three tables to connect customers to their transactions.",
            "Group by customer, compute AVG, filter with HAVING.",
            "Sort by average descending.",
        ],
        "common_mistakes": [
            "Forgetting the intermediate accounts join.",
            "Using WHERE instead of HAVING to filter on the count.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "AVG", "HAVING", "GROUP BY"],
    },
    {
        "id": "fi-044",
        "slug": "total-interest-paid-per-loan-type",
        "title": "Total Interest Paid by Loan Type",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The finance department wants to know how much interest has been "
            "collected for each loan type. Return loan_type and total_interest "
            "(sum of interest_paid from payments). Sort by total_interest descending."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.loan_type,\n"
            "       SUM(p.interest_paid) AS total_interest\n"
            "FROM loans l\n"
            "JOIN payments p ON l.id = p.loan_id\n"
            "GROUP BY l.loan_type\n"
            "ORDER BY total_interest DESC;"
        ),
        "hints": [
            "Join loans to payments to access interest_paid.",
            "SUM the interest_paid column grouped by loan_type.",
            "The foreign key is payments.loan_id referencing loans.id.",
            "Sort by the sum descending to see the most profitable types first.",
        ],
        "explanation": (
            "1. JOIN loans to payments on loan_id.\n"
            "2. GROUP BY loan_type to aggregate across all loans of each type.\n"
            "3. SUM(interest_paid) totals the interest collected per type."
        ),
        "approach": [
            "Join loans and payments.",
            "Group by loan type and sum interest paid.",
            "Sort descending.",
        ],
        "common_mistakes": [
            "Forgetting the join and trying to sum from payments alone (no loan_type there).",
            "Using principal_paid instead of interest_paid.",
        ],
        "concept_tags": ["JOIN", "SUM", "GROUP BY", "ORDER BY"],
    },
    {
        "id": "fi-045",
        "slug": "credit-card-utilization",
        "title": "Credit Card Utilization Rate",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The risk team needs to assess credit card utilization. For each credit "
            "card (card_type = 'credit') that has a credit_limit > 0, compute the "
            "utilization rate as (account balance / credit_limit * 100). Return "
            "card_number, credit_limit, account balance, and utilization_pct "
            "rounded to 1 decimal. Sort by utilization_pct descending."
        ),
        "schema_hint": ["cards", "accounts"],
        "solution_query": (
            "SELECT cd.card_number, cd.credit_limit, a.balance,\n"
            "       ROUND(a.balance / cd.credit_limit * 100, 1) AS utilization_pct\n"
            "FROM cards cd\n"
            "JOIN accounts a ON cd.account_id = a.id\n"
            "WHERE cd.card_type = 'credit'\n"
            "  AND cd.credit_limit > 0\n"
            "ORDER BY utilization_pct DESC;"
        ),
        "hints": [
            "Join cards to accounts to get the account balance.",
            "Filter for credit cards with a positive credit limit.",
            "Utilization = balance / credit_limit * 100.",
            "Use ROUND to format the percentage to 1 decimal place.",
        ],
        "explanation": (
            "1. JOIN cards to accounts on account_id.\n"
            "2. WHERE filters for credit cards with valid limits.\n"
            "3. The formula balance / credit_limit * 100 gives the utilization percentage.\n"
            "4. ROUND formats the result."
        ),
        "approach": [
            "Join cards to accounts.",
            "Filter for credit card type and positive limit.",
            "Compute utilization and sort.",
        ],
        "common_mistakes": [
            "Not filtering for credit_limit > 0, risking division by zero.",
            "Confusing card_type with account_type.",
        ],
        "concept_tags": ["JOIN", "arithmetic", "ROUND", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-046",
        "slug": "customers-in-multiple-states",
        "title": "Customers with Accounts in Multiple Branch States",
        "difficulty": "hard",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The compliance team wants to find customers who live in the same "
            "city as a bank branch. Join customers to branches on the city column. "
            "Return customer_id, first_name, last_name, city, and the branch name. "
            "Sort by city, then last_name."
        ),
        "schema_hint": ["customers", "branches"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name,\n"
            "       c.city, b.name AS branch_name\n"
            "FROM customers c\n"
            "JOIN branches b ON c.city = b.city\n"
            "ORDER BY c.city, c.last_name;"
        ),
        "hints": [
            "You need to connect customers to branches through the city column.",
            "This is a non-foreign-key join — the matching column is city.",
            "Only customers whose city matches a branch city will appear.",
            "Sort by city first, then by last name.",
        ],
        "explanation": (
            "1. JOIN customers to branches on the city column.\n"
            "2. This finds customers co-located with a bank branch.\n"
            "3. Only matching cities produce results (INNER JOIN behavior).\n"
            "4. ORDER BY city, last_name for organized output."
        ),
        "approach": [
            "Join customers to branches on city (non-key join).",
            "Select identifying columns from both tables.",
            "Sort by city and last name.",
        ],
        "common_mistakes": [
            "Trying to join on id columns — there is no foreign key between these tables.",
            "Using LEFT JOIN when you only want customers who are near a branch.",
        ],
        "concept_tags": ["JOIN", "non-key join", "ORDER BY"],
    },
    {
        "id": "fi-047",
        "slug": "inactive-accounts-with-balance",
        "title": "Closed Accounts with Remaining Balance",
        "difficulty": "easy",
        "category": "where",
        "dataset": "finance",
        "description": (
            "The operations team needs to identify closed accounts that still have "
            "a positive balance, which may indicate an error. Return the account id, "
            "customer_id, account_type, balance, and status. Sort by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, account_type, balance, status\n"
            "FROM accounts\n"
            "WHERE status = 'closed'\n"
            "  AND balance > 0\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "You need two conditions: status is closed AND balance is positive.",
            "Combine both conditions with AND in the WHERE clause.",
            "This is a single-table query with no joins needed.",
            "Sort by balance descending to show the largest discrepancies first.",
        ],
        "explanation": (
            "1. WHERE status = 'closed' AND balance > 0 finds problematic accounts.\n"
            "2. ORDER BY balance DESC prioritizes the largest remaining balances."
        ),
        "approach": [
            "Filter accounts for closed status and positive balance.",
            "Sort by balance descending.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, returning all closed accounts or all positive-balance accounts.",
            "Forgetting to check for balance > 0 specifically.",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "ORDER BY"],
    },
    {
        "id": "fi-048",
        "slug": "customer-age-groups",
        "title": "Customer Count by Age Group",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The marketing team wants to segment customers by age group. Using "
            "date_of_birth, classify customers into groups: 'Under 30', '30-49', "
            "'50-69', '70+'. Return age_group and customer_count. Sort by "
            "customer_count descending. Use '2025-01-01' as the reference date."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT CASE\n"
            "         WHEN (julianday('2025-01-01') - julianday(date_of_birth)) / 365.25 < 30 THEN 'Under 30'\n"
            "         WHEN (julianday('2025-01-01') - julianday(date_of_birth)) / 365.25 < 50 THEN '30-49'\n"
            "         WHEN (julianday('2025-01-01') - julianday(date_of_birth)) / 365.25 < 70 THEN '50-69'\n"
            "         ELSE '70+'\n"
            "       END AS age_group,\n"
            "       COUNT(*) AS customer_count\n"
            "FROM customers\n"
            "GROUP BY age_group\n"
            "ORDER BY customer_count DESC;"
        ),
        "hints": [
            "Use julianday to compute the difference between two dates.",
            "Divide the day difference by 365.25 for approximate years.",
            "CASE WHEN lets you create categorical buckets.",
            "Group by the CASE expression to count customers per bucket.",
        ],
        "explanation": (
            "1. julianday computes age in days, divided by 365.25 for years.\n"
            "2. CASE WHEN classifies each customer into an age group.\n"
            "3. GROUP BY age_group counts customers per bucket.\n"
            "4. ORDER BY count descending shows the largest group first."
        ),
        "approach": [
            "Compute age from date_of_birth using julianday.",
            "Use CASE WHEN to create age group labels.",
            "Group and count per group.",
        ],
        "common_mistakes": [
            "Using SUBSTR-based year subtraction without accounting for month/day.",
            "Forgetting the ELSE clause for the oldest age group.",
            "Not using GROUP BY on the CASE expression.",
        ],
        "concept_tags": ["CASE WHEN", "julianday", "GROUP BY", "COUNT", "date arithmetic"],
    },
    {
        "id": "fi-049",
        "slug": "largest-account-per-customer",
        "title": "Largest Account Balance Per Customer",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "For each customer who has at least one account, find their account "
            "with the highest balance. Return customer_id, first_name, last_name, "
            "account_type, and balance. Sort by balance descending. Limit to 25."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name,\n"
            "       a.account_type, a.balance\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "WHERE a.balance = (\n"
            "    SELECT MAX(a2.balance)\n"
            "    FROM accounts a2\n"
            "    WHERE a2.customer_id = c.id\n"
            ")\n"
            "ORDER BY a.balance DESC\n"
            "LIMIT 25;"
        ),
        "hints": [
            "You need a correlated subquery to find the MAX balance per customer.",
            "The subquery references the outer customer's id.",
            "Join customers to accounts, then filter for the max-balance account.",
            "Ties are possible if a customer has two accounts with the same max balance.",
        ],
        "explanation": (
            "1. Join customers to accounts.\n"
            "2. The correlated subquery finds the MAX balance for each customer.\n"
            "3. WHERE filters to only the top-balance account per customer.\n"
            "4. ORDER BY and LIMIT show the top 25."
        ),
        "approach": [
            "Join customers and accounts.",
            "Use a correlated subquery for the per-customer max.",
            "Filter, sort, and limit.",
        ],
        "common_mistakes": [
            "Using a global MAX instead of a per-customer MAX.",
            "Not handling ties where a customer has two accounts with identical max balances.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "JOIN", "WHERE", "LIMIT"],
    },
    {
        "id": "fi-050",
        "slug": "loan-status-summary",
        "title": "Loan Portfolio Status Summary",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The executive team needs a quick overview of the loan portfolio. "
            "For each loan status (active, paid, defaulted), return the status, "
            "the count of loans, the total principal, and the average interest rate "
            "rounded to 2 decimals. Sort by total_principal descending."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT status,\n"
            "       COUNT(*) AS loan_count,\n"
            "       SUM(principal) AS total_principal,\n"
            "       ROUND(AVG(interest_rate), 2) AS avg_interest_rate\n"
            "FROM loans\n"
            "GROUP BY status\n"
            "ORDER BY total_principal DESC;"
        ),
        "hints": [
            "Group by the status column to create one row per status.",
            "Use COUNT, SUM, and AVG for the three requested metrics.",
            "ROUND the average interest rate to 2 decimal places.",
            "Sort by total_principal descending.",
        ],
        "explanation": (
            "1. GROUP BY status creates groups for active, paid, and defaulted.\n"
            "2. COUNT, SUM, and AVG compute the requested aggregates.\n"
            "3. ROUND formats the average rate.\n"
            "4. ORDER BY total_principal DESC shows the largest category first."
        ),
        "approach": [
            "Group loans by status.",
            "Apply multiple aggregate functions.",
            "Sort by total principal.",
        ],
        "common_mistakes": [
            "Forgetting to round the average interest rate.",
            "Using SUM on interest_rate instead of AVG.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "SUM", "AVG", "ROUND", "ORDER BY"],
    },
    {
        "id": "fi-051",
        "slug": "customers-with-frozen-accounts",
        "title": "Customers with Any Frozen Account",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The compliance team needs a list of customers who have at least one "
            "frozen account. Return distinct customer first_name, last_name, and "
            "email. Sort by last_name."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT DISTINCT c.first_name, c.last_name, c.email\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "WHERE a.status = 'frozen'\n"
            "ORDER BY c.last_name;"
        ),
        "hints": [
            "Join customers to accounts to access account status.",
            "Filter for frozen accounts in the WHERE clause.",
            "Use DISTINCT to avoid duplicate customers with multiple frozen accounts.",
            "Sort by last_name alphabetically.",
        ],
        "explanation": (
            "1. JOIN customers to accounts on customer_id.\n"
            "2. WHERE a.status = 'frozen' filters for frozen accounts.\n"
            "3. DISTINCT removes duplicate customer rows."
        ),
        "approach": [
            "Join and filter for frozen status.",
            "Use DISTINCT to deduplicate.",
            "Sort by name.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT, which shows a customer once per frozen account.",
            "Filtering on customer status instead of account status.",
        ],
        "concept_tags": ["JOIN", "WHERE", "DISTINCT", "ORDER BY"],
    },
    {
        "id": "fi-052",
        "slug": "expired-cards-report",
        "title": "Expired Cards with Customer Info",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card services team needs a report of all expired cards along with "
            "customer contact information. Return customer first_name, last_name, "
            "email, card_number, card_type, and expiry_date. Only include cards "
            "where status is 'expired'. Sort by expiry_date ascending."
        ),
        "schema_hint": ["customers", "accounts", "cards"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, c.email,\n"
            "       cd.card_number, cd.card_type, cd.expiry_date\n"
            "FROM cards cd\n"
            "JOIN accounts a ON cd.account_id = a.id\n"
            "JOIN customers c ON a.customer_id = c.id\n"
            "WHERE cd.status = 'expired'\n"
            "ORDER BY cd.expiry_date;"
        ),
        "hints": [
            "Cards connect to customers through accounts (cards -> accounts -> customers).",
            "Filter for expired card status.",
            "Chain two JOINs to reach the customer table.",
            "Sort by expiry_date ascending to see the oldest expirations first.",
        ],
        "explanation": (
            "1. JOIN cards to accounts, then accounts to customers.\n"
            "2. WHERE cd.status = 'expired' filters for expired cards.\n"
            "3. SELECT pulls contact info and card details.\n"
            "4. ORDER BY expiry_date shows the earliest expirations first."
        ),
        "approach": [
            "Chain joins: cards -> accounts -> customers.",
            "Filter for expired cards.",
            "Sort by expiry date.",
        ],
        "common_mistakes": [
            "Trying to join cards directly to customers (no direct foreign key).",
            "Forgetting one of the intermediate joins.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-053",
        "slug": "deposits-per-day-of-week",
        "title": "Deposit Volume by Day of Week",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The operations team wants to understand deposit patterns by day of "
            "week. For deposit transactions only, return the day of the week "
            "(0=Sunday through 6=Saturday using strftime), the count of deposits, "
            "and the average deposit amount rounded to 2 decimals. Sort by day_of_week."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT CAST(strftime('%w', transaction_date) AS INTEGER) AS day_of_week,\n"
            "       COUNT(*) AS deposit_count,\n"
            "       ROUND(AVG(amount), 2) AS avg_deposit\n"
            "FROM transactions\n"
            "WHERE type = 'deposit'\n"
            "GROUP BY day_of_week\n"
            "ORDER BY day_of_week;"
        ),
        "hints": [
            "strftime('%w', date) returns the day of week as a string (0=Sunday).",
            "Filter for type = 'deposit' before aggregating.",
            "Group by the day-of-week value.",
            "CAST to INTEGER for proper numeric sorting.",
        ],
        "explanation": (
            "1. strftime('%w', transaction_date) extracts the day of week.\n"
            "2. WHERE type = 'deposit' filters to deposits only.\n"
            "3. GROUP BY day_of_week aggregates per weekday.\n"
            "4. COUNT and AVG provide the requested metrics."
        ),
        "approach": [
            "Extract day of week using strftime.",
            "Filter for deposits, group, and aggregate.",
            "Sort by day of week.",
        ],
        "common_mistakes": [
            "Forgetting to filter for deposits before aggregating.",
            "Not casting the strftime result, which can cause string-based sorting.",
        ],
        "concept_tags": ["strftime", "GROUP BY", "COUNT", "AVG", "WHERE", "CAST"],
    },
    {
        "id": "fi-054",
        "slug": "card-count-per-customer",
        "title": "Number of Cards Per Customer",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card operations team wants to know how many cards each customer "
            "has. Return first_name, last_name, and card_count. Include customers "
            "with zero cards. Sort by card_count descending, then last_name."
        ),
        "schema_hint": ["customers", "accounts", "cards"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       COUNT(cd.id) AS card_count\n"
            "FROM customers c\n"
            "LEFT JOIN accounts a ON c.id = a.customer_id\n"
            "LEFT JOIN cards cd ON a.id = cd.account_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY card_count DESC, c.last_name;"
        ),
        "hints": [
            "Cards connect to customers through accounts.",
            "Use LEFT JOINs to include customers with no accounts or no cards.",
            "COUNT(cd.id) counts actual cards, returning 0 for NULLs.",
            "Group by customer to get one row per customer.",
        ],
        "explanation": (
            "1. LEFT JOIN customers to accounts, then accounts to cards.\n"
            "2. LEFT JOINs ensure all customers appear even with no cards.\n"
            "3. COUNT(cd.id) counts only non-NULL card ids.\n"
            "4. GROUP BY customer aggregates the card count."
        ),
        "approach": [
            "Chain LEFT JOINs through accounts to cards.",
            "Count card ids per customer.",
            "Sort by count descending, then name.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which excludes customers without cards.",
            "Using COUNT(*) which gives 1 instead of 0 for customers without cards.",
        ],
        "concept_tags": ["LEFT JOIN", "multi-table join", "COUNT", "GROUP BY"],
    },
    {
        "id": "fi-055",
        "slug": "high-value-savings-customers",
        "title": "High-Value Savings Account Holders",
        "difficulty": "easy",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The wealth management team wants customers with savings account "
            "balances over 25000. Return first_name, last_name, balance, and "
            "the account opened_at date. Sort by balance descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, a.balance, a.opened_at\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "WHERE a.account_type = 'savings'\n"
            "  AND a.balance > 25000\n"
            "ORDER BY a.balance DESC;"
        ),
        "hints": [
            "Join customers to accounts on customer_id.",
            "Filter for savings accounts with balance over 25000.",
            "Both conditions go in the WHERE clause with AND.",
            "Sort by balance descending.",
        ],
        "explanation": (
            "1. JOIN customers to accounts.\n"
            "2. WHERE filters for savings type and high balance.\n"
            "3. ORDER BY balance DESC shows the highest balances first."
        ),
        "approach": [
            "Join customers and accounts.",
            "Apply two filters with AND.",
            "Sort by balance descending.",
        ],
        "common_mistakes": [
            "Filtering on the wrong account type.",
            "Using OR instead of AND for the two conditions.",
        ],
        "concept_tags": ["JOIN", "WHERE", "AND", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 8 — WINDOW FUNCTIONS & SUBQUERIES (fi-056 through fi-060)
    # =========================================================================
    {
        "id": "fi-056",
        "slug": "dense-rank-customers-by-total-balance",
        "title": "Dense Rank Customers by Total Balance",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "Rank customers by their total account balance using DENSE_RANK. "
            "First compute the total balance across all active accounts per "
            "customer, then assign a dense rank. Return first_name, last_name, "
            "total_balance, and balance_rank. Show top 20 by rank."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT first_name, last_name, total_balance, balance_rank\n"
            "FROM (\n"
            "    SELECT c.first_name, c.last_name,\n"
            "           SUM(a.balance) AS total_balance,\n"
            "           DENSE_RANK() OVER (ORDER BY SUM(a.balance) DESC) AS balance_rank\n"
            "    FROM customers c\n"
            "    JOIN accounts a ON c.id = a.customer_id\n"
            "    WHERE a.status = 'active'\n"
            "    GROUP BY c.id, c.first_name, c.last_name\n"
            ") ranked\n"
            "WHERE balance_rank <= 20\n"
            "ORDER BY balance_rank;"
        ),
        "hints": [
            "You need to aggregate balances per customer first, then rank.",
            "DENSE_RANK() does not leave gaps after ties, unlike RANK().",
            "Window functions can be applied over GROUP BY results.",
            "Use a subquery to filter on the rank value since you cannot use window functions in WHERE.",
        ],
        "explanation": (
            "1. GROUP BY customer with SUM(balance) gets total per customer.\n"
            "2. DENSE_RANK() OVER (ORDER BY SUM(balance) DESC) ranks them.\n"
            "3. A subquery wrapper lets us filter WHERE balance_rank <= 20.\n"
            "4. DENSE_RANK ensures tied customers share the same rank with no gaps."
        ),
        "approach": [
            "Aggregate balances per customer.",
            "Apply DENSE_RANK window function over the sum.",
            "Wrap in a subquery to filter by rank.",
        ],
        "common_mistakes": [
            "Using RANK() instead of DENSE_RANK() when gaps are not desired.",
            "Trying to filter on the window function in WHERE without a subquery.",
            "Forgetting to filter for active accounts.",
        ],
        "concept_tags": ["DENSE_RANK", "window function", "GROUP BY", "SUM", "subquery"],
    },
    {
        "id": "fi-057",
        "slug": "percentage-of-total-balance",
        "title": "Each Account as Percentage of Customer Total",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "For each account, show what percentage it represents of its customer's "
            "total balance. Return customer_id, account_type, balance, customer_total "
            "(sum of all the customer's account balances), and pct_of_total rounded "
            "to 1 decimal. Only include active accounts. Sort by customer_id, then "
            "pct_of_total descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT customer_id, account_type, balance,\n"
            "       SUM(balance) OVER (PARTITION BY customer_id) AS customer_total,\n"
            "       ROUND(balance * 100.0 / SUM(balance) OVER (PARTITION BY customer_id), 1) AS pct_of_total\n"
            "FROM accounts\n"
            "WHERE status = 'active'\n"
            "ORDER BY customer_id, pct_of_total DESC;"
        ),
        "hints": [
            "SUM() OVER (PARTITION BY customer_id) gives the customer total without collapsing rows.",
            "Divide the row's balance by the customer total and multiply by 100.",
            "Use ROUND to format to 1 decimal place.",
            "Window functions compute across partitions while keeping every row.",
        ],
        "explanation": (
            "1. SUM(balance) OVER (PARTITION BY customer_id) computes each customer's total.\n"
            "2. balance * 100.0 / customer_total gives the percentage.\n"
            "3. ROUND formats to 1 decimal.\n"
            "4. Unlike GROUP BY, the window function preserves each row."
        ),
        "approach": [
            "Use SUM as a window function partitioned by customer_id.",
            "Compute the percentage from each row's balance and the partition total.",
            "Sort by customer and percentage.",
        ],
        "common_mistakes": [
            "Using GROUP BY which collapses rows and loses individual account details.",
            "Integer division — multiply by 100.0 (not 100) to get decimal results.",
            "Forgetting to handle customers with zero total balance (division by zero).",
        ],
        "concept_tags": ["SUM", "window function", "PARTITION BY", "ROUND", "arithmetic"],
    },
    {
        "id": "fi-058",
        "slug": "lead-next-payment-date",
        "title": "Next Payment Date for Each Loan Payment",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The collections team wants to see each loan payment alongside the "
            "next scheduled payment date. For each payment, use LEAD to get the "
            "next payment_date on the same loan. Return loan_id, payment_date, "
            "amount, next_payment_date, and days_until_next (difference in days). "
            "Filter to loan_id = 1 for readability. Order by payment_date."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT loan_id, payment_date, amount,\n"
            "       LEAD(payment_date) OVER (PARTITION BY loan_id ORDER BY payment_date) AS next_payment_date,\n"
            "       CAST(julianday(LEAD(payment_date) OVER (PARTITION BY loan_id ORDER BY payment_date))\n"
            "            - julianday(payment_date) AS INTEGER) AS days_until_next\n"
            "FROM payments\n"
            "WHERE loan_id = 1\n"
            "ORDER BY payment_date;"
        ),
        "hints": [
            "LEAD() accesses the next row's value in the window.",
            "PARTITION BY loan_id ensures we only look at payments for the same loan.",
            "julianday difference gives the number of days between two dates.",
            "The last payment for each loan will have NULL for next_payment_date.",
        ],
        "explanation": (
            "1. LEAD(payment_date) OVER (...) gets the next payment date per loan.\n"
            "2. julianday difference computes the gap in days.\n"
            "3. The last row per loan has NULL since there is no next payment.\n"
            "4. Filtering to loan_id = 1 simplifies the output."
        ),
        "approach": [
            "Use LEAD window function partitioned by loan.",
            "Compute date difference using julianday.",
            "Filter to a single loan for clarity.",
        ],
        "common_mistakes": [
            "Confusing LEAD (next row) with LAG (previous row).",
            "Forgetting PARTITION BY, which would look across all loans.",
            "Not handling the NULL in the last row of each partition.",
        ],
        "concept_tags": ["LEAD", "window function", "PARTITION BY", "julianday", "date arithmetic"],
    },
    {
        "id": "fi-059",
        "slug": "accounts-opened-same-day",
        "title": "Accounts Opened on the Same Day as Another",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The fraud team wants to find accounts that were opened on the same "
            "day as at least one other account. Return account id, customer_id, "
            "account_type, and opened_at. Sort by opened_at, then id."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, account_type, opened_at\n"
            "FROM accounts\n"
            "WHERE opened_at IN (\n"
            "    SELECT opened_at\n"
            "    FROM accounts\n"
            "    GROUP BY opened_at\n"
            "    HAVING COUNT(*) > 1\n"
            ")\n"
            "ORDER BY opened_at, id;"
        ),
        "hints": [
            "First find dates where more than one account was opened.",
            "A subquery with GROUP BY and HAVING can identify such dates.",
            "Then filter the main query to only those dates.",
            "IN is a good operator for matching against a list of values.",
        ],
        "explanation": (
            "1. The subquery finds opened_at dates with more than one account.\n"
            "2. The outer query selects all accounts opened on those dates.\n"
            "3. ORDER BY opened_at, id provides a clean sort."
        ),
        "approach": [
            "Subquery: group by opened_at, filter HAVING COUNT > 1.",
            "Outer query: filter with IN to match those dates.",
            "Sort results.",
        ],
        "common_mistakes": [
            "Using a self-join which is more complex than needed here.",
            "Forgetting HAVING and using WHERE with COUNT.",
        ],
        "concept_tags": ["subquery", "IN", "GROUP BY", "HAVING", "ORDER BY"],
    },
    {
        "id": "fi-060",
        "slug": "customers-without-loans",
        "title": "Customers Without Any Loans",
        "difficulty": "easy",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The sales team wants to target customers who have never taken a loan. "
            "Return customer id, first_name, last_name, and email. Use NOT IN "
            "with a subquery. Sort by last_name."
        ),
        "schema_hint": ["customers", "loans"],
        "solution_query": (
            "SELECT id, first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE id NOT IN (\n"
            "    SELECT DISTINCT customer_id FROM loans\n"
            ")\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "A subquery can list all customer_ids that appear in the loans table.",
            "NOT IN excludes customers whose id is in that list.",
            "DISTINCT in the subquery is optional but improves clarity.",
            "Be careful with NOT IN when the subquery could return NULLs.",
        ],
        "explanation": (
            "1. The subquery returns all customer_ids from the loans table.\n"
            "2. NOT IN filters to customers whose id is not in that set.\n"
            "3. ORDER BY last_name sorts alphabetically."
        ),
        "approach": [
            "Subquery to get all customer_ids from loans.",
            "Filter main query with NOT IN.",
            "Sort by name.",
        ],
        "common_mistakes": [
            "If customer_id in loans could be NULL, NOT IN might return no rows.",
            "Using NOT EXISTS is safer but NOT IN works when NULLs are absent.",
        ],
        "concept_tags": ["NOT IN", "subquery", "WHERE", "ORDER BY"],
    },

    # =========================================================================
    # LEVEL 9 — CTEs & ADVANCED PATTERNS (fi-061 through fi-070)
    # =========================================================================
    {
        "id": "fi-061",
        "slug": "monthly-new-accounts-cte",
        "title": "Monthly New Account Trend with CTE",
        "difficulty": "medium",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "The growth team wants a monthly trend of new account openings. "
            "Use a CTE to extract the month from opened_at and count accounts "
            "per month. In the main query, also compute a running total of "
            "accounts opened using a window function. Return month, monthly_count, "
            "and cumulative_count. Sort by month."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "WITH monthly AS (\n"
            "    SELECT SUBSTR(opened_at, 1, 7) AS month,\n"
            "           COUNT(*) AS monthly_count\n"
            "    FROM accounts\n"
            "    GROUP BY SUBSTR(opened_at, 1, 7)\n"
            ")\n"
            "SELECT month, monthly_count,\n"
            "       SUM(monthly_count) OVER (ORDER BY month\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS cumulative_count\n"
            "FROM monthly\n"
            "ORDER BY month;"
        ),
        "hints": [
            "A CTE can compute the monthly counts first.",
            "SUM() as a window function with ROWS frame creates a running total.",
            "The window ORDER BY month ensures chronological accumulation.",
            "This pattern separates aggregation (CTE) from analytics (main query).",
        ],
        "explanation": (
            "1. The CTE groups accounts by month and counts them.\n"
            "2. The main query applies SUM as a window function for a running total.\n"
            "3. ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW accumulates all prior months."
        ),
        "approach": [
            "CTE: group by month, count accounts.",
            "Main query: apply cumulative SUM window function.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Trying to combine GROUP BY and window functions in the same query level.",
            "Omitting the frame clause, leading to unexpected default behavior.",
        ],
        "concept_tags": ["CTE", "window function", "SUM", "running total", "GROUP BY"],
    },
    {
        "id": "fi-062",
        "slug": "customer-first-and-last-transaction",
        "title": "Customer First and Last Transaction Dates",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "For each customer, find the date of their very first and very last "
            "transaction. Return first_name, last_name, first_tx_date, and "
            "last_tx_date. Only include customers who have transactions. Sort "
            "by first_tx_date."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       MIN(t.transaction_date) AS first_tx_date,\n"
            "       MAX(t.transaction_date) AS last_tx_date\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY first_tx_date;"
        ),
        "hints": [
            "Chain joins: customers -> accounts -> transactions.",
            "MIN(transaction_date) gives the earliest transaction.",
            "MAX(transaction_date) gives the latest transaction.",
            "Group by customer to aggregate across all their accounts.",
        ],
        "explanation": (
            "1. JOIN through accounts to transactions.\n"
            "2. GROUP BY customer to aggregate across all their accounts.\n"
            "3. MIN and MAX find the first and last transaction dates.\n"
            "4. INNER JOIN naturally excludes customers without transactions."
        ),
        "approach": [
            "Chain three-table join.",
            "Group by customer, apply MIN and MAX on dates.",
            "Sort by first transaction date.",
        ],
        "common_mistakes": [
            "Forgetting the intermediate accounts join.",
            "Using LIMIT 1 in a subquery instead of aggregate MIN/MAX.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "MIN", "MAX", "GROUP BY"],
    },
    {
        "id": "fi-063",
        "slug": "top-transaction-per-type-cte",
        "title": "Top Transaction Amount by Type (CTE)",
        "difficulty": "medium",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "For each transaction type, find the single transaction with the "
            "highest amount. Use a CTE with ROW_NUMBER to rank transactions "
            "within each type. Return the type, transaction id, account_id, "
            "amount, and transaction_date. Sort by amount descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH ranked AS (\n"
            "    SELECT id, account_id, type, amount, transaction_date,\n"
            "           ROW_NUMBER() OVER (PARTITION BY type ORDER BY amount DESC) AS rn\n"
            "    FROM transactions\n"
            ")\n"
            "SELECT type, id, account_id, amount, transaction_date\n"
            "FROM ranked\n"
            "WHERE rn = 1\n"
            "ORDER BY amount DESC;"
        ),
        "hints": [
            "ROW_NUMBER() OVER (PARTITION BY type ORDER BY amount DESC) ranks within each type.",
            "Filtering for rn = 1 gives the top transaction per type.",
            "A CTE makes it cleaner to wrap the window function and filter.",
            "This pattern is useful whenever you need 'top N per group'.",
        ],
        "explanation": (
            "1. The CTE assigns ROW_NUMBER() within each transaction type.\n"
            "2. The main query filters for rn = 1 to get the top per type.\n"
            "3. ORDER BY amount DESC sorts the final results."
        ),
        "approach": [
            "CTE with ROW_NUMBER partitioned by type, ordered by amount DESC.",
            "Filter for row number 1 in the main query.",
            "Sort by amount.",
        ],
        "common_mistakes": [
            "Using RANK which could return multiple rows per type on ties.",
            "Trying to filter on ROW_NUMBER in WHERE without a CTE or subquery.",
        ],
        "concept_tags": ["CTE", "ROW_NUMBER", "PARTITION BY", "top-N-per-group"],
    },
    {
        "id": "fi-064",
        "slug": "loan-payment-progress",
        "title": "Loan Repayment Progress Report",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Build a loan repayment progress report. CTE 1: compute total_paid "
            "(sum of amount from payments) per loan. CTE 2: join to loans for "
            "loan details. Main query: return loan_id, loan_type, principal, "
            "total_paid, remaining (principal - total_paid), and progress_pct "
            "(total_paid / principal * 100 rounded to 1 decimal). Include loans "
            "with no payments. Sort by progress_pct descending."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "WITH payment_totals AS (\n"
            "    SELECT loan_id, SUM(amount) AS total_paid\n"
            "    FROM payments\n"
            "    GROUP BY loan_id\n"
            ")\n"
            "SELECT l.id AS loan_id, l.loan_type, l.principal,\n"
            "       COALESCE(pt.total_paid, 0) AS total_paid,\n"
            "       l.principal - COALESCE(pt.total_paid, 0) AS remaining,\n"
            "       ROUND(COALESCE(pt.total_paid, 0) / l.principal * 100, 1) AS progress_pct\n"
            "FROM loans l\n"
            "LEFT JOIN payment_totals pt ON l.id = pt.loan_id\n"
            "ORDER BY progress_pct DESC;"
        ),
        "hints": [
            "A CTE can pre-aggregate payment totals per loan.",
            "LEFT JOIN ensures loans with no payments appear with 0 progress.",
            "COALESCE converts NULL sums to 0.",
            "The remaining amount is principal minus total paid.",
        ],
        "explanation": (
            "1. CTE aggregates total payments per loan.\n"
            "2. LEFT JOIN to loans ensures all loans appear.\n"
            "3. COALESCE handles loans with no payments.\n"
            "4. Arithmetic computes remaining balance and progress percentage."
        ),
        "approach": [
            "CTE: sum payments per loan.",
            "Left join to loans table.",
            "Compute remaining and progress percentage.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops loans without payments.",
            "Forgetting COALESCE, causing NULL arithmetic.",
            "Dividing by zero if principal is 0.",
        ],
        "concept_tags": ["CTE", "LEFT JOIN", "COALESCE", "ROUND", "arithmetic"],
    },
    {
        "id": "fi-065",
        "slug": "transaction-type-pivot",
        "title": "Transaction Type Pivot by Account",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The analytics team wants a pivot-style report showing each account's "
            "total amount broken down by transaction type. Return account_id, "
            "total_deposits, total_withdrawals, total_transfers, total_fees, and "
            "total_interest. Use conditional aggregation. Sort by account_id. "
            "Limit to 30 rows."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id,\n"
            "       SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) AS total_deposits,\n"
            "       SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS total_withdrawals,\n"
            "       SUM(CASE WHEN type = 'transfer' THEN amount ELSE 0 END) AS total_transfers,\n"
            "       SUM(CASE WHEN type = 'fee' THEN amount ELSE 0 END) AS total_fees,\n"
            "       SUM(CASE WHEN type = 'interest' THEN amount ELSE 0 END) AS total_interest\n"
            "FROM transactions\n"
            "GROUP BY account_id\n"
            "ORDER BY account_id\n"
            "LIMIT 30;"
        ),
        "hints": [
            "Conditional aggregation with CASE WHEN inside SUM creates pivot columns.",
            "Each CASE checks for a specific transaction type.",
            "ELSE 0 ensures non-matching rows contribute zero instead of NULL.",
            "Group by account_id to get one row per account.",
        ],
        "explanation": (
            "1. Each SUM(CASE WHEN type = '...' THEN amount ELSE 0 END) totals one type.\n"
            "2. GROUP BY account_id creates one row per account.\n"
            "3. This simulates a PIVOT operation which SQLite lacks natively."
        ),
        "approach": [
            "Write one SUM(CASE WHEN ...) for each transaction type.",
            "Group by account_id.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Missing the ELSE 0, which leads to NULL instead of 0.",
            "Forgetting a transaction type in the pivot.",
            "Using separate queries instead of a single grouped query.",
        ],
        "concept_tags": ["CASE WHEN", "conditional aggregation", "pivot", "GROUP BY"],
    },
    {
        "id": "fi-066",
        "slug": "moving-average-transaction-amount",
        "title": "3-Transaction Moving Average",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The analytics team wants a 3-transaction moving average of amounts "
            "for account_id = 1. For each transaction, compute the average of "
            "the current and two preceding transactions. Return transaction_date, "
            "amount, and moving_avg rounded to 2 decimals. Order by date."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT transaction_date, amount,\n"
            "       ROUND(AVG(amount) OVER (\n"
            "           ORDER BY transaction_date\n"
            "           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg\n"
            "FROM transactions\n"
            "WHERE account_id = 1\n"
            "ORDER BY transaction_date;"
        ),
        "hints": [
            "AVG() as a window function can compute a moving average.",
            "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW defines a 3-row window.",
            "The first two rows will have fewer than 3 values in the window.",
            "Filter to a single account for clarity.",
        ],
        "explanation": (
            "1. AVG(amount) OVER (...) with a ROWS frame computes a moving average.\n"
            "2. The frame includes the current row and the 2 rows before it.\n"
            "3. For the first row, only 1 value is averaged; for the second, 2 values.\n"
            "4. ROUND formats the result to 2 decimals."
        ),
        "approach": [
            "Use AVG as a window function with a ROWS frame.",
            "Define the frame as 2 PRECEDING to CURRENT ROW.",
            "Filter to one account, sort by date.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS, which behaves differently with ties.",
            "Setting the wrong frame boundaries.",
            "Forgetting that early rows have fewer than 3 values in the window.",
        ],
        "concept_tags": ["AVG", "window function", "ROWS BETWEEN", "moving average"],
    },
    {
        "id": "fi-067",
        "slug": "customer-lifetime-value-cte",
        "title": "Customer Lifetime Value Estimate",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Estimate customer lifetime value using multiple CTEs. CTE 1: "
            "total_deposits — sum of deposit transactions per customer (through "
            "accounts). CTE 2: total_interest_earned — sum of interest transactions "
            "per customer. Main query: join both CTEs to customers and return "
            "first_name, last_name, total_deposits, total_interest_earned, and "
            "estimated_value (deposits + interest). Sort by estimated_value DESC. "
            "Limit to 15."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "WITH total_deposits AS (\n"
            "    SELECT a.customer_id,\n"
            "           SUM(t.amount) AS deposit_sum\n"
            "    FROM accounts a\n"
            "    JOIN transactions t ON a.id = t.account_id\n"
            "    WHERE t.type = 'deposit'\n"
            "    GROUP BY a.customer_id\n"
            "),\n"
            "total_interest AS (\n"
            "    SELECT a.customer_id,\n"
            "           SUM(t.amount) AS interest_sum\n"
            "    FROM accounts a\n"
            "    JOIN transactions t ON a.id = t.account_id\n"
            "    WHERE t.type = 'interest'\n"
            "    GROUP BY a.customer_id\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       COALESCE(td.deposit_sum, 0) AS total_deposits,\n"
            "       COALESCE(ti.interest_sum, 0) AS total_interest_earned,\n"
            "       COALESCE(td.deposit_sum, 0) + COALESCE(ti.interest_sum, 0) AS estimated_value\n"
            "FROM customers c\n"
            "LEFT JOIN total_deposits td ON c.id = td.customer_id\n"
            "LEFT JOIN total_interest ti ON c.id = ti.customer_id\n"
            "WHERE COALESCE(td.deposit_sum, 0) + COALESCE(ti.interest_sum, 0) > 0\n"
            "ORDER BY estimated_value DESC\n"
            "LIMIT 15;"
        ),
        "hints": [
            "Use separate CTEs for deposits and interest to keep logic clean.",
            "Join accounts to transactions in each CTE to reach customer_id.",
            "LEFT JOIN both CTEs to customers in the main query.",
            "COALESCE handles customers who may have deposits but no interest or vice versa.",
        ],
        "explanation": (
            "1. CTE total_deposits sums deposit transactions per customer.\n"
            "2. CTE total_interest sums interest transactions per customer.\n"
            "3. Main query LEFT JOINs both CTEs to customers.\n"
            "4. COALESCE handles NULLs, and the sum gives estimated lifetime value."
        ),
        "approach": [
            "Two CTEs for different transaction types.",
            "Left join both to customers.",
            "Sum and sort for the final estimate.",
        ],
        "common_mistakes": [
            "Forgetting COALESCE, causing NULL in arithmetic.",
            "Using INNER JOIN which excludes customers missing one type.",
            "Forgetting the comma between CTEs.",
        ],
        "concept_tags": ["CTE", "multiple CTEs", "LEFT JOIN", "COALESCE", "SUM"],
    },
    {
        "id": "fi-068",
        "slug": "self-join-same-city-customers",
        "title": "Customer Pairs in the Same City",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The networking team wants to find pairs of customers who live in "
            "the same city. Return customer1_name (first_name || ' ' || last_name), "
            "customer2_name, and city. Ensure each pair appears only once "
            "(customer1 id < customer2 id). Sort by city, then customer1_name. "
            "Limit to 50."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT c1.first_name || ' ' || c1.last_name AS customer1_name,\n"
            "       c2.first_name || ' ' || c2.last_name AS customer2_name,\n"
            "       c1.city\n"
            "FROM customers c1\n"
            "JOIN customers c2 ON c1.city = c2.city AND c1.id < c2.id\n"
            "ORDER BY c1.city, customer1_name\n"
            "LIMIT 50;"
        ),
        "hints": [
            "A self-join matches the customers table against itself.",
            "Join on city to find customers in the same city.",
            "Use c1.id < c2.id to avoid duplicate pairs and self-matches.",
            "String concatenation with || builds the full name.",
        ],
        "explanation": (
            "1. Self-join customers on city to find same-city pairs.\n"
            "2. c1.id < c2.id ensures each pair appears once and excludes self-matches.\n"
            "3. || concatenates first and last names."
        ),
        "approach": [
            "Self-join on city.",
            "Use id inequality to deduplicate pairs.",
            "Concatenate names and sort.",
        ],
        "common_mistakes": [
            "Using c1.id != c2.id which produces each pair twice (A,B and B,A).",
            "Forgetting the city join condition, producing a cross join.",
        ],
        "concept_tags": ["self-join", "string concatenation", "ORDER BY", "LIMIT"],
    },
    {
        "id": "fi-069",
        "slug": "union-deposits-and-payments",
        "title": "Combined Cash Inflow Report",
        "difficulty": "medium",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The treasury team wants a unified view of all cash inflows: deposit "
            "transactions and loan payments. Use UNION ALL to combine deposit "
            "transactions (with source = 'deposit') and loan payments (with "
            "source = 'loan_payment'). Return source, the date (transaction_date "
            "or payment_date), and amount. Sort by date descending. Limit to 50."
        ),
        "schema_hint": ["transactions", "payments"],
        "solution_query": (
            "SELECT 'deposit' AS source, transaction_date AS date, amount\n"
            "FROM transactions\n"
            "WHERE type = 'deposit'\n"
            "UNION ALL\n"
            "SELECT 'loan_payment' AS source, payment_date AS date, amount\n"
            "FROM payments\n"
            "ORDER BY date DESC\n"
            "LIMIT 50;"
        ),
        "hints": [
            "UNION ALL combines result sets from two queries.",
            "Both SELECT statements must have the same number of columns.",
            "Add a literal string column to identify the source of each row.",
            "ORDER BY and LIMIT apply to the entire combined result.",
        ],
        "explanation": (
            "1. First SELECT gets deposits with a 'deposit' source label.\n"
            "2. Second SELECT gets loan payments with a 'loan_payment' label.\n"
            "3. UNION ALL combines both without removing duplicates.\n"
            "4. ORDER BY date DESC and LIMIT 50 shape the final output."
        ),
        "approach": [
            "Write two SELECTs with matching column counts.",
            "Add a source label column to each.",
            "Combine with UNION ALL, sort, and limit.",
        ],
        "common_mistakes": [
            "Using UNION instead of UNION ALL, which removes duplicates unnecessarily.",
            "Mismatching column counts or types between the two SELECTs.",
            "Putting ORDER BY inside a UNION member instead of at the end.",
        ],
        "concept_tags": ["UNION ALL", "literal values", "ORDER BY", "LIMIT"],
    },
    {
        "id": "fi-070",
        "slug": "accounts-opened-before-first-branch",
        "title": "Accounts Opened Before Their City Got a Branch",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "Find accounts belonging to customers whose account was opened before "
            "any branch in the customer's city was established. Return customer "
            "first_name, last_name, account opened_at, and branch opened_at. "
            "Sort by account opened_at."
        ),
        "schema_hint": ["customers", "accounts", "branches"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       a.opened_at AS account_opened_at,\n"
            "       b.opened_at AS branch_opened_at\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN branches b ON c.city = b.city\n"
            "WHERE a.opened_at < b.opened_at\n"
            "ORDER BY a.opened_at;"
        ),
        "hints": [
            "Join customers to accounts and branches (on city).",
            "Compare the account opened_at with the branch opened_at.",
            "Accounts opened before the branch are the interesting ones.",
            "The date comparison works on text strings in YYYY-MM-DD format.",
        ],
        "explanation": (
            "1. JOIN customers to accounts and branches (on city).\n"
            "2. WHERE a.opened_at < b.opened_at finds accounts opened before the branch.\n"
            "3. Text date comparison works because dates are in ISO format."
        ),
        "approach": [
            "Chain joins through city.",
            "Compare dates to find early accounts.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Forgetting that customers may not live in a city with a branch.",
            "Date comparison failing if dates are not in ISO format (they are here).",
        ],
        "concept_tags": ["JOIN", "non-key join", "date comparison", "WHERE"],
    },

    # =========================================================================
    # LEVEL 10 — MORE WINDOW FUNCTIONS & ADVANCED (fi-071 through fi-080)
    # =========================================================================
    {
        "id": "fi-071",
        "slug": "percent-rank-account-balance",
        "title": "Percent Rank of Account Balances",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The analytics team wants to see what percentile each account's "
            "balance falls in within its account type. Use PERCENT_RANK() to "
            "compute the percentile. Return account_type, balance, and "
            "balance_percentile rounded to 2 decimals. Only include active "
            "accounts. Sort by account_type, then balance DESC."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT account_type, balance,\n"
            "       ROUND(PERCENT_RANK() OVER (\n"
            "           PARTITION BY account_type ORDER BY balance\n"
            "       ), 2) AS balance_percentile\n"
            "FROM accounts\n"
            "WHERE status = 'active'\n"
            "ORDER BY account_type, balance DESC;"
        ),
        "hints": [
            "PERCENT_RANK() returns a value between 0 and 1 indicating relative position.",
            "PARTITION BY account_type computes percentiles within each type.",
            "ORDER BY balance in the OVER clause determines the ranking direction.",
            "ROUND formats the percentile to 2 decimal places.",
        ],
        "explanation": (
            "1. PERCENT_RANK() computes (rank - 1) / (total rows - 1) within each partition.\n"
            "2. PARTITION BY account_type creates separate percentile calculations per type.\n"
            "3. The result ranges from 0.0 (lowest) to 1.0 (highest balance)."
        ),
        "approach": [
            "Apply PERCENT_RANK window function partitioned by account type.",
            "Filter for active accounts.",
            "Round and sort.",
        ],
        "common_mistakes": [
            "Confusing PERCENT_RANK with CUME_DIST (slightly different formula).",
            "Forgetting that PERCENT_RANK returns 0 for the first row, not a percentage.",
        ],
        "concept_tags": ["PERCENT_RANK", "window function", "PARTITION BY"],
    },
    {
        "id": "fi-072",
        "slug": "first-value-highest-balance-account",
        "title": "Highest Balance Account per Type",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "For each active account, show the highest balance within that account "
            "type using FIRST_VALUE. Return account_type, id, balance, and "
            "type_max_balance. Sort by account_type, balance DESC."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT account_type, id, balance,\n"
            "       FIRST_VALUE(balance) OVER (\n"
            "           PARTITION BY account_type ORDER BY balance DESC\n"
            "       ) AS type_max_balance\n"
            "FROM accounts\n"
            "WHERE status = 'active'\n"
            "ORDER BY account_type, balance DESC;"
        ),
        "hints": [
            "FIRST_VALUE() returns the first value in the window partition.",
            "With ORDER BY balance DESC, the first value is the maximum balance.",
            "Every row in the partition sees the same FIRST_VALUE result.",
            "This is similar to MAX() but FIRST_VALUE is a window function pattern.",
        ],
        "explanation": (
            "1. FIRST_VALUE(balance) OVER (...) returns the highest balance per type.\n"
            "2. ORDER BY balance DESC in the window puts the highest first.\n"
            "3. All rows in the partition see the same max value."
        ),
        "approach": [
            "Use FIRST_VALUE window function partitioned by type.",
            "Order by balance DESC within the window.",
            "Filter and sort.",
        ],
        "common_mistakes": [
            "Confusing FIRST_VALUE with LAST_VALUE (default frame affects LAST_VALUE).",
            "Not specifying ORDER BY in the OVER clause.",
        ],
        "concept_tags": ["FIRST_VALUE", "window function", "PARTITION BY"],
    },
    {
        "id": "fi-073",
        "slug": "row-number-top3-per-type",
        "title": "Top 3 Accounts by Balance Per Type",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "Find the top 3 highest-balance active accounts for each account "
            "type. Use ROW_NUMBER() in a CTE, then filter for the top 3. "
            "Return account_type, id, balance, and the row number (rn). "
            "Sort by account_type, rn."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "WITH ranked AS (\n"
            "    SELECT account_type, id, balance,\n"
            "           ROW_NUMBER() OVER (PARTITION BY account_type ORDER BY balance DESC) AS rn\n"
            "    FROM accounts\n"
            "    WHERE status = 'active'\n"
            ")\n"
            "SELECT account_type, id, balance, rn\n"
            "FROM ranked\n"
            "WHERE rn <= 3\n"
            "ORDER BY account_type, rn;"
        ),
        "hints": [
            "This is the classic 'top N per group' pattern.",
            "ROW_NUMBER assigns a unique rank within each partition.",
            "Use a CTE or subquery to filter on the row number.",
            "Filter WHERE rn <= 3 in the outer query.",
        ],
        "explanation": (
            "1. CTE assigns ROW_NUMBER() partitioned by account_type, ordered by balance DESC.\n"
            "2. Main query filters for rn <= 3 to get the top 3 per type.\n"
            "3. ORDER BY account_type, rn provides clean output."
        ),
        "approach": [
            "CTE: ROW_NUMBER partitioned by type, ordered by balance DESC.",
            "Filter for rn <= 3.",
            "Sort by type and rank.",
        ],
        "common_mistakes": [
            "Trying to use LIMIT per group (LIMIT does not work per partition).",
            "Forgetting to filter for active accounts.",
        ],
        "concept_tags": ["ROW_NUMBER", "CTE", "top-N-per-group", "PARTITION BY"],
    },
    {
        "id": "fi-074",
        "slug": "month-over-month-transaction-growth",
        "title": "Month-over-Month Transaction Growth Rate",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Compute the month-over-month growth rate of total transaction amounts. "
            "CTE: aggregate total amount per month. Main query: use LAG to get "
            "the previous month's total, then compute growth_rate as "
            "(current - previous) / previous * 100, rounded to 1 decimal. "
            "Sort by month."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH monthly AS (\n"
            "    SELECT SUBSTR(transaction_date, 1, 7) AS month,\n"
            "           SUM(amount) AS total_amount\n"
            "    FROM transactions\n"
            "    GROUP BY SUBSTR(transaction_date, 1, 7)\n"
            ")\n"
            "SELECT month, total_amount,\n"
            "       LAG(total_amount) OVER (ORDER BY month) AS prev_month_amount,\n"
            "       ROUND(\n"
            "           (total_amount - LAG(total_amount) OVER (ORDER BY month))\n"
            "           * 100.0 / LAG(total_amount) OVER (ORDER BY month),\n"
            "       1) AS growth_rate\n"
            "FROM monthly\n"
            "ORDER BY month;"
        ),
        "hints": [
            "First aggregate totals per month in a CTE.",
            "LAG gets the previous month's total in the main query.",
            "Growth rate = (current - previous) / previous * 100.",
            "The first month will have NULL for growth_rate since there is no previous month.",
        ],
        "explanation": (
            "1. CTE computes monthly transaction totals.\n"
            "2. LAG(total_amount) gets the prior month's value.\n"
            "3. The growth formula computes percentage change.\n"
            "4. First month has NULL growth rate (no predecessor)."
        ),
        "approach": [
            "CTE: monthly aggregation.",
            "LAG window function for prior month.",
            "Compute growth rate formula.",
        ],
        "common_mistakes": [
            "Division by zero if previous month had zero transactions.",
            "Using LEAD instead of LAG.",
            "Integer division — multiply by 100.0 not 100.",
        ],
        "concept_tags": ["CTE", "LAG", "window function", "growth rate", "arithmetic"],
    },
    {
        "id": "fi-075",
        "slug": "cumulative-loan-disbursement",
        "title": "Cumulative Loan Disbursements by Month",
        "difficulty": "medium",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The finance team wants a monthly view of loan disbursements with a "
            "running total. For each month (YYYY-MM from start_date), return the "
            "month, the count of new loans, total principal disbursed that month, "
            "and a cumulative principal total. Sort by month."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT SUBSTR(start_date, 1, 7) AS month,\n"
            "       COUNT(*) AS loan_count,\n"
            "       SUM(principal) AS monthly_principal,\n"
            "       SUM(SUM(principal)) OVER (\n"
            "           ORDER BY SUBSTR(start_date, 1, 7)\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS cumulative_principal\n"
            "FROM loans\n"
            "GROUP BY SUBSTR(start_date, 1, 7)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "First GROUP BY month to aggregate loan counts and principals.",
            "Apply SUM as a window function over the grouped results for cumulative total.",
            "SUM(SUM(principal)) OVER (...) nests an aggregate inside a window function.",
            "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW creates the running total.",
        ],
        "explanation": (
            "1. GROUP BY month aggregates loan data per month.\n"
            "2. SUM(SUM(principal)) OVER (...) applies a window function over the grouped result.\n"
            "3. The running total accumulates all prior months' disbursements."
        ),
        "approach": [
            "Group by month with COUNT and SUM.",
            "Apply cumulative SUM as a window function.",
            "Sort by month.",
        ],
        "common_mistakes": [
            "Not realizing you can nest aggregates inside window functions.",
            "Omitting the frame clause.",
        ],
        "concept_tags": ["GROUP BY", "window function", "SUM", "running total", "ROWS BETWEEN"],
    },
    {
        "id": "fi-076",
        "slug": "customers-all-account-types",
        "title": "Customers with Every Account Type",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "Find customers who have at least one account of every possible type "
            "(checking, savings, investment, credit). Return customer_id, "
            "first_name, and last_name. Sort by last_name."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(DISTINCT a.account_type) = 4\n"
            "ORDER BY c.last_name;"
        ),
        "hints": [
            "There are 4 possible account types in the schema.",
            "COUNT(DISTINCT account_type) per customer tells you how many types they hold.",
            "HAVING filters grouped results on aggregate conditions.",
            "If a customer has all 4 distinct types, the count equals 4.",
        ],
        "explanation": (
            "1. JOIN customers to accounts.\n"
            "2. GROUP BY customer to count their distinct account types.\n"
            "3. HAVING COUNT(DISTINCT account_type) = 4 finds customers with all 4 types.\n"
            "4. This assumes the schema has exactly 4 account types."
        ),
        "approach": [
            "Join and group by customer.",
            "Count distinct account types.",
            "Filter for count = 4.",
        ],
        "common_mistakes": [
            "Hardcoding the count wrong (there are 4 types, not 3).",
            "Using COUNT without DISTINCT, which counts total accounts not types.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT", "relational division"],
    },
    {
        "id": "fi-077",
        "slug": "gap-detection-payments",
        "title": "Detect Payment Gaps Over 60 Days",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The collections team wants to find loan payments that came more than "
            "60 days after the previous payment on the same loan. Use LAG to "
            "get the previous payment date, then compute the gap in days. "
            "Return loan_id, payment_date, prev_payment_date, and gap_days. "
            "Only include rows where gap_days > 60. Sort by gap_days descending."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT loan_id, payment_date, prev_payment_date, gap_days\n"
            "FROM (\n"
            "    SELECT loan_id, payment_date,\n"
            "           LAG(payment_date) OVER (PARTITION BY loan_id ORDER BY payment_date) AS prev_payment_date,\n"
            "           CAST(julianday(payment_date)\n"
            "                - julianday(LAG(payment_date) OVER (PARTITION BY loan_id ORDER BY payment_date))\n"
            "                AS INTEGER) AS gap_days\n"
            "    FROM payments\n"
            ") sub\n"
            "WHERE gap_days > 60\n"
            "ORDER BY gap_days DESC;"
        ),
        "hints": [
            "LAG(payment_date) OVER (PARTITION BY loan_id ORDER BY payment_date) gets the previous payment.",
            "julianday difference gives the number of days between dates.",
            "Wrap in a subquery to filter on gap_days.",
            "The first payment per loan has NULL for prev_payment_date.",
        ],
        "explanation": (
            "1. LAG gets the previous payment date per loan.\n"
            "2. julianday computes the day gap.\n"
            "3. Subquery allows filtering WHERE gap_days > 60.\n"
            "4. This detects late or missed payments."
        ),
        "approach": [
            "Use LAG partitioned by loan, ordered by date.",
            "Compute gap using julianday difference.",
            "Wrap and filter for gaps > 60 days.",
        ],
        "common_mistakes": [
            "Trying to filter on the window function directly in WHERE.",
            "Forgetting PARTITION BY, which compares across different loans.",
        ],
        "concept_tags": ["LAG", "window function", "julianday", "gap detection", "subquery"],
    },
    {
        "id": "fi-078",
        "slug": "account-balance-change-since-opening",
        "title": "Account Balance Change Since Opening",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "For each active account, compute the net change in balance by "
            "summing all transaction amounts. Return account id, account_type, "
            "current balance, net_transaction_total (sum of all transaction "
            "amounts), and the difference. Sort by the difference descending. "
            "Limit to 20."
        ),
        "schema_hint": ["accounts", "transactions"],
        "solution_query": (
            "SELECT a.id, a.account_type, a.balance,\n"
            "       COALESCE(SUM(t.amount), 0) AS net_transaction_total,\n"
            "       a.balance - COALESCE(SUM(t.amount), 0) AS difference\n"
            "FROM accounts a\n"
            "LEFT JOIN transactions t ON a.id = t.account_id\n"
            "WHERE a.status = 'active'\n"
            "GROUP BY a.id, a.account_type, a.balance\n"
            "ORDER BY difference DESC\n"
            "LIMIT 20;"
        ),
        "hints": [
            "LEFT JOIN to include accounts with no transactions.",
            "SUM all transaction amounts per account.",
            "COALESCE handles NULL for accounts with no transactions.",
            "The difference between current balance and net transactions may reveal adjustments.",
        ],
        "explanation": (
            "1. LEFT JOIN accounts to transactions.\n"
            "2. SUM(t.amount) totals all transactions per account.\n"
            "3. The difference between balance and net transactions shows unexplained changes.\n"
            "4. COALESCE handles accounts with no transactions."
        ),
        "approach": [
            "Left join and aggregate transactions.",
            "Compute the difference.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops accounts with no transactions.",
            "Forgetting COALESCE for NULL sums.",
        ],
        "concept_tags": ["LEFT JOIN", "SUM", "COALESCE", "GROUP BY", "arithmetic"],
    },
    {
        "id": "fi-079",
        "slug": "correlated-subquery-above-avg-per-type",
        "title": "Transactions Above Account Type Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "Find transactions whose amount exceeds the average transaction "
            "amount for their account's type. Join transactions to accounts "
            "to get the type, then use a correlated subquery comparing against "
            "the average for that type. Return transaction id, account_type, "
            "amount, and the type_avg. Sort by amount DESC. Limit to 30."
        ),
        "schema_hint": ["transactions", "accounts"],
        "solution_query": (
            "SELECT t.id, a.account_type, t.amount,\n"
            "       (SELECT ROUND(AVG(t2.amount), 2)\n"
            "        FROM transactions t2\n"
            "        JOIN accounts a2 ON t2.account_id = a2.id\n"
            "        WHERE a2.account_type = a.account_type) AS type_avg\n"
            "FROM transactions t\n"
            "JOIN accounts a ON t.account_id = a.id\n"
            "WHERE t.amount > (\n"
            "    SELECT AVG(t2.amount)\n"
            "    FROM transactions t2\n"
            "    JOIN accounts a2 ON t2.account_id = a2.id\n"
            "    WHERE a2.account_type = a.account_type\n"
            ")\n"
            "ORDER BY t.amount DESC\n"
            "LIMIT 30;"
        ),
        "hints": [
            "You need to know each transaction's account type via a join.",
            "The correlated subquery computes the average for the same account type.",
            "The subquery joins transactions to accounts to filter by type.",
            "To also display the average, include it as a correlated subquery in SELECT.",
        ],
        "explanation": (
            "1. Join transactions to accounts for the type.\n"
            "2. Correlated subquery computes AVG for the same account type.\n"
            "3. WHERE filters for above-average transactions.\n"
            "4. A SELECT subquery also returns the type_avg for display."
        ),
        "approach": [
            "Join transactions to accounts.",
            "Correlated subquery for per-type average.",
            "Filter and display.",
        ],
        "common_mistakes": [
            "Using a global average instead of per-type.",
            "Forgetting the join inside the correlated subquery.",
        ],
        "concept_tags": ["correlated subquery", "JOIN", "AVG", "WHERE"],
    },
    {
        "id": "fi-080",
        "slug": "customers-with-loans-no-payments",
        "title": "Customers with Active Loans but No Payments",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The collections team needs to find customers who have active loans "
            "but have never made a payment. Return first_name, last_name, "
            "loan_type, principal, and start_date. Sort by start_date."
        ),
        "schema_hint": ["customers", "loans", "payments"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, l.loan_type,\n"
            "       l.principal, l.start_date\n"
            "FROM customers c\n"
            "JOIN loans l ON c.id = l.customer_id\n"
            "LEFT JOIN payments p ON l.id = p.loan_id\n"
            "WHERE l.status = 'active'\n"
            "  AND p.id IS NULL\n"
            "ORDER BY l.start_date;"
        ),
        "hints": [
            "Join customers to loans, then LEFT JOIN to payments.",
            "LEFT JOIN with IS NULL check is the anti-join pattern.",
            "Filter for active loan status.",
            "If p.id IS NULL, no payment exists for that loan.",
        ],
        "explanation": (
            "1. JOIN customers to loans for customer details.\n"
            "2. LEFT JOIN loans to payments to detect missing payments.\n"
            "3. WHERE p.id IS NULL finds loans with no payments.\n"
            "4. AND l.status = 'active' restricts to current loans."
        ),
        "approach": [
            "Chain joins: customers -> loans -> payments (LEFT).",
            "Filter for active loans with no payments.",
            "Sort by start date.",
        ],
        "common_mistakes": [
            "Using INNER JOIN for payments, which excludes the loans we want to find.",
            "Checking for NULL on the wrong column.",
        ],
        "concept_tags": ["LEFT JOIN", "anti-join", "IS NULL", "multi-table join"],
    },

    # =========================================================================
    # LEVEL 11 — MIXED DIFFICULTY EXPANSION (fi-081 through fi-105)
    # =========================================================================

    # --- 4 Easy SELECT/WHERE problems (fi-081 to fi-084) ---
    {
        "id": "fi-081",
        "slug": "savings-accounts-above-threshold",
        "title": "Savings Accounts with Balance Over 10000",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The branch manager wants a list of all savings accounts with a "
            "balance exceeding $10,000. Return the account id, customer_id, "
            "balance, and opened_at. Sort by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, balance, opened_at\n"
            "FROM accounts\n"
            "WHERE account_type = 'savings' AND balance > 10000\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "Filter on account_type and balance in the WHERE clause.",
            "Use AND to combine multiple conditions.",
            "ORDER BY balance DESC puts the largest balances first.",
            "No joins needed — all data is in the accounts table.",
        ],
        "explanation": (
            "1. WHERE filters for savings accounts with balance > 10000.\n"
            "2. ORDER BY balance DESC sorts from highest to lowest.\n"
            "3. This is a straightforward single-table filter query."
        ),
        "approach": [
            "Filter accounts by type and balance threshold.",
            "Sort by balance in descending order.",
        ],
        "common_mistakes": [
            "Forgetting to filter by account_type, returning all account types.",
            "Using >= instead of > if the requirement says 'exceeding'.",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "ORDER BY"],
    },
    {
        "id": "fi-082",
        "slug": "expired-cards-list",
        "title": "List All Expired Cards",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The compliance department needs a report of all cards that have "
            "expired. Return card id, account_id, card_number, card_type, "
            "and expiry_date for cards where the status is 'expired'. "
            "Sort by expiry_date ascending."
        ),
        "schema_hint": ["cards"],
        "solution_query": (
            "SELECT id, account_id, card_number, card_type, expiry_date\n"
            "FROM cards\n"
            "WHERE status = 'expired'\n"
            "ORDER BY expiry_date;"
        ),
        "hints": [
            "Filter on the status column for 'expired'.",
            "No date comparison is needed — just check the status field.",
            "ORDER BY expiry_date defaults to ascending.",
            "All data comes from the cards table.",
        ],
        "explanation": (
            "1. WHERE status = 'expired' filters for expired cards.\n"
            "2. ORDER BY expiry_date sorts chronologically.\n"
            "3. This is a simple single-table query with equality filter."
        ),
        "approach": [
            "Select the required columns from cards.",
            "Filter where status equals 'expired'.",
            "Sort by expiry date.",
        ],
        "common_mistakes": [
            "Comparing expiry_date to the current date instead of using the status field.",
            "Misspelling the status value string.",
        ],
        "concept_tags": ["SELECT", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-083",
        "slug": "recent-large-transactions",
        "title": "Large Transactions in the Last 30 Days",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The fraud monitoring team wants to review all large deposit "
            "transactions (amount > 5,000 and type = 'deposit'). Return transaction id, "
            "account_id, transaction_date, amount, and description. Sort by amount "
            "descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT id, account_id, transaction_date, amount, description\n"
            "FROM transactions\n"
            "WHERE amount > 5000\n"
            "  AND type = 'deposit'\n"
            "ORDER BY amount DESC;"
        ),
        "hints": [
            "Filter on both amount and type columns.",
            "Combine conditions with AND.",
            "Sort by amount DESC to see the largest first.",
            "No joins needed — all data is in the transactions table.",
        ],
        "explanation": (
            "1. WHERE amount > 5000 filters for large transactions.\n"
            "2. AND type = 'deposit' limits to deposits only.\n"
            "3. ORDER BY amount DESC shows largest deposits first."
        ),
        "approach": [
            "Filter transactions by amount and type.",
            "Sort by amount descending.",
        ],
        "common_mistakes": [
            "Forgetting to filter by type, which includes all transaction types.",
            "Using OR instead of AND, which broadens the filter incorrectly.",
        ],
        "concept_tags": ["SELECT", "WHERE", "DATE", "ORDER BY"],
    },
    {
        "id": "fi-084",
        "slug": "customers-born-in-1990s",
        "title": "Customers Born in the 1990s",
        "difficulty": "easy",
        "category": "select",
        "dataset": "finance",
        "description": (
            "The marketing team wants to target customers born between 1990 "
            "and 1999 (inclusive). Return first_name, last_name, email, and "
            "date_of_birth. Sort by date_of_birth ascending."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name, email, date_of_birth\n"
            "FROM customers\n"
            "WHERE date_of_birth >= '1990-01-01'\n"
            "  AND date_of_birth < '2000-01-01'\n"
            "ORDER BY date_of_birth;"
        ),
        "hints": [
            "Use a range filter on date_of_birth for the 1990s decade.",
            "ISO date strings compare correctly in SQLite.",
            "Use >= '1990-01-01' AND < '2000-01-01' for the full decade.",
            "BETWEEN could also work: BETWEEN '1990-01-01' AND '1999-12-31'.",
        ],
        "explanation": (
            "1. The WHERE clause defines a date range for the 1990s.\n"
            "2. Using >= and < avoids edge case issues with BETWEEN.\n"
            "3. ISO format dates compare lexicographically in SQLite."
        ),
        "approach": [
            "Filter customers by date_of_birth range.",
            "Sort by date_of_birth ascending.",
        ],
        "common_mistakes": [
            "Using YEAR() function which does not exist natively in SQLite.",
            "Off-by-one error on the decade boundary.",
        ],
        "concept_tags": ["SELECT", "WHERE", "date range", "ORDER BY"],
    },

    # --- 4 Medium Aggregation problems (fi-085 to fi-088) ---
    {
        "id": "fi-085",
        "slug": "average-loan-principal-by-type",
        "title": "Average Loan Principal by Loan Type",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The risk team needs the average principal amount for each loan "
            "type. Return loan_type, the count of loans, and the average "
            "principal rounded to 2 decimals (avg_principal). Only include "
            "loan types with more than 5 loans. Sort by avg_principal descending."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT loan_type,\n"
            "       COUNT(*) AS loan_count,\n"
            "       ROUND(AVG(principal), 2) AS avg_principal\n"
            "FROM loans\n"
            "GROUP BY loan_type\n"
            "HAVING COUNT(*) > 5\n"
            "ORDER BY avg_principal DESC;"
        ),
        "hints": [
            "GROUP BY loan_type to aggregate per type.",
            "AVG(principal) computes the average principal.",
            "HAVING filters groups after aggregation.",
            "ROUND formats the result to 2 decimal places.",
        ],
        "explanation": (
            "1. GROUP BY loan_type creates one row per loan type.\n"
            "2. COUNT(*) counts loans, AVG(principal) averages them.\n"
            "3. HAVING COUNT(*) > 5 excludes small groups.\n"
            "4. ROUND formats the average to 2 decimals."
        ),
        "approach": [
            "Group by loan type.",
            "Compute COUNT and AVG aggregates.",
            "Filter with HAVING, sort by average.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING for aggregate filters.",
            "Forgetting ROUND, producing many decimal places.",
        ],
        "concept_tags": ["GROUP BY", "AVG", "COUNT", "HAVING", "ROUND"],
    },
    {
        "id": "fi-086",
        "slug": "monthly-transaction-count-and-volume",
        "title": "Monthly Transaction Count and Volume",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The operations team wants a monthly summary of transaction "
            "activity. For each month (YYYY-MM extracted from transaction_date), "
            "return the month, total number of transactions (tx_count), total "
            "amount (total_volume), and the average amount (avg_amount) rounded "
            "to 2 decimals. Sort by month."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT SUBSTR(transaction_date, 1, 7) AS month,\n"
            "       COUNT(*) AS tx_count,\n"
            "       SUM(amount) AS total_volume,\n"
            "       ROUND(AVG(amount), 2) AS avg_amount\n"
            "FROM transactions\n"
            "GROUP BY SUBSTR(transaction_date, 1, 7)\n"
            "ORDER BY month;"
        ),
        "hints": [
            "SUBSTR(transaction_date, 1, 7) extracts YYYY-MM.",
            "GROUP BY the extracted month to aggregate per period.",
            "COUNT, SUM, and AVG provide different perspectives on the data.",
            "The GROUP BY expression must match the SELECT expression.",
        ],
        "explanation": (
            "1. SUBSTR extracts the year-month portion of the date.\n"
            "2. GROUP BY month aggregates all metrics per month.\n"
            "3. COUNT, SUM, and AVG give count, volume, and average."
        ),
        "approach": [
            "Extract month from date using SUBSTR.",
            "Group and aggregate with COUNT, SUM, AVG.",
            "Sort chronologically.",
        ],
        "common_mistakes": [
            "Using MONTH() or DATE_TRUNC() which are not available in SQLite.",
            "Grouping by the alias instead of the expression (works in SQLite but not all databases).",
        ],
        "concept_tags": ["GROUP BY", "SUBSTR", "COUNT", "SUM", "AVG", "ROUND"],
    },
    {
        "id": "fi-087",
        "slug": "branch-with-most-accounts",
        "title": "Branch with the Most Customer Accounts",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "Management wants to know which branch city has the most customer "
            "accounts. Count the number of accounts per branch city by joining "
            "customers to accounts and matching customer city to branch city. "
            "Return city, branch name, and account_count. Sort by account_count "
            "descending. Limit to 10."
        ),
        "schema_hint": ["branches", "customers", "accounts"],
        "solution_query": (
            "SELECT b.city, b.name AS branch_name,\n"
            "       COUNT(a.id) AS account_count\n"
            "FROM branches b\n"
            "JOIN customers c ON b.city = c.city\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY b.city, b.name\n"
            "ORDER BY account_count DESC\n"
            "LIMIT 10;"
        ),
        "hints": [
            "Join branches to customers on city, then customers to accounts.",
            "COUNT(a.id) counts the accounts per branch city.",
            "GROUP BY branch city and name to aggregate.",
            "This uses a non-key join (city) between branches and customers.",
        ],
        "explanation": (
            "1. JOIN branches to customers on city links geographic data.\n"
            "2. JOIN customers to accounts connects to account data.\n"
            "3. GROUP BY city and branch name aggregates account counts.\n"
            "4. ORDER BY and LIMIT give the top branches."
        ),
        "approach": [
            "Chain joins: branches -> customers (on city) -> accounts.",
            "Group by branch and count accounts.",
            "Sort descending, limit to top 10.",
        ],
        "common_mistakes": [
            "Joining on id instead of city between branches and customers.",
            "Forgetting to group by both city and branch name.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT", "ORDER BY", "LIMIT"],
    },
    {
        "id": "fi-088",
        "slug": "total-interest-paid-per-loan-type",
        "title": "Total Interest Paid by Loan Type",
        "difficulty": "medium",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The finance department wants to know how much interest has been "
            "collected for each loan type. Join loans to payments and sum the "
            "interest_paid column per loan_type. Return loan_type, the number "
            "of payments (payment_count), and total_interest_collected rounded "
            "to 2 decimals. Sort by total_interest_collected descending."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.loan_type,\n"
            "       COUNT(p.id) AS payment_count,\n"
            "       ROUND(SUM(p.interest_paid), 2) AS total_interest_collected\n"
            "FROM loans l\n"
            "JOIN payments p ON l.id = p.loan_id\n"
            "GROUP BY l.loan_type\n"
            "ORDER BY total_interest_collected DESC;"
        ),
        "hints": [
            "Join loans to payments on loan_id.",
            "SUM(interest_paid) gives total interest per group.",
            "GROUP BY loan_type aggregates across all loans of that type.",
            "ROUND formats the monetary output.",
        ],
        "explanation": (
            "1. JOIN loans to payments to access interest_paid.\n"
            "2. GROUP BY loan_type aggregates across types.\n"
            "3. SUM(interest_paid) totals the interest collected.\n"
            "4. COUNT(p.id) shows how many payments contributed."
        ),
        "approach": [
            "Join loans to payments.",
            "Group by loan type, aggregate interest.",
            "Sort by total interest descending.",
        ],
        "common_mistakes": [
            "Summing amount instead of interest_paid.",
            "Using LEFT JOIN when we only want loans that have payments.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "SUM", "COUNT", "ROUND"],
    },

    # --- 4 Medium Join problems (fi-089 to fi-092) ---
    {
        "id": "fi-089",
        "slug": "customer-card-details",
        "title": "Customer Card Details Report",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card services team needs a report linking customers to their "
            "cards. Join customers to accounts to cards. Return first_name, "
            "last_name, account_type, card_number, card_type, and "
            "card status. Only include active cards. Sort by last_name, "
            "first_name. Limit to 50."
        ),
        "schema_hint": ["customers", "accounts", "cards"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, a.account_type,\n"
            "       cr.card_number, cr.card_type, cr.status\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN cards cr ON a.id = cr.account_id\n"
            "WHERE cr.status = 'active'\n"
            "ORDER BY c.last_name, c.first_name\n"
            "LIMIT 50;"
        ),
        "hints": [
            "Chain three tables: customers -> accounts -> cards.",
            "Cards are linked to accounts, not directly to customers.",
            "Filter on card status in the WHERE clause.",
            "Sort alphabetically by last name then first name.",
        ],
        "explanation": (
            "1. JOIN customers to accounts, then accounts to cards.\n"
            "2. WHERE cr.status = 'active' filters for active cards.\n"
            "3. The three-table chain connects customers to their cards."
        ),
        "approach": [
            "Chain joins through accounts to reach cards.",
            "Filter for active card status.",
            "Sort alphabetically and limit.",
        ],
        "common_mistakes": [
            "Trying to join cards directly to customers (no direct relationship).",
            "Forgetting the intermediate accounts table in the join chain.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-090",
        "slug": "loans-with-latest-payment",
        "title": "Each Loan with Its Most Recent Payment",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "For each loan, show the most recent payment date and amount. "
            "Use a subquery to find the max payment_date per loan, then join "
            "back to get the payment details. Return loan_id, loan_type, "
            "principal, payment_date, and payment amount. Sort by payment_date "
            "descending. Limit to 30."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.id AS loan_id, l.loan_type, l.principal,\n"
            "       p.payment_date, p.amount\n"
            "FROM loans l\n"
            "JOIN payments p ON l.id = p.loan_id\n"
            "WHERE p.payment_date = (\n"
            "    SELECT MAX(p2.payment_date)\n"
            "    FROM payments p2\n"
            "    WHERE p2.loan_id = l.id\n"
            ")\n"
            "ORDER BY p.payment_date DESC\n"
            "LIMIT 30;"
        ),
        "hints": [
            "A correlated subquery finds the MAX payment_date per loan.",
            "Join loans to payments, then filter for the max date.",
            "The subquery references the outer query's loan id.",
            "This returns one row per loan (assuming unique max dates).",
        ],
        "explanation": (
            "1. JOIN loans to payments.\n"
            "2. Correlated subquery finds MAX(payment_date) per loan.\n"
            "3. WHERE filters for only the most recent payment per loan.\n"
            "4. Sort by payment date descending for recent-first ordering."
        ),
        "approach": [
            "Join loans to payments.",
            "Use correlated subquery for max date per loan.",
            "Filter and sort.",
        ],
        "common_mistakes": [
            "Using a non-correlated subquery that returns a single global max.",
            "Forgetting that ties on payment_date could produce multiple rows.",
        ],
        "concept_tags": ["JOIN", "correlated subquery", "MAX", "WHERE"],
    },
    {
        "id": "fi-091",
        "slug": "accounts-without-cards",
        "title": "Accounts That Have No Cards Issued",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "The card operations team wants to identify accounts that have "
            "never been issued a card. Use a LEFT JOIN from accounts to cards "
            "and filter for NULL. Return account id, customer_id, account_type, "
            "balance, and status. Sort by balance descending. Limit to 30."
        ),
        "schema_hint": ["accounts", "cards"],
        "solution_query": (
            "SELECT a.id, a.customer_id, a.account_type,\n"
            "       a.balance, a.status\n"
            "FROM accounts a\n"
            "LEFT JOIN cards cr ON a.id = cr.account_id\n"
            "WHERE cr.id IS NULL\n"
            "ORDER BY a.balance DESC\n"
            "LIMIT 30;"
        ),
        "hints": [
            "LEFT JOIN keeps all accounts, even without matching cards.",
            "WHERE cr.id IS NULL finds accounts with no card matches.",
            "This is the anti-join pattern.",
            "Sort by balance to highlight high-value uncarded accounts.",
        ],
        "explanation": (
            "1. LEFT JOIN accounts to cards preserves all accounts.\n"
            "2. WHERE cr.id IS NULL filters for accounts with no cards.\n"
            "3. This anti-join pattern is a standard way to find missing relationships."
        ),
        "approach": [
            "Left join accounts to cards.",
            "Filter for NULL card id.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which excludes the accounts we want to find.",
            "Checking IS NULL on the wrong column.",
        ],
        "concept_tags": ["LEFT JOIN", "anti-join", "IS NULL", "ORDER BY"],
    },
    {
        "id": "fi-092",
        "slug": "customer-total-balances-with-branch",
        "title": "Customer Total Balance with Branch Info",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "finance",
        "description": (
            "Create a report showing each customer's total account balance "
            "alongside their local branch info. Join customers to accounts "
            "(summing balance) and to branches (on city). Return first_name, "
            "last_name, city, branch name, and total_balance. Sort by "
            "total_balance descending. Limit to 25."
        ),
        "schema_hint": ["customers", "accounts", "branches"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, c.city,\n"
            "       b.name AS branch_name,\n"
            "       SUM(a.balance) AS total_balance\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN branches b ON c.city = b.city\n"
            "GROUP BY c.id, c.first_name, c.last_name, c.city, b.name\n"
            "ORDER BY total_balance DESC\n"
            "LIMIT 25;"
        ),
        "hints": [
            "Join customers to accounts for balances, and to branches on city.",
            "SUM(a.balance) aggregates across all accounts per customer.",
            "GROUP BY customer and branch to avoid duplication.",
            "The branch join uses city as a non-key join column.",
        ],
        "explanation": (
            "1. JOIN customers to accounts for balance data.\n"
            "2. JOIN customers to branches on city for branch details.\n"
            "3. GROUP BY and SUM aggregate total balance per customer.\n"
            "4. Sort by total balance to see wealthiest customers first."
        ),
        "approach": [
            "Multi-table join: customers -> accounts + branches.",
            "Aggregate balance per customer.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY, leading to incorrect sums if a customer has multiple accounts.",
            "Not grouping by branch name, causing errors with multiple branches per city.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "SUM", "non-key join", "ORDER BY"],
    },

    # --- 4 Medium Subquery problems (fi-093 to fi-096) ---
    {
        "id": "fi-093",
        "slug": "accounts-above-average-balance",
        "title": "Accounts with Balance Above Overall Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The wealth management team wants to identify accounts whose "
            "balance exceeds the bank-wide average balance. Use a scalar "
            "subquery in the WHERE clause. Return account id, customer_id, "
            "account_type, and balance. Sort by balance descending. Limit to 30."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, account_type, balance\n"
            "FROM accounts\n"
            "WHERE balance > (SELECT AVG(balance) FROM accounts)\n"
            "ORDER BY balance DESC\n"
            "LIMIT 30;"
        ),
        "hints": [
            "A scalar subquery computes the overall average balance.",
            "The outer query filters for accounts above that average.",
            "The subquery runs once and returns a single value.",
            "No joins needed — both queries reference accounts.",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(balance) FROM accounts) computes the global average.\n"
            "2. The outer WHERE filters for balances above that average.\n"
            "3. This is a non-correlated scalar subquery — it runs once."
        ),
        "approach": [
            "Write a scalar subquery for the average balance.",
            "Use it in the WHERE clause of the outer query.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Trying to use AVG directly in WHERE without a subquery.",
            "Confusing this with a correlated subquery (this one is non-correlated).",
        ],
        "concept_tags": ["scalar subquery", "AVG", "WHERE", "ORDER BY"],
    },
    {
        "id": "fi-094",
        "slug": "customers-with-multiple-active-loans",
        "title": "Customers Who Have Multiple Active Loans",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The credit risk team needs to find customers who have more than "
            "one active loan. Use a subquery with GROUP BY and HAVING to "
            "identify qualifying customer_ids, then join to customers for "
            "details. Return first_name, last_name, and the number of active "
            "loans (active_loan_count). Sort by active_loan_count descending."
        ),
        "schema_hint": ["customers", "loans"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, sub.active_loan_count\n"
            "FROM customers c\n"
            "JOIN (\n"
            "    SELECT customer_id, COUNT(*) AS active_loan_count\n"
            "    FROM loans\n"
            "    WHERE status = 'active'\n"
            "    GROUP BY customer_id\n"
            "    HAVING COUNT(*) > 1\n"
            ") sub ON c.id = sub.customer_id\n"
            "ORDER BY sub.active_loan_count DESC;"
        ),
        "hints": [
            "A derived table (subquery in FROM) counts active loans per customer.",
            "HAVING COUNT(*) > 1 filters for multiple active loans.",
            "Join the derived table to customers for name details.",
            "Filter for status = 'active' inside the subquery.",
        ],
        "explanation": (
            "1. The subquery groups loans by customer, counting active ones.\n"
            "2. HAVING COUNT(*) > 1 keeps only customers with multiple active loans.\n"
            "3. JOIN to customers retrieves first and last names."
        ),
        "approach": [
            "Subquery: count active loans per customer with HAVING.",
            "Join result to customers for names.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Filtering status in the outer query instead of the subquery.",
            "Using WHERE instead of HAVING for aggregate conditions.",
        ],
        "concept_tags": ["derived table", "GROUP BY", "HAVING", "JOIN", "COUNT"],
    },
    {
        "id": "fi-095",
        "slug": "highest-single-transaction-per-customer",
        "title": "Highest Single Transaction per Customer",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "For each customer, find their single largest transaction amount. "
            "Use a correlated subquery to get the max transaction amount per "
            "customer. Return first_name, last_name, and max_transaction. "
            "Only include customers with at least one transaction. Sort by "
            "max_transaction descending. Limit to 20."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       (SELECT MAX(t.amount)\n"
            "        FROM transactions t\n"
            "        JOIN accounts a ON t.account_id = a.id\n"
            "        WHERE a.customer_id = c.id) AS max_transaction\n"
            "FROM customers c\n"
            "WHERE (SELECT MAX(t.amount)\n"
            "       FROM transactions t\n"
            "       JOIN accounts a ON t.account_id = a.id\n"
            "       WHERE a.customer_id = c.id) IS NOT NULL\n"
            "ORDER BY max_transaction DESC\n"
            "LIMIT 20;"
        ),
        "hints": [
            "A correlated subquery in SELECT computes the max per customer.",
            "The subquery must join transactions to accounts to reach customer_id.",
            "Filter out NULLs (customers with no transactions) in WHERE.",
            "The correlated subquery references c.id from the outer query.",
        ],
        "explanation": (
            "1. Correlated subquery joins transactions through accounts to find MAX amount.\n"
            "2. The subquery is correlated on customer_id = c.id.\n"
            "3. WHERE IS NOT NULL excludes customers without transactions.\n"
            "4. Sort by max_transaction descending for highest first."
        ),
        "approach": [
            "Correlated subquery in SELECT for max transaction.",
            "Same subquery in WHERE to filter out NULLs.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Forgetting the accounts join inside the subquery.",
            "Not handling NULL for customers without transactions.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "JOIN", "IS NOT NULL"],
    },
    {
        "id": "fi-096",
        "slug": "loans-with-above-avg-interest-rate",
        "title": "Loans with Interest Rate Above Their Type Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "finance",
        "description": (
            "The pricing team wants to find loans whose interest rate exceeds "
            "the average rate for their loan type. Use a correlated subquery. "
            "Return loan id, loan_type, interest_rate, and the type_avg_rate "
            "rounded to 2 decimals. Sort by interest_rate descending. Limit to 25."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT l.id, l.loan_type, l.interest_rate,\n"
            "       (SELECT ROUND(AVG(l2.interest_rate), 2)\n"
            "        FROM loans l2\n"
            "        WHERE l2.loan_type = l.loan_type) AS type_avg_rate\n"
            "FROM loans l\n"
            "WHERE l.interest_rate > (\n"
            "    SELECT AVG(l2.interest_rate)\n"
            "    FROM loans l2\n"
            "    WHERE l2.loan_type = l.loan_type\n"
            ")\n"
            "ORDER BY l.interest_rate DESC\n"
            "LIMIT 25;"
        ),
        "hints": [
            "A correlated subquery computes the average rate for the same loan type.",
            "The subquery filters WHERE l2.loan_type = l.loan_type.",
            "Include the type_avg_rate in SELECT for comparison.",
            "This runs the subquery once per row in the outer query.",
        ],
        "explanation": (
            "1. Correlated subquery computes AVG interest_rate per loan type.\n"
            "2. WHERE filters for loans above their type's average.\n"
            "3. A SELECT subquery also returns the average for display.\n"
            "4. This identifies potentially overpriced loans."
        ),
        "approach": [
            "Correlated subquery for per-type average rate.",
            "Filter in WHERE, display in SELECT.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Computing a global average instead of per-type.",
            "Forgetting to round the display average.",
        ],
        "concept_tags": ["correlated subquery", "AVG", "ROUND", "WHERE"],
    },

    # --- 3 Hard Window Function problems (fi-097 to fi-099) ---
    {
        "id": "fi-097",
        "slug": "ntile-balance-quartiles",
        "title": "Account Balance Quartile Classification",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "The analytics team wants to divide all active accounts into 4 "
            "equal quartiles based on balance. Use a CTE to first assign quartiles "
            "with NTILE(4), then compute the min and max balance per quartile. "
            "Return account id, account_type, balance, balance_quartile, "
            "quartile_min, and quartile_max. Sort by balance DESC."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "WITH ranked AS (\n"
            "    SELECT id, account_type, balance,\n"
            "           NTILE(4) OVER (ORDER BY balance) AS balance_quartile\n"
            "    FROM accounts\n"
            "    WHERE status = 'active'\n"
            ")\n"
            "SELECT r.id, r.account_type, r.balance, r.balance_quartile,\n"
            "       MIN(r.balance) OVER (PARTITION BY r.balance_quartile) AS quartile_min,\n"
            "       MAX(r.balance) OVER (PARTITION BY r.balance_quartile) AS quartile_max\n"
            "FROM ranked r\n"
            "ORDER BY r.balance DESC;"
        ),
        "hints": [
            "NTILE(4) divides rows into 4 roughly equal buckets.",
            "You cannot nest window functions — use a CTE to compute NTILE first.",
            "Then use MIN/MAX OVER (PARTITION BY quartile) in the outer query.",
            "Quartile 1 has the lowest balances, quartile 4 the highest.",
        ],
        "explanation": (
            "1. CTE assigns each active account to one of 4 quartiles by balance using NTILE(4).\n"
            "2. Outer query computes MIN/MAX per quartile using PARTITION BY.\n"
            "3. This two-step approach avoids nesting window functions (which SQL does not allow)."
        ),
        "approach": [
            "Use a CTE to compute NTILE(4) quartile assignments.",
            "In the outer query, use MIN/MAX window functions partitioned by quartile.",
            "Filter for active accounts, sort by balance.",
        ],
        "common_mistakes": [
            "Trying to nest NTILE inside PARTITION BY — SQL doesn't allow window functions inside window functions.",
            "Confusing NTILE with PERCENT_RANK (NTILE assigns bucket numbers, not percentiles).",
        ],
        "concept_tags": ["NTILE", "window function", "MIN", "MAX", "PARTITION BY"],
    },
    {
        "id": "fi-098",
        "slug": "transaction-running-balance",
        "title": "Running Balance After Each Transaction",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "For account_id = 1, compute a running sum of transaction amounts "
            "ordered by transaction_date. Return the row number, transaction_date, "
            "type, amount, and running_total using a SUM window function with an "
            "appropriate frame (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW). "
            "Sort by transaction_date."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT ROW_NUMBER() OVER (ORDER BY transaction_date) AS row_num,\n"
            "       transaction_date, type, amount,\n"
            "       SUM(amount) OVER (\n"
            "           ORDER BY transaction_date\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS running_total\n"
            "FROM transactions\n"
            "WHERE account_id = 1\n"
            "ORDER BY transaction_date;"
        ),
        "hints": [
            "SUM as a window function with ROWS BETWEEN creates a running total.",
            "UNBOUNDED PRECEDING to CURRENT ROW accumulates all prior rows.",
            "ROW_NUMBER provides sequential numbering.",
            "Filter to a single account for a clear ledger view.",
        ],
        "explanation": (
            "1. SUM(amount) OVER (...) with a cumulative frame produces the running total.\n"
            "2. ROW_NUMBER numbers each transaction sequentially.\n"
            "3. The frame ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW includes all prior rows.\n"
            "4. This simulates a bank statement ledger."
        ),
        "approach": [
            "Filter to one account.",
            "Apply SUM window function with cumulative frame.",
            "Add ROW_NUMBER for sequential ordering.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS, which behaves differently with duplicate dates.",
            "Omitting the frame clause entirely (default frame may not be cumulative).",
        ],
        "concept_tags": ["SUM", "window function", "ROWS BETWEEN", "ROW_NUMBER", "running total"],
    },
    {
        "id": "fi-099",
        "slug": "dense-rank-transaction-amounts",
        "title": "Dense Rank Transactions by Amount per Account Type",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "finance",
        "description": (
            "Rank all transactions by amount within their account's type "
            "using DENSE_RANK. Join transactions to accounts. Return "
            "account_type, transaction id, amount, and the dense_rank. "
            "Only include the top 5 ranked transactions per account type. "
            "Sort by account_type, then rank."
        ),
        "schema_hint": ["transactions", "accounts"],
        "solution_query": (
            "SELECT account_type, tx_id, amount, dr\n"
            "FROM (\n"
            "    SELECT a.account_type, t.id AS tx_id, t.amount,\n"
            "           DENSE_RANK() OVER (\n"
            "               PARTITION BY a.account_type\n"
            "               ORDER BY t.amount DESC\n"
            "           ) AS dr\n"
            "    FROM transactions t\n"
            "    JOIN accounts a ON t.account_id = a.id\n"
            ") sub\n"
            "WHERE dr <= 5\n"
            "ORDER BY account_type, dr;"
        ),
        "hints": [
            "DENSE_RANK assigns the same rank to ties, with no gaps.",
            "PARTITION BY account_type ranks within each type.",
            "Wrap in a subquery to filter WHERE dr <= 5.",
            "DENSE_RANK may return more than 5 rows per type if there are ties.",
        ],
        "explanation": (
            "1. JOIN transactions to accounts for the account type.\n"
            "2. DENSE_RANK partitioned by type ranks transactions by amount.\n"
            "3. Subquery wrapper allows filtering for top 5 ranks.\n"
            "4. Unlike ROW_NUMBER, DENSE_RANK allows ties to share a rank."
        ),
        "approach": [
            "Join transactions to accounts.",
            "Apply DENSE_RANK partitioned by account type.",
            "Wrap in subquery, filter for rank <= 5.",
        ],
        "common_mistakes": [
            "Using ROW_NUMBER when ties should share a rank.",
            "Trying to filter on DENSE_RANK without a subquery or CTE.",
        ],
        "concept_tags": ["DENSE_RANK", "window function", "PARTITION BY", "top-N-per-group"],
    },

    # --- 3 Hard CTE problems (fi-100 to fi-102) ---
    {
        "id": "fi-100",
        "slug": "customer-account-summary-cte",
        "title": "Customer Account Summary with Multiple CTEs",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Build a comprehensive customer summary. CTE 1: account_summary — "
            "count accounts and sum balances per customer. CTE 2: loan_summary "
            "— count loans and sum principal per customer. Main query: join "
            "both CTEs to customers. Return first_name, last_name, "
            "account_count, total_balance, loan_count, total_principal. "
            "Include customers even if they have no loans. Sort by "
            "total_balance descending. Limit to 20."
        ),
        "schema_hint": ["customers", "accounts", "loans"],
        "solution_query": (
            "WITH account_summary AS (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS account_count,\n"
            "           SUM(balance) AS total_balance\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "loan_summary AS (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS loan_count,\n"
            "           SUM(principal) AS total_principal\n"
            "    FROM loans\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       COALESCE(ac.account_count, 0) AS account_count,\n"
            "       COALESCE(ac.total_balance, 0) AS total_balance,\n"
            "       COALESCE(ls.loan_count, 0) AS loan_count,\n"
            "       COALESCE(ls.total_principal, 0) AS total_principal\n"
            "FROM customers c\n"
            "LEFT JOIN account_summary ac ON c.id = ac.customer_id\n"
            "LEFT JOIN loan_summary ls ON c.id = ls.customer_id\n"
            "ORDER BY total_balance DESC\n"
            "LIMIT 20;"
        ),
        "hints": [
            "Use separate CTEs for account and loan aggregations.",
            "LEFT JOIN both CTEs to customers to include all customers.",
            "COALESCE handles NULLs for customers without accounts or loans.",
            "This avoids the fan-out problem of joining both tables directly.",
        ],
        "explanation": (
            "1. CTE account_summary aggregates accounts per customer.\n"
            "2. CTE loan_summary aggregates loans per customer.\n"
            "3. LEFT JOIN both CTEs to customers preserves all customers.\n"
            "4. COALESCE replaces NULLs with 0 for clean output."
        ),
        "approach": [
            "Two CTEs: one for accounts, one for loans.",
            "Left join both to customers.",
            "COALESCE for nulls, sort and limit.",
        ],
        "common_mistakes": [
            "Joining accounts and loans directly, causing cross-product multiplication.",
            "Using INNER JOIN which drops customers without accounts or loans.",
            "Forgetting COALESCE leading to NULL totals.",
        ],
        "concept_tags": ["CTE", "multiple CTEs", "LEFT JOIN", "COALESCE", "SUM", "COUNT"],
    },
    {
        "id": "fi-101",
        "slug": "recursive-payment-schedule",
        "title": "Recursive Loan Payment Schedule Projection",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Using a recursive CTE, generate a projected 12-month payment "
            "schedule for the loan with id = 1. Start with month 1 and the "
            "loan's monthly_payment and principal. Each month, compute the "
            "interest (remaining_balance * interest_rate / 12), principal_paid "
            "(monthly_payment - interest), and new remaining_balance. Return "
            "month_number, payment, interest, principal_paid, and "
            "remaining_balance rounded to 2 decimals."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "WITH RECURSIVE schedule AS (\n"
            "    SELECT 1 AS month_number,\n"
            "           monthly_payment AS payment,\n"
            "           ROUND(principal * interest_rate / 100.0 / 12, 2) AS interest,\n"
            "           ROUND(monthly_payment - principal * interest_rate / 100.0 / 12, 2) AS principal_paid,\n"
            "           ROUND(principal - (monthly_payment - principal * interest_rate / 100.0 / 12), 2) AS remaining_balance\n"
            "    FROM loans\n"
            "    WHERE id = 1\n"
            "    UNION ALL\n"
            "    SELECT month_number + 1,\n"
            "           payment,\n"
            "           ROUND(remaining_balance * (SELECT interest_rate FROM loans WHERE id = 1) / 100.0 / 12, 2),\n"
            "           ROUND(payment - remaining_balance * (SELECT interest_rate FROM loans WHERE id = 1) / 100.0 / 12, 2),\n"
            "           ROUND(remaining_balance - (payment - remaining_balance * (SELECT interest_rate FROM loans WHERE id = 1) / 100.0 / 12), 2)\n"
            "    FROM schedule\n"
            "    WHERE month_number < 12\n"
            ")\n"
            "SELECT month_number, payment, interest, principal_paid, remaining_balance\n"
            "FROM schedule;"
        ),
        "hints": [
            "A recursive CTE has an anchor member (month 1) and a recursive member.",
            "The anchor reads the loan details from the loans table.",
            "Each recursive step computes interest on the remaining balance.",
            "Stop recursion at month_number = 12.",
        ],
        "explanation": (
            "1. Anchor member: first month's payment breakdown from loan details.\n"
            "2. Recursive member: each subsequent month recalculates interest on remaining balance.\n"
            "3. Interest = remaining_balance * rate / 12.\n"
            "4. Principal_paid = payment - interest.\n"
            "5. Remaining_balance decreases each month."
        ),
        "approach": [
            "Anchor: compute first month from loans table.",
            "Recurse: recompute interest on new remaining balance.",
            "Stop at month 12.",
        ],
        "common_mistakes": [
            "Forgetting to divide interest_rate by 100 (it is stored as a percentage).",
            "Not rounding intermediate results, causing floating-point drift.",
            "Missing the termination condition (month_number < 12).",
        ],
        "concept_tags": ["recursive CTE", "UNION ALL", "arithmetic", "ROUND"],
    },
    {
        "id": "fi-102",
        "slug": "customer-transaction-category-breakdown-cte",
        "title": "Customer Spending by Category (CTE with Percentages)",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "finance",
        "description": (
            "Build a spending breakdown by transaction type for each customer. "
            "CTE 1: customer_totals — total transaction amount per customer. "
            "CTE 2: type_totals — total amount per customer per transaction type. "
            "Main query: join both to compute the percentage of spend in each "
            "type. Return first_name, last_name, type, type_amount, "
            "total_amount, and spend_pct rounded to 1 decimal. Sort by "
            "last_name, spend_pct descending. Limit to 50."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "WITH customer_totals AS (\n"
            "    SELECT a.customer_id,\n"
            "           SUM(t.amount) AS total_amount\n"
            "    FROM accounts a\n"
            "    JOIN transactions t ON a.id = t.account_id\n"
            "    GROUP BY a.customer_id\n"
            "),\n"
            "type_totals AS (\n"
            "    SELECT a.customer_id, t.type,\n"
            "           SUM(t.amount) AS type_amount\n"
            "    FROM accounts a\n"
            "    JOIN transactions t ON a.id = t.account_id\n"
            "    GROUP BY a.customer_id, t.type\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       tt.type, tt.type_amount,\n"
            "       cust.total_amount,\n"
            "       ROUND(tt.type_amount * 100.0 / cust.total_amount, 1) AS spend_pct\n"
            "FROM type_totals tt\n"
            "JOIN customer_totals cust ON tt.customer_id = cust.customer_id\n"
            "JOIN customers c ON tt.customer_id = c.id\n"
            "ORDER BY c.last_name, spend_pct DESC\n"
            "LIMIT 50;"
        ),
        "hints": [
            "CTE 1 computes total spend per customer across all transaction types.",
            "CTE 2 computes spend per customer per transaction type.",
            "Join both CTEs to compute percentage: type_amount / total * 100.",
            "Join to customers for names.",
        ],
        "explanation": (
            "1. CTE customer_totals: overall transaction volume per customer.\n"
            "2. CTE type_totals: breakdown per customer per transaction type.\n"
            "3. Main query divides type amount by total to get percentage.\n"
            "4. This reveals which transaction types dominate each customer's activity."
        ),
        "approach": [
            "Two CTEs for total and per-type aggregations.",
            "Join CTEs together and compute percentages.",
            "Join to customers for names, sort and limit.",
        ],
        "common_mistakes": [
            "Division by zero if a customer has zero total amount.",
            "Integer division — use 100.0 not 100.",
            "Forgetting the accounts join to reach customer_id.",
        ],
        "concept_tags": ["CTE", "multiple CTEs", "JOIN", "percentage", "ROUND"],
    },

    # --- 3 Hard Advanced problems (fi-103 to fi-105) ---
    {
        "id": "fi-103",
        "slug": "case-when-risk-classification",
        "title": "Loan Risk Classification with CASE",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The risk team needs loans classified into risk tiers. Use CASE "
            "WHEN to assign a risk_tier: 'High Risk' if interest_rate > 15 "
            "or the loan has no payments, 'Medium Risk' if interest_rate "
            "between 8 and 15, 'Low Risk' otherwise. Return loan id, "
            "loan_type, interest_rate, principal, payment_count, and "
            "risk_tier. Sort by risk_tier, interest_rate DESC. Limit to 40."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.id, l.loan_type, l.interest_rate, l.principal,\n"
            "       COUNT(p.id) AS payment_count,\n"
            "       CASE\n"
            "           WHEN l.interest_rate > 15 OR COUNT(p.id) = 0 THEN 'High Risk'\n"
            "           WHEN l.interest_rate BETWEEN 8 AND 15 THEN 'Medium Risk'\n"
            "           ELSE 'Low Risk'\n"
            "       END AS risk_tier\n"
            "FROM loans l\n"
            "LEFT JOIN payments p ON l.id = p.loan_id\n"
            "GROUP BY l.id, l.loan_type, l.interest_rate, l.principal\n"
            "ORDER BY risk_tier, l.interest_rate DESC\n"
            "LIMIT 40;"
        ),
        "hints": [
            "LEFT JOIN to payments and COUNT(p.id) detects loans with no payments.",
            "CASE WHEN evaluates conditions top to bottom — first match wins.",
            "GROUP BY is needed because of the COUNT aggregate.",
            "BETWEEN is inclusive on both ends.",
        ],
        "explanation": (
            "1. LEFT JOIN to payments to count payments per loan.\n"
            "2. GROUP BY loan to aggregate payment counts.\n"
            "3. CASE WHEN classifies based on interest rate and payment activity.\n"
            "4. High risk catches both high-rate loans and non-paying loans."
        ),
        "approach": [
            "Left join loans to payments, group by loan.",
            "Count payments per loan.",
            "CASE WHEN for risk tier classification.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which misses loans with no payments.",
            "Putting the CASE conditions in wrong order (first match wins).",
            "Forgetting GROUP BY when using COUNT.",
        ],
        "concept_tags": ["CASE WHEN", "LEFT JOIN", "COUNT", "GROUP BY", "BETWEEN"],
    },
    {
        "id": "fi-104",
        "slug": "exists-customers-with-all-products",
        "title": "Customers with Both Accounts and Loans (EXISTS)",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "The cross-sell team wants to identify customers who have at least "
            "one active account AND at least one active loan. Use EXISTS "
            "subqueries for both checks. Return first_name, last_name, and "
            "email. Sort by last_name, first_name."
        ),
        "schema_hint": ["customers", "accounts", "loans"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, c.email\n"
            "FROM customers c\n"
            "WHERE EXISTS (\n"
            "    SELECT 1 FROM accounts a\n"
            "    WHERE a.customer_id = c.id AND a.status = 'active'\n"
            ")\n"
            "AND EXISTS (\n"
            "    SELECT 1 FROM loans l\n"
            "    WHERE l.customer_id = c.id AND l.status = 'active'\n"
            ")\n"
            "ORDER BY c.last_name, c.first_name;"
        ),
        "hints": [
            "EXISTS returns TRUE if the subquery returns at least one row.",
            "Use two EXISTS subqueries combined with AND.",
            "SELECT 1 in the EXISTS subquery is a common convention.",
            "Each EXISTS is correlated — it references c.id from the outer query.",
        ],
        "explanation": (
            "1. First EXISTS checks for at least one active account.\n"
            "2. Second EXISTS checks for at least one active loan.\n"
            "3. Both must be true for the customer to be included.\n"
            "4. EXISTS is often more efficient than JOIN for existence checks."
        ),
        "approach": [
            "Two EXISTS subqueries: one for accounts, one for loans.",
            "Combine with AND in the WHERE clause.",
            "Sort alphabetically.",
        ],
        "common_mistakes": [
            "Using IN instead of EXISTS (less efficient for large datasets).",
            "Forgetting the correlation condition (customer_id = c.id).",
            "Not filtering for 'active' status in the subqueries.",
        ],
        "concept_tags": ["EXISTS", "correlated subquery", "AND", "ORDER BY"],
    },
    {
        "id": "fi-105",
        "slug": "complex-financial-dashboard",
        "title": "Executive Financial Dashboard Query",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "finance",
        "description": (
            "Build an executive dashboard row per customer showing: full_name, "
            "total_accounts, total_balance, total_loans, total_principal, "
            "total_cards, and a customer_segment classified as 'Premium' if "
            "total_balance > 50000, 'Standard' if > 10000, else 'Basic'. Use "
            "subqueries or left joins to gather all metrics. Include all "
            "customers. Sort by total_balance descending. Limit to 25."
        ),
        "schema_hint": ["customers", "accounts", "loans", "cards"],
        "solution_query": (
            "SELECT c.first_name || ' ' || c.last_name AS full_name,\n"
            "       COALESCE(acc.acct_count, 0) AS total_accounts,\n"
            "       COALESCE(acc.total_balance, 0) AS total_balance,\n"
            "       COALESCE(ln.loan_count, 0) AS total_loans,\n"
            "       COALESCE(ln.total_principal, 0) AS total_principal,\n"
            "       COALESCE(crd.card_count, 0) AS total_cards,\n"
            "       CASE\n"
            "           WHEN COALESCE(acc.total_balance, 0) > 50000 THEN 'Premium'\n"
            "           WHEN COALESCE(acc.total_balance, 0) > 10000 THEN 'Standard'\n"
            "           ELSE 'Basic'\n"
            "       END AS customer_segment\n"
            "FROM customers c\n"
            "LEFT JOIN (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS acct_count,\n"
            "           SUM(balance) AS total_balance\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            ") acc ON c.id = acc.customer_id\n"
            "LEFT JOIN (\n"
            "    SELECT customer_id,\n"
            "           COUNT(*) AS loan_count,\n"
            "           SUM(principal) AS total_principal\n"
            "    FROM loans\n"
            "    GROUP BY customer_id\n"
            ") ln ON c.id = ln.customer_id\n"
            "LEFT JOIN (\n"
            "    SELECT a.customer_id,\n"
            "           COUNT(cr.id) AS card_count\n"
            "    FROM accounts a\n"
            "    JOIN cards cr ON a.id = cr.account_id\n"
            "    GROUP BY a.customer_id\n"
            ") crd ON c.id = crd.customer_id\n"
            "ORDER BY total_balance DESC\n"
            "LIMIT 25;"
        ),
        "hints": [
            "Use derived tables (subqueries in FROM) to pre-aggregate each entity.",
            "LEFT JOIN all derived tables to customers to include everyone.",
            "COALESCE all aggregates to 0 for customers missing any entity.",
            "CASE WHEN on total_balance classifies the customer segment.",
        ],
        "explanation": (
            "1. Three derived tables aggregate accounts, loans, and cards per customer.\n"
            "2. LEFT JOIN all three to customers preserves all customers.\n"
            "3. COALESCE ensures zero instead of NULL.\n"
            "4. CASE WHEN classifies customers into segments based on balance.\n"
            "5. This avoids fan-out issues from joining un-aggregated tables."
        ),
        "approach": [
            "Three derived tables: accounts, loans, cards (through accounts).",
            "Left join all to customers.",
            "COALESCE for nulls, CASE for segmentation.",
            "Sort and limit.",
        ],
        "common_mistakes": [
            "Joining all tables directly without pre-aggregation (causes row multiplication).",
            "Using INNER JOIN which drops customers without certain products.",
            "Forgetting that cards connect through accounts, not directly to customers.",
        ],
        "concept_tags": ["derived table", "LEFT JOIN", "COALESCE", "CASE WHEN", "string concatenation"],
    },

    # =========================================================================
    # INTERVIEW-STYLE PROBLEMS (32 problems: interview-fin-001 through interview-fin-032)
    # =========================================================================

    # --- EASY (10 problems) ---

    {
        "id": "interview-fin-001",
        "slug": "int-fin-active-checking-accounts",
        "title": "Active Checking Accounts",
        "difficulty": "easy",
        "category": "filtering",
        "dataset": "finance",
        "description": (
            "A bank auditor needs a list of all checking accounts that are currently active. "
            "Return the account id, customer_id, balance, and opened_at for every account "
            "where account_type is 'checking' and status is 'active'. Order by balance descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, balance, opened_at\n"
            "FROM accounts\n"
            "WHERE account_type = 'checking'\n"
            "  AND status = 'active'\n"
            "ORDER BY balance DESC;"
        ),
        "hints": [
            "Filter on two conditions using AND.",
            "The account_type column stores values like 'checking', 'savings', etc.",
            "Use ORDER BY balance DESC to show highest balances first.",
            "SELECT id, customer_id, balance, opened_at FROM accounts WHERE ... ORDER BY ...;",
        ],
        "explanation": (
            "1. SELECT the requested columns from accounts.\n"
            "2. WHERE filters to checking accounts that are active.\n"
            "3. ORDER BY balance DESC puts the largest balances first."
        ),
        "approach": [
            "Identify the accounts table as the data source.",
            "Apply two WHERE conditions with AND.",
            "Sort results by balance in descending order.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, which returns all checking accounts plus all active accounts.",
            "Forgetting to specify the sort direction (DESC).",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "ORDER BY"],
    },
    {
        "id": "interview-fin-002",
        "slug": "int-fin-total-deposits-per-account",
        "title": "Total Deposits Per Account",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The finance team wants to know how much money has been deposited into each account. "
            "Write a query that returns the account_id and the total deposit amount for each account. "
            "Only include deposit transactions. Order by total deposits descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id, SUM(amount) AS total_deposits\n"
            "FROM transactions\n"
            "WHERE type = 'deposit'\n"
            "ORDER BY total_deposits DESC;"
        ),
        "hints": [
            "Filter for deposit transactions using WHERE.",
            "Use SUM to add up the amounts.",
            "GROUP BY account_id to get totals per account.",
            "SELECT account_id, SUM(amount) AS total_deposits FROM transactions WHERE type = 'deposit' GROUP BY ...;",
        ],
        "explanation": (
            "1. Filter transactions to only deposits with WHERE type = 'deposit'.\n"
            "2. GROUP BY account_id groups rows by account.\n"
            "3. SUM(amount) totals the deposit amounts per group."
        ),
        "approach": [
            "Filter for deposit type transactions.",
            "Group by account_id.",
            "Use SUM to aggregate the amounts.",
        ],
        "common_mistakes": [
            "Forgetting the WHERE clause and summing all transaction types.",
            "Using COUNT instead of SUM to get the total dollar amount.",
        ],
        "concept_tags": ["SUM", "GROUP BY", "WHERE", "aggregation"],
    },
    {
        "id": "interview-fin-003",
        "slug": "int-fin-customers-with-email-domain",
        "title": "Customers by Email Domain",
        "difficulty": "easy",
        "category": "string filtering",
        "dataset": "finance",
        "description": (
            "Marketing wants to find all customers who use Gmail. "
            "Return the first_name, last_name, and email of every customer "
            "whose email address ends with '@gmail.com'. Sort alphabetically by last_name."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM customers\n"
            "WHERE email LIKE '%@gmail.com'\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "Use the LIKE operator with a wildcard to match email patterns.",
            "The '%' wildcard matches any sequence of characters.",
            "Place '%' before '@gmail.com' to match any username.",
            "SELECT first_name, last_name, email FROM customers WHERE email LIKE ...;",
        ],
        "explanation": (
            "1. LIKE '%@gmail.com' matches any email ending with @gmail.com.\n"
            "2. The '%' wildcard at the start matches any characters before the domain.\n"
            "3. ORDER BY last_name sorts results alphabetically."
        ),
        "approach": [
            "Use the LIKE operator for pattern matching on the email column.",
            "Place the wildcard before the domain pattern.",
            "Apply alphabetical ordering on last_name.",
        ],
        "common_mistakes": [
            "Using '=' instead of LIKE, which would require an exact match.",
            "Forgetting the '%' wildcard, which would match only the literal string '@gmail.com'.",
        ],
        "concept_tags": ["LIKE", "WHERE", "string pattern", "ORDER BY"],
    },
    {
        "id": "interview-fin-004",
        "slug": "int-fin-branch-account-count",
        "title": "Count of Accounts Per Branch City",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "Management wants to know how many customer accounts exist in each branch city. "
            "Since accounts are linked to customers and customers have a city, count the number "
            "of accounts grouped by the customer's city. Return city and account_count, "
            "ordered by account_count descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.city, COUNT(a.id) AS account_count\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY c.city\n"
            "ORDER BY account_count DESC;"
        ),
        "hints": [
            "Join customers and accounts on customer_id.",
            "Group by the customer's city.",
            "Use COUNT to tally accounts per city.",
            "SELECT c.city, COUNT(a.id) AS account_count FROM customers c JOIN accounts a ON ... GROUP BY ...;",
        ],
        "explanation": (
            "1. JOIN customers and accounts to link accounts to customer cities.\n"
            "2. GROUP BY c.city aggregates by city.\n"
            "3. COUNT(a.id) counts the number of accounts per city."
        ),
        "approach": [
            "Join the two tables on the customer relationship.",
            "Group results by city.",
            "Count accounts within each group.",
        ],
        "common_mistakes": [
            "Grouping by account columns instead of customer city.",
            "Using COUNT(*) which works but COUNT(a.id) is more explicit.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "interview-fin-005",
        "slug": "int-fin-blocked-cards-list",
        "title": "List All Blocked Cards",
        "difficulty": "easy",
        "category": "filtering",
        "dataset": "finance",
        "description": (
            "The fraud department needs a list of all blocked cards. "
            "Return the card id, card_number, card_type, and issued_at "
            "for every card with status 'blocked'. Sort by issued_at descending."
        ),
        "schema_hint": ["cards"],
        "solution_query": (
            "SELECT id, card_number, card_type, issued_at\n"
            "FROM cards\n"
            "WHERE status = 'blocked'\n"
            "ORDER BY issued_at DESC;"
        ),
        "hints": [
            "Filter on the status column.",
            "The status values are 'active', 'blocked', or 'expired'.",
            "Use ORDER BY issued_at DESC for newest first.",
            "SELECT id, card_number, card_type, issued_at FROM cards WHERE ...;",
        ],
        "explanation": (
            "1. SELECT the requested columns from cards.\n"
            "2. WHERE status = 'blocked' filters to blocked cards only.\n"
            "3. ORDER BY issued_at DESC shows the most recently issued blocked cards first."
        ),
        "approach": [
            "Query the cards table.",
            "Filter for blocked status.",
            "Sort by issue date descending.",
        ],
        "common_mistakes": [
            "Using LIKE instead of exact match for a known set of status values.",
            "Forgetting to specify DESC for the sort order.",
        ],
        "concept_tags": ["SELECT", "WHERE", "ORDER BY"],
    },
    {
        "id": "interview-fin-006",
        "slug": "int-fin-oldest-customers",
        "title": "Five Oldest Customer Accounts",
        "difficulty": "easy",
        "category": "sorting and limiting",
        "dataset": "finance",
        "description": (
            "Find the five customers who have been with the bank the longest. "
            "Return their first_name, last_name, and created_at. "
            "Order by created_at ascending and limit to 5."
        ),
        "schema_hint": ["customers"],
        "solution_query": (
            "SELECT first_name, last_name, created_at\n"
            "FROM customers\n"
            "ORDER BY created_at ASC\n"
            "LIMIT 5;"
        ),
        "hints": [
            "Use ORDER BY on created_at to sort by signup date.",
            "ASC order puts the earliest dates first.",
            "LIMIT restricts the result to a specific number of rows.",
            "SELECT first_name, last_name, created_at FROM customers ORDER BY ... LIMIT ...;",
        ],
        "explanation": (
            "1. SELECT the requested columns from customers.\n"
            "2. ORDER BY created_at ASC sorts from oldest to newest.\n"
            "3. LIMIT 5 restricts output to the first five rows."
        ),
        "approach": [
            "Query the customers table.",
            "Sort by created_at ascending to get the oldest first.",
            "Use LIMIT to restrict to 5 results.",
        ],
        "common_mistakes": [
            "Sorting DESC instead of ASC, which returns the newest customers.",
            "Forgetting LIMIT and returning all customers.",
        ],
        "concept_tags": ["ORDER BY", "LIMIT", "date sorting"],
    },
    {
        "id": "interview-fin-007",
        "slug": "int-fin-negative-balance-accounts",
        "title": "Overdrawn Accounts",
        "difficulty": "easy",
        "category": "filtering",
        "dataset": "finance",
        "description": (
            "The risk team needs to identify all overdrawn accounts. "
            "Return the id, customer_id, account_type, and balance for every account "
            "where the balance is less than 0. Order by balance ascending (most overdrawn first)."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT id, customer_id, account_type, balance\n"
            "FROM accounts\n"
            "WHERE balance < 0\n"
            "ORDER BY balance ASC;"
        ),
        "hints": [
            "Use a comparison operator to check for negative balances.",
            "balance < 0 finds overdrawn accounts.",
            "ORDER BY balance ASC puts the most negative values first.",
            "SELECT id, customer_id, account_type, balance FROM accounts WHERE balance < 0 ORDER BY ...;",
        ],
        "explanation": (
            "1. WHERE balance < 0 filters to accounts with negative balances.\n"
            "2. ORDER BY balance ASC puts the most overdrawn accounts first."
        ),
        "approach": [
            "Filter accounts where balance is negative.",
            "Sort ascending so the worst overdrafts appear first.",
        ],
        "common_mistakes": [
            "Using balance = 0 which finds zero-balance accounts, not overdrawn ones.",
            "Sorting DESC which puts the least overdrawn accounts first.",
        ],
        "concept_tags": ["WHERE", "comparison operator", "ORDER BY"],
    },
    {
        "id": "interview-fin-008",
        "slug": "int-fin-loan-count-by-status",
        "title": "Loan Count by Status",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "Produce a summary showing how many loans exist for each loan status. "
            "Return the status and the loan_count. Order by loan_count descending."
        ),
        "schema_hint": ["loans"],
        "solution_query": (
            "SELECT status, COUNT(*) AS loan_count\n"
            "FROM loans\n"
            "GROUP BY status\n"
            "ORDER BY loan_count DESC;"
        ),
        "hints": [
            "Group by the status column to categorize loans.",
            "COUNT(*) counts the number of loans in each group.",
            "Use an alias for the count to make it readable.",
            "SELECT status, COUNT(*) AS loan_count FROM loans GROUP BY ...;",
        ],
        "explanation": (
            "1. GROUP BY status partitions loans by their status.\n"
            "2. COUNT(*) tallies the number of loans per status.\n"
            "3. ORDER BY loan_count DESC shows the most common status first."
        ),
        "approach": [
            "Group loans by their status.",
            "Count rows in each group.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY and getting a single total count.",
            "Using SUM instead of COUNT when you want to count rows.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "interview-fin-009",
        "slug": "int-fin-fee-transactions",
        "title": "Total Fees Charged Per Account",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "finance",
        "description": (
            "The billing team wants to see total fees charged to each account. "
            "Return account_id and total_fees for accounts that have at least one fee transaction. "
            "Only consider transactions where type is 'fee'. Order by total_fees descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id, SUM(amount) AS total_fees\n"
            "FROM transactions\n"
            "WHERE type = 'fee'\n"
            "GROUP BY account_id\n"
            "ORDER BY total_fees DESC;"
        ),
        "hints": [
            "Filter for fee transactions with WHERE.",
            "Group by account_id to get per-account totals.",
            "SUM(amount) computes the total fees.",
            "The WHERE clause naturally excludes accounts with no fee transactions.",
        ],
        "explanation": (
            "1. WHERE type = 'fee' limits to fee transactions.\n"
            "2. GROUP BY account_id aggregates per account.\n"
            "3. SUM(amount) totals the fee amounts.\n"
            "4. Accounts with no fees are automatically excluded by the WHERE filter."
        ),
        "approach": [
            "Filter transactions to fees only.",
            "Group by account.",
            "Sum the fee amounts.",
        ],
        "common_mistakes": [
            "Including all transaction types in the sum.",
            "Using HAVING instead of WHERE for the type filter.",
        ],
        "concept_tags": ["SUM", "WHERE", "GROUP BY", "filtering"],
    },
    {
        "id": "interview-fin-010",
        "slug": "int-fin-credit-card-limits",
        "title": "Credit Cards Ordered by Credit Limit",
        "difficulty": "easy",
        "category": "sorting",
        "dataset": "finance",
        "description": (
            "List all credit cards with their credit limit. Return the card id, card_number, "
            "credit_limit, and status for cards where card_type is 'credit' and credit_limit "
            "is not null. Order by credit_limit descending."
        ),
        "schema_hint": ["cards"],
        "solution_query": (
            "SELECT id, card_number, credit_limit, status\n"
            "FROM cards\n"
            "WHERE card_type = 'credit'\n"
            "  AND credit_limit IS NOT NULL\n"
            "ORDER BY credit_limit DESC;"
        ),
        "hints": [
            "Filter for credit cards and non-null credit limits.",
            "Use IS NOT NULL to exclude rows without a credit limit.",
            "ORDER BY credit_limit DESC shows the highest limits first.",
            "Combine two conditions with AND.",
        ],
        "explanation": (
            "1. WHERE card_type = 'credit' selects only credit cards.\n"
            "2. AND credit_limit IS NOT NULL excludes cards without a limit.\n"
            "3. ORDER BY credit_limit DESC sorts by highest limit first."
        ),
        "approach": [
            "Filter to credit card type.",
            "Exclude NULL credit limits.",
            "Sort descending by credit limit.",
        ],
        "common_mistakes": [
            "Using != NULL instead of IS NOT NULL (SQL treats NULL comparisons differently).",
            "Including debit cards which may have NULL credit limits.",
        ],
        "concept_tags": ["WHERE", "IS NOT NULL", "ORDER BY", "AND"],
    },

    # --- MEDIUM (12 problems) ---

    {
        "id": "interview-fin-011",
        "slug": "int-fin-customer-transaction-summary",
        "title": "Customer Transaction Summary",
        "difficulty": "medium",
        "category": "joins and aggregation",
        "dataset": "finance",
        "description": (
            "Build a report showing each customer's transaction activity. "
            "Return first_name, last_name, the total number of transactions (txn_count), "
            "and the total transaction amount (total_amount). Join customers to accounts "
            "to transactions. Only include customers who have at least one transaction. "
            "Order by total_amount descending."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       COUNT(t.id) AS txn_count,\n"
            "       SUM(t.amount) AS total_amount\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "ORDER BY total_amount DESC;"
        ),
        "hints": [
            "You need two JOINs: customers -> accounts -> transactions.",
            "GROUP BY customer to aggregate transaction data per person.",
            "COUNT counts transactions, SUM totals the amounts.",
            "INNER JOIN naturally excludes customers with no transactions.",
        ],
        "explanation": (
            "1. JOIN customers to accounts on customer_id.\n"
            "2. JOIN accounts to transactions on account_id.\n"
            "3. GROUP BY customer aggregates across all their accounts.\n"
            "4. COUNT and SUM produce the summary metrics."
        ),
        "approach": [
            "Chain the joins through the foreign key relationships.",
            "Group by customer identifier.",
            "Aggregate with COUNT and SUM.",
        ],
        "common_mistakes": [
            "Forgetting that customers connect to transactions through accounts.",
            "Grouping only by name without including c.id, risking duplicate names.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT", "SUM", "multi-table"],
    },
    {
        "id": "interview-fin-012",
        "slug": "int-fin-monthly-deposit-withdrawal-totals",
        "title": "Monthly Deposit and Withdrawal Totals",
        "difficulty": "medium",
        "category": "conditional aggregation",
        "dataset": "finance",
        "description": (
            "Create a monthly report showing total deposits and total withdrawals side by side. "
            "Return the month (as YYYY-MM), total_deposits, and total_withdrawals. "
            "Use conditional aggregation (CASE inside SUM). Order by month ascending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT SUBSTR(transaction_date, 1, 7) AS month,\n"
            "       SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) AS total_deposits,\n"
            "       SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS total_withdrawals\n"
            "FROM transactions\n"
            "GROUP BY SUBSTR(transaction_date, 1, 7)\n"
            "ORDER BY month ASC;"
        ),
        "hints": [
            "Extract the year-month from transaction_date using SUBSTR.",
            "Use CASE inside SUM to conditionally sum by transaction type.",
            "Group by the extracted month.",
            "SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) sums only deposits.",
        ],
        "explanation": (
            "1. SUBSTR(transaction_date, 1, 7) extracts the YYYY-MM portion.\n"
            "2. SUM with CASE WHEN creates conditional totals for each type.\n"
            "3. GROUP BY month aggregates all transactions in the same month.\n"
            "4. This pivot-style technique is a classic interview pattern."
        ),
        "approach": [
            "Extract year-month from the date.",
            "Use conditional SUM for deposits and withdrawals.",
            "Group by the month.",
        ],
        "common_mistakes": [
            "Using separate queries for deposits and withdrawals instead of CASE.",
            "Forgetting the ELSE 0 in the CASE, which would produce NULL for months without that type.",
        ],
        "concept_tags": ["CASE WHEN", "SUM", "GROUP BY", "conditional aggregation", "SUBSTR"],
    },
    {
        "id": "interview-fin-013",
        "slug": "int-fin-loan-payment-progress",
        "title": "Loan Payment Progress Tracker",
        "difficulty": "medium",
        "category": "joins and calculation",
        "dataset": "finance",
        "description": (
            "For each active loan, show the loan id, principal, total amount paid so far "
            "(total_paid), and the percentage of the principal that has been paid "
            "(pct_paid, rounded to 2 decimal places). Join loans to payments. "
            "Only include loans with status 'active'. Order by pct_paid descending."
        ),
        "schema_hint": ["loans", "payments"],
        "solution_query": (
            "SELECT l.id AS loan_id,\n"
            "       l.principal,\n"
            "       SUM(p.amount) AS total_paid,\n"
            "       ROUND(SUM(p.amount) * 100.0 / l.principal, 2) AS pct_paid\n"
            "FROM loans l\n"
            "JOIN payments p ON l.id = p.loan_id\n"
            "WHERE l.status = 'active'\n"
            "GROUP BY l.id, l.principal\n"
            "ORDER BY pct_paid DESC;"
        ),
        "hints": [
            "Join loans to payments on loan_id.",
            "Filter for active loans.",
            "SUM(p.amount) gives total paid per loan.",
            "Divide total paid by principal and multiply by 100 for percentage.",
        ],
        "explanation": (
            "1. JOIN loans to payments to link each loan with its payments.\n"
            "2. WHERE filters to active loans only.\n"
            "3. SUM(p.amount) totals payments per loan.\n"
            "4. The percentage is calculated as (total_paid / principal) * 100.\n"
            "5. ROUND(..., 2) limits to two decimal places."
        ),
        "approach": [
            "Join the two tables.",
            "Filter for active status.",
            "Aggregate payments per loan.",
            "Calculate the percentage paid.",
        ],
        "common_mistakes": [
            "Integer division truncating the percentage (use 100.0 to force float).",
            "Forgetting to group by loan, which would sum all payments together.",
        ],
        "concept_tags": ["JOIN", "SUM", "ROUND", "percentage calculation", "GROUP BY"],
    },
    {
        "id": "interview-fin-014",
        "slug": "int-fin-customers-multiple-account-types",
        "title": "Customers Holding Multiple Account Types",
        "difficulty": "medium",
        "category": "having and distinct",
        "dataset": "finance",
        "description": (
            "Find customers who hold more than one distinct type of account (e.g., both checking and savings). "
            "Return customer_id, the customer's first_name, last_name, and the count of distinct "
            "account types (type_count). Only include customers with type_count > 1. "
            "Order by type_count descending, then last_name ascending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.id AS customer_id, c.first_name, c.last_name,\n"
            "       COUNT(DISTINCT a.account_type) AS type_count\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY c.id, c.first_name, c.last_name\n"
            "HAVING COUNT(DISTINCT a.account_type) > 1\n"
            "ORDER BY type_count DESC, c.last_name ASC;"
        ),
        "hints": [
            "Use COUNT(DISTINCT account_type) to count unique types per customer.",
            "HAVING filters groups after aggregation.",
            "Join customers to accounts for the name fields.",
            "HAVING COUNT(DISTINCT ...) > 1 keeps only multi-type customers.",
        ],
        "explanation": (
            "1. JOIN customers to accounts.\n"
            "2. GROUP BY customer to count account types per person.\n"
            "3. COUNT(DISTINCT a.account_type) counts unique types.\n"
            "4. HAVING > 1 filters to those with multiple types."
        ),
        "approach": [
            "Join the tables.",
            "Group by customer.",
            "Count distinct account types.",
            "Filter with HAVING.",
        ],
        "common_mistakes": [
            "Using COUNT without DISTINCT, which counts all accounts not distinct types.",
            "Using WHERE instead of HAVING for the aggregate filter.",
        ],
        "concept_tags": ["COUNT DISTINCT", "HAVING", "JOIN", "GROUP BY"],
    },
    {
        "id": "interview-fin-015",
        "slug": "int-fin-above-avg-transaction-accounts",
        "title": "Accounts with Above-Average Transaction Volume",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "finance",
        "description": (
            "Find accounts whose total number of transactions exceeds the average "
            "transaction count across all accounts. Return account_id and txn_count. "
            "Use a subquery or HAVING to compare against the overall average. "
            "Order by txn_count descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "SELECT account_id, COUNT(*) AS txn_count\n"
            "FROM transactions\n"
            "GROUP BY account_id\n"
            "HAVING COUNT(*) > (\n"
            "    SELECT AVG(cnt) FROM (\n"
            "        SELECT COUNT(*) AS cnt\n"
            "        FROM transactions\n"
            "        GROUP BY account_id\n"
            "    )\n"
            ")\n"
            "ORDER BY txn_count DESC;"
        ),
        "hints": [
            "First calculate the average number of transactions per account.",
            "A subquery can compute the overall average transaction count.",
            "Use HAVING to compare each account's count to the average.",
            "The inner subquery needs its own GROUP BY to get per-account counts before averaging.",
        ],
        "explanation": (
            "1. The innermost subquery counts transactions per account.\n"
            "2. The middle subquery computes the average of those counts.\n"
            "3. The outer query groups by account and uses HAVING to keep only "
            "accounts exceeding the average."
        ),
        "approach": [
            "Build a subquery that computes per-account transaction counts.",
            "Wrap it in AVG to get the overall average.",
            "Use HAVING to filter the main query.",
        ],
        "common_mistakes": [
            "Computing AVG(amount) instead of average count of transactions.",
            "Trying to use WHERE with an aggregate function.",
        ],
        "concept_tags": ["subquery", "HAVING", "AVG", "GROUP BY", "nested query"],
    },
    {
        "id": "interview-fin-016",
        "slug": "int-fin-cross-branch-balance-comparison",
        "title": "Average Balance by Branch City",
        "difficulty": "medium",
        "category": "joins and aggregation",
        "dataset": "finance",
        "description": (
            "Compare average account balances across branch cities. Join customers to accounts "
            "using customer_id, then group by the customer's city. Return city, the number of "
            "accounts (num_accounts), and the average balance (avg_balance, rounded to 2 decimals). "
            "Only include cities with at least 3 accounts. Order by avg_balance descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "SELECT c.city,\n"
            "       COUNT(a.id) AS num_accounts,\n"
            "       ROUND(AVG(a.balance), 2) AS avg_balance\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "GROUP BY c.city\n"
            "HAVING COUNT(a.id) >= 3\n"
            "ORDER BY avg_balance DESC;"
        ),
        "hints": [
            "Join customers to accounts to associate balances with cities.",
            "Group by city to get per-city aggregates.",
            "HAVING filters groups by count.",
            "ROUND(AVG(a.balance), 2) rounds the average.",
        ],
        "explanation": (
            "1. JOIN customers to accounts to get the city for each account.\n"
            "2. GROUP BY c.city aggregates per city.\n"
            "3. HAVING COUNT(a.id) >= 3 excludes small cities.\n"
            "4. AVG and ROUND produce the formatted average balance."
        ),
        "approach": [
            "Join the tables.",
            "Group by city.",
            "Apply HAVING for minimum account threshold.",
            "Compute the average balance.",
        ],
        "common_mistakes": [
            "Confusing branch city with customer city.",
            "Forgetting HAVING and including cities with very few accounts.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "AVG", "ROUND"],
    },
    {
        "id": "interview-fin-017",
        "slug": "int-fin-largest-withdrawal-per-customer",
        "title": "Largest Withdrawal Per Customer",
        "difficulty": "medium",
        "category": "correlated subquery",
        "dataset": "finance",
        "description": (
            "For each customer, find their single largest withdrawal transaction. "
            "Return the customer's first_name, last_name, the transaction amount, "
            "and the transaction_date. Use a correlated subquery or window function "
            "to pick the maximum withdrawal. Order by amount descending."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name, t.amount, t.transaction_date\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "WHERE t.type = 'withdrawal'\n"
            "  AND t.amount = (\n"
            "      SELECT MAX(t2.amount)\n"
            "      FROM transactions t2\n"
            "      JOIN accounts a2 ON t2.account_id = a2.id\n"
            "      WHERE a2.customer_id = c.id\n"
            "        AND t2.type = 'withdrawal'\n"
            "  )\n"
            "ORDER BY t.amount DESC;"
        ),
        "hints": [
            "Join customers to accounts to transactions.",
            "Filter for withdrawal type.",
            "A correlated subquery can find the MAX amount per customer.",
            "The subquery references the outer customer to correlate.",
        ],
        "explanation": (
            "1. The main query joins all three tables and filters for withdrawals.\n"
            "2. The correlated subquery finds the MAX withdrawal amount for each customer.\n"
            "3. The WHERE clause matches only the row with that maximum amount.\n"
            "4. If a customer has ties, both rows appear."
        ),
        "approach": [
            "Join the three tables.",
            "Filter for withdrawals.",
            "Use a correlated subquery to find the max per customer.",
            "Match the outer row to that max.",
        ],
        "common_mistakes": [
            "Forgetting the correlation condition (a2.customer_id = c.id).",
            "Not filtering by withdrawal type in the subquery.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "JOIN", "WHERE"],
    },
    {
        "id": "interview-fin-018",
        "slug": "int-fin-accounts-no-recent-transactions",
        "title": "Dormant Accounts (No Recent Transactions)",
        "difficulty": "medium",
        "category": "subquery and date logic",
        "dataset": "finance",
        "description": (
            "Identify active accounts that have had no transactions in the last 90 days "
            "(relative to the most recent transaction_date in the database). "
            "Return account id, account_type, balance, and the last_txn_date for the account. "
            "Use a subquery to determine the cutoff date. Order by last_txn_date ascending."
        ),
        "schema_hint": ["accounts", "transactions"],
        "solution_query": (
            "SELECT a.id, a.account_type, a.balance,\n"
            "       MAX(t.transaction_date) AS last_txn_date\n"
            "FROM accounts a\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "WHERE a.status = 'active'\n"
            "GROUP BY a.id, a.account_type, a.balance\n"
            "HAVING MAX(t.transaction_date) < DATE(\n"
            "    (SELECT MAX(transaction_date) FROM transactions), '-90 days'\n"
            ")\n"
            "ORDER BY last_txn_date ASC;"
        ),
        "hints": [
            "Find the most recent date in the database first.",
            "DATE(max_date, '-90 days') computes the cutoff in SQLite.",
            "Group by account and use HAVING on MAX(transaction_date).",
            "Only include accounts with status 'active'.",
        ],
        "explanation": (
            "1. Join accounts to transactions.\n"
            "2. Filter for active accounts.\n"
            "3. GROUP BY account to find each account's latest transaction.\n"
            "4. HAVING compares the latest transaction date against a cutoff "
            "computed from the database's max transaction date minus 90 days."
        ),
        "approach": [
            "Determine the latest transaction date in the entire table.",
            "Subtract 90 days for the cutoff.",
            "Group by account and filter using HAVING on MAX date.",
        ],
        "common_mistakes": [
            "Using CURRENT_DATE instead of the database's max date (data may not be current).",
            "Forgetting to filter for active accounts.",
        ],
        "concept_tags": ["HAVING", "MAX", "DATE", "subquery", "GROUP BY"],
    },
    {
        "id": "interview-fin-019",
        "slug": "int-fin-self-join-same-day-accounts",
        "title": "Customers Who Opened Accounts on the Same Day",
        "difficulty": "medium",
        "category": "self join",
        "dataset": "finance",
        "description": (
            "Find pairs of different customers who opened an account on the same date. "
            "Return customer1_id, customer2_id, and the shared opened_at date. "
            "Ensure each pair appears only once (customer1_id < customer2_id). "
            "Order by opened_at, then customer1_id."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT DISTINCT a1.customer_id AS customer1_id,\n"
            "       a2.customer_id AS customer2_id,\n"
            "       a1.opened_at\n"
            "FROM accounts a1\n"
            "JOIN accounts a2\n"
            "  ON a1.opened_at = a2.opened_at\n"
            "  AND a1.customer_id < a2.customer_id\n"
            "ORDER BY a1.opened_at, customer1_id;"
        ),
        "hints": [
            "Self-join the accounts table to itself on the same opened_at date.",
            "Use customer_id < customer_id to avoid duplicates and self-pairs.",
            "DISTINCT removes duplicate pairs if customers have multiple accounts opened the same day.",
            "This is a classic self-join interview pattern.",
        ],
        "explanation": (
            "1. Self-join accounts on matching opened_at dates.\n"
            "2. The condition a1.customer_id < a2.customer_id ensures each pair "
            "appears once and excludes self-matches.\n"
            "3. DISTINCT handles cases where multiple account pairs match."
        ),
        "approach": [
            "Self-join the table on the date column.",
            "Use inequality to deduplicate pairs.",
            "Add DISTINCT for safety.",
        ],
        "common_mistakes": [
            "Using != instead of < which produces duplicate pairs (A,B) and (B,A).",
            "Forgetting DISTINCT when customers have multiple accounts.",
        ],
        "concept_tags": ["self join", "DISTINCT", "deduplication", "inequality join"],
    },
    {
        "id": "interview-fin-020",
        "slug": "int-fin-payment-pattern-analysis",
        "title": "Average Days Between Loan Payments",
        "difficulty": "medium",
        "category": "date arithmetic",
        "dataset": "finance",
        "description": (
            "For each loan that has at least 2 payments, calculate the average number "
            "of days between consecutive payments. Return loan_id, payment_count, and "
            "avg_days_between (rounded to 1 decimal). Use the difference between "
            "the earliest and latest payment dates divided by (payment_count - 1). "
            "Order by avg_days_between ascending."
        ),
        "schema_hint": ["payments"],
        "solution_query": (
            "SELECT loan_id,\n"
            "       COUNT(*) AS payment_count,\n"
            "       ROUND(\n"
            "           CAST(JULIANDAY(MAX(payment_date)) - JULIANDAY(MIN(payment_date)) AS REAL)\n"
            "           / (COUNT(*) - 1),\n"
            "           1\n"
            "       ) AS avg_days_between\n"
            "FROM payments\n"
            "GROUP BY loan_id\n"
            "HAVING COUNT(*) >= 2\n"
            "ORDER BY avg_days_between ASC;"
        ),
        "hints": [
            "JULIANDAY converts a date string to a Julian day number for arithmetic.",
            "The average gap is (latest - earliest) / (count - 1).",
            "HAVING COUNT(*) >= 2 ensures there is at least one gap to measure.",
            "ROUND(..., 1) rounds to one decimal place.",
        ],
        "explanation": (
            "1. GROUP BY loan_id aggregates payments per loan.\n"
            "2. JULIANDAY(MAX) - JULIANDAY(MIN) gives the total span in days.\n"
            "3. Dividing by (COUNT - 1) gives the average gap between consecutive payments.\n"
            "4. HAVING >= 2 excludes loans with a single payment."
        ),
        "approach": [
            "Group payments by loan.",
            "Compute the date span using JULIANDAY.",
            "Divide by the number of intervals.",
            "Filter for at least 2 payments.",
        ],
        "common_mistakes": [
            "Dividing by COUNT instead of COUNT - 1 (n payments create n-1 gaps).",
            "Forgetting to use JULIANDAY for date arithmetic in SQLite.",
        ],
        "concept_tags": ["JULIANDAY", "date arithmetic", "GROUP BY", "HAVING", "ROUND"],
    },
    {
        "id": "interview-fin-021",
        "slug": "int-fin-account-type-balance-share",
        "title": "Account Type Balance Share",
        "difficulty": "medium",
        "category": "subquery and percentage",
        "dataset": "finance",
        "description": (
            "Calculate the percentage of total bank balance held in each account type. "
            "Return account_type, type_total (sum of balances for that type), and "
            "pct_of_total (rounded to 2 decimals). Use a subquery to get the overall total. "
            "Order by pct_of_total descending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "SELECT account_type,\n"
            "       SUM(balance) AS type_total,\n"
            "       ROUND(SUM(balance) * 100.0 / (SELECT SUM(balance) FROM accounts), 2) AS pct_of_total\n"
            "FROM accounts\n"
            "GROUP BY account_type\n"
            "ORDER BY pct_of_total DESC;"
        ),
        "hints": [
            "A scalar subquery in the SELECT can compute the overall total.",
            "Divide the group total by the overall total and multiply by 100.",
            "ROUND to 2 decimal places for clean output.",
            "GROUP BY account_type to get per-type totals.",
        ],
        "explanation": (
            "1. GROUP BY account_type computes per-type totals.\n"
            "2. The scalar subquery (SELECT SUM(balance) FROM accounts) computes the bank-wide total.\n"
            "3. The percentage is (type_total / overall_total) * 100.\n"
            "4. ROUND formats the result."
        ),
        "approach": [
            "Group by account type and sum balances.",
            "Use a subquery for the grand total.",
            "Compute the percentage.",
        ],
        "common_mistakes": [
            "Integer division truncating results (use 100.0).",
            "Forgetting that the subquery runs once and returns the same total for all rows.",
        ],
        "concept_tags": ["scalar subquery", "SUM", "percentage", "GROUP BY", "ROUND"],
    },
    {
        "id": "interview-fin-022",
        "slug": "int-fin-customer-first-transaction",
        "title": "Each Customer's First Transaction",
        "difficulty": "medium",
        "category": "correlated subquery",
        "dataset": "finance",
        "description": (
            "For every customer who has at least one transaction, find their earliest transaction. "
            "Return first_name, last_name, the transaction_date, type, and amount of their "
            "first transaction. If a customer has multiple transactions on the same earliest date, "
            "return the one with the smallest transaction id. Order by transaction_date ascending."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       t.transaction_date, t.type, t.amount\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "WHERE t.id = (\n"
            "    SELECT t2.id\n"
            "    FROM transactions t2\n"
            "    JOIN accounts a2 ON t2.account_id = a2.id\n"
            "    WHERE a2.customer_id = c.id\n"
            "    ORDER BY t2.transaction_date ASC, t2.id ASC\n"
            "    LIMIT 1\n"
            ")\n"
            "ORDER BY t.transaction_date ASC;"
        ),
        "hints": [
            "Use a correlated subquery to find the earliest transaction per customer.",
            "ORDER BY date ASC, id ASC in the subquery with LIMIT 1 picks the first one.",
            "The subquery correlates on customer_id.",
            "Join through accounts to connect customers to transactions.",
        ],
        "explanation": (
            "1. The correlated subquery finds the transaction with the earliest date "
            "(and smallest id as tiebreaker) for each customer.\n"
            "2. The outer query matches only that transaction.\n"
            "3. INNER JOIN ensures only customers with transactions appear."
        ),
        "approach": [
            "Chain the three-table join.",
            "Use a correlated subquery with ORDER BY and LIMIT 1.",
            "Match the outer row on the subquery's returned id.",
        ],
        "common_mistakes": [
            "Using MIN(transaction_date) which loses access to other columns of that row.",
            "Forgetting the tiebreaker on id.",
        ],
        "concept_tags": ["correlated subquery", "LIMIT", "ORDER BY", "JOIN"],
    },

    # --- HARD (10 problems) ---

    {
        "id": "interview-fin-023",
        "slug": "int-fin-rank-customers-by-net-worth",
        "title": "Rank Customers by Net Worth",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "finance",
        "description": (
            "Rank all customers by their total net worth (sum of all account balances minus "
            "sum of all active loan principals). Return first_name, last_name, total_balance, "
            "total_loan_principal, net_worth, and a dense_rank (net_worth_rank). "
            "Use CTEs and window functions. Include customers even if they have no loans "
            "(treat as 0). Order by net_worth_rank ascending."
        ),
        "schema_hint": ["customers", "accounts", "loans"],
        "solution_query": (
            "WITH balances AS (\n"
            "    SELECT customer_id, SUM(balance) AS total_balance\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "loan_totals AS (\n"
            "    SELECT customer_id, SUM(principal) AS total_loan_principal\n"
            "    FROM loans\n"
            "    WHERE status = 'active'\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT c.first_name, c.last_name,\n"
            "       COALESCE(b.total_balance, 0) AS total_balance,\n"
            "       COALESCE(lt.total_loan_principal, 0) AS total_loan_principal,\n"
            "       COALESCE(b.total_balance, 0) - COALESCE(lt.total_loan_principal, 0) AS net_worth,\n"
            "       DENSE_RANK() OVER (ORDER BY COALESCE(b.total_balance, 0) - COALESCE(lt.total_loan_principal, 0) DESC) AS net_worth_rank\n"
            "FROM customers c\n"
            "LEFT JOIN balances b ON c.id = b.customer_id\n"
            "LEFT JOIN loan_totals lt ON c.id = lt.customer_id\n"
            "ORDER BY net_worth_rank ASC;"
        ),
        "hints": [
            "Use CTEs to pre-aggregate balances and loan principals separately.",
            "LEFT JOIN both CTEs to customers to include everyone.",
            "COALESCE handles customers with no accounts or no loans.",
            "DENSE_RANK() OVER (ORDER BY net_worth DESC) assigns the ranking.",
        ],
        "explanation": (
            "1. CTE 'balances' sums account balances per customer.\n"
            "2. CTE 'loan_totals' sums active loan principals per customer.\n"
            "3. LEFT JOIN both to customers to include all customers.\n"
            "4. Net worth = total_balance - total_loan_principal.\n"
            "5. DENSE_RANK ranks customers by net worth descending."
        ),
        "approach": [
            "Create two CTEs for balance and loan aggregation.",
            "Left join both to customers.",
            "Compute net worth.",
            "Apply DENSE_RANK window function.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops customers without accounts or loans.",
            "Joining accounts and loans directly, causing row multiplication.",
            "Forgetting COALESCE, leading to NULL net worth values.",
        ],
        "concept_tags": ["CTE", "DENSE_RANK", "window function", "LEFT JOIN", "COALESCE"],
    },
    {
        "id": "interview-fin-024",
        "slug": "int-fin-consecutive-deposits",
        "title": "Detect Three Consecutive Deposits",
        "difficulty": "hard",
        "category": "window functions and pattern detection",
        "dataset": "finance",
        "description": (
            "Find accounts that have three or more consecutive deposit transactions "
            "(with no other transaction type in between, ordered by transaction id). "
            "Return the account_id and the count of such consecutive deposit streaks "
            "(streak_count). Use LAG or LEAD window functions to detect consecutive types. "
            "Order by streak_count descending, then account_id ascending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH numbered AS (\n"
            "    SELECT id, account_id, type,\n"
            "           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY id) AS rn,\n"
            "           ROW_NUMBER() OVER (PARTITION BY account_id, type ORDER BY id) AS rn_type\n"
            "    FROM transactions\n"
            "),\n"
            "streaks AS (\n"
            "    SELECT account_id, type, (rn - rn_type) AS grp,\n"
            "           COUNT(*) AS streak_len\n"
            "    FROM numbered\n"
            "    WHERE type = 'deposit'\n"
            "    GROUP BY account_id, type, grp\n"
            "    HAVING COUNT(*) >= 3\n"
            ")\n"
            "SELECT account_id, COUNT(*) AS streak_count\n"
            "FROM streaks\n"
            "GROUP BY account_id\n"
            "ORDER BY streak_count DESC, account_id ASC;"
        ),
        "hints": [
            "The classic 'gaps and islands' technique detects consecutive sequences.",
            "Assign two row numbers: one overall and one partitioned by type.",
            "The difference between these two row numbers is constant within a consecutive run.",
            "Group by that difference to identify each streak.",
        ],
        "explanation": (
            "1. The 'numbered' CTE assigns two row numbers per account: one overall (rn) "
            "and one within each type (rn_type).\n"
            "2. The difference (rn - rn_type) is constant for consecutive same-type transactions.\n"
            "3. The 'streaks' CTE groups by this difference and counts streak length.\n"
            "4. HAVING >= 3 keeps only streaks of three or more.\n"
            "5. The final query counts how many such streaks each account has."
        ),
        "approach": [
            "Apply the gaps-and-islands technique with dual row numbers.",
            "Filter for deposit type.",
            "Group by the computed group identifier to find streaks.",
            "Filter for streaks of length >= 3.",
        ],
        "common_mistakes": [
            "Trying to use LAG/LEAD three times instead of the gaps-and-islands pattern.",
            "Ordering by transaction_date instead of id (dates may not be unique).",
            "Forgetting to partition by account_id.",
        ],
        "concept_tags": ["gaps and islands", "ROW_NUMBER", "window function", "CTE", "HAVING"],
    },
    {
        "id": "interview-fin-025",
        "slug": "int-fin-suspicious-large-withdrawals",
        "title": "Detect Suspicious Large Withdrawal Patterns",
        "difficulty": "hard",
        "category": "fraud detection",
        "dataset": "finance",
        "description": (
            "Flag accounts where a single withdrawal exceeds 1.5 times the "
            "account's average withdrawal amount. Return account_id, the "
            "suspicious transaction id (txn_id), the withdrawal amount, and "
            "the account's avg_withdrawal (rounded to 2 decimals). "
            "Use a CTE to compute average withdrawals per account, then join "
            "back. Order by amount descending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH avg_withdrawals AS (\n"
            "    SELECT account_id, AVG(amount) AS avg_withdrawal\n"
            "    FROM transactions\n"
            "    WHERE type = 'withdrawal'\n"
            "    GROUP BY account_id\n"
            ")\n"
            "SELECT t.account_id,\n"
            "       t.id AS txn_id,\n"
            "       t.amount,\n"
            "       ROUND(aw.avg_withdrawal, 2) AS avg_withdrawal\n"
            "FROM transactions t\n"
            "JOIN avg_withdrawals aw ON t.account_id = aw.account_id\n"
            "WHERE t.type = 'withdrawal'\n"
            "  AND t.amount > 1.5 * aw.avg_withdrawal\n"
            "ORDER BY t.amount DESC;"
        ),
        "hints": [
            "Compute the average withdrawal per account in a CTE.",
            "Join the CTE back to individual withdrawal transactions.",
            "Compare each transaction's amount to 1.5 times the average.",
            "Filter in the WHERE clause after the join.",
        ],
        "explanation": (
            "1. The CTE computes the average withdrawal amount per account.\n"
            "2. The main query joins back to individual withdrawal transactions.\n"
            "3. WHERE filters for transactions exceeding 1.5x the average.\n"
            "4. This is a common fraud detection pattern in banking interviews."
        ),
        "approach": [
            "CTE for average withdrawal per account.",
            "Join CTE to individual transactions.",
            "Filter for outliers exceeding 1.5x average.",
        ],
        "common_mistakes": [
            "Including non-withdrawal transactions in the average calculation.",
            "Comparing against the overall average instead of per-account average.",
        ],
        "concept_tags": ["CTE", "AVG", "JOIN", "fraud detection", "outlier analysis"],
    },
    {
        "id": "interview-fin-026",
        "slug": "int-fin-portfolio-diversification-score",
        "title": "Portfolio Diversification Score",
        "difficulty": "hard",
        "category": "advanced aggregation",
        "dataset": "finance",
        "description": (
            "Calculate a diversification score for each customer based on how many distinct "
            "financial products they hold. Products include: distinct account types, distinct "
            "card types, and distinct loan types. Return first_name, last_name, "
            "num_account_types, num_card_types, num_loan_types, and total_products "
            "(the sum of all three). Use CTEs for each product category. Include all customers "
            "(use 0 for missing products). Order by total_products descending, last_name ascending."
        ),
        "schema_hint": ["customers", "accounts", "cards", "loans"],
        "solution_query": (
            "WITH acct_types AS (\n"
            "    SELECT customer_id, COUNT(DISTINCT account_type) AS num_account_types\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "card_types AS (\n"
            "    SELECT a.customer_id, COUNT(DISTINCT c.card_type) AS num_card_types\n"
            "    FROM cards c\n"
            "    JOIN accounts a ON c.account_id = a.id\n"
            "    GROUP BY a.customer_id\n"
            "),\n"
            "loan_types AS (\n"
            "    SELECT customer_id, COUNT(DISTINCT loan_type) AS num_loan_types\n"
            "    FROM loans\n"
            "    GROUP BY customer_id\n"
            ")\n"
            "SELECT cu.first_name, cu.last_name,\n"
            "       COALESCE(at2.num_account_types, 0) AS num_account_types,\n"
            "       COALESCE(ct.num_card_types, 0) AS num_card_types,\n"
            "       COALESCE(lt.num_loan_types, 0) AS num_loan_types,\n"
            "       COALESCE(at2.num_account_types, 0) + COALESCE(ct.num_card_types, 0) + COALESCE(lt.num_loan_types, 0) AS total_products\n"
            "FROM customers cu\n"
            "LEFT JOIN acct_types at2 ON cu.id = at2.customer_id\n"
            "LEFT JOIN card_types ct ON cu.id = ct.customer_id\n"
            "LEFT JOIN loan_types lt ON cu.id = lt.customer_id\n"
            "ORDER BY total_products DESC, cu.last_name ASC;"
        ),
        "hints": [
            "Build three CTEs: one per product category.",
            "Cards link to customers through accounts.",
            "LEFT JOIN all CTEs to customers to preserve everyone.",
            "COALESCE null counts to 0 before summing.",
        ],
        "explanation": (
            "1. Three CTEs count distinct product types per customer.\n"
            "2. Cards require joining through accounts to get customer_id.\n"
            "3. LEFT JOINs preserve all customers.\n"
            "4. COALESCE ensures 0 instead of NULL for missing products.\n"
            "5. Total products is the sum of all three counts."
        ),
        "approach": [
            "CTE per product category with COUNT DISTINCT.",
            "Left join all to customers.",
            "COALESCE and sum.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops customers missing a product type.",
            "Forgetting that cards connect through accounts, not directly to customers.",
            "Adding NULL values (which propagate NULL) instead of using COALESCE.",
        ],
        "concept_tags": ["CTE", "COUNT DISTINCT", "LEFT JOIN", "COALESCE", "multi-CTE"],
    },
    {
        "id": "interview-fin-027",
        "slug": "int-fin-yoy-balance-growth",
        "title": "Year-over-Year Account Balance Growth",
        "difficulty": "hard",
        "category": "window functions and date logic",
        "dataset": "finance",
        "description": (
            "Calculate the year-over-year growth in total account balances opened per year. "
            "For each year, compute the total balance of accounts opened that year and the "
            "growth rate compared to the previous year. Return the year, yearly_total, "
            "prev_year_total, and growth_pct (rounded to 2 decimals). "
            "Use LAG window function. Order by year ascending."
        ),
        "schema_hint": ["accounts"],
        "solution_query": (
            "WITH yearly AS (\n"
            "    SELECT SUBSTR(opened_at, 1, 4) AS year,\n"
            "           SUM(balance) AS yearly_total\n"
            "    FROM accounts\n"
            "    GROUP BY SUBSTR(opened_at, 1, 4)\n"
            ")\n"
            "SELECT year,\n"
            "       yearly_total,\n"
            "       LAG(yearly_total) OVER (ORDER BY year) AS prev_year_total,\n"
            "       ROUND(\n"
            "           (yearly_total - LAG(yearly_total) OVER (ORDER BY year)) * 100.0\n"
            "           / LAG(yearly_total) OVER (ORDER BY year),\n"
            "           2\n"
            "       ) AS growth_pct\n"
            "FROM yearly\n"
            "ORDER BY year ASC;"
        ),
        "hints": [
            "First aggregate balances per year using SUBSTR on opened_at.",
            "LAG(yearly_total) OVER (ORDER BY year) gets the previous year's total.",
            "Growth rate = (current - previous) / previous * 100.",
            "The first year will have NULL for prev_year_total and growth_pct.",
        ],
        "explanation": (
            "1. The CTE aggregates total balances by year.\n"
            "2. LAG accesses the previous year's total.\n"
            "3. Growth percentage is the standard YoY formula.\n"
            "4. The first year naturally has NULL for previous values."
        ),
        "approach": [
            "Aggregate per year in a CTE.",
            "Use LAG window function for the previous year's value.",
            "Compute the growth rate.",
        ],
        "common_mistakes": [
            "Using a self-join instead of LAG (less efficient).",
            "Dividing by zero when the previous year has no data.",
            "Extracting the year incorrectly from the date string.",
        ],
        "concept_tags": ["LAG", "window function", "CTE", "YoY growth", "ROUND"],
    },
    {
        "id": "interview-fin-028",
        "slug": "int-fin-three-txn-moving-avg-per-customer",
        "title": "Per-Customer 3-Transaction Moving Average",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "finance",
        "description": (
            "For each customer, compute a 3-transaction moving average of withdrawal amounts. "
            "Return first_name, last_name, transaction_date, amount, and moving_avg_3 "
            "(rounded to 2 decimals). The moving average should consider the current and "
            "two preceding withdrawal transactions ordered by transaction id. "
            "Only include withdrawal transactions. Order by last_name, transaction_date."
        ),
        "schema_hint": ["customers", "accounts", "transactions"],
        "solution_query": (
            "SELECT c.first_name, c.last_name,\n"
            "       t.transaction_date, t.amount,\n"
            "       ROUND(\n"
            "           AVG(t.amount) OVER (\n"
            "               PARTITION BY c.id\n"
            "               ORDER BY t.id\n"
            "               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
            "           ), 2\n"
            "       ) AS moving_avg_3\n"
            "FROM customers c\n"
            "JOIN accounts a ON c.id = a.customer_id\n"
            "JOIN transactions t ON a.id = t.account_id\n"
            "WHERE t.type = 'withdrawal'\n"
            "ORDER BY c.last_name, t.transaction_date;"
        ),
        "hints": [
            "Use AVG() with a window frame: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.",
            "Partition by customer to compute separate moving averages.",
            "Order within the window by transaction id.",
            "Filter for withdrawals before applying the window function.",
        ],
        "explanation": (
            "1. Join customers -> accounts -> transactions.\n"
            "2. Filter for withdrawals.\n"
            "3. The window function AVG with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW "
            "computes the moving average of 3 transactions.\n"
            "4. PARTITION BY customer ensures each customer's average is independent."
        ),
        "approach": [
            "Join the three tables and filter for withdrawals.",
            "Apply AVG with a sliding window frame.",
            "Partition by customer, order by transaction id.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS for the window frame.",
            "Forgetting to partition by customer, mixing all customers together.",
            "Using BETWEEN 1 PRECEDING AND 1 FOLLOWING which is a centered average.",
        ],
        "concept_tags": ["window function", "moving average", "ROWS BETWEEN", "AVG OVER", "PARTITION BY"],
    },
    {
        "id": "interview-fin-029",
        "slug": "int-fin-account-cohort-retention",
        "title": "Account Cohort Activity Analysis",
        "difficulty": "hard",
        "category": "cohort analysis",
        "dataset": "finance",
        "description": (
            "Perform a cohort analysis on accounts. The cohort is defined by the month "
            "the account was opened (cohort_month). For each cohort, count how many accounts "
            "had at least one transaction in the same month they were opened (active_in_month_0) "
            "versus the total accounts in that cohort (cohort_size). "
            "Return cohort_month, cohort_size, active_in_month_0, and activation_rate "
            "(rounded to 2 decimals, as a percentage). Order by cohort_month."
        ),
        "schema_hint": ["accounts", "transactions"],
        "solution_query": (
            "WITH cohorts AS (\n"
            "    SELECT id AS account_id,\n"
            "           SUBSTR(opened_at, 1, 7) AS cohort_month\n"
            "    FROM accounts\n"
            "),\n"
            "active AS (\n"
            "    SELECT DISTINCT co.account_id, co.cohort_month\n"
            "    FROM cohorts co\n"
            "    JOIN transactions t ON co.account_id = t.account_id\n"
            "    WHERE SUBSTR(t.transaction_date, 1, 7) = co.cohort_month\n"
            ")\n"
            "SELECT co.cohort_month,\n"
            "       COUNT(DISTINCT co.account_id) AS cohort_size,\n"
            "       COUNT(DISTINCT a.account_id) AS active_in_month_0,\n"
            "       ROUND(COUNT(DISTINCT a.account_id) * 100.0 / COUNT(DISTINCT co.account_id), 2) AS activation_rate\n"
            "FROM cohorts co\n"
            "LEFT JOIN active a ON co.account_id = a.account_id\n"
            "GROUP BY co.cohort_month\n"
            "ORDER BY co.cohort_month;"
        ),
        "hints": [
            "Define cohorts by the account's opened_at month.",
            "An account is 'active in month 0' if it has a transaction in the same month.",
            "Use a CTE to identify which accounts had transactions in their opening month.",
            "LEFT JOIN to preserve accounts with no activity.",
        ],
        "explanation": (
            "1. The 'cohorts' CTE assigns each account its opening month.\n"
            "2. The 'active' CTE finds accounts with transactions in their cohort month.\n"
            "3. LEFT JOIN preserves all cohort accounts.\n"
            "4. COUNT DISTINCT on the active CTE's account_id gives the activation count.\n"
            "5. The ratio gives the activation rate."
        ),
        "approach": [
            "Define cohorts by opening month.",
            "Identify which accounts transacted in their opening month.",
            "Left join and compute the activation rate.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops inactive accounts from the cohort count.",
            "Comparing full dates instead of year-month for the cohort match.",
            "Forgetting COUNT DISTINCT which can double-count accounts.",
        ],
        "concept_tags": ["CTE", "cohort analysis", "LEFT JOIN", "COUNT DISTINCT", "activation rate"],
    },
    {
        "id": "interview-fin-030",
        "slug": "int-fin-balance-volatility-ranking",
        "title": "Account Balance Volatility Ranking",
        "difficulty": "hard",
        "category": "window functions and statistics",
        "dataset": "finance",
        "description": (
            "Rank accounts by balance volatility. Volatility is measured as the difference "
            "between the maximum and minimum balance_after values across all transactions "
            "for that account divided by the average balance_after. Return account_id, "
            "min_balance, max_balance, avg_balance (rounded to 2), volatility (rounded to 4), "
            "and volatility_rank using RANK(). Order by volatility_rank ascending."
        ),
        "schema_hint": ["transactions"],
        "solution_query": (
            "WITH stats AS (\n"
            "    SELECT account_id,\n"
            "           MIN(balance_after) AS min_balance,\n"
            "           MAX(balance_after) AS max_balance,\n"
            "           ROUND(AVG(balance_after), 2) AS avg_balance,\n"
            "           ROUND(\n"
            "               CASE WHEN AVG(balance_after) = 0 THEN NULL\n"
            "                    ELSE (MAX(balance_after) - MIN(balance_after)) * 1.0 / AVG(balance_after)\n"
            "               END, 4\n"
            "           ) AS volatility\n"
            "    FROM transactions\n"
            "    GROUP BY account_id\n"
            ")\n"
            "SELECT account_id, min_balance, max_balance, avg_balance, volatility,\n"
            "       RANK() OVER (ORDER BY volatility DESC) AS volatility_rank\n"
            "FROM stats\n"
            "WHERE volatility IS NOT NULL\n"
            "ORDER BY volatility_rank ASC;"
        ),
        "hints": [
            "Compute min, max, and avg of balance_after per account.",
            "Volatility = (max - min) / avg. Handle zero average with CASE.",
            "Use RANK() OVER to assign rankings by volatility.",
            "A CTE keeps the query clean.",
        ],
        "explanation": (
            "1. The CTE computes per-account balance statistics.\n"
            "2. Volatility is the range divided by the mean.\n"
            "3. CASE handles division by zero when avg is 0.\n"
            "4. RANK() assigns rankings, with ties receiving the same rank.\n"
            "5. WHERE volatility IS NOT NULL excludes degenerate cases."
        ),
        "approach": [
            "Aggregate balance_after stats per account.",
            "Compute volatility ratio.",
            "Apply RANK window function.",
        ],
        "common_mistakes": [
            "Dividing by zero when average balance is 0.",
            "Using balance instead of balance_after for historical volatility.",
            "Using DENSE_RANK when RANK is specified.",
        ],
        "concept_tags": ["RANK", "window function", "CTE", "statistical measure", "CASE WHEN"],
    },
    {
        "id": "interview-fin-031",
        "slug": "int-fin-multi-cte-financial-health-report",
        "title": "Multi-CTE Financial Health Report",
        "difficulty": "hard",
        "category": "complex CTE",
        "dataset": "finance",
        "description": (
            "Build a comprehensive financial health report per customer using multiple CTEs. "
            "The report should include: full_name, total_balance (from accounts), "
            "total_outstanding_loans (sum of remaining_balance from the latest payment per active loan), "
            "debt_to_asset_ratio (total_outstanding_loans / total_balance, rounded to 4, NULL if no balance), "
            "and health_status classified as 'Excellent' if ratio < 0.3, 'Good' if < 0.6, "
            "'At Risk' if < 1.0, else 'Critical'. Only include customers with both accounts and "
            "active loans. Order by debt_to_asset_ratio ascending."
        ),
        "schema_hint": ["customers", "accounts", "loans", "payments"],
        "solution_query": (
            "WITH balances AS (\n"
            "    SELECT customer_id, SUM(balance) AS total_balance\n"
            "    FROM accounts\n"
            "    GROUP BY customer_id\n"
            "),\n"
            "latest_payments AS (\n"
            "    SELECT p.loan_id, p.remaining_balance\n"
            "    FROM payments p\n"
            "    INNER JOIN (\n"
            "        SELECT loan_id, MAX(payment_date) AS max_date\n"
            "        FROM payments\n"
            "        GROUP BY loan_id\n"
            "    ) mp ON p.loan_id = mp.loan_id AND p.payment_date = mp.max_date\n"
            "),\n"
            "outstanding AS (\n"
            "    SELECT l.customer_id,\n"
            "           SUM(COALESCE(lp.remaining_balance, l.principal)) AS total_outstanding\n"
            "    FROM loans l\n"
            "    LEFT JOIN latest_payments lp ON l.id = lp.loan_id\n"
            "    WHERE l.status = 'active'\n"
            "    GROUP BY l.customer_id\n"
            ")\n"
            "SELECT c.first_name || ' ' || c.last_name AS full_name,\n"
            "       b.total_balance,\n"
            "       o.total_outstanding AS total_outstanding_loans,\n"
            "       ROUND(\n"
            "           CASE WHEN b.total_balance = 0 THEN NULL\n"
            "                ELSE o.total_outstanding * 1.0 / b.total_balance\n"
            "           END, 4\n"
            "       ) AS debt_to_asset_ratio,\n"
            "       CASE\n"
            "           WHEN b.total_balance = 0 THEN 'Critical'\n"
            "           WHEN o.total_outstanding * 1.0 / b.total_balance < 0.3 THEN 'Excellent'\n"
            "           WHEN o.total_outstanding * 1.0 / b.total_balance < 0.6 THEN 'Good'\n"
            "           WHEN o.total_outstanding * 1.0 / b.total_balance < 1.0 THEN 'At Risk'\n"
            "           ELSE 'Critical'\n"
            "       END AS health_status\n"
            "FROM customers c\n"
            "JOIN balances b ON c.id = b.customer_id\n"
            "JOIN outstanding o ON c.id = o.customer_id\n"
            "ORDER BY debt_to_asset_ratio ASC;"
        ),
        "hints": [
            "Use multiple CTEs: one for balances, one for latest payments, one for outstanding loans.",
            "The latest payment per loan gives the current remaining_balance.",
            "If a loan has no payments, use the original principal as outstanding.",
            "CASE WHEN classifies the health status based on the ratio.",
        ],
        "explanation": (
            "1. 'balances' CTE sums account balances per customer.\n"
            "2. 'latest_payments' finds the most recent payment per loan for remaining_balance.\n"
            "3. 'outstanding' sums remaining balances for active loans per customer.\n"
            "4. INNER JOINs keep only customers with both accounts and active loans.\n"
            "5. Debt-to-asset ratio and CASE classify financial health."
        ),
        "approach": [
            "Build CTEs for each data component.",
            "Find latest payment per loan for current balance.",
            "Compute the debt-to-asset ratio.",
            "Classify health status with CASE.",
        ],
        "common_mistakes": [
            "Using the original principal instead of remaining balance for outstanding debt.",
            "Forgetting to handle loans with no payments (COALESCE to principal).",
            "Division by zero when total balance is 0.",
        ],
        "concept_tags": ["multi-CTE", "CASE WHEN", "COALESCE", "financial ratio", "complex join"],
    },
    {
        "id": "interview-fin-032",
        "slug": "int-fin-ntile-customer-segmentation",
        "title": "NTILE Customer Segmentation",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "finance",
        "description": (
            "Segment customers into 4 tiers based on their total account balance using NTILE. "
            "Tier 1 is the top 25%% by balance, tier 4 is the bottom 25%%. "
            "Return first_name, last_name, total_balance, tier, and the count of customers "
            "in each tier (tier_size). Use a CTE for the tier assignment and a window function "
            "for tier_size. Order by tier ascending, total_balance descending."
        ),
        "schema_hint": ["customers", "accounts"],
        "solution_query": (
            "WITH customer_balances AS (\n"
            "    SELECT c.id, c.first_name, c.last_name,\n"
            "           COALESCE(SUM(a.balance), 0) AS total_balance\n"
            "    FROM customers c\n"
            "    LEFT JOIN accounts a ON c.id = a.customer_id\n"
            "    GROUP BY c.id, c.first_name, c.last_name\n"
            "),\n"
            "tiered AS (\n"
            "    SELECT first_name, last_name, total_balance,\n"
            "           NTILE(4) OVER (ORDER BY total_balance DESC) AS tier\n"
            "    FROM customer_balances\n"
            ")\n"
            "SELECT first_name, last_name, total_balance, tier,\n"
            "       COUNT(*) OVER (PARTITION BY tier) AS tier_size\n"
            "FROM tiered\n"
            "ORDER BY tier ASC, total_balance DESC;"
        ),
        "hints": [
            "NTILE(4) divides rows into 4 roughly equal groups.",
            "Order by total_balance DESC so tier 1 gets the highest balances.",
            "Use COUNT(*) OVER (PARTITION BY tier) for tier_size.",
            "A CTE first computes total balance per customer.",
        ],
        "explanation": (
            "1. 'customer_balances' CTE sums balances per customer (LEFT JOIN for those with no accounts).\n"
            "2. 'tiered' CTE assigns NTILE(4) tier based on balance descending.\n"
            "3. The final query adds tier_size using a window count.\n"
            "4. NTILE distributes rows as evenly as possible across tiers."
        ),
        "approach": [
            "Aggregate customer balances.",
            "Apply NTILE(4) window function.",
            "Add tier_size with COUNT OVER.",
        ],
        "common_mistakes": [
            "Ordering NTILE ascending instead of descending (swapping tier meaning).",
            "Forgetting LEFT JOIN for customers with no accounts.",
            "Confusing NTILE with PERCENT_RANK or CUME_DIST.",
        ],
        "concept_tags": ["NTILE", "window function", "CTE", "segmentation", "COUNT OVER"],
    },
]
