"""
Healthcare dataset practice problems.

40 progressive SQL problems covering fundamentals through advanced topics,
designed around a realistic healthcare database schema.

Tables:
  - patients (id, first_name, last_name, date_of_birth, gender, email, phone,
              blood_type, city, state, insurance_id, created_at)
  - doctors (id, first_name, last_name, specialty, department_id, email, phone,
             hire_date, salary)
  - departments (id, name, floor, head_doctor_id, budget)
  - visits (id, patient_id, doctor_id, visit_date, diagnosis, notes,
            follow_up_date, status)
  - prescriptions (id, visit_id, medication, dosage, frequency, start_date,
                   end_date, refills)
  - insurance (id, provider_name, plan_type, coverage_amount, copay, deductible)
  - lab_results (id, visit_id, test_name, result_value, unit, reference_range,
                 is_abnormal, tested_at)
  - billing (id, visit_id, amount, insurance_covered, patient_responsibility,
             status, billed_at, paid_at)
"""

PROBLEMS: list[dict] = [
    # =========================================================================
    # LEVEL 1 — FUNDAMENTALS (8 problems: hc-001 through hc-008)
    # =========================================================================
    {
        "id": "hc-001",
        "slug": "list-all-patients",
        "title": "List All Patients",
        "difficulty": "easy",
        "category": "select",
        "dataset": "healthcare",
        "description": (
            "The front desk needs a roster of all patients. Write a query that "
            "returns the first name, last name, and email of every patient, "
            "sorted alphabetically by last name."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM patients\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "You only need to query a single table.",
            "Think about which columns the question asks you to return.",
            "Use ORDER BY to control the sort direction.",
            "SELECT first_name, last_name, email FROM patients ORDER BY ...;",
        ],
        "explanation": (
            "1. SELECT the three requested columns from the patients table.\n"
            "2. ORDER BY last_name sorts alphabetically (ascending by default)."
        ),
        "approach": [
            "Identify the table that stores patient information.",
            "Pick only the columns requested: first_name, last_name, email.",
            "Apply an ORDER BY on last_name for alphabetical sorting.",
        ],
        "common_mistakes": [
            "Using SELECT * instead of the three specific columns.",
            "Forgetting ORDER BY, which returns results in an undefined order.",
        ],
        "concept_tags": ["SELECT", "ORDER BY"],
    },
    {
        "id": "hc-002",
        "slug": "patients-from-texas",
        "title": "Patients from Texas",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "The Texas regional office needs a list of all patients in their "
            "state. Retrieve the first name, last name, and city of every "
            "patient whose state is 'TX'."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, city\n"
            "FROM patients\n"
            "WHERE state = 'TX';"
        ),
        "hints": [
            "You need to filter rows based on a column value.",
            "The WHERE clause lets you restrict which rows are returned.",
            "The state column stores two-letter abbreviations.",
            "WHERE state = 'TX' is the filter you need.",
        ],
        "explanation": (
            "1. SELECT the requested columns from patients.\n"
            "2. WHERE state = 'TX' filters to only Texas patients."
        ),
        "approach": [
            "Identify that the patients table holds location info.",
            "Use WHERE to filter on the state column.",
            "Return only the columns the office needs.",
        ],
        "common_mistakes": [
            "Using LIKE '%TX%' which could match unintended values.",
            "Forgetting that string comparisons may be case-sensitive.",
        ],
        "concept_tags": ["SELECT", "WHERE", "string comparison"],
    },
    {
        "id": "hc-003",
        "slug": "completed-visits-after-date",
        "title": "Completed Visits After a Date",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "Hospital administration wants to review all completed visits "
            "from 2024 onward. Return the visit id, visit_date, and diagnosis "
            "for all visits with status 'completed' and visit_date on or "
            "after '2024-01-01'."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT id, visit_date, diagnosis\n"
            "FROM visits\n"
            "WHERE status = 'completed'\n"
            "  AND visit_date >= '2024-01-01';"
        ),
        "hints": [
            "You need two conditions in your WHERE clause.",
            "Combine conditions with AND so both must be true.",
            "One condition is a string match, the other a date comparison.",
            "WHERE status = 'completed' AND visit_date >= '2024-01-01'",
        ],
        "explanation": (
            "1. SELECT id, visit_date, and diagnosis from visits.\n"
            "2. WHERE status = 'completed' keeps only completed visits.\n"
            "3. AND visit_date >= '2024-01-01' further narrows to 2024+."
        ),
        "approach": [
            "Identify that the visits table has both status and visit_date.",
            "Combine a string equality check with a date comparison using AND.",
            "Return only the requested columns.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, returning visits matching either condition.",
            "Using > instead of >= and missing visits exactly on 2024-01-01.",
        ],
        "concept_tags": ["SELECT", "WHERE", "AND", "date comparison"],
    },
    {
        "id": "hc-004",
        "slug": "doctors-salary-range",
        "title": "Doctors in a Salary Range",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "HR needs to identify mid-range earners. Find all doctors whose "
            "salary is between 200000 and 350000 (inclusive). Return their "
            "first name, last name, specialty, and salary, ordered by salary "
            "descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT first_name, last_name, specialty, salary\n"
            "FROM doctors\n"
            "WHERE salary BETWEEN 200000 AND 350000\n"
            "ORDER BY salary DESC;"
        ),
        "hints": [
            "There is a SQL keyword designed for range checks.",
            "BETWEEN is inclusive on both ends.",
            "Remember to sort descending with DESC.",
            "WHERE salary BETWEEN 200000 AND 350000 ORDER BY salary DESC;",
        ],
        "explanation": (
            "1. SELECT the four requested columns from doctors.\n"
            "2. WHERE salary BETWEEN 200000 AND 350000 filters the range.\n"
            "3. ORDER BY salary DESC sorts highest salary first."
        ),
        "approach": [
            "Use the BETWEEN operator for an inclusive range filter.",
            "Add ORDER BY salary DESC for descending sort.",
        ],
        "common_mistakes": [
            "Using > and < instead of BETWEEN, accidentally excluding bounds.",
            "Forgetting DESC, which defaults to ascending order.",
        ],
        "concept_tags": ["SELECT", "WHERE", "BETWEEN", "ORDER BY"],
    },
    {
        "id": "hc-005",
        "slug": "search-diagnosis-keyword",
        "title": "Search Visits by Diagnosis",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "A researcher is studying diabetes-related visits. Find all visits "
            "whose diagnosis contains the word 'Diabetes'. Return the visit id, "
            "visit_date, and diagnosis."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT id, visit_date, diagnosis\n"
            "FROM visits\n"
            "WHERE diagnosis LIKE '%Diabetes%';"
        ),
        "hints": [
            "Use pattern matching to search within text.",
            "The LIKE operator with % wildcards matches substrings.",
            "Place % on both sides to find the word anywhere in the string.",
            "WHERE diagnosis LIKE '%Diabetes%'",
        ],
        "explanation": (
            "1. SELECT id, visit_date, diagnosis from visits.\n"
            "2. WHERE diagnosis LIKE '%Diabetes%' finds any diagnosis "
            "containing 'Diabetes'."
        ),
        "approach": [
            "Use LIKE with wildcard characters for substring matching.",
            "The % wildcard matches any sequence of characters.",
        ],
        "common_mistakes": [
            "Forgetting the % wildcards and matching only exact strings.",
            "Using = instead of LIKE, which requires an exact match.",
        ],
        "concept_tags": ["SELECT", "WHERE", "LIKE", "pattern matching"],
    },
    {
        "id": "hc-006",
        "slug": "patients-missing-phone",
        "title": "Patients with Missing Phone Numbers",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "The contact center needs to identify patients whose phone number "
            "is missing. Return the first name, last name, and email of all "
            "patients where phone is NULL."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM patients\n"
            "WHERE phone IS NULL;"
        ),
        "hints": [
            "NULL values require special comparison in SQL.",
            "You cannot use = NULL; you must use IS NULL.",
            "The WHERE clause filters for missing data.",
            "WHERE phone IS NULL",
        ],
        "explanation": (
            "1. SELECT the three columns from patients.\n"
            "2. WHERE phone IS NULL correctly checks for missing phone numbers."
        ),
        "approach": [
            "Recognize that NULL comparisons use IS NULL, not = NULL.",
            "Filter the patients table where the phone column is NULL.",
        ],
        "common_mistakes": [
            "Using WHERE phone = NULL which always returns no rows.",
            "Using WHERE phone = '' which checks for empty strings, not NULL.",
        ],
        "concept_tags": ["SELECT", "WHERE", "NULL", "IS NULL"],
    },
    {
        "id": "hc-007",
        "slug": "distinct-blood-types",
        "title": "Distinct Blood Types",
        "difficulty": "easy",
        "category": "select",
        "dataset": "healthcare",
        "description": (
            "The blood bank needs to know what blood types are represented "
            "in the patient database. Return a list of all distinct blood "
            "types, sorted alphabetically."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT DISTINCT blood_type\n"
            "FROM patients\n"
            "ORDER BY blood_type;"
        ),
        "hints": [
            "You need to remove duplicate values from the results.",
            "The DISTINCT keyword eliminates duplicate rows.",
            "Apply it right after SELECT.",
            "SELECT DISTINCT blood_type FROM patients ORDER BY blood_type;",
        ],
        "explanation": (
            "1. SELECT DISTINCT blood_type removes duplicate blood type values.\n"
            "2. ORDER BY blood_type sorts the results alphabetically."
        ),
        "approach": [
            "Use DISTINCT to get unique blood type values.",
            "Sort the results for readability.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT and getting one row per patient instead.",
            "Adding extra columns that prevent proper deduplication.",
        ],
        "concept_tags": ["SELECT", "DISTINCT", "ORDER BY"],
    },
    {
        "id": "hc-008",
        "slug": "recent-patients-limit",
        "title": "Five Most Recent Patients",
        "difficulty": "easy",
        "category": "select",
        "dataset": "healthcare",
        "description": (
            "Show the five most recently registered patients. Return their "
            "first name, last name, and created_at, ordered from newest to "
            "oldest."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, created_at\n"
            "FROM patients\n"
            "ORDER BY created_at DESC\n"
            "LIMIT 5;"
        ),
        "hints": [
            "You need to sort by registration date in descending order.",
            "Use LIMIT to restrict the number of returned rows.",
            "DESC gives you the most recent dates first.",
            "ORDER BY created_at DESC LIMIT 5;",
        ],
        "explanation": (
            "1. SELECT the requested columns.\n"
            "2. ORDER BY created_at DESC puts the newest registrations first.\n"
            "3. LIMIT 5 returns only the top five rows."
        ),
        "approach": [
            "Sort patients by created_at descending.",
            "Use LIMIT to cap the results at five.",
        ],
        "common_mistakes": [
            "Forgetting DESC, which returns the oldest patients instead.",
            "Omitting LIMIT and returning all patients.",
        ],
        "concept_tags": ["SELECT", "ORDER BY", "LIMIT", "DESC"],
    },

    # =========================================================================
    # LEVEL 2 — AGGREGATIONS (8 problems: hc-009 through hc-016)
    # =========================================================================
    {
        "id": "hc-009",
        "slug": "count-patients-by-state",
        "title": "Count Patients by State",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Management wants to know where the patients are located. Count "
            "the number of patients in each state, ordered from the most "
            "patients to the fewest."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT state, COUNT(*) AS patient_count\n"
            "FROM patients\n"
            "GROUP BY state\n"
            "ORDER BY patient_count DESC;"
        ),
        "hints": [
            "Use GROUP BY to partition rows by state.",
            "COUNT(*) counts the rows in each group.",
            "Alias the count column for clarity.",
            "GROUP BY state ORDER BY patient_count DESC;",
        ],
        "explanation": (
            "1. GROUP BY state creates one group per state.\n"
            "2. COUNT(*) counts patients in each group.\n"
            "3. ORDER BY patient_count DESC shows the largest groups first."
        ),
        "approach": [
            "Group the patients table by the state column.",
            "Use COUNT(*) to tally each group.",
            "Sort descending to see the most populated states first.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY, which would count all patients as one row.",
            "Not aliasing the COUNT column, making ORDER BY harder.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY", "aggregate"],
    },
    {
        "id": "hc-010",
        "slug": "average-doctor-salary-by-department",
        "title": "Average Doctor Salary by Department",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Finance needs to compare average salaries across departments. "
            "For each department_id, calculate the average salary. Round to "
            "two decimal places and order by average salary descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT department_id, ROUND(AVG(salary), 2) AS avg_salary\n"
            "FROM doctors\n"
            "GROUP BY department_id\n"
            "ORDER BY avg_salary DESC;"
        ),
        "hints": [
            "AVG() computes the average of a numeric column.",
            "ROUND(value, 2) limits to two decimal places.",
            "GROUP BY department_id creates one row per department.",
            "SELECT department_id, ROUND(AVG(salary), 2) ...",
        ],
        "explanation": (
            "1. GROUP BY department_id creates one group per department.\n"
            "2. AVG(salary) computes the mean salary within each group.\n"
            "3. ROUND(..., 2) formats to two decimal places.\n"
            "4. ORDER BY avg_salary DESC shows highest-paid departments first."
        ),
        "approach": [
            "Group doctors by department_id.",
            "Apply AVG on salary and ROUND the result.",
            "Sort descending by the computed average.",
        ],
        "common_mistakes": [
            "Forgetting ROUND, which may return many decimal places.",
            "Using SUM instead of AVG, which gives the total not the average.",
        ],
        "concept_tags": ["GROUP BY", "AVG", "ROUND", "ORDER BY"],
    },
    {
        "id": "hc-011",
        "slug": "visits-per-status",
        "title": "Visit Count by Status",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Operations wants a breakdown of visit outcomes. Count the number "
            "of visits for each status value (scheduled, completed, cancelled, "
            "no_show)."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT status, COUNT(*) AS visit_count\n"
            "FROM visits\n"
            "GROUP BY status\n"
            "ORDER BY visit_count DESC;"
        ),
        "hints": [
            "GROUP BY status gives one row per status value.",
            "COUNT(*) tallies the visits in each group.",
            "Order by count descending to see the most common status first.",
            "SELECT status, COUNT(*) AS visit_count FROM visits GROUP BY status;",
        ],
        "explanation": (
            "1. GROUP BY status partitions visits by their status.\n"
            "2. COUNT(*) counts rows in each partition.\n"
            "3. ORDER BY visit_count DESC shows the most frequent status first."
        ),
        "approach": [
            "Group the visits table by status.",
            "Count the rows per group.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Selecting columns not in the GROUP BY without an aggregate.",
            "Forgetting to alias the count column.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "hc-012",
        "slug": "total-billing-by-status",
        "title": "Total Billing Amount by Status",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "The billing department wants to see the total billed amount "
            "grouped by billing status. Return each status and the sum of "
            "amount, rounded to two decimal places, ordered by total descending."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT status, ROUND(SUM(amount), 2) AS total_amount\n"
            "FROM billing\n"
            "GROUP BY status\n"
            "ORDER BY total_amount DESC;"
        ),
        "hints": [
            "SUM() adds up all values in a column within each group.",
            "GROUP BY status creates one row per billing status.",
            "ROUND the result to two decimal places.",
            "SELECT status, ROUND(SUM(amount), 2) FROM billing GROUP BY status;",
        ],
        "explanation": (
            "1. GROUP BY status partitions billing records.\n"
            "2. SUM(amount) totals the billed amounts per status.\n"
            "3. ROUND(..., 2) ensures clean output.\n"
            "4. ORDER BY total_amount DESC shows the largest totals first."
        ),
        "approach": [
            "Group billing records by status.",
            "Sum the amount column in each group.",
            "Round and sort the results.",
        ],
        "common_mistakes": [
            "Confusing SUM with COUNT — SUM adds values, COUNT counts rows.",
            "Forgetting to GROUP BY and getting a single total.",
        ],
        "concept_tags": ["GROUP BY", "SUM", "ROUND", "ORDER BY"],
    },
    {
        "id": "hc-013",
        "slug": "most-prescribed-medications",
        "title": "Top 10 Most Prescribed Medications",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "The pharmacy wants to know which medications are prescribed most "
            "often. Return the medication name and its prescription count for "
            "the top 10 most-prescribed medications."
        ),
        "schema_hint": ["prescriptions"],
        "solution_query": (
            "SELECT medication, COUNT(*) AS prescription_count\n"
            "FROM prescriptions\n"
            "GROUP BY medication\n"
            "ORDER BY prescription_count DESC\n"
            "LIMIT 10;"
        ),
        "hints": [
            "Group by the medication column to count per medication.",
            "Use COUNT(*) to tally prescriptions.",
            "ORDER BY descending and LIMIT to 10.",
            "GROUP BY medication ORDER BY prescription_count DESC LIMIT 10;",
        ],
        "explanation": (
            "1. GROUP BY medication creates one row per medication.\n"
            "2. COUNT(*) counts how many times each was prescribed.\n"
            "3. ORDER BY prescription_count DESC and LIMIT 10 gives top 10."
        ),
        "approach": [
            "Group prescriptions by medication name.",
            "Count occurrences per group.",
            "Sort descending and limit to 10.",
        ],
        "common_mistakes": [
            "Forgetting LIMIT and returning all medications.",
            "Sorting ascending instead of descending.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY", "LIMIT"],
    },
    {
        "id": "hc-014",
        "slug": "departments-with-many-doctors",
        "title": "Departments with More Than 4 Doctors",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Management wants to identify large departments. Find all "
            "department_id values that have more than 4 doctors. Return the "
            "department_id and the doctor count."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT department_id, COUNT(*) AS doctor_count\n"
            "FROM doctors\n"
            "GROUP BY department_id\n"
            "HAVING COUNT(*) > 4;"
        ),
        "hints": [
            "First GROUP BY department_id and count the doctors.",
            "To filter on an aggregate, use HAVING not WHERE.",
            "HAVING is applied after grouping, WHERE is applied before.",
            "HAVING COUNT(*) > 4",
        ],
        "explanation": (
            "1. GROUP BY department_id groups doctors by their department.\n"
            "2. COUNT(*) counts doctors per department.\n"
            "3. HAVING COUNT(*) > 4 filters to departments with more than 4."
        ),
        "approach": [
            "Group doctors by department.",
            "Count per group.",
            "Use HAVING to filter groups by count.",
        ],
        "common_mistakes": [
            "Using WHERE COUNT(*) > 4 — WHERE cannot filter on aggregates.",
            "Confusing HAVING and WHERE.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "HAVING"],
    },
    {
        "id": "hc-015",
        "slug": "abnormal-lab-percentage",
        "title": "Abnormal Lab Result Percentage",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Quality assurance wants to know the percentage of lab results "
            "that are abnormal. Return a single row with the total count, "
            "the abnormal count, and the abnormal percentage rounded to one "
            "decimal place."
        ),
        "schema_hint": ["lab_results"],
        "solution_query": (
            "SELECT\n"
            "  COUNT(*) AS total_tests,\n"
            "  SUM(is_abnormal) AS abnormal_count,\n"
            "  ROUND(100.0 * SUM(is_abnormal) / COUNT(*), 1) AS abnormal_pct\n"
            "FROM lab_results;"
        ),
        "hints": [
            "is_abnormal is 0 or 1, so SUM gives the count of abnormals.",
            "Divide the abnormal count by total count for the percentage.",
            "Multiply by 100.0 (not 100) to avoid integer division.",
            "ROUND(100.0 * SUM(is_abnormal) / COUNT(*), 1)",
        ],
        "explanation": (
            "1. COUNT(*) gives the total number of lab tests.\n"
            "2. SUM(is_abnormal) counts abnormal results (since the flag is 0/1).\n"
            "3. 100.0 * SUM / COUNT computes the percentage.\n"
            "4. ROUND(..., 1) formats to one decimal place."
        ),
        "approach": [
            "Use SUM on a boolean-like (0/1) column to count true values.",
            "Divide by total count and multiply by 100 for percentage.",
            "Use 100.0 to force floating-point division.",
        ],
        "common_mistakes": [
            "Using 100 instead of 100.0, causing integer division that truncates.",
            "Forgetting to ROUND the percentage.",
        ],
        "concept_tags": ["COUNT", "SUM", "ROUND", "percentage calculation"],
    },
    {
        "id": "hc-016",
        "slug": "min-max-billing",
        "title": "Min and Max Billing Amounts",
        "difficulty": "easy",
        "category": "aggregation",
        "dataset": "healthcare",
        "description": (
            "Finance wants to understand the billing range. For each billing "
            "status, return the minimum amount, maximum amount, and average "
            "amount (rounded to 2 decimal places)."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT status,\n"
            "  MIN(amount) AS min_amount,\n"
            "  MAX(amount) AS max_amount,\n"
            "  ROUND(AVG(amount), 2) AS avg_amount\n"
            "FROM billing\n"
            "GROUP BY status;"
        ),
        "hints": [
            "MIN and MAX find the smallest and largest values.",
            "AVG computes the average.",
            "Group by status to get per-status statistics.",
            "SELECT status, MIN(amount), MAX(amount), ROUND(AVG(amount), 2) ...",
        ],
        "explanation": (
            "1. GROUP BY status partitions billing records.\n"
            "2. MIN(amount) and MAX(amount) find the extremes.\n"
            "3. AVG(amount) computes the mean.\n"
            "4. ROUND formats to two decimal places."
        ),
        "approach": [
            "Group billing by status.",
            "Apply MIN, MAX, and AVG aggregate functions on amount.",
            "Round the average for clean output.",
        ],
        "common_mistakes": [
            "Selecting columns not in the GROUP BY without an aggregate.",
            "Using SUM instead of AVG for the average.",
        ],
        "concept_tags": ["GROUP BY", "MIN", "MAX", "AVG", "ROUND"],
    },

    # =========================================================================
    # LEVEL 3 — JOINS (8 problems: hc-017 through hc-024)
    # =========================================================================
    {
        "id": "hc-017",
        "slug": "visits-with-patient-names",
        "title": "Visits with Patient Names",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "The records department needs a list of visits that includes "
            "patient names. Return the visit id, visit_date, diagnosis, and "
            "the patient's first and last name for all completed visits."
        ),
        "schema_hint": ["visits", "patients"],
        "solution_query": (
            "SELECT v.id, v.visit_date, v.diagnosis,\n"
            "       p.first_name, p.last_name\n"
            "FROM visits v\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE v.status = 'completed';"
        ),
        "hints": [
            "You need data from two tables: visits and patients.",
            "JOIN connects rows where visit.patient_id matches patient.id.",
            "Use table aliases (v, p) for readability.",
            "JOIN patients p ON v.patient_id = p.id WHERE v.status = 'completed'",
        ],
        "explanation": (
            "1. FROM visits v starts with the visits table.\n"
            "2. JOIN patients p ON v.patient_id = p.id links each visit to its patient.\n"
            "3. WHERE v.status = 'completed' filters to completed visits.\n"
            "4. SELECT pulls the needed columns from both tables."
        ),
        "approach": [
            "Identify the foreign key: visits.patient_id -> patients.id.",
            "Use an INNER JOIN to combine the tables.",
            "Filter on status and select the required columns.",
        ],
        "common_mistakes": [
            "Forgetting the JOIN condition, creating a cartesian product.",
            "Omitting the WHERE filter for completed visits.",
        ],
        "concept_tags": ["JOIN", "INNER JOIN", "WHERE", "table aliases"],
    },
    {
        "id": "hc-018",
        "slug": "doctor-department-list",
        "title": "Doctors with Department Names",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "Create a staff directory showing each doctor's full name, "
            "specialty, and their department name. Sort by department name "
            "then by last name."
        ),
        "schema_hint": ["doctors", "departments"],
        "solution_query": (
            "SELECT d.first_name, d.last_name, d.specialty,\n"
            "       dept.name AS department_name\n"
            "FROM doctors d\n"
            "JOIN departments dept ON d.department_id = dept.id\n"
            "ORDER BY dept.name, d.last_name;"
        ),
        "hints": [
            "Join doctors to departments on department_id.",
            "Use aliases to distinguish the two tables.",
            "ORDER BY can sort on multiple columns.",
            "JOIN departments dept ON d.department_id = dept.id",
        ],
        "explanation": (
            "1. JOIN doctors with departments on department_id.\n"
            "2. Select names, specialty, and department name.\n"
            "3. ORDER BY dept.name, d.last_name sorts by department first."
        ),
        "approach": [
            "Join doctors to departments using the foreign key.",
            "Select the required columns from both tables.",
            "Apply multi-column sorting.",
        ],
        "common_mistakes": [
            "Forgetting to alias the department name column.",
            "Sorting by only one column instead of both.",
        ],
        "concept_tags": ["JOIN", "ORDER BY", "table aliases", "column alias"],
    },
    {
        "id": "hc-019",
        "slug": "patients-with-insurance-details",
        "title": "Patients with Insurance Details",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "List all patients along with their insurance provider name and "
            "plan type. Include patients who have no insurance (insurance_id "
            "is NULL). Return first_name, last_name, provider_name, and "
            "plan_type."
        ),
        "schema_hint": ["patients", "insurance"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       i.provider_name, i.plan_type\n"
            "FROM patients p\n"
            "LEFT JOIN insurance i ON p.insurance_id = i.id;"
        ),
        "hints": [
            "Some patients have NULL insurance_id.",
            "LEFT JOIN keeps all patients even without a match.",
            "An INNER JOIN would exclude uninsured patients.",
            "LEFT JOIN insurance i ON p.insurance_id = i.id",
        ],
        "explanation": (
            "1. FROM patients p starts with all patients.\n"
            "2. LEFT JOIN insurance i keeps every patient row even if "
            "insurance_id is NULL.\n"
            "3. Uninsured patients will have NULL for provider_name and plan_type."
        ),
        "approach": [
            "Recognize that insurance_id is nullable, requiring a LEFT JOIN.",
            "Join patients to insurance on insurance_id.",
            "Select the four requested columns.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops patients without insurance.",
            "Forgetting that NULL insurance_id means no match in insurance table.",
        ],
        "concept_tags": ["LEFT JOIN", "NULL", "foreign key"],
    },
    {
        "id": "hc-020",
        "slug": "visit-prescriptions-details",
        "title": "Visit Details with Prescriptions",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "For each prescription, show the visit date, patient name, "
            "doctor's last name, medication, and dosage. This requires "
            "joining multiple tables."
        ),
        "schema_hint": ["prescriptions", "visits", "patients", "doctors"],
        "solution_query": (
            "SELECT v.visit_date, p.first_name, p.last_name,\n"
            "       d.last_name AS doctor_name,\n"
            "       rx.medication, rx.dosage\n"
            "FROM prescriptions rx\n"
            "JOIN visits v ON rx.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN doctors d ON v.doctor_id = d.id;"
        ),
        "hints": [
            "You need four tables: prescriptions, visits, patients, doctors.",
            "Chain JOINs — prescriptions to visits, then visits to patients and doctors.",
            "Use different aliases for each table.",
            "JOIN visits v ON rx.visit_id = v.id JOIN patients p ON v.patient_id = p.id ...",
        ],
        "explanation": (
            "1. Start from prescriptions (rx).\n"
            "2. JOIN visits on visit_id to get visit details.\n"
            "3. JOIN patients on patient_id for patient name.\n"
            "4. JOIN doctors on doctor_id for doctor name.\n"
            "5. SELECT the requested columns from each table."
        ),
        "approach": [
            "Identify the chain of foreign keys: prescriptions -> visits -> patients/doctors.",
            "Join each table step by step.",
            "Select columns from all four tables.",
        ],
        "common_mistakes": [
            "Missing one of the intermediate JOINs.",
            "Confusing which table holds the foreign key.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "foreign key chain"],
    },
    {
        "id": "hc-021",
        "slug": "visits-per-doctor-with-names",
        "title": "Visit Count per Doctor",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "Show each doctor's full name, specialty, and the total number "
            "of visits they have had. Sort by visit count descending."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name, d.last_name, d.specialty,\n"
            "       COUNT(v.id) AS visit_count\n"
            "FROM doctors d\n"
            "LEFT JOIN visits v ON d.id = v.doctor_id\n"
            "GROUP BY d.id, d.first_name, d.last_name, d.specialty\n"
            "ORDER BY visit_count DESC;"
        ),
        "hints": [
            "Join doctors to visits to count visits per doctor.",
            "Use LEFT JOIN to include doctors with zero visits.",
            "GROUP BY doctor columns and COUNT visits.",
            "LEFT JOIN visits v ON d.id = v.doctor_id GROUP BY d.id ...",
        ],
        "explanation": (
            "1. LEFT JOIN ensures doctors with no visits still appear.\n"
            "2. GROUP BY d.id (and name/specialty) creates one row per doctor.\n"
            "3. COUNT(v.id) counts visits (NULL v.id gives 0).\n"
            "4. ORDER BY visit_count DESC shows busiest doctors first."
        ),
        "approach": [
            "Use LEFT JOIN to keep all doctors.",
            "Group by doctor and count their visits.",
            "Sort descending by count.",
        ],
        "common_mistakes": [
            "Using INNER JOIN and losing doctors with no visits.",
            "Using COUNT(*) instead of COUNT(v.id) with a LEFT JOIN.",
        ],
        "concept_tags": ["LEFT JOIN", "GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "hc-022",
        "slug": "billing-with-patient-info",
        "title": "Billing Records with Patient Info",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "Finance needs overdue bills with patient details. Return the "
            "billing id, amount, patient_responsibility, patient first_name "
            "and last_name for all billing records with status 'overdue'."
        ),
        "schema_hint": ["billing", "visits", "patients"],
        "solution_query": (
            "SELECT b.id, b.amount, b.patient_responsibility,\n"
            "       p.first_name, p.last_name\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE b.status = 'overdue';"
        ),
        "hints": [
            "Billing links to patients through the visits table.",
            "Chain: billing -> visits -> patients.",
            "Filter WHERE b.status = 'overdue'.",
            "JOIN visits v ON b.visit_id = v.id JOIN patients p ON v.patient_id = p.id",
        ],
        "explanation": (
            "1. Join billing to visits on visit_id.\n"
            "2. Join visits to patients on patient_id.\n"
            "3. WHERE b.status = 'overdue' filters to overdue bills.\n"
            "4. Select the required columns."
        ),
        "approach": [
            "Trace the foreign key path from billing to patients via visits.",
            "Apply the status filter.",
            "Select columns from billing and patients.",
        ],
        "common_mistakes": [
            "Trying to join billing directly to patients (no direct FK).",
            "Forgetting the WHERE clause for overdue status.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "WHERE"],
    },
    {
        "id": "hc-023",
        "slug": "lab-results-with-visit-info",
        "title": "Lab Results with Visit and Patient Info",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "Show all abnormal lab results with patient and visit details. "
            "Return the test_name, result_value, unit, patient first_name "
            "and last_name, visit_date, and diagnosis for abnormal results "
            "(is_abnormal = 1)."
        ),
        "schema_hint": ["lab_results", "visits", "patients"],
        "solution_query": (
            "SELECT lr.test_name, lr.result_value, lr.unit,\n"
            "       p.first_name, p.last_name,\n"
            "       v.visit_date, v.diagnosis\n"
            "FROM lab_results lr\n"
            "JOIN visits v ON lr.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE lr.is_abnormal = 1;"
        ),
        "hints": [
            "Join lab_results to visits, then visits to patients.",
            "Filter on is_abnormal = 1.",
            "Select columns from all three tables.",
            "WHERE lr.is_abnormal = 1",
        ],
        "explanation": (
            "1. Join lab_results to visits on visit_id.\n"
            "2. Join visits to patients on patient_id.\n"
            "3. WHERE is_abnormal = 1 filters to abnormal results.\n"
            "4. Select the requested columns from all three tables."
        ),
        "approach": [
            "Chain lab_results -> visits -> patients.",
            "Filter on the abnormal flag.",
            "Select the required columns.",
        ],
        "common_mistakes": [
            "Using is_abnormal = '1' as a string instead of integer.",
            "Forgetting to include the visit details (date, diagnosis).",
        ],
        "concept_tags": ["JOIN", "multi-table join", "WHERE", "boolean filter"],
    },
    {
        "id": "hc-024",
        "slug": "department-visit-revenue",
        "title": "Revenue per Department",
        "difficulty": "medium",
        "category": "joins",
        "dataset": "healthcare",
        "description": (
            "Calculate the total billing amount generated by each department. "
            "Join billing to visits to doctors to departments. Return the "
            "department name and total amount, rounded to 2 decimal places, "
            "sorted by total descending."
        ),
        "schema_hint": ["billing", "visits", "doctors", "departments"],
        "solution_query": (
            "SELECT dept.name AS department_name,\n"
            "       ROUND(SUM(b.amount), 2) AS total_revenue\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "JOIN departments dept ON d.department_id = dept.id\n"
            "GROUP BY dept.name\n"
            "ORDER BY total_revenue DESC;"
        ),
        "hints": [
            "Chain four tables: billing -> visits -> doctors -> departments.",
            "GROUP BY department name and SUM the billing amounts.",
            "Round to 2 decimal places.",
            "JOIN visits v ... JOIN doctors d ... JOIN departments dept ...",
        ],
        "explanation": (
            "1. Chain JOINs from billing through visits and doctors to departments.\n"
            "2. GROUP BY dept.name aggregates per department.\n"
            "3. SUM(b.amount) totals the revenue.\n"
            "4. ROUND and ORDER BY format and sort the output."
        ),
        "approach": [
            "Trace the join path: billing -> visits -> doctors -> departments.",
            "Group by department name.",
            "Sum and round the billing amounts.",
        ],
        "common_mistakes": [
            "Missing one join in the chain, getting incorrect groupings.",
            "Grouping by department_id but selecting name without joining.",
        ],
        "concept_tags": ["JOIN", "multi-table join", "GROUP BY", "SUM"],
    },

    # =========================================================================
    # LEVEL 4 — SUBQUERIES (6 problems: hc-025 through hc-030)
    # =========================================================================
    {
        "id": "hc-025",
        "slug": "doctors-above-avg-salary",
        "title": "Doctors Earning Above Average",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "Find all doctors whose salary is above the overall average "
            "salary. Return their first name, last name, specialty, and "
            "salary, ordered by salary descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT first_name, last_name, specialty, salary\n"
            "FROM doctors\n"
            "WHERE salary > (SELECT AVG(salary) FROM doctors)\n"
            "ORDER BY salary DESC;"
        ),
        "hints": [
            "You need to compare each doctor's salary to the average.",
            "A subquery can compute the average independently.",
            "Place the subquery in the WHERE clause.",
            "WHERE salary > (SELECT AVG(salary) FROM doctors)",
        ],
        "explanation": (
            "1. The subquery (SELECT AVG(salary) FROM doctors) computes the average.\n"
            "2. The outer query filters doctors whose salary exceeds that average.\n"
            "3. ORDER BY salary DESC shows the highest earners first."
        ),
        "approach": [
            "Use a scalar subquery to compute the average salary.",
            "Compare each row's salary to that computed average.",
            "Sort the results descending.",
        ],
        "common_mistakes": [
            "Trying to use AVG(salary) directly in the WHERE clause without a subquery.",
            "Forgetting that the subquery returns a single value.",
        ],
        "concept_tags": ["subquery", "AVG", "WHERE", "scalar subquery"],
    },
    {
        "id": "hc-026",
        "slug": "patients-with-no-visits",
        "title": "Patients Who Have Never Visited",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "Identify patients who have no visit records at all. Return "
            "their first name, last name, and email. Use a subquery approach."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT first_name, last_name, email\n"
            "FROM patients\n"
            "WHERE id NOT IN (\n"
            "  SELECT DISTINCT patient_id FROM visits\n"
            ");"
        ),
        "hints": [
            "You need to find patients not present in the visits table.",
            "NOT IN with a subquery checks for absence.",
            "The subquery selects all patient_id values from visits.",
            "WHERE id NOT IN (SELECT DISTINCT patient_id FROM visits)",
        ],
        "explanation": (
            "1. The subquery collects all patient_ids that appear in visits.\n"
            "2. NOT IN filters out patients whose id is in that set.\n"
            "3. Only patients with zero visits remain."
        ),
        "approach": [
            "Use a subquery to get the set of patient_ids with visits.",
            "Filter the patients table using NOT IN.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT in the subquery (works but less efficient).",
            "Using NOT IN with a subquery that could return NULL values.",
        ],
        "concept_tags": ["subquery", "NOT IN", "set membership"],
    },
    {
        "id": "hc-027",
        "slug": "highest-billing-per-department",
        "title": "Highest Single Bill per Department",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "For each department, find the single largest billing amount. "
            "Return the department name, the maximum billing amount, and "
            "the visit_id associated with it."
        ),
        "schema_hint": ["billing", "visits", "doctors", "departments"],
        "solution_query": (
            "SELECT dept.name AS department_name,\n"
            "       b.amount AS max_amount,\n"
            "       b.visit_id\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "JOIN departments dept ON d.department_id = dept.id\n"
            "WHERE b.amount = (\n"
            "  SELECT MAX(b2.amount)\n"
            "  FROM billing b2\n"
            "  JOIN visits v2 ON b2.visit_id = v2.id\n"
            "  JOIN doctors d2 ON v2.doctor_id = d2.id\n"
            "  WHERE d2.department_id = d.department_id\n"
            ");"
        ),
        "hints": [
            "You need to find the max billing amount within each department.",
            "A correlated subquery can compute the max per department.",
            "The subquery references the outer query's department_id.",
            "WHERE b.amount = (SELECT MAX(b2.amount) ... WHERE d2.department_id = d.department_id)",
        ],
        "explanation": (
            "1. The outer query joins billing through visits and doctors to departments.\n"
            "2. The correlated subquery finds the MAX amount for the same department.\n"
            "3. The WHERE clause keeps only the row(s) matching that maximum."
        ),
        "approach": [
            "Join billing to departments through visits and doctors.",
            "Use a correlated subquery to find the max amount per department.",
            "Filter the outer query to rows matching the max.",
        ],
        "common_mistakes": [
            "Using a non-correlated subquery that returns a single global max.",
            "Forgetting to correlate on department_id.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "multi-table join"],
    },
    {
        "id": "hc-028",
        "slug": "patients-multiple-diagnoses",
        "title": "Patients with Multiple Different Diagnoses",
        "difficulty": "medium",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "Find patients who have been diagnosed with 5 or more distinct "
            "conditions. Return their first name, last name, and the count "
            "of distinct diagnoses."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT p.first_name, p.last_name, sub.diag_count\n"
            "FROM patients p\n"
            "JOIN (\n"
            "  SELECT patient_id, COUNT(DISTINCT diagnosis) AS diag_count\n"
            "  FROM visits\n"
            "  GROUP BY patient_id\n"
            "  HAVING COUNT(DISTINCT diagnosis) >= 5\n"
            ") sub ON p.id = sub.patient_id;"
        ),
        "hints": [
            "Count distinct diagnoses per patient in a subquery.",
            "Use HAVING to filter patients with 5+ distinct diagnoses.",
            "Join the subquery result back to patients for names.",
            "SELECT patient_id, COUNT(DISTINCT diagnosis) ... HAVING ... >= 5",
        ],
        "explanation": (
            "1. The subquery groups visits by patient_id and counts distinct diagnoses.\n"
            "2. HAVING filters to patients with 5 or more.\n"
            "3. The outer query joins to patients for names."
        ),
        "approach": [
            "Use a derived table (subquery in FROM) to compute per-patient stats.",
            "Filter with HAVING in the subquery.",
            "Join to patients for the final output.",
        ],
        "common_mistakes": [
            "Using COUNT(diagnosis) instead of COUNT(DISTINCT diagnosis).",
            "Trying to use HAVING in the outer query instead of the subquery.",
        ],
        "concept_tags": ["subquery", "derived table", "COUNT DISTINCT", "HAVING"],
    },
    {
        "id": "hc-029",
        "slug": "expensive-visits-above-avg",
        "title": "Visits Billed Above Department Average",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "Find visits where the billing amount exceeds the average billing "
            "amount for that doctor's department. Return the visit_id, "
            "billing amount, department name, and the department average."
        ),
        "schema_hint": ["billing", "visits", "doctors", "departments"],
        "solution_query": (
            "SELECT b.visit_id,\n"
            "       b.amount,\n"
            "       dept.name AS department_name,\n"
            "       dept_avg.avg_amount\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "JOIN departments dept ON d.department_id = dept.id\n"
            "JOIN (\n"
            "  SELECT d2.department_id,\n"
            "         ROUND(AVG(b2.amount), 2) AS avg_amount\n"
            "  FROM billing b2\n"
            "  JOIN visits v2 ON b2.visit_id = v2.id\n"
            "  JOIN doctors d2 ON v2.doctor_id = d2.id\n"
            "  GROUP BY d2.department_id\n"
            ") dept_avg ON d.department_id = dept_avg.department_id\n"
            "WHERE b.amount > dept_avg.avg_amount;"
        ),
        "hints": [
            "Compute the average billing per department in a subquery.",
            "Join that average back to the main query.",
            "Compare each billing amount to its department average.",
            "Use a derived table for department averages.",
        ],
        "explanation": (
            "1. The dept_avg subquery computes average billing per department.\n"
            "2. The main query joins billing to departments.\n"
            "3. Joining dept_avg on department_id brings in the average.\n"
            "4. WHERE b.amount > dept_avg.avg_amount filters above-average bills."
        ),
        "approach": [
            "Create a derived table with department-level averages.",
            "Join it to the main multi-table query.",
            "Filter where individual amount exceeds department average.",
        ],
        "common_mistakes": [
            "Trying to compare to the global average instead of per-department.",
            "Forgetting to join through visits and doctors to get department_id.",
        ],
        "concept_tags": ["subquery", "derived table", "AVG", "multi-table join"],
    },
    {
        "id": "hc-030",
        "slug": "doctors-all-visit-statuses",
        "title": "Doctors Who Have Every Visit Status",
        "difficulty": "hard",
        "category": "subqueries",
        "dataset": "healthcare",
        "description": (
            "Find doctors who have visits in every possible status "
            "(completed, scheduled, cancelled, no_show). Return the "
            "doctor's first name, last name, and the count of distinct "
            "statuses they have."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name, d.last_name,\n"
            "       COUNT(DISTINCT v.status) AS status_count\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "GROUP BY d.id, d.first_name, d.last_name\n"
            "HAVING COUNT(DISTINCT v.status) = (\n"
            "  SELECT COUNT(DISTINCT status) FROM visits\n"
            ");"
        ),
        "hints": [
            "Count distinct statuses per doctor.",
            "Compare to the total number of distinct statuses overall.",
            "A subquery in HAVING can compute the total distinct count.",
            "HAVING COUNT(DISTINCT v.status) = (SELECT COUNT(DISTINCT status) FROM visits)",
        ],
        "explanation": (
            "1. Join doctors to visits and GROUP BY doctor.\n"
            "2. COUNT(DISTINCT v.status) counts statuses per doctor.\n"
            "3. The subquery counts all distinct statuses in the table.\n"
            "4. HAVING ensures only doctors with all statuses are returned."
        ),
        "approach": [
            "Group visits by doctor and count distinct statuses.",
            "Use a subquery to find the total number of possible statuses.",
            "Filter with HAVING to match the total count.",
        ],
        "common_mistakes": [
            "Hardcoding 4 instead of using a subquery (fragile if statuses change).",
            "Using COUNT(status) instead of COUNT(DISTINCT status).",
        ],
        "concept_tags": ["subquery", "HAVING", "COUNT DISTINCT", "relational division"],
    },

    # =========================================================================
    # LEVEL 5 — WINDOW FUNCTIONS (5 problems: hc-031 through hc-035)
    # =========================================================================
    {
        "id": "hc-031",
        "slug": "rank-doctors-by-salary",
        "title": "Rank Doctors by Salary Within Department",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "healthcare",
        "description": (
            "Rank doctors by salary within each department. Return the "
            "department_id, first name, last name, salary, and the rank "
            "(1 = highest salary). Use RANK()."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT department_id, first_name, last_name, salary,\n"
            "       RANK() OVER (\n"
            "         PARTITION BY department_id\n"
            "         ORDER BY salary DESC\n"
            "       ) AS salary_rank\n"
            "FROM doctors;"
        ),
        "hints": [
            "Window functions compute values across sets of rows.",
            "PARTITION BY groups the ranking within each department.",
            "ORDER BY salary DESC ranks highest salary as 1.",
            "RANK() OVER (PARTITION BY department_id ORDER BY salary DESC)",
        ],
        "explanation": (
            "1. PARTITION BY department_id creates a separate ranking per department.\n"
            "2. ORDER BY salary DESC sorts within each partition.\n"
            "3. RANK() assigns a rank number, with ties getting the same rank."
        ),
        "approach": [
            "Use the RANK() window function.",
            "Partition by department_id for per-department ranking.",
            "Order by salary descending within each partition.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY and ranking across all departments.",
            "Using ROW_NUMBER instead of RANK (which handles ties differently).",
        ],
        "concept_tags": ["RANK", "OVER", "PARTITION BY", "window function"],
    },
    {
        "id": "hc-032",
        "slug": "running-total-billing",
        "title": "Running Total of Billing Amounts",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "healthcare",
        "description": (
            "Calculate a running total of billing amounts ordered by billed_at "
            "date. Return the billing id, billed_at, amount, and the "
            "cumulative total up to and including that row."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT id, billed_at, amount,\n"
            "       ROUND(SUM(amount) OVER (\n"
            "         ORDER BY billed_at, id\n"
            "       ), 2) AS running_total\n"
            "FROM billing\n"
            "ORDER BY billed_at, id;"
        ),
        "hints": [
            "SUM() can be used as a window function with OVER.",
            "Without PARTITION BY, it runs across all rows.",
            "ORDER BY inside OVER defines the running order.",
            "SUM(amount) OVER (ORDER BY billed_at, id)",
        ],
        "explanation": (
            "1. SUM(amount) OVER (ORDER BY billed_at, id) computes a cumulative sum.\n"
            "2. Each row includes the sum of all previous rows plus itself.\n"
            "3. ROUND ensures clean decimal output.\n"
            "4. The outer ORDER BY matches the window ordering."
        ),
        "approach": [
            "Use SUM as a window function for a running total.",
            "Order by billed_at and id for deterministic results.",
            "Round the result.",
        ],
        "common_mistakes": [
            "Forgetting ORDER BY in the OVER clause, which sums all rows for each.",
            "Not including id in the ORDER BY for deterministic tie-breaking.",
        ],
        "concept_tags": ["SUM", "OVER", "running total", "window function"],
    },
    {
        "id": "hc-033",
        "slug": "patient-visit-gaps",
        "title": "Days Between Consecutive Visits",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "healthcare",
        "description": (
            "For each patient's visits (completed only), calculate the number "
            "of days since their previous visit. Return patient_id, visit_date, "
            "the previous visit date, and the gap in days. Order by patient_id "
            "and visit_date."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT patient_id,\n"
            "       visit_date,\n"
            "       LAG(visit_date) OVER (\n"
            "         PARTITION BY patient_id\n"
            "         ORDER BY visit_date\n"
            "       ) AS prev_visit_date,\n"
            "       CAST(\n"
            "         julianday(visit_date) -\n"
            "         julianday(LAG(visit_date) OVER (\n"
            "           PARTITION BY patient_id\n"
            "           ORDER BY visit_date\n"
            "         )) AS INTEGER\n"
            "       ) AS days_gap\n"
            "FROM visits\n"
            "WHERE status = 'completed'\n"
            "ORDER BY patient_id, visit_date;"
        ),
        "hints": [
            "LAG() accesses a value from the previous row in the window.",
            "PARTITION BY patient_id keeps the lag within each patient.",
            "julianday() converts dates to day numbers for subtraction.",
            "LAG(visit_date) OVER (PARTITION BY patient_id ORDER BY visit_date)",
        ],
        "explanation": (
            "1. LAG(visit_date) gets the previous visit date per patient.\n"
            "2. julianday(current) - julianday(previous) gives the gap in days.\n"
            "3. CAST AS INTEGER removes any fractional part.\n"
            "4. The first visit per patient has NULL for prev_visit_date."
        ),
        "approach": [
            "Use LAG to access the previous row's visit_date.",
            "Partition by patient_id so lag stays within each patient.",
            "Compute the difference using julianday.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY, computing lag across all patients.",
            "Not filtering to completed visits first.",
        ],
        "concept_tags": ["LAG", "OVER", "PARTITION BY", "window function", "date arithmetic"],
    },
    {
        "id": "hc-034",
        "slug": "top-biller-per-department",
        "title": "Top Billing Doctor per Department",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "healthcare",
        "description": (
            "Find the doctor with the highest total billing in each "
            "department. Return the department name, doctor name, and their "
            "total billing amount. Use ROW_NUMBER to pick the top one per "
            "department."
        ),
        "schema_hint": ["billing", "visits", "doctors", "departments"],
        "solution_query": (
            "SELECT department_name, first_name, last_name, total_billed\n"
            "FROM (\n"
            "  SELECT dept.name AS department_name,\n"
            "         d.first_name, d.last_name,\n"
            "         ROUND(SUM(b.amount), 2) AS total_billed,\n"
            "         ROW_NUMBER() OVER (\n"
            "           PARTITION BY dept.id\n"
            "           ORDER BY SUM(b.amount) DESC\n"
            "         ) AS rn\n"
            "  FROM billing b\n"
            "  JOIN visits v ON b.visit_id = v.id\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "  JOIN departments dept ON d.department_id = dept.id\n"
            "  GROUP BY dept.id, dept.name, d.id, d.first_name, d.last_name\n"
            ") ranked\n"
            "WHERE rn = 1;"
        ),
        "hints": [
            "First compute total billing per doctor per department.",
            "Use ROW_NUMBER partitioned by department to rank doctors.",
            "Wrap in an outer query and filter WHERE rn = 1.",
            "ROW_NUMBER() OVER (PARTITION BY dept.id ORDER BY SUM(b.amount) DESC)",
        ],
        "explanation": (
            "1. The inner query sums billing per doctor and department.\n"
            "2. ROW_NUMBER ranks doctors within each department by total.\n"
            "3. The outer query filters to rank 1 — the top biller."
        ),
        "approach": [
            "Aggregate billing by doctor and department.",
            "Rank with ROW_NUMBER partitioned by department.",
            "Filter to rank 1 in the outer query.",
        ],
        "common_mistakes": [
            "Using RANK instead of ROW_NUMBER (ties could return multiple rows).",
            "Forgetting to GROUP BY before applying the window function.",
        ],
        "concept_tags": ["ROW_NUMBER", "OVER", "PARTITION BY", "derived table", "top-N per group"],
    },
    {
        "id": "hc-035",
        "slug": "moving-average-billing",
        "title": "7-Day Moving Average of Daily Billing",
        "difficulty": "hard",
        "category": "window-functions",
        "dataset": "healthcare",
        "description": (
            "Compute a 7-day trailing moving average of total daily billing. "
            "First aggregate billing by billed_at date, then compute the "
            "moving average over the preceding 6 rows and the current row."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT billed_at,\n"
            "       daily_total,\n"
            "       ROUND(AVG(daily_total) OVER (\n"
            "         ORDER BY billed_at\n"
            "         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg_7day\n"
            "FROM (\n"
            "  SELECT billed_at,\n"
            "         ROUND(SUM(amount), 2) AS daily_total\n"
            "  FROM billing\n"
            "  GROUP BY billed_at\n"
            ") daily\n"
            "ORDER BY billed_at;"
        ),
        "hints": [
            "First aggregate billing per day in a subquery.",
            "Use AVG as a window function with a frame clause.",
            "ROWS BETWEEN 6 PRECEDING AND CURRENT ROW gives a 7-row window.",
            "AVG(daily_total) OVER (ORDER BY billed_at ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)",
        ],
        "explanation": (
            "1. The inner query sums billing per day.\n"
            "2. AVG as a window function with a 7-row frame computes the moving average.\n"
            "3. ROWS BETWEEN 6 PRECEDING AND CURRENT ROW includes the current row "
            "and 6 prior rows.\n"
            "4. ROUND formats the output."
        ),
        "approach": [
            "Aggregate to daily totals first.",
            "Apply AVG with a ROWS frame clause for the moving window.",
            "Order results by date.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS (RANGE works on value ranges, not row counts).",
            "Forgetting to aggregate to daily level first.",
        ],
        "concept_tags": [
            "AVG", "OVER", "ROWS BETWEEN", "moving average",
            "window function", "frame clause",
        ],
    },

    # =========================================================================
    # LEVEL 6 — ADVANCED (5 problems: hc-036 through hc-040)
    # =========================================================================
    {
        "id": "hc-036",
        "slug": "patient-visit-summary-cte",
        "title": "Patient Visit Summary with CTE",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Using a CTE, create a patient visit summary that shows each "
            "patient's name, total visits, completed visits, and completion "
            "rate (percentage of visits that are completed). Only include "
            "patients with at least 3 visits. Round the rate to 1 decimal."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "WITH visit_stats AS (\n"
            "  SELECT patient_id,\n"
            "         COUNT(*) AS total_visits,\n"
            "         SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) "
            "AS completed_visits\n"
            "  FROM visits\n"
            "  GROUP BY patient_id\n"
            "  HAVING COUNT(*) >= 3\n"
            ")\n"
            "SELECT p.first_name, p.last_name,\n"
            "       vs.total_visits,\n"
            "       vs.completed_visits,\n"
            "       ROUND(100.0 * vs.completed_visits / vs.total_visits, 1) "
            "AS completion_rate\n"
            "FROM visit_stats vs\n"
            "JOIN patients p ON vs.patient_id = p.id\n"
            "ORDER BY completion_rate DESC;"
        ),
        "hints": [
            "A CTE (WITH clause) lets you define a named temporary result set.",
            "Use CASE WHEN to conditionally count completed visits.",
            "Divide completed by total and multiply by 100 for percentage.",
            "WITH visit_stats AS (SELECT patient_id, COUNT(*), SUM(CASE ...) ...)",
        ],
        "explanation": (
            "1. The CTE visit_stats computes total and completed visits per patient.\n"
            "2. HAVING COUNT(*) >= 3 filters to active patients.\n"
            "3. The main query joins to patients for names.\n"
            "4. Completion rate = 100 * completed / total."
        ),
        "approach": [
            "Define a CTE that aggregates visit stats per patient.",
            "Filter with HAVING in the CTE.",
            "Join the CTE to patients for the final output.",
        ],
        "common_mistakes": [
            "Using integer division (100 instead of 100.0).",
            "Putting the HAVING filter in the outer query instead of the CTE.",
        ],
        "concept_tags": ["CTE", "WITH", "CASE WHEN", "percentage", "HAVING"],
    },
    {
        "id": "hc-037",
        "slug": "duplicate-patient-emails",
        "title": "Find Duplicate Patient Emails",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Data quality check: find all patients who share an email address "
            "with at least one other patient. Return the email, patient id, "
            "first name, and last name for each duplicate. Order by email, "
            "then by id."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT p.email, p.id, p.first_name, p.last_name\n"
            "FROM patients p\n"
            "WHERE p.email IN (\n"
            "  SELECT email\n"
            "  FROM patients\n"
            "  GROUP BY email\n"
            "  HAVING COUNT(*) > 1\n"
            ")\n"
            "ORDER BY p.email, p.id;"
        ),
        "hints": [
            "First identify emails that appear more than once.",
            "Use GROUP BY email HAVING COUNT(*) > 1 to find duplicates.",
            "Then filter the patients table to those emails.",
            "WHERE email IN (SELECT email ... HAVING COUNT(*) > 1)",
        ],
        "explanation": (
            "1. The subquery finds emails with more than one occurrence.\n"
            "2. The outer query returns all patients matching those emails.\n"
            "3. ORDER BY email, id groups duplicates together."
        ),
        "approach": [
            "Use a subquery with GROUP BY and HAVING to find duplicate emails.",
            "Filter the main query to those emails.",
            "Order for readability.",
        ],
        "common_mistakes": [
            "Returning only one row per duplicate email instead of all patients.",
            "Using DISTINCT which would hide the duplicates.",
        ],
        "concept_tags": ["subquery", "HAVING", "data quality", "duplicates"],
    },
    {
        "id": "hc-038",
        "slug": "department-budget-vs-salary",
        "title": "Department Budget Utilization",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Compare each department's total doctor salaries to its budget. "
            "Return the department name, budget, total salary cost, and the "
            "percentage of budget used (salary / budget * 100). Round to 1 "
            "decimal place. Order by utilization descending."
        ),
        "schema_hint": ["departments", "doctors"],
        "solution_query": (
            "SELECT dept.name,\n"
            "       dept.budget,\n"
            "       ROUND(SUM(d.salary), 2) AS total_salary,\n"
            "       ROUND(100.0 * SUM(d.salary) / dept.budget, 1) "
            "AS budget_utilization_pct\n"
            "FROM departments dept\n"
            "JOIN doctors d ON dept.id = d.department_id\n"
            "GROUP BY dept.id, dept.name, dept.budget\n"
            "ORDER BY budget_utilization_pct DESC;"
        ),
        "hints": [
            "Join departments to doctors and sum salaries per department.",
            "Divide total salary by budget and multiply by 100.",
            "Use 100.0 to avoid integer division.",
            "ROUND(100.0 * SUM(d.salary) / dept.budget, 1)",
        ],
        "explanation": (
            "1. JOIN departments to doctors on department_id.\n"
            "2. GROUP BY department to sum salaries.\n"
            "3. Compute utilization as salary / budget * 100.\n"
            "4. Round and order by utilization descending."
        ),
        "approach": [
            "Join departments to doctors.",
            "Group by department and sum salaries.",
            "Compute the budget utilization percentage.",
        ],
        "common_mistakes": [
            "Forgetting 100.0 and getting integer division.",
            "Not grouping by department, computing one global total.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "SUM", "percentage", "budget analysis"],
    },
    {
        "id": "hc-039",
        "slug": "monthly-visit-trends",
        "title": "Monthly Visit Trends with CTEs",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Using CTEs, calculate the monthly visit count and the "
            "month-over-month change in visits. Return the month (as "
            "YYYY-MM), visit count, previous month count, and the change. "
            "Order by month."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "WITH monthly AS (\n"
            "  SELECT strftime('%Y-%m', visit_date) AS month,\n"
            "         COUNT(*) AS visit_count\n"
            "  FROM visits\n"
            "  GROUP BY strftime('%Y-%m', visit_date)\n"
            "),\n"
            "with_lag AS (\n"
            "  SELECT month,\n"
            "         visit_count,\n"
            "         LAG(visit_count) OVER (ORDER BY month) AS prev_count\n"
            "  FROM monthly\n"
            ")\n"
            "SELECT month,\n"
            "       visit_count,\n"
            "       prev_count,\n"
            "       visit_count - prev_count AS month_change\n"
            "FROM with_lag\n"
            "ORDER BY month;"
        ),
        "hints": [
            "Use strftime('%Y-%m', visit_date) to extract year-month.",
            "First CTE aggregates visits per month.",
            "Second CTE uses LAG to get the previous month's count.",
            "Subtract previous from current for the change.",
        ],
        "explanation": (
            "1. The monthly CTE groups visits by year-month.\n"
            "2. The with_lag CTE adds the previous month's count using LAG.\n"
            "3. The final query computes the difference.\n"
            "4. The first month has NULL for prev_count and month_change."
        ),
        "approach": [
            "Aggregate to monthly counts in the first CTE.",
            "Apply LAG in the second CTE.",
            "Compute the difference in the final SELECT.",
        ],
        "common_mistakes": [
            "Using substr instead of strftime for date extraction.",
            "Forgetting ORDER BY in the LAG window clause.",
        ],
        "concept_tags": ["CTE", "WITH", "LAG", "strftime", "trend analysis"],
    },
    {
        "id": "hc-040",
        "slug": "comprehensive-doctor-scorecard",
        "title": "Comprehensive Doctor Scorecard",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Build a doctor scorecard that shows: department name, doctor "
            "full name, total visits, total prescriptions written, total "
            "billing generated, and their rank by total billing within "
            "their department. Use CTEs for clarity. Only include doctors "
            "with at least 1 visit."
        ),
        "schema_hint": [
            "doctors", "departments", "visits", "prescriptions", "billing",
        ],
        "solution_query": (
            "WITH doc_visits AS (\n"
            "  SELECT doctor_id, COUNT(*) AS total_visits\n"
            "  FROM visits\n"
            "  GROUP BY doctor_id\n"
            "),\n"
            "doc_prescriptions AS (\n"
            "  SELECT v.doctor_id, COUNT(rx.id) AS total_prescriptions\n"
            "  FROM visits v\n"
            "  JOIN prescriptions rx ON v.id = rx.visit_id\n"
            "  GROUP BY v.doctor_id\n"
            "),\n"
            "doc_billing AS (\n"
            "  SELECT v.doctor_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_billed\n"
            "  FROM visits v\n"
            "  JOIN billing b ON v.id = b.visit_id\n"
            "  GROUP BY v.doctor_id\n"
            ")\n"
            "SELECT dept.name AS department_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       COALESCE(dv.total_visits, 0) AS total_visits,\n"
            "       COALESCE(dp.total_prescriptions, 0) AS total_prescriptions,\n"
            "       COALESCE(db.total_billed, 0) AS total_billed,\n"
            "       RANK() OVER (\n"
            "         PARTITION BY dept.id\n"
            "         ORDER BY COALESCE(db.total_billed, 0) DESC\n"
            "       ) AS dept_billing_rank\n"
            "FROM doctors d\n"
            "JOIN departments dept ON d.department_id = dept.id\n"
            "JOIN doc_visits dv ON d.id = dv.doctor_id\n"
            "LEFT JOIN doc_prescriptions dp ON d.id = dp.doctor_id\n"
            "LEFT JOIN doc_billing db ON d.id = db.doctor_id\n"
            "ORDER BY dept.name, dept_billing_rank;"
        ),
        "hints": [
            "Use separate CTEs for visit counts, prescription counts, and billing sums.",
            "JOIN the CTEs to the doctors and departments tables.",
            "Use COALESCE to handle doctors with no prescriptions or billing.",
            "Add RANK() partitioned by department for the billing rank.",
        ],
        "explanation": (
            "1. Three CTEs compute per-doctor stats independently.\n"
            "2. The main query joins doctors to departments and the CTEs.\n"
            "3. LEFT JOIN for prescriptions and billing handles doctors with none.\n"
            "4. COALESCE replaces NULL with 0.\n"
            "5. RANK() partitioned by department ranks by billing."
        ),
        "approach": [
            "Break the problem into independent aggregations (CTEs).",
            "Join everything together in the final query.",
            "Use LEFT JOIN and COALESCE for optional data.",
            "Add a window function for ranking.",
        ],
        "common_mistakes": [
            "Using INNER JOIN for all CTEs, losing doctors with no prescriptions.",
            "Not using COALESCE, resulting in NULL instead of 0.",
            "Trying to compute everything in a single query without CTEs.",
        ],
        "concept_tags": [
            "CTE", "WITH", "LEFT JOIN", "COALESCE", "RANK",
            "PARTITION BY", "multi-CTE", "scorecard",
        ],
    },
    # =========================================================================
    # LEVEL 6 — EXTENDED SET (60 problems: hc-041 through hc-100)
    # =========================================================================
    {
        "id": "hc-041",
        "slug": "count-patients-per-blood-type",
        "title": "Count Patients per Blood Type",
        "difficulty": "easy",
        "category": "group_by",
        "dataset": "healthcare",
        "description": (
            "The blood bank coordinator needs an inventory forecast. "
            "Count the number of patients for each blood type. Return "
            "the blood_type and patient_count, ordered by patient_count "
            "descending."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT blood_type, COUNT(*) AS patient_count\n"
            "FROM patients\n"
            "GROUP BY blood_type\n"
            "ORDER BY patient_count DESC;"
        ),
        "hints": [
            "You need to group rows that share the same blood type.",
            "COUNT(*) counts the number of rows in each group.",
            "Use GROUP BY blood_type to create the groups.",
            "Add ORDER BY on the count alias to sort the results.",
        ],
        "explanation": (
            "1. GROUP BY blood_type partitions patients by blood type.\n"
            "2. COUNT(*) counts patients in each group.\n"
            "3. ORDER BY patient_count DESC shows the most common type first."
        ),
        "approach": [
            "Identify that patients table has blood_type.",
            "Group by blood_type and count.",
            "Sort by the count descending.",
        ],
        "common_mistakes": [
            "Forgetting GROUP BY and getting a single total count.",
            "Using COUNT(blood_type) instead of COUNT(*) — same here but conceptually different.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "hc-042",
        "slug": "patients-without-insurance",
        "title": "Patients Without Insurance",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "The financial counseling team wants to reach out to uninsured "
            "patients. List the first name, last name, and city of patients "
            "who have no insurance (insurance_id is NULL). Order by last name."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, city\n"
            "FROM patients\n"
            "WHERE insurance_id IS NULL\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "NULL values require a special comparison operator.",
            "You cannot use = NULL; use IS NULL instead.",
            "Filter the patients table on the insurance_id column.",
            "WHERE insurance_id IS NULL is the correct filter.",
        ],
        "explanation": (
            "1. SELECT the requested columns from patients.\n"
            "2. WHERE insurance_id IS NULL finds uninsured patients.\n"
            "3. ORDER BY last_name sorts alphabetically."
        ),
        "approach": [
            "Check the patients table for the insurance_id column.",
            "Use IS NULL to find missing values.",
            "Sort by last name.",
        ],
        "common_mistakes": [
            "Using = NULL instead of IS NULL.",
            "Using != '' which does not detect NULL values.",
        ],
        "concept_tags": ["WHERE", "IS NULL", "ORDER BY"],
    },
    {
        "id": "hc-043",
        "slug": "earliest-and-latest-hire",
        "title": "Earliest and Latest Doctor Hire Dates",
        "difficulty": "easy",
        "category": "aggregate",
        "dataset": "healthcare",
        "description": (
            "HR wants to know the tenure range of the medical staff. "
            "Return the earliest hire_date and the latest hire_date "
            "from the doctors table as min_hire_date and max_hire_date."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT MIN(hire_date) AS min_hire_date,\n"
            "       MAX(hire_date) AS max_hire_date\n"
            "FROM doctors;"
        ),
        "hints": [
            "You need aggregate functions that find extreme values.",
            "MIN and MAX work on date strings in YYYY-MM-DD format.",
            "No GROUP BY is needed when aggregating the whole table.",
            "SELECT MIN(hire_date) AS min_hire_date, MAX(hire_date) AS max_hire_date FROM doctors;",
        ],
        "explanation": (
            "1. MIN(hire_date) finds the earliest date.\n"
            "2. MAX(hire_date) finds the latest date.\n"
            "3. No GROUP BY means one row for the entire table."
        ),
        "approach": [
            "Use MIN and MAX aggregate functions on hire_date.",
            "Alias the results as requested.",
        ],
        "common_mistakes": [
            "Adding an unnecessary GROUP BY clause.",
            "Confusing MIN/MAX with FIRST/LAST which are not standard SQL.",
        ],
        "concept_tags": ["MIN", "MAX", "aggregate"],
    },
    {
        "id": "hc-044",
        "slug": "distinct-diagnoses",
        "title": "Distinct Diagnoses",
        "difficulty": "easy",
        "category": "select",
        "dataset": "healthcare",
        "description": (
            "The medical records department needs a clean list of every "
            "unique diagnosis that has been recorded. Return all distinct "
            "diagnosis values from the visits table, sorted alphabetically."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT DISTINCT diagnosis\n"
            "FROM visits\n"
            "ORDER BY diagnosis;"
        ),
        "hints": [
            "You need to eliminate duplicate values from the results.",
            "The DISTINCT keyword removes duplicate rows.",
            "Place DISTINCT right after SELECT.",
            "SELECT DISTINCT diagnosis FROM visits ORDER BY diagnosis;",
        ],
        "explanation": (
            "1. SELECT DISTINCT diagnosis removes duplicate diagnoses.\n"
            "2. ORDER BY diagnosis sorts the list alphabetically."
        ),
        "approach": [
            "Use DISTINCT to get unique diagnosis values.",
            "Sort alphabetically.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT and getting repeated diagnoses.",
            "Using GROUP BY without an aggregate — works but DISTINCT is cleaner here.",
        ],
        "concept_tags": ["SELECT", "DISTINCT", "ORDER BY"],
    },
    {
        "id": "hc-045",
        "slug": "average-billing-by-status",
        "title": "Average Billing Amount by Status",
        "difficulty": "easy",
        "category": "group_by",
        "dataset": "healthcare",
        "description": (
            "Finance wants to understand billing patterns. Calculate "
            "the average billing amount for each billing status. Return "
            "status and avg_amount (rounded to 2 decimal places), "
            "ordered by avg_amount descending."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT status, ROUND(AVG(amount), 2) AS avg_amount\n"
            "FROM billing\n"
            "GROUP BY status\n"
            "ORDER BY avg_amount DESC;"
        ),
        "hints": [
            "Use AVG() to compute the average of a numeric column.",
            "Group by the status column to get per-status averages.",
            "ROUND(value, 2) rounds to two decimal places.",
            "SELECT status, ROUND(AVG(amount), 2) AS avg_amount FROM billing GROUP BY status;",
        ],
        "explanation": (
            "1. GROUP BY status partitions billing rows by status.\n"
            "2. AVG(amount) computes the average per group.\n"
            "3. ROUND(..., 2) formats to two decimals.\n"
            "4. ORDER BY avg_amount DESC shows highest average first."
        ),
        "approach": [
            "Group billing records by status.",
            "Compute the average amount per group.",
            "Round and sort.",
        ],
        "common_mistakes": [
            "Forgetting ROUND and getting many decimal places.",
            "Not aliasing the column, making ORDER BY harder.",
        ],
        "concept_tags": ["GROUP BY", "AVG", "ROUND", "ORDER BY"],
    },
    {
        "id": "hc-046",
        "slug": "patients-with-doctor-names",
        "title": "Patient Visits with Doctor Names",
        "difficulty": "easy",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "The patient portal needs to display visit history with "
            "doctor names. Return patient first_name, patient last_name, "
            "visit_date, and the doctor's full name (first_name || ' ' || "
            "last_name) as doctor_name. Join visits with patients and "
            "doctors. Order by visit_date descending."
        ),
        "schema_hint": ["patients", "visits", "doctors"],
        "solution_query": (
            "SELECT p.first_name, p.last_name, v.visit_date,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name\n"
            "FROM visits v\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "ORDER BY v.visit_date DESC;"
        ),
        "hints": [
            "You need data from three tables: patients, visits, and doctors.",
            "Use JOIN to connect visits to both patients and doctors.",
            "The || operator concatenates strings in SQLite.",
            "Join visits to patients on patient_id and to doctors on doctor_id.",
        ],
        "explanation": (
            "1. JOIN visits to patients on patient_id.\n"
            "2. JOIN visits to doctors on doctor_id.\n"
            "3. Concatenate doctor first and last name.\n"
            "4. Order by visit_date descending."
        ),
        "approach": [
            "Identify the foreign keys linking the three tables.",
            "Use two JOINs from the visits table.",
            "Concatenate doctor name with ||.",
        ],
        "common_mistakes": [
            "Ambiguous column names — use table aliases.",
            "Joining on the wrong columns.",
        ],
        "concept_tags": ["JOIN", "string concatenation", "multi-table"],
    },
    {
        "id": "hc-047",
        "slug": "top-prescribed-medications",
        "title": "Top 5 Most Prescribed Medications",
        "difficulty": "easy",
        "category": "group_by",
        "dataset": "healthcare",
        "description": (
            "The pharmacy manager wants to know which medications are "
            "prescribed most often. Return the medication name and "
            "prescription_count for the top 5 most frequently prescribed "
            "medications."
        ),
        "schema_hint": ["prescriptions"],
        "solution_query": (
            "SELECT medication, COUNT(*) AS prescription_count\n"
            "FROM prescriptions\n"
            "GROUP BY medication\n"
            "ORDER BY prescription_count DESC\n"
            "LIMIT 5;"
        ),
        "hints": [
            "Group prescriptions by medication name.",
            "Count how many times each medication appears.",
            "Use ORDER BY and LIMIT to get only the top 5.",
            "GROUP BY medication ... ORDER BY prescription_count DESC LIMIT 5;",
        ],
        "explanation": (
            "1. GROUP BY medication groups all prescriptions by drug name.\n"
            "2. COUNT(*) counts prescriptions per medication.\n"
            "3. ORDER BY ... DESC LIMIT 5 returns the top 5."
        ),
        "approach": [
            "Group by medication.",
            "Count occurrences.",
            "Sort descending and limit to 5.",
        ],
        "common_mistakes": [
            "Forgetting LIMIT and returning all medications.",
            "Sorting ascending instead of descending.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY", "LIMIT"],
    },
    {
        "id": "hc-048",
        "slug": "visits-with-abnormal-labs",
        "title": "Visits That Had Abnormal Lab Results",
        "difficulty": "easy",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "Quality assurance wants to review visits where patients had "
            "abnormal lab results. Return distinct visit_id, visit_date, "
            "and diagnosis for visits that have at least one lab result "
            "where is_abnormal = 1. Order by visit_date."
        ),
        "schema_hint": ["visits", "lab_results"],
        "solution_query": (
            "SELECT DISTINCT v.id AS visit_id, v.visit_date, v.diagnosis\n"
            "FROM visits v\n"
            "JOIN lab_results lr ON v.id = lr.visit_id\n"
            "WHERE lr.is_abnormal = 1\n"
            "ORDER BY v.visit_date;"
        ),
        "hints": [
            "Join visits to lab_results on visit_id.",
            "Filter for abnormal results with WHERE is_abnormal = 1.",
            "A visit may have multiple abnormal labs — use DISTINCT.",
            "SELECT DISTINCT v.id, v.visit_date, v.diagnosis FROM visits v JOIN lab_results lr ON ...",
        ],
        "explanation": (
            "1. JOIN visits to lab_results.\n"
            "2. WHERE is_abnormal = 1 filters to abnormal labs.\n"
            "3. DISTINCT prevents duplicate visit rows.\n"
            "4. ORDER BY visit_date for chronological order."
        ),
        "approach": [
            "Join the two tables on visit_id.",
            "Filter for abnormal results.",
            "Use DISTINCT to avoid duplicates.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT when a visit has multiple abnormal labs.",
            "Using is_abnormal = 'true' instead of is_abnormal = 1.",
        ],
        "concept_tags": ["JOIN", "WHERE", "DISTINCT"],
    },
    {
        "id": "hc-049",
        "slug": "departments-on-each-floor",
        "title": "Departments on Each Floor",
        "difficulty": "easy",
        "category": "group_by",
        "dataset": "healthcare",
        "description": (
            "Facilities management needs to know how many departments "
            "are on each floor of the hospital. Return floor and "
            "dept_count, ordered by floor."
        ),
        "schema_hint": ["departments"],
        "solution_query": (
            "SELECT floor, COUNT(*) AS dept_count\n"
            "FROM departments\n"
            "GROUP BY floor\n"
            "ORDER BY floor;"
        ),
        "hints": [
            "Group departments by their floor number.",
            "Count the departments in each group.",
            "Order the results by floor number.",
            "SELECT floor, COUNT(*) AS dept_count FROM departments GROUP BY floor ORDER BY floor;",
        ],
        "explanation": (
            "1. GROUP BY floor groups departments by floor.\n"
            "2. COUNT(*) counts departments per floor.\n"
            "3. ORDER BY floor sorts numerically."
        ),
        "approach": [
            "Group by floor.",
            "Count departments per floor.",
            "Sort by floor.",
        ],
        "common_mistakes": [
            "Forgetting ORDER BY, returning floors in arbitrary order.",
        ],
        "concept_tags": ["GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "hc-050",
        "slug": "prescriptions-with-high-refills",
        "title": "Prescriptions with High Refill Counts",
        "difficulty": "easy",
        "category": "where",
        "dataset": "healthcare",
        "description": (
            "The controlled substances team wants to audit prescriptions "
            "with many refills. Find all prescriptions where refills >= 5. "
            "Return medication, dosage, frequency, and refills, ordered "
            "by refills descending."
        ),
        "schema_hint": ["prescriptions"],
        "solution_query": (
            "SELECT medication, dosage, frequency, refills\n"
            "FROM prescriptions\n"
            "WHERE refills >= 5\n"
            "ORDER BY refills DESC;"
        ),
        "hints": [
            "Filter the prescriptions table based on the refills column.",
            "Use >= for 'greater than or equal to'.",
            "Order results by refills in descending order.",
            "WHERE refills >= 5 ORDER BY refills DESC;",
        ],
        "explanation": (
            "1. SELECT the four columns from prescriptions.\n"
            "2. WHERE refills >= 5 filters to high-refill prescriptions.\n"
            "3. ORDER BY refills DESC shows the highest refill counts first."
        ),
        "approach": [
            "Filter prescriptions by refill count.",
            "Sort by refills descending.",
        ],
        "common_mistakes": [
            "Using > 5 instead of >= 5, missing prescriptions with exactly 5 refills.",
        ],
        "concept_tags": ["WHERE", "comparison operators", "ORDER BY"],
    },
    {
        "id": "hc-051",
        "slug": "doctor-patient-count",
        "title": "Number of Unique Patients per Doctor",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "Hospital management wants to understand each doctor's patient "
            "load. For each doctor, return their full name (first_name || "
            "' ' || last_name) as doctor_name, specialty, and the number "
            "of distinct patients they have seen as patient_count. Only "
            "include doctors who have seen at least one patient. Order by "
            "patient_count descending."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       d.specialty,\n"
            "       COUNT(DISTINCT v.patient_id) AS patient_count\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "GROUP BY d.id, d.first_name, d.last_name, d.specialty\n"
            "ORDER BY patient_count DESC;"
        ),
        "hints": [
            "Join doctors to visits to find which patients each doctor saw.",
            "A doctor may see the same patient multiple times — use COUNT(DISTINCT ...).",
            "Group by doctor to get per-doctor counts.",
            "The JOIN naturally excludes doctors with no visits.",
        ],
        "explanation": (
            "1. JOIN doctors to visits on doctor_id.\n"
            "2. GROUP BY doctor to aggregate.\n"
            "3. COUNT(DISTINCT patient_id) avoids counting repeat visits.\n"
            "4. The INNER JOIN excludes doctors with zero visits."
        ),
        "approach": [
            "Join doctors to visits.",
            "Group by doctor.",
            "Count distinct patients per doctor.",
        ],
        "common_mistakes": [
            "Using COUNT(*) instead of COUNT(DISTINCT patient_id).",
            "Forgetting to group by doctor.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT DISTINCT"],
    },
    {
        "id": "hc-052",
        "slug": "insurance-plan-revenue",
        "title": "Total Billing by Insurance Plan Type",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "The CFO wants to compare revenue across insurance plan types. "
            "Join billing through visits and patients to insurance. Return "
            "plan_type, total_billed (sum of billing amount), and "
            "total_covered (sum of insurance_covered), both rounded to 2 "
            "decimals. Order by total_billed descending."
        ),
        "schema_hint": ["billing", "visits", "patients", "insurance"],
        "solution_query": (
            "SELECT i.plan_type,\n"
            "       ROUND(SUM(b.amount), 2) AS total_billed,\n"
            "       ROUND(SUM(b.insurance_covered), 2) AS total_covered\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN insurance i ON p.insurance_id = i.id\n"
            "GROUP BY i.plan_type\n"
            "ORDER BY total_billed DESC;"
        ),
        "hints": [
            "You need to traverse billing -> visits -> patients -> insurance.",
            "Each JOIN connects through a foreign key.",
            "Group by plan_type and sum the billing amounts.",
            "Use ROUND to format the monetary totals.",
        ],
        "explanation": (
            "1. Chain JOINs: billing -> visits -> patients -> insurance.\n"
            "2. GROUP BY plan_type aggregates across plan types.\n"
            "3. SUM computes totals, ROUND formats to 2 decimals."
        ),
        "approach": [
            "Trace the foreign key path from billing to insurance.",
            "Join all four tables.",
            "Group by plan type and sum amounts.",
        ],
        "common_mistakes": [
            "Missing one of the intermediate joins.",
            "Grouping by the wrong column.",
            "Not handling patients with NULL insurance_id (INNER JOIN skips them).",
        ],
        "concept_tags": ["JOIN", "multi-table", "GROUP BY", "SUM", "ROUND"],
    },
    {
        "id": "hc-053",
        "slug": "doctors-above-dept-avg-salary",
        "title": "Doctors Earning Above Department Average",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "HR wants to identify high earners relative to their peers. "
            "Find doctors whose salary is above the average salary of "
            "their department. Return doctor full name, department_id, "
            "salary, and the department average salary (rounded to 2 "
            "decimals) as dept_avg_salary. Order by salary descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       d.department_id,\n"
            "       d.salary,\n"
            "       ROUND(dept.avg_sal, 2) AS dept_avg_salary\n"
            "FROM doctors d\n"
            "JOIN (\n"
            "  SELECT department_id, AVG(salary) AS avg_sal\n"
            "  FROM doctors\n"
            "  GROUP BY department_id\n"
            ") dept ON d.department_id = dept.department_id\n"
            "WHERE d.salary > dept.avg_sal\n"
            "ORDER BY d.salary DESC;"
        ),
        "hints": [
            "You need the average salary per department to compare against.",
            "A subquery can compute department averages.",
            "Join each doctor to their department's average.",
            "Filter where the doctor's salary exceeds the average.",
        ],
        "explanation": (
            "1. Subquery computes AVG(salary) per department.\n"
            "2. JOIN each doctor to their department's average.\n"
            "3. WHERE salary > avg_sal filters to above-average earners.\n"
            "4. ORDER BY salary DESC."
        ),
        "approach": [
            "Compute department averages in a subquery.",
            "Join doctors to the subquery.",
            "Filter for doctors above their department average.",
        ],
        "common_mistakes": [
            "Comparing against the global average instead of department average.",
            "Using a correlated subquery in WHERE which is less efficient.",
        ],
        "concept_tags": ["subquery", "JOIN", "AVG", "comparison"],
    },
    {
        "id": "hc-054",
        "slug": "visit-count-by-month-year",
        "title": "Visit Count by Month and Year",
        "difficulty": "medium",
        "category": "group_by",
        "dataset": "healthcare",
        "description": (
            "Operations wants a monthly breakdown of visits. Extract the "
            "year and month from visit_date and count visits per month. "
            "Return visit_year, visit_month, and visit_count. Order by "
            "year then month."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT CAST(strftime('%Y', visit_date) AS INTEGER) AS visit_year,\n"
            "       CAST(strftime('%m', visit_date) AS INTEGER) AS visit_month,\n"
            "       COUNT(*) AS visit_count\n"
            "FROM visits\n"
            "GROUP BY strftime('%Y', visit_date), strftime('%m', visit_date)\n"
            "ORDER BY visit_year, visit_month;"
        ),
        "hints": [
            "SQLite uses strftime() to extract date parts.",
            "strftime('%Y', date) gives the year, '%m' gives the month.",
            "Group by both year and month to get monthly counts.",
            "CAST to INTEGER removes leading zeros from months.",
        ],
        "explanation": (
            "1. strftime extracts year and month from visit_date.\n"
            "2. GROUP BY year and month partitions visits by month.\n"
            "3. COUNT(*) counts visits per month.\n"
            "4. ORDER BY year, month for chronological order."
        ),
        "approach": [
            "Use strftime to extract year and month.",
            "Group by both fields.",
            "Count and order.",
        ],
        "common_mistakes": [
            "Forgetting to group by both year and month.",
            "Not using strftime in SQLite (YEAR() is not available).",
        ],
        "concept_tags": ["GROUP BY", "strftime", "COUNT", "date extraction"],
    },
    {
        "id": "hc-055",
        "slug": "patients-multiple-visits",
        "title": "Patients with More Than 3 Visits",
        "difficulty": "medium",
        "category": "having",
        "dataset": "healthcare",
        "description": (
            "Care management wants to identify frequent visitors. Find "
            "patients who have had more than 3 visits. Return patient "
            "first_name, last_name, and visit_count. Order by visit_count "
            "descending."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       COUNT(*) AS visit_count\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "HAVING COUNT(*) > 3\n"
            "ORDER BY visit_count DESC;"
        ),
        "hints": [
            "Join patients to visits and count visits per patient.",
            "Use HAVING to filter groups after aggregation.",
            "WHERE filters rows; HAVING filters groups.",
            "HAVING COUNT(*) > 3 keeps only frequent visitors.",
        ],
        "explanation": (
            "1. JOIN patients to visits.\n"
            "2. GROUP BY patient to count visits.\n"
            "3. HAVING COUNT(*) > 3 filters to frequent visitors.\n"
            "4. ORDER BY visit_count DESC."
        ),
        "approach": [
            "Join and group by patient.",
            "Count visits per patient.",
            "Use HAVING to filter groups.",
        ],
        "common_mistakes": [
            "Using WHERE COUNT(*) > 3 instead of HAVING.",
            "Forgetting the JOIN and only querying visits.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT"],
    },
    {
        "id": "hc-056",
        "slug": "unpaid-billing-with-patient-info",
        "title": "Overdue Bills with Patient Contact Info",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "Collections needs contact info for overdue accounts. Find "
            "all billing records with status 'overdue'. Return patient "
            "full name, email, phone, billing amount, and "
            "patient_responsibility. Order by patient_responsibility "
            "descending."
        ),
        "schema_hint": ["billing", "visits", "patients"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       p.email, p.phone,\n"
            "       b.amount, b.patient_responsibility\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE b.status = 'overdue'\n"
            "ORDER BY b.patient_responsibility DESC;"
        ),
        "hints": [
            "Billing connects to patients through the visits table.",
            "Filter billing by status = 'overdue'.",
            "Join billing -> visits -> patients to get contact info.",
            "Concatenate first and last name for the full name.",
        ],
        "explanation": (
            "1. JOIN billing to visits to patients.\n"
            "2. WHERE status = 'overdue' filters to overdue bills.\n"
            "3. Concatenate patient name.\n"
            "4. Order by patient_responsibility descending."
        ),
        "approach": [
            "Trace the join path from billing to patients.",
            "Filter by billing status.",
            "Return contact information.",
        ],
        "common_mistakes": [
            "Joining billing directly to patients — there is no direct FK.",
            "Forgetting the WHERE filter.",
        ],
        "concept_tags": ["JOIN", "multi-table", "WHERE", "string concatenation"],
    },
    {
        "id": "hc-057",
        "slug": "lab-tests-per-visit",
        "title": "Number of Lab Tests per Visit",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "The lab director wants to know how many tests are ordered "
            "per visit on average. Return the visit_id, visit_date, "
            "diagnosis, and test_count for each visit that had lab tests. "
            "Order by test_count descending, then visit_date."
        ),
        "schema_hint": ["visits", "lab_results"],
        "solution_query": (
            "SELECT v.id AS visit_id, v.visit_date, v.diagnosis,\n"
            "       COUNT(lr.id) AS test_count\n"
            "FROM visits v\n"
            "JOIN lab_results lr ON v.id = lr.visit_id\n"
            "GROUP BY v.id, v.visit_date, v.diagnosis\n"
            "ORDER BY test_count DESC, v.visit_date;"
        ),
        "hints": [
            "Join visits to lab_results.",
            "Group by visit to count tests per visit.",
            "The INNER JOIN excludes visits with no lab tests.",
            "Order by test_count descending, then by visit_date.",
        ],
        "explanation": (
            "1. JOIN visits to lab_results on visit_id.\n"
            "2. GROUP BY visit aggregates lab tests per visit.\n"
            "3. COUNT(lr.id) counts the tests.\n"
            "4. Multi-column ORDER BY for the requested sort."
        ),
        "approach": [
            "Join the two tables.",
            "Group by visit.",
            "Count tests and sort.",
        ],
        "common_mistakes": [
            "Using LEFT JOIN when only visits with tests are needed.",
            "Forgetting the secondary sort column.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT", "ORDER BY"],
    },
    {
        "id": "hc-058",
        "slug": "diagnosis-frequency-percentage",
        "title": "Diagnosis Frequency as Percentage",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "Medical research wants to know the distribution of diagnoses. "
            "For each diagnosis, return the diagnosis, count, and what "
            "percentage of all visits it represents (as pct, rounded to 1 "
            "decimal). Order by pct descending."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT diagnosis,\n"
            "       COUNT(*) AS cnt,\n"
            "       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM visits), 1) AS pct\n"
            "FROM visits\n"
            "GROUP BY diagnosis\n"
            "ORDER BY pct DESC;"
        ),
        "hints": [
            "You need each diagnosis count divided by total visits.",
            "A scalar subquery can get the total visit count.",
            "Multiply by 100.0 to get a percentage (avoid integer division).",
            "The subquery (SELECT COUNT(*) FROM visits) gives the denominator.",
        ],
        "explanation": (
            "1. GROUP BY diagnosis counts visits per diagnosis.\n"
            "2. Scalar subquery gets total visit count.\n"
            "3. 100.0 * count / total gives the percentage.\n"
            "4. ROUND(..., 1) formats to one decimal."
        ),
        "approach": [
            "Count visits per diagnosis.",
            "Divide by total visits using a subquery.",
            "Multiply by 100 and round.",
        ],
        "common_mistakes": [
            "Integer division giving 0 — use 100.0 not 100.",
            "Putting the subquery in the wrong place.",
        ],
        "concept_tags": ["GROUP BY", "subquery", "percentage", "ROUND"],
    },
    {
        "id": "hc-059",
        "slug": "doctors-no-visits",
        "title": "Doctors with No Visits",
        "difficulty": "medium",
        "category": "left_join",
        "dataset": "healthcare",
        "description": (
            "Scheduling wants to find doctors who have never had a visit. "
            "Return the doctor's full name and specialty for doctors with "
            "zero visits. Use a LEFT JOIN approach. Order by last_name."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       d.specialty\n"
            "FROM doctors d\n"
            "LEFT JOIN visits v ON d.id = v.doctor_id\n"
            "WHERE v.id IS NULL\n"
            "ORDER BY d.last_name;"
        ),
        "hints": [
            "A LEFT JOIN keeps all doctors even if they have no visits.",
            "When there is no matching visit, the visit columns will be NULL.",
            "Check for NULL on the visit side to find unmatched doctors.",
            "WHERE v.id IS NULL identifies doctors with no visits.",
        ],
        "explanation": (
            "1. LEFT JOIN doctors to visits keeps all doctors.\n"
            "2. WHERE v.id IS NULL filters to doctors with no matching visits.\n"
            "3. These are the doctors who have never had a visit."
        ),
        "approach": [
            "Use LEFT JOIN from doctors to visits.",
            "Filter for NULL visit IDs.",
            "Return doctor details.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which would exclude the doctors we want.",
            "Checking the wrong column for NULL.",
        ],
        "concept_tags": ["LEFT JOIN", "IS NULL", "anti-join pattern"],
    },
    {
        "id": "hc-060",
        "slug": "prescription-duration-days",
        "title": "Prescription Duration in Days",
        "difficulty": "medium",
        "category": "date_functions",
        "dataset": "healthcare",
        "description": (
            "Pharmacy analytics wants to know prescription durations. "
            "Calculate the number of days between start_date and end_date "
            "for each prescription. Return medication, start_date, "
            "end_date, and duration_days. Order by duration_days "
            "descending."
        ),
        "schema_hint": ["prescriptions"],
        "solution_query": (
            "SELECT medication, start_date, end_date,\n"
            "       CAST(julianday(end_date) - julianday(start_date) AS INTEGER) "
            "AS duration_days\n"
            "FROM prescriptions\n"
            "ORDER BY duration_days DESC;"
        ),
        "hints": [
            "SQLite does not have DATEDIFF — use julianday() instead.",
            "julianday() converts a date to a Julian day number.",
            "Subtract two Julian day numbers to get the difference in days.",
            "CAST the result AS INTEGER to remove fractional days.",
        ],
        "explanation": (
            "1. julianday(end_date) - julianday(start_date) gives days as a float.\n"
            "2. CAST AS INTEGER truncates to whole days.\n"
            "3. ORDER BY duration_days DESC shows longest prescriptions first."
        ),
        "approach": [
            "Use julianday for date arithmetic in SQLite.",
            "Subtract start from end date.",
            "Cast to integer.",
        ],
        "common_mistakes": [
            "Trying to use DATEDIFF which does not exist in SQLite.",
            "Forgetting to cast, leaving fractional days.",
        ],
        "concept_tags": ["julianday", "date arithmetic", "CAST"],
    },
    {
        "id": "hc-061",
        "slug": "rank-doctors-by-salary",
        "title": "Rank Doctors by Salary Within Specialty",
        "difficulty": "medium",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "HR needs a salary ranking report. Rank each doctor by salary "
            "within their specialty using RANK(). Return first_name, "
            "last_name, specialty, salary, and salary_rank. Order by "
            "specialty then salary_rank."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT first_name, last_name, specialty, salary,\n"
            "       RANK() OVER (PARTITION BY specialty ORDER BY salary DESC) "
            "AS salary_rank\n"
            "FROM doctors\n"
            "ORDER BY specialty, salary_rank;"
        ),
        "hints": [
            "Window functions let you compute a value across a set of rows.",
            "RANK() assigns a rank within a partition.",
            "PARTITION BY specialty creates groups; ORDER BY salary DESC ranks within.",
            "The OVER clause defines the window for the ranking.",
        ],
        "explanation": (
            "1. RANK() OVER (PARTITION BY specialty ORDER BY salary DESC) "
            "ranks doctors within each specialty.\n"
            "2. Ties get the same rank, and the next rank is skipped.\n"
            "3. ORDER BY specialty, salary_rank sorts the output."
        ),
        "approach": [
            "Use RANK() with a PARTITION BY clause.",
            "Partition by specialty.",
            "Order within the partition by salary descending.",
        ],
        "common_mistakes": [
            "Using ROW_NUMBER instead of RANK when ties should get the same rank.",
            "Forgetting PARTITION BY and ranking across all doctors.",
        ],
        "concept_tags": ["RANK", "PARTITION BY", "window function"],
    },
    {
        "id": "hc-062",
        "slug": "running-total-billing",
        "title": "Running Total of Billing Amounts",
        "difficulty": "medium",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "Finance needs a cumulative billing report. For each billing "
            "record, show the id, billed_at, amount, and a running_total "
            "of amount ordered by billed_at. Use a window function."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT id, billed_at, amount,\n"
            "       SUM(amount) OVER (ORDER BY billed_at, id) AS running_total\n"
            "FROM billing\n"
            "ORDER BY billed_at, id;"
        ),
        "hints": [
            "A running total is a cumulative sum over an ordered set.",
            "SUM() can be used as a window function with OVER.",
            "ORDER BY in the OVER clause defines the accumulation order.",
            "Include id in the ORDER BY to break ties on billed_at.",
        ],
        "explanation": (
            "1. SUM(amount) OVER (ORDER BY billed_at, id) computes a cumulative sum.\n"
            "2. The default frame is ROWS UNBOUNDED PRECEDING to CURRENT ROW.\n"
            "3. Including id ensures deterministic ordering for ties."
        ),
        "approach": [
            "Use SUM as a window function.",
            "Order by billed_at within the window.",
            "Add id to break ties.",
        ],
        "common_mistakes": [
            "Forgetting the OVER clause and getting a single total.",
            "Not breaking ties, leading to non-deterministic results.",
        ],
        "concept_tags": ["window function", "SUM", "running total", "OVER"],
    },
    {
        "id": "hc-063",
        "slug": "patients-visited-multiple-doctors",
        "title": "Patients Who Saw Multiple Doctors",
        "difficulty": "medium",
        "category": "having",
        "dataset": "healthcare",
        "description": (
            "Care coordination wants to identify patients who have been "
            "seen by more than one doctor. Return patient first_name, "
            "last_name, and doctor_count (distinct doctors). Only include "
            "patients with doctor_count > 1. Order by doctor_count descending."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       COUNT(DISTINCT v.doctor_id) AS doctor_count\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "HAVING COUNT(DISTINCT v.doctor_id) > 1\n"
            "ORDER BY doctor_count DESC;"
        ),
        "hints": [
            "Join patients to visits and count distinct doctors per patient.",
            "Use HAVING to filter after aggregation.",
            "COUNT(DISTINCT doctor_id) counts unique doctors.",
            "Group by patient, then filter with HAVING.",
        ],
        "explanation": (
            "1. JOIN patients to visits.\n"
            "2. GROUP BY patient.\n"
            "3. COUNT(DISTINCT doctor_id) counts unique doctors per patient.\n"
            "4. HAVING > 1 keeps patients with multiple doctors."
        ),
        "approach": [
            "Join and group by patient.",
            "Count distinct doctors.",
            "Filter with HAVING.",
        ],
        "common_mistakes": [
            "Using COUNT(doctor_id) without DISTINCT.",
            "Using WHERE instead of HAVING for aggregate filter.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT"],
    },
    {
        "id": "hc-064",
        "slug": "case-visit-status-summary",
        "title": "Visit Status Summary with CASE",
        "difficulty": "medium",
        "category": "case",
        "dataset": "healthcare",
        "description": (
            "Create a summary of visits by classifying their status into "
            "broader categories. Use CASE to map: 'completed' -> 'Finished', "
            "'cancelled' and 'no_show' -> 'Did Not Happen', 'scheduled' -> "
            "'Upcoming'. Return status_category and visit_count. Order by "
            "visit_count descending."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT CASE\n"
            "         WHEN status = 'completed' THEN 'Finished'\n"
            "         WHEN status IN ('cancelled', 'no_show') THEN 'Did Not Happen'\n"
            "         WHEN status = 'scheduled' THEN 'Upcoming'\n"
            "       END AS status_category,\n"
            "       COUNT(*) AS visit_count\n"
            "FROM visits\n"
            "GROUP BY status_category\n"
            "ORDER BY visit_count DESC;"
        ),
        "hints": [
            "CASE WHEN ... THEN ... END creates conditional expressions.",
            "You can group multiple values with IN().",
            "Group by the CASE expression (or its alias) to aggregate.",
            "Map cancelled and no_show together using IN.",
        ],
        "explanation": (
            "1. CASE maps each status to a broader category.\n"
            "2. IN ('cancelled', 'no_show') groups two statuses together.\n"
            "3. GROUP BY the CASE result aggregates by category.\n"
            "4. COUNT(*) counts visits per category."
        ),
        "approach": [
            "Write a CASE expression for the mapping.",
            "Group by the resulting category.",
            "Count visits per category.",
        ],
        "common_mistakes": [
            "Forgetting END in the CASE expression.",
            "Not handling all possible status values.",
        ],
        "concept_tags": ["CASE", "GROUP BY", "IN", "conditional logic"],
    },
    {
        "id": "hc-065",
        "slug": "self-join-same-department-doctors",
        "title": "Doctor Pairs in the Same Department",
        "difficulty": "medium",
        "category": "self_join",
        "dataset": "healthcare",
        "description": (
            "Administration wants to list all pairs of doctors who work "
            "in the same department. Return doctor1_name, doctor2_name, "
            "and department_id. Ensure each pair appears only once (doctor1 "
            "id < doctor2 id). Order by department_id, doctor1_name."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT d1.first_name || ' ' || d1.last_name AS doctor1_name,\n"
            "       d2.first_name || ' ' || d2.last_name AS doctor2_name,\n"
            "       d1.department_id\n"
            "FROM doctors d1\n"
            "JOIN doctors d2 ON d1.department_id = d2.department_id\n"
            "  AND d1.id < d2.id\n"
            "ORDER BY d1.department_id, doctor1_name;"
        ),
        "hints": [
            "A self-join joins a table to itself using two aliases.",
            "Match on department_id to find same-department doctors.",
            "Use d1.id < d2.id to avoid duplicate pairs and self-pairs.",
            "Each pair should appear only once.",
        ],
        "explanation": (
            "1. Self-join doctors to doctors on department_id.\n"
            "2. d1.id < d2.id ensures each pair appears once.\n"
            "3. Concatenate names for readability."
        ),
        "approach": [
            "Alias the doctors table twice.",
            "Join on department_id.",
            "Use < to prevent duplicates.",
        ],
        "common_mistakes": [
            "Using != instead of < which gives each pair twice.",
            "Forgetting the self-join condition and getting a cross join.",
        ],
        "concept_tags": ["self-join", "JOIN", "string concatenation"],
    },
    {
        "id": "hc-066",
        "slug": "patients-all-visit-statuses",
        "title": "Patients with All Visit Status Types",
        "difficulty": "hard",
        "category": "having",
        "dataset": "healthcare",
        "description": (
            "Find patients who have had visits in every possible status "
            "('scheduled', 'completed', 'cancelled', 'no_show'). Return "
            "patient first_name, last_name, and the count of distinct "
            "statuses. Order by last_name."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       COUNT(DISTINCT v.status) AS status_count\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "HAVING COUNT(DISTINCT v.status) = 4\n"
            "ORDER BY p.last_name;"
        ),
        "hints": [
            "There are 4 possible visit statuses.",
            "Count the distinct statuses each patient has.",
            "A patient with all statuses will have COUNT(DISTINCT status) = 4.",
            "Use HAVING to filter groups after counting.",
        ],
        "explanation": (
            "1. JOIN patients to visits.\n"
            "2. GROUP BY patient.\n"
            "3. COUNT(DISTINCT status) counts unique statuses per patient.\n"
            "4. HAVING = 4 means the patient has all four status types."
        ),
        "approach": [
            "Join and group by patient.",
            "Count distinct statuses.",
            "Filter for patients with all 4.",
        ],
        "common_mistakes": [
            "Hardcoding the status count without knowing all statuses.",
            "Using COUNT(status) without DISTINCT.",
        ],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT", "set completeness"],
    },
    {
        "id": "hc-067",
        "slug": "row-number-latest-visit-per-patient",
        "title": "Latest Visit per Patient Using ROW_NUMBER",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each patient, find their most recent visit. Use "
            "ROW_NUMBER() to rank visits by date descending within each "
            "patient, then filter to only the latest. Return patient_id, "
            "first_name, last_name, visit_date, and diagnosis."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT patient_id, first_name, last_name,\n"
            "       visit_date, diagnosis\n"
            "FROM (\n"
            "  SELECT p.id AS patient_id, p.first_name, p.last_name,\n"
            "         v.visit_date, v.diagnosis,\n"
            "         ROW_NUMBER() OVER (\n"
            "           PARTITION BY p.id ORDER BY v.visit_date DESC\n"
            "         ) AS rn\n"
            "  FROM patients p\n"
            "  JOIN visits v ON p.id = v.patient_id\n"
            ") sub\n"
            "WHERE rn = 1\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "ROW_NUMBER() assigns sequential numbers within a partition.",
            "Partition by patient and order by visit_date descending.",
            "The most recent visit gets ROW_NUMBER = 1.",
            "Wrap the window function in a subquery, then filter WHERE rn = 1.",
        ],
        "explanation": (
            "1. ROW_NUMBER() partitioned by patient, ordered by visit_date DESC.\n"
            "2. rn = 1 is the most recent visit per patient.\n"
            "3. Filter in the outer query since WHERE cannot reference window functions directly."
        ),
        "approach": [
            "Use ROW_NUMBER with PARTITION BY patient.",
            "Order by date descending in the window.",
            "Wrap in subquery and filter rn = 1.",
        ],
        "common_mistakes": [
            "Trying to filter WHERE ROW_NUMBER() = 1 directly (not allowed).",
            "Using RANK instead of ROW_NUMBER when you want exactly one row per patient.",
        ],
        "concept_tags": ["ROW_NUMBER", "PARTITION BY", "window function", "top-N per group"],
    },
    {
        "id": "hc-068",
        "slug": "correlated-subquery-above-avg-billing",
        "title": "Visits with Above-Average Billing for Their Doctor",
        "difficulty": "hard",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "Identify visits where the billing amount exceeded the average "
            "billing amount for that doctor. Return visit_id, doctor_id, "
            "amount, and the doctor's average billing as doctor_avg_amount "
            "(rounded to 2 decimals). Order by amount descending."
        ),
        "schema_hint": ["visits", "billing"],
        "solution_query": (
            "SELECT b.visit_id, v.doctor_id, b.amount,\n"
            "       ROUND((\n"
            "         SELECT AVG(b2.amount)\n"
            "         FROM billing b2\n"
            "         JOIN visits v2 ON b2.visit_id = v2.id\n"
            "         WHERE v2.doctor_id = v.doctor_id\n"
            "       ), 2) AS doctor_avg_amount\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "WHERE b.amount > (\n"
            "  SELECT AVG(b2.amount)\n"
            "  FROM billing b2\n"
            "  JOIN visits v2 ON b2.visit_id = v2.id\n"
            "  WHERE v2.doctor_id = v.doctor_id\n"
            ")\n"
            "ORDER BY b.amount DESC;"
        ),
        "hints": [
            "A correlated subquery references columns from the outer query.",
            "The subquery computes the average for the current row's doctor.",
            "Join billing to visits in both the outer and inner queries.",
            "The WHERE clause compares each row's amount to the correlated average.",
        ],
        "explanation": (
            "1. Outer query joins billing to visits.\n"
            "2. Correlated subquery computes AVG(amount) for the same doctor.\n"
            "3. WHERE b.amount > (subquery) filters to above-average bills.\n"
            "4. The same subquery appears in SELECT for display."
        ),
        "approach": [
            "Write a correlated subquery for doctor average.",
            "Use it in both SELECT and WHERE.",
            "Join billing to visits in both queries.",
        ],
        "common_mistakes": [
            "Using a non-correlated subquery that computes the global average.",
            "Forgetting to join billing to visits inside the subquery.",
        ],
        "concept_tags": ["correlated subquery", "AVG", "JOIN"],
    },
    {
        "id": "hc-069",
        "slug": "cte-department-visit-stats",
        "title": "Department Visit Statistics with CTE",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Using a CTE, compute per-department visit statistics. Return "
            "department name, total_visits, avg_visits_per_doctor (rounded "
            "to 1 decimal), and the department's share of all visits as "
            "visit_share_pct (rounded to 1 decimal). Order by total_visits "
            "descending."
        ),
        "schema_hint": ["departments", "doctors", "visits"],
        "solution_query": (
            "WITH dept_stats AS (\n"
            "  SELECT d.department_id,\n"
            "         COUNT(*) AS total_visits,\n"
            "         COUNT(DISTINCT d.id) AS doctor_count\n"
            "  FROM doctors d\n"
            "  JOIN visits v ON d.id = v.doctor_id\n"
            "  GROUP BY d.department_id\n"
            ")\n"
            "SELECT dep.name,\n"
            "       ds.total_visits,\n"
            "       ROUND(1.0 * ds.total_visits / ds.doctor_count, 1) "
            "AS avg_visits_per_doctor,\n"
            "       ROUND(100.0 * ds.total_visits / "
            "(SELECT SUM(total_visits) FROM dept_stats), 1) AS visit_share_pct\n"
            "FROM dept_stats ds\n"
            "JOIN departments dep ON ds.department_id = dep.id\n"
            "ORDER BY ds.total_visits DESC;"
        ),
        "hints": [
            "Use a CTE to aggregate visits per department first.",
            "Count visits and distinct doctors in the CTE.",
            "Divide total visits by doctor count for the average.",
            "Use a scalar subquery on the CTE to get the grand total for percentages.",
        ],
        "explanation": (
            "1. CTE joins doctors to visits and groups by department.\n"
            "2. Main query joins CTE to departments for the name.\n"
            "3. avg_visits_per_doctor = total_visits / doctor_count.\n"
            "4. visit_share_pct uses a scalar subquery on the CTE for the total."
        ),
        "approach": [
            "Build a CTE with per-department visit and doctor counts.",
            "Compute averages and percentages in the main query.",
            "Use a scalar subquery for the grand total.",
        ],
        "common_mistakes": [
            "Integer division — use 1.0 * or 100.0 *.",
            "Forgetting to count distinct doctors.",
        ],
        "concept_tags": ["CTE", "JOIN", "GROUP BY", "percentage", "ROUND"],
    },
    {
        "id": "hc-070",
        "slug": "ntile-salary-quartiles",
        "title": "Doctor Salary Quartiles with NTILE",
        "difficulty": "medium",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "HR wants to classify doctors into salary quartiles. Use "
            "NTILE(4) to assign each doctor to a quartile based on salary. "
            "Return first_name, last_name, salary, and salary_quartile. "
            "Order by salary descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT first_name, last_name, salary,\n"
            "       NTILE(4) OVER (ORDER BY salary) AS salary_quartile\n"
            "FROM doctors\n"
            "ORDER BY salary DESC;"
        ),
        "hints": [
            "NTILE(n) divides rows into n roughly equal groups.",
            "NTILE(4) creates quartiles numbered 1 through 4.",
            "The OVER clause orders rows for the distribution.",
            "ORDER BY salary in OVER assigns quartile 1 to lowest salaries.",
        ],
        "explanation": (
            "1. NTILE(4) OVER (ORDER BY salary) assigns quartile 1 to the "
            "lowest 25%, up to quartile 4 for the highest.\n"
            "2. The outer ORDER BY salary DESC sorts the display."
        ),
        "approach": [
            "Use NTILE(4) as a window function.",
            "Order by salary in the OVER clause.",
            "Sort the final output by salary descending.",
        ],
        "common_mistakes": [
            "Confusing NTILE ordering with the output ORDER BY.",
            "Using PERCENTILE functions that don't exist in SQLite.",
        ],
        "concept_tags": ["NTILE", "window function", "OVER", "quartile"],
    },
    {
        "id": "hc-071",
        "slug": "exists-patients-with-prescriptions",
        "title": "Patients Who Have At Least One Prescription",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "The pharmacy needs a list of patients who have received at "
            "least one prescription. Use EXISTS to find them. Return "
            "first_name, last_name, and email. Order by last_name."
        ),
        "schema_hint": ["patients", "visits", "prescriptions"],
        "solution_query": (
            "SELECT p.first_name, p.last_name, p.email\n"
            "FROM patients p\n"
            "WHERE EXISTS (\n"
            "  SELECT 1 FROM visits v\n"
            "  JOIN prescriptions rx ON v.id = rx.visit_id\n"
            "  WHERE v.patient_id = p.id\n"
            ")\n"
            "ORDER BY p.last_name;"
        ),
        "hints": [
            "EXISTS checks whether a subquery returns any rows.",
            "Prescriptions link to patients through the visits table.",
            "The correlated subquery references the outer patient.",
            "SELECT 1 inside EXISTS — the selected value does not matter.",
        ],
        "explanation": (
            "1. EXISTS subquery checks if any prescription exists for the patient.\n"
            "2. Joins visits to prescriptions inside the subquery.\n"
            "3. Correlates on patient_id.\n"
            "4. Only patients with at least one match are returned."
        ),
        "approach": [
            "Use EXISTS with a correlated subquery.",
            "Join visits to prescriptions inside the subquery.",
            "Correlate on patient_id.",
        ],
        "common_mistakes": [
            "Using IN instead of EXISTS — works but less idiomatic for this pattern.",
            "Forgetting the correlation to the outer query.",
        ],
        "concept_tags": ["EXISTS", "correlated subquery", "JOIN"],
    },
    {
        "id": "hc-072",
        "slug": "union-doctor-patient-contacts",
        "title": "Combined Doctor and Patient Contact List",
        "difficulty": "medium",
        "category": "set_operations",
        "dataset": "healthcare",
        "description": (
            "Administration needs a combined contact directory of all "
            "doctors and patients. Return full_name, email, phone, and "
            "a contact_type column ('Doctor' or 'Patient'). Use UNION ALL. "
            "Order by contact_type, full_name."
        ),
        "schema_hint": ["doctors", "patients"],
        "solution_query": (
            "SELECT first_name || ' ' || last_name AS full_name,\n"
            "       email, phone, 'Doctor' AS contact_type\n"
            "FROM doctors\n"
            "UNION ALL\n"
            "SELECT first_name || ' ' || last_name AS full_name,\n"
            "       email, phone, 'Patient' AS contact_type\n"
            "FROM patients\n"
            "ORDER BY contact_type, full_name;"
        ),
        "hints": [
            "UNION ALL combines the results of two SELECT statements.",
            "Both SELECTs must have the same number and type of columns.",
            "Add a literal string column to identify the source.",
            "ORDER BY applies to the entire combined result.",
        ],
        "explanation": (
            "1. First SELECT gets doctors with type 'Doctor'.\n"
            "2. Second SELECT gets patients with type 'Patient'.\n"
            "3. UNION ALL combines them (preserving duplicates).\n"
            "4. ORDER BY sorts the combined result."
        ),
        "approach": [
            "Write two SELECTs with matching column structures.",
            "Add a contact_type literal to each.",
            "Combine with UNION ALL.",
        ],
        "common_mistakes": [
            "Using UNION instead of UNION ALL (removes duplicates unnecessarily).",
            "Mismatched column counts between the two SELECTs.",
        ],
        "concept_tags": ["UNION ALL", "set operations", "string concatenation"],
    },
    {
        "id": "hc-073",
        "slug": "lag-billing-comparison",
        "title": "Compare Each Bill to the Previous One",
        "difficulty": "medium",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "Finance wants to see how each billing amount compares to the "
            "previous one chronologically. Return id, billed_at, amount, "
            "prev_amount (using LAG), and the difference as amount_change. "
            "Order by billed_at, id."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "SELECT id, billed_at, amount,\n"
            "       LAG(amount) OVER (ORDER BY billed_at, id) AS prev_amount,\n"
            "       amount - LAG(amount) OVER (ORDER BY billed_at, id) "
            "AS amount_change\n"
            "FROM billing\n"
            "ORDER BY billed_at, id;"
        ),
        "hints": [
            "LAG(column) accesses the previous row's value.",
            "The OVER clause defines the ordering for LAG.",
            "The first row will have NULL for prev_amount and amount_change.",
            "Subtract LAG value from current value for the change.",
        ],
        "explanation": (
            "1. LAG(amount) OVER (ORDER BY billed_at, id) gets previous amount.\n"
            "2. amount - LAG(...) computes the difference.\n"
            "3. First row has NULL since there is no previous row."
        ),
        "approach": [
            "Use LAG as a window function.",
            "Order by billed_at and id in the OVER clause.",
            "Compute the difference.",
        ],
        "common_mistakes": [
            "Forgetting ORDER BY in the OVER clause.",
            "Not handling the NULL in the first row.",
        ],
        "concept_tags": ["LAG", "window function", "OVER"],
    },
    {
        "id": "hc-074",
        "slug": "insurance-coverage-gap",
        "title": "Patient Out-of-Pocket vs Insurance Coverage",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "For each patient with insurance, calculate total billed, "
            "total covered by insurance, and total patient responsibility "
            "across all their visits. Return patient full name, "
            "provider_name, total_billed, total_covered, and "
            "total_out_of_pocket (all rounded to 2 decimals). Only "
            "include patients with at least one billing record. Order "
            "by total_out_of_pocket descending."
        ),
        "schema_hint": ["patients", "insurance", "visits", "billing"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       i.provider_name,\n"
            "       ROUND(SUM(b.amount), 2) AS total_billed,\n"
            "       ROUND(SUM(b.insurance_covered), 2) AS total_covered,\n"
            "       ROUND(SUM(b.patient_responsibility), 2) AS total_out_of_pocket\n"
            "FROM patients p\n"
            "JOIN insurance i ON p.insurance_id = i.id\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "JOIN billing b ON v.id = b.visit_id\n"
            "GROUP BY p.id, p.first_name, p.last_name, i.provider_name\n"
            "ORDER BY total_out_of_pocket DESC;"
        ),
        "hints": [
            "You need to join four tables: patients, insurance, visits, billing.",
            "Group by patient to aggregate billing totals.",
            "The join path goes patients -> visits -> billing for amounts.",
            "Patients -> insurance for the provider name.",
        ],
        "explanation": (
            "1. Join patients to insurance, visits, and billing.\n"
            "2. Group by patient to sum billing amounts.\n"
            "3. ROUND to 2 decimals for monetary values.\n"
            "4. Order by total_out_of_pocket descending."
        ),
        "approach": [
            "Join all four tables.",
            "Group by patient and insurance provider.",
            "Sum the billing columns.",
        ],
        "common_mistakes": [
            "Not joining through visits to billing.",
            "Including patients without insurance or billing records.",
        ],
        "concept_tags": ["JOIN", "multi-table", "GROUP BY", "SUM", "ROUND"],
    },
    {
        "id": "hc-075",
        "slug": "dense-rank-visit-frequency",
        "title": "Dense Rank Patients by Visit Frequency",
        "difficulty": "medium",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "Rank patients by how many visits they have had using "
            "DENSE_RANK(). Return first_name, last_name, visit_count, "
            "and frequency_rank. Order by frequency_rank, last_name."
        ),
        "schema_hint": ["patients", "visits"],
        "solution_query": (
            "SELECT p.first_name, p.last_name, COUNT(*) AS visit_count,\n"
            "       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS frequency_rank\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "ORDER BY frequency_rank, p.last_name;"
        ),
        "hints": [
            "First aggregate visits per patient using GROUP BY.",
            "DENSE_RANK ranks without gaps between ranks.",
            "Window functions can reference aggregate results.",
            "ORDER BY COUNT(*) DESC inside OVER ranks most visits first.",
        ],
        "explanation": (
            "1. GROUP BY patient and COUNT visits.\n"
            "2. DENSE_RANK() over the count assigns ranks.\n"
            "3. DENSE_RANK has no gaps: 1, 2, 2, 3 (not 1, 2, 2, 4).\n"
            "4. ORDER BY rank then last_name."
        ),
        "approach": [
            "Group by patient and count visits.",
            "Apply DENSE_RANK over the count.",
            "Sort by rank and name.",
        ],
        "common_mistakes": [
            "Using RANK instead of DENSE_RANK (RANK has gaps).",
            "Trying to use a window function without GROUP BY first.",
        ],
        "concept_tags": ["DENSE_RANK", "window function", "GROUP BY", "COUNT"],
    },
    {
        "id": "hc-076",
        "slug": "coalesce-null-handling",
        "title": "Patient Contact Info with COALESCE",
        "difficulty": "easy",
        "category": "functions",
        "dataset": "healthcare",
        "description": (
            "Create a contact list where missing phone numbers display "
            "'No phone on file'. Return first_name, last_name, email, "
            "and COALESCE(phone, 'No phone on file') as contact_phone. "
            "Order by last_name."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, email,\n"
            "       COALESCE(phone, 'No phone on file') AS contact_phone\n"
            "FROM patients\n"
            "ORDER BY last_name;"
        ),
        "hints": [
            "COALESCE returns the first non-NULL argument.",
            "If phone is NULL, the fallback string will be used.",
            "COALESCE(phone, 'default') replaces NULL phones.",
            "This is simpler than using CASE WHEN phone IS NULL THEN ...",
        ],
        "explanation": (
            "1. COALESCE(phone, 'No phone on file') returns phone if not NULL.\n"
            "2. If phone IS NULL, it returns the fallback string.\n"
            "3. ORDER BY last_name sorts alphabetically."
        ),
        "approach": [
            "Use COALESCE to provide a default for NULL values.",
            "Select the required columns.",
            "Sort by last name.",
        ],
        "common_mistakes": [
            "Using IFNULL instead of COALESCE — works in SQLite but not portable.",
            "Checking for empty string '' instead of NULL.",
        ],
        "concept_tags": ["COALESCE", "NULL handling", "functions"],
    },
    {
        "id": "hc-077",
        "slug": "multi-cte-billing-aging",
        "title": "Billing Aging Report with Multiple CTEs",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Build a billing aging report using CTEs. First CTE computes "
            "the age in days of each unpaid bill (status != 'paid') as of "
            "'2025-01-01'. Second CTE categorizes: 0-30 days = 'Current', "
            "31-60 = '31-60 Days', 61-90 = '61-90 Days', 91+ = '90+ Days'. "
            "Return the aging_bucket and total_amount (sum of amount, "
            "rounded to 2). Order by the bucket in the order listed."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "WITH unpaid AS (\n"
            "  SELECT amount,\n"
            "         CAST(julianday('2025-01-01') - julianday(billed_at) "
            "AS INTEGER) AS age_days\n"
            "  FROM billing\n"
            "  WHERE status != 'paid'\n"
            "),\n"
            "bucketed AS (\n"
            "  SELECT amount,\n"
            "         CASE\n"
            "           WHEN age_days BETWEEN 0 AND 30 THEN 'Current'\n"
            "           WHEN age_days BETWEEN 31 AND 60 THEN '31-60 Days'\n"
            "           WHEN age_days BETWEEN 61 AND 90 THEN '61-90 Days'\n"
            "           ELSE '90+ Days'\n"
            "         END AS aging_bucket,\n"
            "         CASE\n"
            "           WHEN age_days BETWEEN 0 AND 30 THEN 1\n"
            "           WHEN age_days BETWEEN 31 AND 60 THEN 2\n"
            "           WHEN age_days BETWEEN 61 AND 90 THEN 3\n"
            "           ELSE 4\n"
            "         END AS bucket_order\n"
            "  FROM unpaid\n"
            ")\n"
            "SELECT aging_bucket,\n"
            "       ROUND(SUM(amount), 2) AS total_amount\n"
            "FROM bucketed\n"
            "GROUP BY aging_bucket, bucket_order\n"
            "ORDER BY bucket_order;"
        ),
        "hints": [
            "Use julianday to compute the age of each bill.",
            "A CASE expression can assign each bill to an aging bucket.",
            "Create a numeric ordering column for the buckets.",
            "Sum amounts per bucket in the final query.",
        ],
        "explanation": (
            "1. First CTE filters unpaid bills and computes age in days.\n"
            "2. Second CTE assigns aging buckets using CASE.\n"
            "3. A bucket_order column ensures correct sort order.\n"
            "4. Final query sums amounts per bucket."
        ),
        "approach": [
            "Compute bill age in the first CTE.",
            "Assign buckets in the second CTE.",
            "Aggregate in the final SELECT.",
        ],
        "common_mistakes": [
            "Sorting alphabetically instead of by bucket order.",
            "Including paid bills in the aging report.",
        ],
        "concept_tags": ["CTE", "CASE", "julianday", "GROUP BY", "aging report"],
    },
    {
        "id": "hc-078",
        "slug": "recursive-follow-up-chain",
        "title": "Follow-Up Visit Chains",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Find visits that have a follow-up date, and count how many "
            "subsequent visits (by the same patient with the same doctor) "
            "occurred on or after the follow_up_date. Return visit_id, "
            "patient_id, doctor_id, visit_date, follow_up_date, and "
            "subsequent_visit_count. Only include visits where "
            "follow_up_date is not NULL. Order by subsequent_visit_count "
            "descending."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT v1.id AS visit_id, v1.patient_id, v1.doctor_id,\n"
            "       v1.visit_date, v1.follow_up_date,\n"
            "       COUNT(v2.id) AS subsequent_visit_count\n"
            "FROM visits v1\n"
            "LEFT JOIN visits v2\n"
            "  ON v1.patient_id = v2.patient_id\n"
            "  AND v1.doctor_id = v2.doctor_id\n"
            "  AND v2.visit_date >= v1.follow_up_date\n"
            "  AND v2.id != v1.id\n"
            "WHERE v1.follow_up_date IS NOT NULL\n"
            "GROUP BY v1.id, v1.patient_id, v1.doctor_id, "
            "v1.visit_date, v1.follow_up_date\n"
            "ORDER BY subsequent_visit_count DESC;"
        ),
        "hints": [
            "Self-join visits to itself to find follow-up visits.",
            "Match on the same patient and same doctor.",
            "The follow-up visit must be on or after the follow_up_date.",
            "Use LEFT JOIN so visits with no actual follow-up show count 0.",
        ],
        "explanation": (
            "1. Self-join: v1 is the original visit, v2 is the potential follow-up.\n"
            "2. Match same patient + doctor, date >= follow_up_date.\n"
            "3. Exclude v1 itself with v2.id != v1.id.\n"
            "4. LEFT JOIN + COUNT gives 0 when no follow-ups exist."
        ),
        "approach": [
            "Self-join visits with conditions for patient, doctor, and date.",
            "Use LEFT JOIN to preserve visits with no follow-ups.",
            "Group and count.",
        ],
        "common_mistakes": [
            "Not excluding the original visit from the count.",
            "Using INNER JOIN and losing visits with no follow-ups.",
        ],
        "concept_tags": ["self-join", "LEFT JOIN", "GROUP BY", "date comparison"],
    },
    {
        "id": "hc-079",
        "slug": "window-percent-rank",
        "title": "Percentile Rank of Doctor Salaries",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "Compute the percentile rank of each doctor's salary using "
            "PERCENT_RANK(). Return first_name, last_name, salary, and "
            "salary_percentile (rounded to 2 decimals). Order by "
            "salary_percentile descending."
        ),
        "schema_hint": ["doctors"],
        "solution_query": (
            "SELECT first_name, last_name, salary,\n"
            "       ROUND(PERCENT_RANK() OVER (ORDER BY salary), 2) "
            "AS salary_percentile\n"
            "FROM doctors\n"
            "ORDER BY salary_percentile DESC;"
        ),
        "hints": [
            "PERCENT_RANK returns a value between 0 and 1.",
            "It represents the relative rank as a fraction.",
            "Use OVER (ORDER BY salary) to rank by salary.",
            "Round to 2 decimal places for readability.",
        ],
        "explanation": (
            "1. PERCENT_RANK() OVER (ORDER BY salary) computes the percentile.\n"
            "2. Values range from 0.0 (lowest) to 1.0 (highest).\n"
            "3. ROUND to 2 decimals.\n"
            "4. ORDER BY descending shows top earners first."
        ),
        "approach": [
            "Use PERCENT_RANK as a window function.",
            "Order by salary in the OVER clause.",
            "Round and sort the output.",
        ],
        "common_mistakes": [
            "Confusing PERCENT_RANK with NTILE.",
            "Expecting percentages (0-100) instead of fractions (0-1).",
        ],
        "concept_tags": ["PERCENT_RANK", "window function", "OVER"],
    },
    {
        "id": "hc-080",
        "slug": "except-patients-no-lab-results",
        "title": "Patients with Visits but No Lab Results",
        "difficulty": "medium",
        "category": "set_operations",
        "dataset": "healthcare",
        "description": (
            "Find patients who have had visits but never had any lab "
            "results. Use EXCEPT to find patient IDs with visits but "
            "not in lab_results. Return first_name, last_name. Order "
            "by last_name."
        ),
        "schema_hint": ["patients", "visits", "lab_results"],
        "solution_query": (
            "SELECT p.first_name, p.last_name\n"
            "FROM patients p\n"
            "WHERE p.id IN (\n"
            "  SELECT v.patient_id FROM visits v\n"
            "  EXCEPT\n"
            "  SELECT v2.patient_id FROM visits v2\n"
            "  JOIN lab_results lr ON v2.id = lr.visit_id\n"
            ")\n"
            "ORDER BY p.last_name;"
        ),
        "hints": [
            "EXCEPT returns rows from the first query not in the second.",
            "Get patient IDs from visits, then subtract those with lab results.",
            "Lab results link to patients through visits.",
            "Use the EXCEPT result as a subquery in WHERE ... IN.",
        ],
        "explanation": (
            "1. First subquery: all patient IDs with visits.\n"
            "2. Second subquery: patient IDs with lab results (via visits).\n"
            "3. EXCEPT removes the second set from the first.\n"
            "4. Outer query gets patient details for the remaining IDs."
        ),
        "approach": [
            "Use EXCEPT to find the set difference.",
            "First set: patients with visits.",
            "Second set: patients with lab results.",
            "Join back to patients for names.",
        ],
        "common_mistakes": [
            "Using NOT IN without EXCEPT — works but different approach.",
            "Forgetting that lab_results connect through visits.",
        ],
        "concept_tags": ["EXCEPT", "set operations", "subquery"],
    },
    {
        "id": "hc-081",
        "slug": "pivot-visits-by-status",
        "title": "Pivot Visit Counts by Status per Doctor",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Create a pivot-style report showing each doctor's visit "
            "counts broken down by status. Return doctor full name, "
            "completed_count, scheduled_count, cancelled_count, and "
            "no_show_count. Use conditional aggregation (SUM + CASE). "
            "Order by completed_count descending."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       SUM(CASE WHEN v.status = 'completed' THEN 1 ELSE 0 END) "
            "AS completed_count,\n"
            "       SUM(CASE WHEN v.status = 'scheduled' THEN 1 ELSE 0 END) "
            "AS scheduled_count,\n"
            "       SUM(CASE WHEN v.status = 'cancelled' THEN 1 ELSE 0 END) "
            "AS cancelled_count,\n"
            "       SUM(CASE WHEN v.status = 'no_show' THEN 1 ELSE 0 END) "
            "AS no_show_count\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "GROUP BY d.id, d.first_name, d.last_name\n"
            "ORDER BY completed_count DESC;"
        ),
        "hints": [
            "SQLite has no PIVOT keyword — use conditional aggregation.",
            "SUM(CASE WHEN status = 'x' THEN 1 ELSE 0 END) counts per status.",
            "Join doctors to visits and group by doctor.",
            "Create one SUM+CASE column for each status value.",
        ],
        "explanation": (
            "1. JOIN doctors to visits.\n"
            "2. GROUP BY doctor.\n"
            "3. Each SUM(CASE ...) column counts one status type.\n"
            "4. This simulates a PIVOT table."
        ),
        "approach": [
            "Join doctors to visits.",
            "Use conditional aggregation for each status.",
            "Group by doctor.",
        ],
        "common_mistakes": [
            "Forgetting ELSE 0 in the CASE, resulting in NULL sums.",
            "Using COUNT instead of SUM with CASE.",
        ],
        "concept_tags": ["CASE", "conditional aggregation", "pivot", "GROUP BY"],
    },
    {
        "id": "hc-082",
        "slug": "cte-readmission-rate",
        "title": "30-Day Readmission Rate by Department",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Calculate the 30-day readmission rate per department. A "
            "readmission is when the same patient visits the same "
            "department within 30 days of a completed visit. Use CTEs "
            "to find readmissions, then compute the rate as "
            "readmissions / total completed visits * 100. Return "
            "department name, total_completed, readmission_count, and "
            "readmission_rate (rounded to 1 decimal). Order by "
            "readmission_rate descending."
        ),
        "schema_hint": ["departments", "doctors", "visits"],
        "solution_query": (
            "WITH completed AS (\n"
            "  SELECT v.id AS visit_id, v.patient_id, d.department_id,\n"
            "         v.visit_date\n"
            "  FROM visits v\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "  WHERE v.status = 'completed'\n"
            "),\n"
            "readmissions AS (\n"
            "  SELECT DISTINCT c1.visit_id\n"
            "  FROM completed c1\n"
            "  JOIN completed c2\n"
            "    ON c1.patient_id = c2.patient_id\n"
            "    AND c1.department_id = c2.department_id\n"
            "    AND c2.visit_date > c1.visit_date\n"
            "    AND julianday(c2.visit_date) - julianday(c1.visit_date) <= 30\n"
            "),\n"
            "dept_totals AS (\n"
            "  SELECT department_id, COUNT(*) AS total_completed\n"
            "  FROM completed\n"
            "  GROUP BY department_id\n"
            "),\n"
            "dept_readmissions AS (\n"
            "  SELECT c.department_id,\n"
            "         COUNT(DISTINCT r.visit_id) AS readmission_count\n"
            "  FROM readmissions r\n"
            "  JOIN completed c ON r.visit_id = c.visit_id\n"
            "  GROUP BY c.department_id\n"
            ")\n"
            "SELECT dep.name,\n"
            "       dt.total_completed,\n"
            "       COALESCE(dr.readmission_count, 0) AS readmission_count,\n"
            "       ROUND(100.0 * COALESCE(dr.readmission_count, 0) "
            "/ dt.total_completed, 1) AS readmission_rate\n"
            "FROM dept_totals dt\n"
            "JOIN departments dep ON dt.department_id = dep.id\n"
            "LEFT JOIN dept_readmissions dr ON dt.department_id = dr.department_id\n"
            "ORDER BY readmission_rate DESC;"
        ),
        "hints": [
            "First CTE: get completed visits with department info.",
            "Self-join completed visits to find same patient + department within 30 days.",
            "Use julianday to compute the day difference.",
            "Compute the rate as readmissions / total * 100.",
        ],
        "explanation": (
            "1. completed CTE: all completed visits with department.\n"
            "2. readmissions CTE: self-join to find 30-day revisits.\n"
            "3. dept_totals and dept_readmissions aggregate per department.\n"
            "4. Final query computes the rate."
        ),
        "approach": [
            "Break the problem into logical CTEs.",
            "Self-join for readmission detection.",
            "Aggregate and compute the rate.",
        ],
        "common_mistakes": [
            "Not matching on department, counting cross-department visits.",
            "Using date string comparison instead of julianday for day difference.",
        ],
        "concept_tags": ["CTE", "self-join", "julianday", "readmission", "healthcare analytics"],
    },
    {
        "id": "hc-083",
        "slug": "window-moving-average",
        "title": "7-Day Moving Average of Daily Billing",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "Compute the 7-day moving average of daily billing totals. "
            "First aggregate billing by day, then use a window function "
            "with ROWS BETWEEN 6 PRECEDING AND CURRENT ROW. Return "
            "bill_date, daily_total, and moving_avg_7d (rounded to 2). "
            "Order by bill_date."
        ),
        "schema_hint": ["billing"],
        "solution_query": (
            "WITH daily AS (\n"
            "  SELECT DATE(billed_at) AS bill_date,\n"
            "         ROUND(SUM(amount), 2) AS daily_total\n"
            "  FROM billing\n"
            "  GROUP BY DATE(billed_at)\n"
            ")\n"
            "SELECT bill_date, daily_total,\n"
            "       ROUND(AVG(daily_total) OVER (\n"
            "         ORDER BY bill_date\n"
            "         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW\n"
            "       ), 2) AS moving_avg_7d\n"
            "FROM daily\n"
            "ORDER BY bill_date;"
        ),
        "hints": [
            "First aggregate to daily totals using a CTE.",
            "Use AVG as a window function with a frame clause.",
            "ROWS BETWEEN 6 PRECEDING AND CURRENT ROW gives 7 rows.",
            "The moving average smooths out daily fluctuations.",
        ],
        "explanation": (
            "1. CTE aggregates billing to daily totals.\n"
            "2. AVG(...) OVER (ORDER BY bill_date ROWS ...) computes the moving average.\n"
            "3. The frame includes the current row and 6 preceding rows.\n"
            "4. Early rows have fewer than 7 data points."
        ),
        "approach": [
            "Aggregate to daily totals in a CTE.",
            "Apply a window function with a frame clause.",
            "Round and order.",
        ],
        "common_mistakes": [
            "Using RANGE instead of ROWS (different behavior with date gaps).",
            "Forgetting to aggregate daily first, computing on raw rows.",
        ],
        "concept_tags": ["CTE", "window function", "moving average", "ROWS BETWEEN"],
    },
    {
        "id": "hc-084",
        "slug": "subquery-max-billing-per-patient",
        "title": "Most Expensive Visit per Patient",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "For each patient, find the visit with the highest billing "
            "amount. Return patient full name, visit_date, diagnosis, "
            "and amount. If a patient has no billing records, exclude "
            "them. Order by amount descending."
        ),
        "schema_hint": ["patients", "visits", "billing"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       v.visit_date, v.diagnosis, b.amount\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE b.amount = (\n"
            "  SELECT MAX(b2.amount)\n"
            "  FROM billing b2\n"
            "  JOIN visits v2 ON b2.visit_id = v2.id\n"
            "  WHERE v2.patient_id = p.id\n"
            ")\n"
            "ORDER BY b.amount DESC;"
        ),
        "hints": [
            "For each patient, find the MAX billing amount.",
            "Use a correlated subquery to get the max for each patient.",
            "Join billing -> visits -> patients in the outer query.",
            "Compare each bill's amount to the patient's max.",
        ],
        "explanation": (
            "1. Outer query joins billing, visits, and patients.\n"
            "2. Correlated subquery finds MAX(amount) for the same patient.\n"
            "3. WHERE b.amount = (max) keeps only the highest bill per patient."
        ),
        "approach": [
            "Join the three tables.",
            "Use a correlated subquery for per-patient max.",
            "Filter to matching amounts.",
        ],
        "common_mistakes": [
            "Getting multiple rows per patient if they have tied max amounts.",
            "Not correlating the subquery to the outer patient.",
        ],
        "concept_tags": ["correlated subquery", "MAX", "JOIN", "top-per-group"],
    },
    {
        "id": "hc-085",
        "slug": "group-concat-medications",
        "title": "All Medications per Patient (Comma-Separated)",
        "difficulty": "medium",
        "category": "aggregate",
        "dataset": "healthcare",
        "description": (
            "The pharmacy wants a compact view of all medications each "
            "patient takes. Use GROUP_CONCAT to list all distinct "
            "medications per patient, separated by ', '. Return patient "
            "full name and medications. Order by patient last name."
        ),
        "schema_hint": ["patients", "visits", "prescriptions"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       GROUP_CONCAT(DISTINCT rx.medication, ', ') AS medications\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "JOIN prescriptions rx ON v.id = rx.visit_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "ORDER BY p.last_name;"
        ),
        "hints": [
            "GROUP_CONCAT concatenates values from multiple rows into one string.",
            "Use DISTINCT inside GROUP_CONCAT to avoid duplicates.",
            "Join patients -> visits -> prescriptions to get medications.",
            "The second argument to GROUP_CONCAT is the separator.",
        ],
        "explanation": (
            "1. Join patients to visits to prescriptions.\n"
            "2. GROUP BY patient.\n"
            "3. GROUP_CONCAT(DISTINCT medication, ', ') lists all unique medications."
        ),
        "approach": [
            "Join the three tables.",
            "Group by patient.",
            "Use GROUP_CONCAT with DISTINCT.",
        ],
        "common_mistakes": [
            "Forgetting DISTINCT, listing the same medication multiple times.",
            "Not specifying the separator (defaults to comma without space).",
        ],
        "concept_tags": ["GROUP_CONCAT", "JOIN", "GROUP BY", "DISTINCT"],
    },
    {
        "id": "hc-086",
        "slug": "first-last-value-department",
        "title": "Highest and Lowest Paid Doctor per Department",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each doctor, show their department name, salary, the "
            "name of the highest-paid doctor in their department "
            "(top_earner), and the name of the lowest-paid (lowest_earner). "
            "Use FIRST_VALUE and LAST_VALUE window functions. Order by "
            "department name, salary descending."
        ),
        "schema_hint": ["doctors", "departments"],
        "solution_query": (
            "SELECT dep.name AS department_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       d.salary,\n"
            "       FIRST_VALUE(d.first_name || ' ' || d.last_name) OVER (\n"
            "         PARTITION BY d.department_id ORDER BY d.salary DESC\n"
            "         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING\n"
            "       ) AS top_earner,\n"
            "       LAST_VALUE(d.first_name || ' ' || d.last_name) OVER (\n"
            "         PARTITION BY d.department_id ORDER BY d.salary DESC\n"
            "         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING\n"
            "       ) AS lowest_earner\n"
            "FROM doctors d\n"
            "JOIN departments dep ON d.department_id = dep.id\n"
            "ORDER BY dep.name, d.salary DESC;"
        ),
        "hints": [
            "FIRST_VALUE returns the first row's value in the window frame.",
            "LAST_VALUE returns the last row's value in the window frame.",
            "You must specify the full frame with ROWS BETWEEN ... AND UNBOUNDED FOLLOWING.",
            "Without the frame clause, LAST_VALUE only sees up to the current row.",
        ],
        "explanation": (
            "1. FIRST_VALUE with ORDER BY salary DESC gives the highest earner.\n"
            "2. LAST_VALUE with the full frame gives the lowest earner.\n"
            "3. The frame ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING "
            "is critical for LAST_VALUE.\n"
            "4. PARTITION BY department_id scopes to each department."
        ),
        "approach": [
            "Use FIRST_VALUE and LAST_VALUE window functions.",
            "Partition by department.",
            "Specify the full frame for LAST_VALUE.",
        ],
        "common_mistakes": [
            "Not specifying the frame clause — LAST_VALUE will only see up to current row.",
            "Forgetting to partition by department.",
        ],
        "concept_tags": ["FIRST_VALUE", "LAST_VALUE", "window function", "PARTITION BY", "frame clause"],
    },
    {
        "id": "hc-087",
        "slug": "inline-view-dept-doctor-count",
        "title": "Departments with Above-Average Doctor Count",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "Find departments that have more doctors than the overall "
            "average number of doctors per department. Return department "
            "name and doctor_count. Order by doctor_count descending."
        ),
        "schema_hint": ["departments", "doctors"],
        "solution_query": (
            "SELECT dep.name, COUNT(d.id) AS doctor_count\n"
            "FROM departments dep\n"
            "JOIN doctors d ON dep.id = d.department_id\n"
            "GROUP BY dep.id, dep.name\n"
            "HAVING COUNT(d.id) > (\n"
            "  SELECT 1.0 * COUNT(*) / COUNT(DISTINCT department_id)\n"
            "  FROM doctors\n"
            ")\n"
            "ORDER BY doctor_count DESC;"
        ),
        "hints": [
            "First figure out the average doctors per department.",
            "Average = total doctors / number of departments with doctors.",
            "Use a scalar subquery in the HAVING clause.",
            "Use 1.0 * to avoid integer division.",
        ],
        "explanation": (
            "1. Outer query counts doctors per department.\n"
            "2. HAVING compares each department's count to the global average.\n"
            "3. Scalar subquery: total doctors / distinct departments.\n"
            "4. 1.0 * forces floating-point division."
        ),
        "approach": [
            "Count doctors per department.",
            "Compute overall average in a subquery.",
            "Filter with HAVING.",
        ],
        "common_mistakes": [
            "Integer division in the subquery giving a truncated average.",
            "Using WHERE instead of HAVING for aggregate comparison.",
        ],
        "concept_tags": ["HAVING", "subquery", "GROUP BY", "AVG"],
    },
    {
        "id": "hc-088",
        "slug": "multi-join-full-visit-detail",
        "title": "Complete Visit Detail Report",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "Build a comprehensive visit detail view. For each visit, "
            "return: visit_id, visit_date, patient full name, doctor "
            "full name, department name, diagnosis, and billing amount. "
            "Include visits even if they have no billing record. Order "
            "by visit_date descending."
        ),
        "schema_hint": ["visits", "patients", "doctors", "departments", "billing"],
        "solution_query": (
            "SELECT v.id AS visit_id, v.visit_date,\n"
            "       p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       dep.name AS department_name,\n"
            "       v.diagnosis,\n"
            "       b.amount AS billing_amount\n"
            "FROM visits v\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "JOIN departments dep ON d.department_id = dep.id\n"
            "LEFT JOIN billing b ON v.id = b.visit_id\n"
            "ORDER BY v.visit_date DESC;"
        ),
        "hints": [
            "You need to join five tables together.",
            "Use LEFT JOIN for billing since not all visits may have bills.",
            "Doctors connect to departments through department_id.",
            "Concatenate first and last names for patient and doctor.",
        ],
        "explanation": (
            "1. Visit is the central table.\n"
            "2. JOIN to patients, doctors, and departments (all required).\n"
            "3. LEFT JOIN to billing (optional — visits may lack bills).\n"
            "4. Order by visit_date descending."
        ),
        "approach": [
            "Start from visits as the central table.",
            "Join required tables with INNER JOIN.",
            "Use LEFT JOIN for optional billing data.",
        ],
        "common_mistakes": [
            "Using INNER JOIN for billing and losing visits without bills.",
            "Joining doctors to departments incorrectly.",
        ],
        "concept_tags": ["JOIN", "LEFT JOIN", "multi-table", "string concatenation"],
    },
    {
        "id": "hc-089",
        "slug": "cte-patient-journey",
        "title": "Patient Journey Summary with CTEs",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Build a patient journey summary using CTEs. For each patient, "
            "show: total visits, total prescriptions, total lab tests, "
            "total billed amount, and days since first visit (as of "
            "'2025-01-01'). Return patient full name and all metrics. "
            "Only include patients with at least one visit. Order by "
            "total_billed descending."
        ),
        "schema_hint": ["patients", "visits", "prescriptions", "lab_results", "billing"],
        "solution_query": (
            "WITH visit_stats AS (\n"
            "  SELECT patient_id,\n"
            "         COUNT(*) AS total_visits,\n"
            "         MIN(visit_date) AS first_visit\n"
            "  FROM visits\n"
            "  GROUP BY patient_id\n"
            "),\n"
            "rx_stats AS (\n"
            "  SELECT v.patient_id,\n"
            "         COUNT(rx.id) AS total_prescriptions\n"
            "  FROM visits v\n"
            "  JOIN prescriptions rx ON v.id = rx.visit_id\n"
            "  GROUP BY v.patient_id\n"
            "),\n"
            "lab_stats AS (\n"
            "  SELECT v.patient_id,\n"
            "         COUNT(lr.id) AS total_labs\n"
            "  FROM visits v\n"
            "  JOIN lab_results lr ON v.id = lr.visit_id\n"
            "  GROUP BY v.patient_id\n"
            "),\n"
            "bill_stats AS (\n"
            "  SELECT v.patient_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_billed\n"
            "  FROM visits v\n"
            "  JOIN billing b ON v.id = b.visit_id\n"
            "  GROUP BY v.patient_id\n"
            ")\n"
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       vs.total_visits,\n"
            "       COALESCE(rs.total_prescriptions, 0) AS total_prescriptions,\n"
            "       COALESCE(ls.total_labs, 0) AS total_labs,\n"
            "       COALESCE(bs.total_billed, 0) AS total_billed,\n"
            "       CAST(julianday('2025-01-01') - julianday(vs.first_visit) "
            "AS INTEGER) AS days_since_first_visit\n"
            "FROM patients p\n"
            "JOIN visit_stats vs ON p.id = vs.patient_id\n"
            "LEFT JOIN rx_stats rs ON p.id = rs.patient_id\n"
            "LEFT JOIN lab_stats ls ON p.id = ls.patient_id\n"
            "LEFT JOIN bill_stats bs ON p.id = bs.patient_id\n"
            "ORDER BY total_billed DESC;"
        ),
        "hints": [
            "Create separate CTEs for visits, prescriptions, labs, and billing.",
            "Each CTE aggregates by patient_id.",
            "Use LEFT JOIN for optional stats (a patient may have visits but no labs).",
            "COALESCE handles NULLs from LEFT JOINs.",
        ],
        "explanation": (
            "1. Four CTEs aggregate different metrics per patient.\n"
            "2. Main query joins patients to all CTEs.\n"
            "3. LEFT JOIN + COALESCE handles patients missing some data.\n"
            "4. julianday computes days since first visit."
        ),
        "approach": [
            "Build one CTE per metric.",
            "Join them all in the final query.",
            "Use COALESCE for missing data.",
        ],
        "common_mistakes": [
            "Using INNER JOIN for all CTEs and losing patients without prescriptions.",
            "Double-counting due to many-to-many relationships.",
        ],
        "concept_tags": ["CTE", "multi-CTE", "LEFT JOIN", "COALESCE", "julianday"],
    },
    {
        "id": "hc-090",
        "slug": "window-cumulative-visits-per-doctor",
        "title": "Cumulative Visit Count per Doctor Over Time",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each doctor, compute a running count of their visits "
            "ordered by visit_date. Return doctor full name, visit_date, "
            "diagnosis, and cumulative_visit_num (the Nth visit for that "
            "doctor). Order by doctor last name, visit_date."
        ),
        "schema_hint": ["doctors", "visits"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       v.visit_date, v.diagnosis,\n"
            "       ROW_NUMBER() OVER (\n"
            "         PARTITION BY d.id ORDER BY v.visit_date, v.id\n"
            "       ) AS cumulative_visit_num\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "ORDER BY d.last_name, v.visit_date;"
        ),
        "hints": [
            "ROW_NUMBER can serve as a cumulative counter.",
            "Partition by doctor to restart counting for each doctor.",
            "Order by visit_date within the partition.",
            "Include visit id in ORDER BY to break ties.",
        ],
        "explanation": (
            "1. ROW_NUMBER() OVER (PARTITION BY doctor ORDER BY visit_date) "
            "gives a sequential count.\n"
            "2. Each doctor's visits are numbered 1, 2, 3, ...\n"
            "3. ORDER BY last_name, visit_date sorts the output."
        ),
        "approach": [
            "Use ROW_NUMBER partitioned by doctor.",
            "Order by visit_date within the window.",
            "Join doctors to visits.",
        ],
        "common_mistakes": [
            "Forgetting PARTITION BY and numbering across all doctors.",
            "Not breaking ties on visit_date.",
        ],
        "concept_tags": ["ROW_NUMBER", "PARTITION BY", "window function", "cumulative"],
    },
    {
        "id": "hc-091",
        "slug": "having-multi-condition",
        "title": "High-Volume High-Revenue Doctors",
        "difficulty": "medium",
        "category": "having",
        "dataset": "healthcare",
        "description": (
            "Find doctors who have both more than 5 completed visits AND "
            "total billing exceeding 5000. Return doctor full name, "
            "completed_visits, and total_billed (rounded to 2 decimals). "
            "Order by total_billed descending."
        ),
        "schema_hint": ["doctors", "visits", "billing"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       COUNT(DISTINCT CASE WHEN v.status = 'completed' "
            "THEN v.id END) AS completed_visits,\n"
            "       ROUND(SUM(b.amount), 2) AS total_billed\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "JOIN billing b ON v.id = b.visit_id\n"
            "GROUP BY d.id, d.first_name, d.last_name\n"
            "HAVING COUNT(DISTINCT CASE WHEN v.status = 'completed' "
            "THEN v.id END) > 5\n"
            "   AND SUM(b.amount) > 5000\n"
            "ORDER BY total_billed DESC;"
        ),
        "hints": [
            "HAVING can have multiple conditions combined with AND.",
            "Count completed visits using CASE inside COUNT.",
            "Sum billing amounts and filter with HAVING.",
            "Join doctors -> visits -> billing and group by doctor.",
        ],
        "explanation": (
            "1. JOIN doctors to visits to billing.\n"
            "2. GROUP BY doctor.\n"
            "3. COUNT with CASE counts only completed visits.\n"
            "4. HAVING with two conditions filters on both metrics."
        ),
        "approach": [
            "Join the three tables.",
            "Use conditional counting for completed visits.",
            "Apply multiple HAVING conditions.",
        ],
        "common_mistakes": [
            "Counting all visits instead of only completed ones.",
            "Using WHERE for aggregate conditions.",
        ],
        "concept_tags": ["HAVING", "CASE", "COUNT", "SUM", "multi-condition"],
    },
    {
        "id": "hc-092",
        "slug": "not-exists-no-prescriptions",
        "title": "Visits Without Any Prescriptions (NOT EXISTS)",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "Find all completed visits that did not result in any "
            "prescriptions. Use NOT EXISTS. Return visit_id, visit_date, "
            "patient_id, and diagnosis. Order by visit_date descending."
        ),
        "schema_hint": ["visits", "prescriptions"],
        "solution_query": (
            "SELECT v.id AS visit_id, v.visit_date,\n"
            "       v.patient_id, v.diagnosis\n"
            "FROM visits v\n"
            "WHERE v.status = 'completed'\n"
            "  AND NOT EXISTS (\n"
            "    SELECT 1 FROM prescriptions rx\n"
            "    WHERE rx.visit_id = v.id\n"
            "  )\n"
            "ORDER BY v.visit_date DESC;"
        ),
        "hints": [
            "NOT EXISTS returns TRUE when the subquery returns no rows.",
            "Correlate the subquery on visit_id.",
            "Also filter for completed visits with WHERE.",
            "Combine the status filter and NOT EXISTS with AND.",
        ],
        "explanation": (
            "1. WHERE status = 'completed' limits to completed visits.\n"
            "2. NOT EXISTS subquery checks if prescriptions exist.\n"
            "3. If no prescriptions exist for the visit, it is included."
        ),
        "approach": [
            "Filter visits by status.",
            "Use NOT EXISTS for the anti-join pattern.",
            "Correlate on visit_id.",
        ],
        "common_mistakes": [
            "Using LEFT JOIN ... WHERE rx.id IS NULL — works but different approach.",
            "Forgetting the correlation condition.",
        ],
        "concept_tags": ["NOT EXISTS", "correlated subquery", "anti-join"],
    },
    {
        "id": "hc-093",
        "slug": "lead-next-visit-date",
        "title": "Days Until Next Visit per Patient",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each patient's visits, compute the number of days until "
            "their next visit using LEAD(). Return patient_id, visit_date, "
            "next_visit_date, and days_until_next. Order by patient_id, "
            "visit_date."
        ),
        "schema_hint": ["visits"],
        "solution_query": (
            "SELECT patient_id, visit_date,\n"
            "       LEAD(visit_date) OVER (\n"
            "         PARTITION BY patient_id ORDER BY visit_date\n"
            "       ) AS next_visit_date,\n"
            "       CAST(\n"
            "         julianday(LEAD(visit_date) OVER (\n"
            "           PARTITION BY patient_id ORDER BY visit_date\n"
            "         )) - julianday(visit_date)\n"
            "       AS INTEGER) AS days_until_next\n"
            "FROM visits\n"
            "ORDER BY patient_id, visit_date;"
        ),
        "hints": [
            "LEAD(column) looks at the next row's value.",
            "Partition by patient to keep visits separate.",
            "Use julianday to compute the day difference.",
            "The last visit per patient will have NULL for next_visit_date.",
        ],
        "explanation": (
            "1. LEAD(visit_date) OVER (PARTITION BY patient_id ORDER BY visit_date) "
            "gets the next visit date.\n"
            "2. julianday subtraction computes the day gap.\n"
            "3. CAST AS INTEGER rounds to whole days.\n"
            "4. Last visit per patient has NULL."
        ),
        "approach": [
            "Use LEAD to get the next visit date.",
            "Partition by patient.",
            "Compute day difference with julianday.",
        ],
        "common_mistakes": [
            "Using LAG instead of LEAD (looks backward, not forward).",
            "Forgetting the partition — mixing different patients.",
        ],
        "concept_tags": ["LEAD", "window function", "PARTITION BY", "julianday"],
    },
    {
        "id": "hc-094",
        "slug": "cte-doctor-revenue-ranking",
        "title": "Doctor Revenue Ranking by Department (CTE + Window)",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Using a CTE, compute each doctor's total revenue (sum of "
            "billing amounts from their visits). Then rank doctors by "
            "revenue within their department using DENSE_RANK. Return "
            "department name, doctor full name, total_revenue, and "
            "dept_revenue_rank. Order by department name, rank."
        ),
        "schema_hint": ["doctors", "departments", "visits", "billing"],
        "solution_query": (
            "WITH doctor_revenue AS (\n"
            "  SELECT v.doctor_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_revenue\n"
            "  FROM visits v\n"
            "  JOIN billing b ON v.id = b.visit_id\n"
            "  GROUP BY v.doctor_id\n"
            ")\n"
            "SELECT dep.name AS department_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       COALESCE(dr.total_revenue, 0) AS total_revenue,\n"
            "       DENSE_RANK() OVER (\n"
            "         PARTITION BY dep.id\n"
            "         ORDER BY COALESCE(dr.total_revenue, 0) DESC\n"
            "       ) AS dept_revenue_rank\n"
            "FROM doctors d\n"
            "JOIN departments dep ON d.department_id = dep.id\n"
            "LEFT JOIN doctor_revenue dr ON d.id = dr.doctor_id\n"
            "ORDER BY dep.name, dept_revenue_rank;"
        ),
        "hints": [
            "CTE: aggregate billing by doctor to get total revenue.",
            "LEFT JOIN the CTE to include doctors with no billing.",
            "DENSE_RANK partitioned by department ranks within each dept.",
            "COALESCE handles NULL revenue for doctors without billing.",
        ],
        "explanation": (
            "1. CTE sums billing amounts per doctor.\n"
            "2. Main query joins doctors, departments, and the CTE.\n"
            "3. LEFT JOIN + COALESCE keeps all doctors.\n"
            "4. DENSE_RANK ranks by revenue within departments."
        ),
        "approach": [
            "Aggregate revenue in a CTE.",
            "Join to doctors and departments.",
            "Rank with DENSE_RANK.",
        ],
        "common_mistakes": [
            "Using INNER JOIN and excluding doctors with no revenue.",
            "Not using COALESCE in the ORDER BY of DENSE_RANK.",
        ],
        "concept_tags": ["CTE", "DENSE_RANK", "PARTITION BY", "LEFT JOIN", "COALESCE"],
    },
    {
        "id": "hc-095",
        "slug": "complex-case-patient-risk",
        "title": "Patient Risk Categorization",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Categorize patients into risk levels based on multiple "
            "criteria. A patient is 'High Risk' if they have more than "
            "3 visits with abnormal lab results, 'Medium Risk' if 1-3, "
            "and 'Low Risk' if none. Return patient full name, "
            "abnormal_visit_count, and risk_level. Include all patients "
            "who have had visits. Order by abnormal_visit_count descending."
        ),
        "schema_hint": ["patients", "visits", "lab_results"],
        "solution_query": (
            "WITH patient_abnormals AS (\n"
            "  SELECT v.patient_id,\n"
            "         COUNT(DISTINCT CASE WHEN lr.is_abnormal = 1 "
            "THEN v.id END) AS abnormal_visit_count\n"
            "  FROM visits v\n"
            "  LEFT JOIN lab_results lr ON v.id = lr.visit_id\n"
            "  GROUP BY v.patient_id\n"
            ")\n"
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       COALESCE(pa.abnormal_visit_count, 0) AS abnormal_visit_count,\n"
            "       CASE\n"
            "         WHEN COALESCE(pa.abnormal_visit_count, 0) > 3 THEN 'High Risk'\n"
            "         WHEN COALESCE(pa.abnormal_visit_count, 0) >= 1 THEN 'Medium Risk'\n"
            "         ELSE 'Low Risk'\n"
            "       END AS risk_level\n"
            "FROM patients p\n"
            "JOIN patient_abnormals pa ON p.id = pa.patient_id\n"
            "ORDER BY abnormal_visit_count DESC;"
        ),
        "hints": [
            "Use a CTE to count visits with abnormal lab results per patient.",
            "COUNT(DISTINCT CASE WHEN ...) counts only matching visits.",
            "Use LEFT JOIN from visits to lab_results to capture visits without labs.",
            "Apply a CASE expression for risk categorization.",
        ],
        "explanation": (
            "1. CTE counts distinct visits with abnormal labs per patient.\n"
            "2. LEFT JOIN keeps visits without lab results (count as 0).\n"
            "3. CASE assigns risk levels based on the count.\n"
            "4. COALESCE handles potential NULLs."
        ),
        "approach": [
            "Count abnormal visits per patient in a CTE.",
            "Categorize with CASE in the main query.",
            "Handle NULLs with COALESCE.",
        ],
        "common_mistakes": [
            "Counting abnormal lab results instead of distinct visits.",
            "Using INNER JOIN and missing patients with no lab results.",
        ],
        "concept_tags": ["CTE", "CASE", "COUNT DISTINCT", "LEFT JOIN", "risk analysis"],
    },
    {
        "id": "hc-096",
        "slug": "window-department-salary-share",
        "title": "Each Doctor's Share of Department Salary Budget",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each doctor, compute what percentage of their department's "
            "total salary they represent. Use a window function to compute "
            "the department total. Return department name, doctor full name, "
            "salary, dept_total_salary, and salary_share_pct (rounded to 1 "
            "decimal). Order by department name, salary_share_pct descending."
        ),
        "schema_hint": ["doctors", "departments"],
        "solution_query": (
            "SELECT dep.name AS department_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       d.salary,\n"
            "       SUM(d.salary) OVER (PARTITION BY d.department_id) "
            "AS dept_total_salary,\n"
            "       ROUND(100.0 * d.salary / SUM(d.salary) OVER "
            "(PARTITION BY d.department_id), 1) AS salary_share_pct\n"
            "FROM doctors d\n"
            "JOIN departments dep ON d.department_id = dep.id\n"
            "ORDER BY dep.name, salary_share_pct DESC;"
        ),
        "hints": [
            "SUM() OVER (PARTITION BY department) gives per-department totals.",
            "Each row retains its individual salary while having the department total.",
            "Divide individual salary by department total and multiply by 100.",
            "No GROUP BY is needed — window functions work without it.",
        ],
        "explanation": (
            "1. SUM(salary) OVER (PARTITION BY department_id) computes the "
            "department total on every row.\n"
            "2. salary / dept_total * 100 gives the percentage.\n"
            "3. Window functions avoid the need for GROUP BY + JOIN."
        ),
        "approach": [
            "Use a window SUM for the department total.",
            "Divide each doctor's salary by the total.",
            "Round to one decimal.",
        ],
        "common_mistakes": [
            "Using GROUP BY instead of a window function.",
            "Integer division — use 100.0.",
        ],
        "concept_tags": ["window function", "SUM OVER", "PARTITION BY", "percentage"],
    },
    {
        "id": "hc-097",
        "slug": "complex-multi-cte-dashboard",
        "title": "Executive Dashboard Metrics with CTEs",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Build an executive dashboard with a single query. Using CTEs, "
            "compute: total_patients, total_doctors, total_visits, "
            "total_revenue (sum of billing amount), avg_revenue_per_visit "
            "(rounded to 2), and pct_completed_visits (rounded to 1). "
            "Return a single row with all metrics."
        ),
        "schema_hint": ["patients", "doctors", "visits", "billing"],
        "solution_query": (
            "WITH metrics AS (\n"
            "  SELECT\n"
            "    (SELECT COUNT(*) FROM patients) AS total_patients,\n"
            "    (SELECT COUNT(*) FROM doctors) AS total_doctors,\n"
            "    (SELECT COUNT(*) FROM visits) AS total_visits,\n"
            "    (SELECT ROUND(SUM(amount), 2) FROM billing) AS total_revenue,\n"
            "    (SELECT ROUND(1.0 * SUM(amount) / COUNT(*), 2) "
            "FROM billing) AS avg_revenue_per_visit,\n"
            "    (SELECT ROUND(100.0 * SUM(CASE WHEN status = 'completed' "
            "THEN 1 ELSE 0 END) / COUNT(*), 1) FROM visits) "
            "AS pct_completed_visits\n"
            ")\n"
            "SELECT * FROM metrics;"
        ),
        "hints": [
            "Scalar subqueries can each compute one metric.",
            "Wrap them all in a CTE for organization.",
            "Use SUM(CASE ...) for conditional counting.",
            "1.0 * and 100.0 * prevent integer division.",
        ],
        "explanation": (
            "1. Each scalar subquery computes one dashboard metric.\n"
            "2. The CTE packages them as a single-row table.\n"
            "3. SELECT * returns all metrics in one row.\n"
            "4. Conditional aggregation for pct_completed_visits."
        ),
        "approach": [
            "Use scalar subqueries for each metric.",
            "Organize in a CTE.",
            "Return a single summary row.",
        ],
        "common_mistakes": [
            "Trying to join all tables and double-counting.",
            "Integer division in percentage calculations.",
        ],
        "concept_tags": ["CTE", "scalar subquery", "dashboard", "conditional aggregation"],
    },
    {
        "id": "hc-098",
        "slug": "string-functions-email-domain",
        "title": "Patient Count by Email Domain",
        "difficulty": "easy",
        "category": "functions",
        "dataset": "healthcare",
        "description": (
            "IT wants to know which email domains are most common among "
            "patients. Extract the domain from the email (everything after "
            "'@') and count patients per domain. Return email_domain and "
            "patient_count. Order by patient_count descending."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT SUBSTR(email, INSTR(email, '@') + 1) AS email_domain,\n"
            "       COUNT(*) AS patient_count\n"
            "FROM patients\n"
            "GROUP BY email_domain\n"
            "ORDER BY patient_count DESC;"
        ),
        "hints": [
            "INSTR(email, '@') finds the position of the @ sign.",
            "SUBSTR(string, start) extracts from start to the end.",
            "Add 1 to the position to skip the @ itself.",
            "Group by the extracted domain and count.",
        ],
        "explanation": (
            "1. INSTR finds the @ position.\n"
            "2. SUBSTR extracts everything after @.\n"
            "3. GROUP BY domain counts patients per domain.\n"
            "4. ORDER BY count descending."
        ),
        "approach": [
            "Extract the domain using INSTR and SUBSTR.",
            "Group by the domain.",
            "Count and sort.",
        ],
        "common_mistakes": [
            "Using LIKE '%@%' which does not extract the domain.",
            "Off-by-one error with SUBSTR position.",
        ],
        "concept_tags": ["SUBSTR", "INSTR", "string functions", "GROUP BY"],
    },
    {
        "id": "hc-099",
        "slug": "patient-age-calculation",
        "title": "Current Patient Age Calculation",
        "difficulty": "easy",
        "category": "date_functions",
        "dataset": "healthcare",
        "description": (
            "Calculate each patient's age in years as of '2025-01-01'. "
            "Return first_name, last_name, date_of_birth, and age. "
            "Order by age descending, last_name."
        ),
        "schema_hint": ["patients"],
        "solution_query": (
            "SELECT first_name, last_name, date_of_birth,\n"
            "       CAST((julianday('2025-01-01') - julianday(date_of_birth)) "
            "/ 365.25 AS INTEGER) AS age\n"
            "FROM patients\n"
            "ORDER BY age DESC, last_name;"
        ),
        "hints": [
            "Use julianday to compute the difference in days.",
            "Divide by 365.25 to convert days to approximate years.",
            "CAST AS INTEGER truncates to whole years.",
            "Use a fixed reference date for consistent results.",
        ],
        "explanation": (
            "1. julianday('2025-01-01') - julianday(date_of_birth) gives age in days.\n"
            "2. Divide by 365.25 for years (accounts for leap years).\n"
            "3. CAST AS INTEGER truncates to whole years.\n"
            "4. Order by age descending, then last_name."
        ),
        "approach": [
            "Compute day difference with julianday.",
            "Convert to years.",
            "Cast to integer.",
        ],
        "common_mistakes": [
            "Dividing by 365 instead of 365.25, slightly off for older patients.",
            "Using strftime('%Y') subtraction which ignores month/day.",
        ],
        "concept_tags": ["julianday", "date arithmetic", "CAST", "age calculation"],
    },
    {
        "id": "hc-100",
        "slug": "comprehensive-hospital-report",
        "title": "Comprehensive Hospital Performance Report",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Build a department-level performance report. For each "
            "department, show: department name, number of doctors, "
            "total completed visits, total revenue, average revenue per "
            "completed visit, cancellation rate (cancelled + no_show as "
            "percentage of total visits), and the top-earning doctor's "
            "name in that department. Use CTEs. Order by total_revenue "
            "descending."
        ),
        "schema_hint": [
            "departments", "doctors", "visits", "billing",
        ],
        "solution_query": (
            "WITH dept_doctors AS (\n"
            "  SELECT department_id, COUNT(*) AS doctor_count\n"
            "  FROM doctors\n"
            "  GROUP BY department_id\n"
            "),\n"
            "dept_visits AS (\n"
            "  SELECT d.department_id,\n"
            "         COUNT(*) AS total_visits,\n"
            "         SUM(CASE WHEN v.status = 'completed' THEN 1 ELSE 0 END) "
            "AS completed_visits,\n"
            "         SUM(CASE WHEN v.status IN ('cancelled', 'no_show') "
            "THEN 1 ELSE 0 END) AS cancelled_visits\n"
            "  FROM visits v\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "  GROUP BY d.department_id\n"
            "),\n"
            "dept_revenue AS (\n"
            "  SELECT d.department_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_revenue\n"
            "  FROM billing b\n"
            "  JOIN visits v ON b.visit_id = v.id\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "  GROUP BY d.department_id\n"
            "),\n"
            "top_doctor AS (\n"
            "  SELECT department_id,\n"
            "         first_name || ' ' || last_name AS doctor_name,\n"
            "         ROW_NUMBER() OVER (\n"
            "           PARTITION BY department_id ORDER BY salary DESC\n"
            "         ) AS rn\n"
            "  FROM doctors\n"
            ")\n"
            "SELECT dep.name AS department_name,\n"
            "       dd.doctor_count,\n"
            "       COALESCE(dv.completed_visits, 0) AS completed_visits,\n"
            "       COALESCE(dr.total_revenue, 0) AS total_revenue,\n"
            "       CASE WHEN COALESCE(dv.completed_visits, 0) > 0\n"
            "            THEN ROUND(1.0 * COALESCE(dr.total_revenue, 0) "
            "/ dv.completed_visits, 2)\n"
            "            ELSE 0 END AS avg_revenue_per_visit,\n"
            "       CASE WHEN COALESCE(dv.total_visits, 0) > 0\n"
            "            THEN ROUND(100.0 * COALESCE(dv.cancelled_visits, 0) "
            "/ dv.total_visits, 1)\n"
            "            ELSE 0 END AS cancellation_rate,\n"
            "       td.doctor_name AS top_earning_doctor\n"
            "FROM departments dep\n"
            "JOIN dept_doctors dd ON dep.id = dd.department_id\n"
            "LEFT JOIN dept_visits dv ON dep.id = dv.department_id\n"
            "LEFT JOIN dept_revenue dr ON dep.id = dr.department_id\n"
            "LEFT JOIN top_doctor td ON dep.id = td.department_id AND td.rn = 1\n"
            "ORDER BY total_revenue DESC;"
        ),
        "hints": [
            "Break into separate CTEs: doctor counts, visit stats, revenue, top doctor.",
            "Use conditional aggregation (SUM + CASE) for status breakdowns.",
            "ROW_NUMBER partitioned by department finds the top earner.",
            "Join all CTEs to the departments table in the final query.",
        ],
        "explanation": (
            "1. dept_doctors: counts doctors per department.\n"
            "2. dept_visits: counts total, completed, and cancelled visits.\n"
            "3. dept_revenue: sums billing per department.\n"
            "4. top_doctor: uses ROW_NUMBER to find the highest-paid doctor.\n"
            "5. Final query joins all CTEs and computes rates."
        ),
        "approach": [
            "Decompose into independent CTEs.",
            "Aggregate different metrics in each CTE.",
            "Use ROW_NUMBER for top-N per group.",
            "Join everything in the final query with COALESCE for NULLs.",
        ],
        "common_mistakes": [
            "Trying to compute everything in one massive query without CTEs.",
            "Division by zero when a department has no completed visits.",
            "Using INNER JOIN and losing departments with no visits.",
        ],
        "concept_tags": [
            "CTE", "multi-CTE", "ROW_NUMBER", "PARTITION BY",
            "conditional aggregation", "COALESCE", "LEFT JOIN",
            "comprehensive report",
        ],
    },
    {
        "id": "hc-101",
        "slug": "dense-rank-doctors-by-patient-count",
        "title": "Rank Doctors by Patient Count Within Each Department",
        "difficulty": "hard",
        "category": "window_function",
        "dataset": "healthcare",
        "description": (
            "For each doctor, count the distinct patients they have seen "
            "and rank them within their department using DENSE_RANK. "
            "Return department name, doctor full name, patient_count, "
            "and dept_rank. Order by department name, dept_rank."
        ),
        "schema_hint": ["doctors", "departments", "visits"],
        "solution_query": (
            "SELECT dep.name AS department_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       COUNT(DISTINCT v.patient_id) AS patient_count,\n"
            "       DENSE_RANK() OVER (\n"
            "         PARTITION BY d.department_id\n"
            "         ORDER BY COUNT(DISTINCT v.patient_id) DESC\n"
            "       ) AS dept_rank\n"
            "FROM doctors d\n"
            "JOIN departments dep ON d.department_id = dep.id\n"
            "LEFT JOIN visits v ON d.id = v.doctor_id\n"
            "GROUP BY d.id, d.first_name, d.last_name, d.department_id, dep.name\n"
            "ORDER BY dep.name, dept_rank;"
        ),
        "hints": [
            "COUNT(DISTINCT patient_id) gives the number of unique patients per doctor.",
            "DENSE_RANK allows ties — two doctors with the same count share a rank.",
            "PARTITION BY department_id scopes the ranking to each department.",
            "Use LEFT JOIN to include doctors who have not yet seen any patients.",
        ],
        "explanation": (
            "1. LEFT JOIN visits to doctors to count patients (including doctors with 0).\n"
            "2. GROUP BY doctor to get per-doctor patient counts.\n"
            "3. DENSE_RANK() OVER (PARTITION BY department ORDER BY count DESC) "
            "ranks within each department.\n"
            "4. DENSE_RANK keeps consecutive ranks even with ties."
        ),
        "approach": [
            "Join doctors, departments, and visits.",
            "Group by doctor and count distinct patients.",
            "Apply DENSE_RANK partitioned by department.",
        ],
        "common_mistakes": [
            "Using RANK instead of DENSE_RANK — RANK skips numbers after ties.",
            "Counting visits instead of distinct patients.",
            "Forgetting GROUP BY when using window functions with aggregates.",
        ],
        "concept_tags": ["DENSE_RANK", "PARTITION BY", "window function", "COUNT DISTINCT", "GROUP BY"],
    },
    {
        "id": "hc-102",
        "slug": "multi-cte-patient-visit-summary",
        "title": "Patient Visit Summary with Diagnosis Counts and Billing",
        "difficulty": "hard",
        "category": "cte",
        "dataset": "healthcare",
        "description": (
            "Using multiple CTEs, build a patient visit summary. For each "
            "patient, show: full name, total_visits, distinct_diagnoses "
            "(number of unique diagnoses across all visits), total_billed "
            "(rounded to 2 decimals), and avg_bill_per_visit (rounded to 2). "
            "Only include patients with at least one visit. Order by "
            "total_billed descending."
        ),
        "schema_hint": ["patients", "visits", "diagnoses", "billing"],
        "solution_query": (
            "WITH visit_counts AS (\n"
            "  SELECT patient_id,\n"
            "         COUNT(*) AS total_visits,\n"
            "         COUNT(DISTINCT diagnosis) AS distinct_diagnoses\n"
            "  FROM visits\n"
            "  GROUP BY patient_id\n"
            "),\n"
            "billing_totals AS (\n"
            "  SELECT v.patient_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_billed\n"
            "  FROM visits v\n"
            "  JOIN billing b ON v.id = b.visit_id\n"
            "  GROUP BY v.patient_id\n"
            ")\n"
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       vc.total_visits,\n"
            "       vc.distinct_diagnoses,\n"
            "       COALESCE(bt.total_billed, 0) AS total_billed,\n"
            "       CASE WHEN vc.total_visits > 0\n"
            "            THEN ROUND(COALESCE(bt.total_billed, 0) "
            "/ vc.total_visits, 2)\n"
            "            ELSE 0 END AS avg_bill_per_visit\n"
            "FROM patients p\n"
            "JOIN visit_counts vc ON p.id = vc.patient_id\n"
            "LEFT JOIN billing_totals bt ON p.id = bt.patient_id\n"
            "ORDER BY total_billed DESC;"
        ),
        "hints": [
            "Use one CTE for visit counts and distinct diagnoses.",
            "Use a second CTE for billing totals per patient.",
            "LEFT JOIN billing totals since some patients may have no bills.",
            "Compute avg_bill_per_visit by dividing total_billed by total_visits.",
        ],
        "explanation": (
            "1. visit_counts CTE: counts visits and distinct diagnoses per patient.\n"
            "2. billing_totals CTE: sums billing amounts per patient.\n"
            "3. Main query joins patients to both CTEs.\n"
            "4. LEFT JOIN + COALESCE handles patients with visits but no billing.\n"
            "5. avg_bill_per_visit = total_billed / total_visits."
        ),
        "approach": [
            "Build a CTE for visit metrics.",
            "Build a CTE for billing metrics.",
            "Join both to the patients table.",
            "Compute the average in the final SELECT.",
        ],
        "common_mistakes": [
            "Using INNER JOIN for billing and losing patients without bills.",
            "Forgetting COALESCE for NULL billing totals.",
            "Division by zero if total_visits could be zero (guarded by JOIN).",
        ],
        "concept_tags": ["CTE", "multi-CTE", "LEFT JOIN", "COALESCE", "ROUND", "COUNT DISTINCT"],
    },
    {
        "id": "hc-103",
        "slug": "patients-without-prescriptions",
        "title": "Patients Who Have Never Had a Prescription",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "Find all patients who have never received a prescription "
            "across any of their visits. Return patient full name, "
            "email, and date_of_birth. Use a subquery approach. "
            "Order by last_name, first_name."
        ),
        "schema_hint": ["patients", "visits", "prescriptions"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       p.email,\n"
            "       p.date_of_birth\n"
            "FROM patients p\n"
            "WHERE p.id NOT IN (\n"
            "  SELECT DISTINCT v.patient_id\n"
            "  FROM visits v\n"
            "  JOIN prescriptions rx ON v.id = rx.visit_id\n"
            ")\n"
            "ORDER BY p.last_name, p.first_name;"
        ),
        "hints": [
            "Find all patient IDs that appear in visits with prescriptions.",
            "Use NOT IN to exclude those patients from the full patient list.",
            "Join visits to prescriptions in the subquery to link them.",
            "DISTINCT in the subquery avoids duplicates.",
        ],
        "explanation": (
            "1. Subquery joins visits to prescriptions and selects distinct patient_ids.\n"
            "2. These are patients who HAVE had prescriptions.\n"
            "3. NOT IN excludes them, leaving only patients with no prescriptions.\n"
            "4. This includes patients with no visits at all."
        ),
        "approach": [
            "Build a subquery that finds patient IDs with prescriptions.",
            "Use NOT IN to filter the patients table.",
            "Order alphabetically.",
        ],
        "common_mistakes": [
            "Using NOT EXISTS without proper correlation.",
            "Forgetting to join visits to prescriptions in the subquery.",
            "Not handling patients who have never visited at all.",
        ],
        "concept_tags": ["NOT IN", "subquery", "anti-join", "DISTINCT"],
    },
    {
        "id": "hc-104",
        "slug": "department-performance-dashboard",
        "title": "Department Performance Dashboard",
        "difficulty": "hard",
        "category": "advanced",
        "dataset": "healthcare",
        "description": (
            "Create a department performance dashboard. For each department, "
            "show: department name, total number of unique patients seen, "
            "total visits, average days between a patient's first and last "
            "visit (rounded to 1 decimal, as avg_visit_span_days), and "
            "total revenue (rounded to 2 decimals). Only include departments "
            "that have had at least one visit. Order by total_revenue "
            "descending."
        ),
        "schema_hint": ["departments", "doctors", "visits", "billing"],
        "solution_query": (
            "WITH dept_visits AS (\n"
            "  SELECT d.department_id,\n"
            "         v.patient_id,\n"
            "         v.id AS visit_id,\n"
            "         v.visit_date\n"
            "  FROM visits v\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "),\n"
            "patient_spans AS (\n"
            "  SELECT department_id, patient_id,\n"
            "         CAST(julianday(MAX(visit_date)) - "
            "julianday(MIN(visit_date)) AS REAL) AS span_days\n"
            "  FROM dept_visits\n"
            "  GROUP BY department_id, patient_id\n"
            "),\n"
            "dept_metrics AS (\n"
            "  SELECT dv.department_id,\n"
            "         COUNT(DISTINCT dv.patient_id) AS unique_patients,\n"
            "         COUNT(DISTINCT dv.visit_id) AS total_visits\n"
            "  FROM dept_visits dv\n"
            "  GROUP BY dv.department_id\n"
            "),\n"
            "dept_spans AS (\n"
            "  SELECT department_id,\n"
            "         ROUND(AVG(span_days), 1) AS avg_visit_span_days\n"
            "  FROM patient_spans\n"
            "  GROUP BY department_id\n"
            "),\n"
            "dept_revenue AS (\n"
            "  SELECT d.department_id,\n"
            "         ROUND(SUM(b.amount), 2) AS total_revenue\n"
            "  FROM billing b\n"
            "  JOIN visits v ON b.visit_id = v.id\n"
            "  JOIN doctors d ON v.doctor_id = d.id\n"
            "  GROUP BY d.department_id\n"
            ")\n"
            "SELECT dep.name AS department_name,\n"
            "       dm.unique_patients,\n"
            "       dm.total_visits,\n"
            "       COALESCE(ds.avg_visit_span_days, 0) AS avg_visit_span_days,\n"
            "       COALESCE(dr.total_revenue, 0) AS total_revenue\n"
            "FROM departments dep\n"
            "JOIN dept_metrics dm ON dep.id = dm.department_id\n"
            "LEFT JOIN dept_spans ds ON dep.id = ds.department_id\n"
            "LEFT JOIN dept_revenue dr ON dep.id = dr.department_id\n"
            "ORDER BY total_revenue DESC;"
        ),
        "hints": [
            "Link visits to departments through the doctors table.",
            "Compute each patient's visit span (MAX date - MIN date) per department.",
            "Average the spans across patients for each department.",
            "Use separate CTEs for visit metrics, spans, and revenue.",
        ],
        "explanation": (
            "1. dept_visits CTE links visits to departments via doctors.\n"
            "2. patient_spans computes the day range between first and last visit "
            "per patient per department.\n"
            "3. dept_metrics counts unique patients and visits.\n"
            "4. dept_spans averages the patient visit spans.\n"
            "5. dept_revenue sums billing amounts.\n"
            "6. Final query joins all CTEs to departments."
        ),
        "approach": [
            "Build a base CTE linking visits to departments.",
            "Compute per-patient spans in a second CTE.",
            "Aggregate department-level metrics in separate CTEs.",
            "Join everything in the final query.",
        ],
        "common_mistakes": [
            "Forgetting that visits connect to departments through doctors.",
            "Not grouping by both department and patient when computing spans.",
            "Using INNER JOIN for revenue and losing departments with no billing.",
        ],
        "concept_tags": [
            "CTE", "multi-CTE", "julianday", "AVG", "COUNT DISTINCT",
            "LEFT JOIN", "COALESCE", "dashboard",
        ],
    },
    {
        "id": "hc-105",
        "slug": "prescriptions-with-patient-doctor-diagnosis",
        "title": "Prescriptions with Patient, Doctor, and Diagnosis Details",
        "difficulty": "medium",
        "category": "join",
        "dataset": "healthcare",
        "description": (
            "List all prescriptions along with the patient full name, "
            "doctor full name, visit diagnosis, medication, and dosage. "
            "Order by patient last name, then visit_date descending."
        ),
        "schema_hint": ["prescriptions", "visits", "patients", "doctors"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       v.diagnosis,\n"
            "       rx.medication,\n"
            "       rx.dosage,\n"
            "       v.visit_date\n"
            "FROM prescriptions rx\n"
            "JOIN visits v ON rx.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "ORDER BY p.last_name, v.visit_date DESC;"
        ),
        "hints": [
            "Prescriptions link to visits via visit_id.",
            "Visits link to patients via patient_id and to doctors via doctor_id.",
            "Join all four tables to get the full picture.",
            "Concatenate first and last names for patient and doctor.",
        ],
        "explanation": (
            "1. Start from prescriptions as the base table.\n"
            "2. JOIN to visits to get the visit context (diagnosis, date).\n"
            "3. JOIN to patients for the patient name.\n"
            "4. JOIN to doctors for the doctor name.\n"
            "5. Order by patient last name, then newest visits first."
        ),
        "approach": [
            "Start from prescriptions.",
            "Join to visits, patients, and doctors.",
            "Select the required columns and order.",
        ],
        "common_mistakes": [
            "Joining on the wrong foreign key columns.",
            "Forgetting to include visit_date for ordering.",
            "Using LEFT JOIN when all prescriptions should have a valid visit.",
        ],
        "concept_tags": ["JOIN", "multi-table", "string concatenation", "ORDER BY"],
    },
    # =========================================================================
    # INTERVIEW-FOCUSED PROBLEMS (30 problems: interview-hc-001 through interview-hc-030)
    # =========================================================================
    # --- EASY (10 problems) ---
    {
        "id": "interview-hc-001",
        "slug": "int-hc-male-patients-by-city",
        "title": "Male Patients Grouped by City",
        "difficulty": "easy",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "A population health team wants to understand the geographic "
            "distribution of male patients. Write a query that returns each "
            "city and the number of male patients in that city, sorted by "
            "count descending."
        ),
        "schema_hint": ["patients"],
        "concept_tags": ["SELECT", "WHERE", "GROUP BY", "COUNT", "ORDER BY"],
        "solution_query": (
            "SELECT city, COUNT(*) AS male_count\n"
            "FROM patients\n"
            "WHERE gender = 'M'\n"
            "GROUP BY city\n"
            "ORDER BY male_count DESC;"
        ),
        "hints": [
            "Filter for male patients first, then aggregate.",
            "COUNT(*) counts rows in each group.",
            "GROUP BY city creates one row per city.",
            "SELECT city, COUNT(*) FROM patients WHERE gender = 'M' GROUP BY city ORDER BY ...;",
        ],
        "explanation": (
            "1. WHERE gender = 'M' filters to male patients only.\n"
            "2. GROUP BY city groups remaining rows by city.\n"
            "3. COUNT(*) tallies each group.\n"
            "4. ORDER BY male_count DESC shows the largest populations first."
        ),
        "approach": [
            "Filter the patients table to males.",
            "Group by city and count each group.",
            "Sort descending by the count.",
        ],
        "common_mistakes": [
            "Forgetting the WHERE clause and counting all genders.",
            "Omitting ORDER BY, returning results in an arbitrary order.",
        ],
    },
    {
        "id": "interview-hc-002",
        "slug": "int-hc-premium-insurance-plans",
        "title": "Premium Insurance Plans with Low Copay",
        "difficulty": "easy",
        "category": "WHERE",
        "dataset": "healthcare",
        "description": (
            "The finance team wants to identify premium insurance plans that "
            "have a copay less than 40. Return the provider_name, plan_type, "
            "coverage_amount, and copay for these plans, ordered by copay ascending."
        ),
        "schema_hint": ["insurance"],
        "concept_tags": ["SELECT", "WHERE", "AND", "ORDER BY"],
        "solution_query": (
            "SELECT provider_name, plan_type, coverage_amount, copay\n"
            "FROM insurance\n"
            "WHERE plan_type = 'premium' AND copay < 40\n"
            "ORDER BY copay ASC;"
        ),
        "hints": [
            "You need two conditions: plan type and copay threshold.",
            "Use AND to combine both conditions in the WHERE clause.",
            "ASC is the default sort direction but can be made explicit.",
            "WHERE plan_type = 'premium' AND copay < 40",
        ],
        "explanation": (
            "1. SELECT the four requested columns from the insurance table.\n"
            "2. WHERE plan_type = 'premium' restricts to premium plans.\n"
            "3. AND copay < 40 further filters for low copay.\n"
            "4. ORDER BY copay ASC sorts lowest copay first."
        ),
        "approach": [
            "Identify the insurance table and needed columns.",
            "Apply a compound WHERE condition.",
            "Sort ascending by copay.",
        ],
        "common_mistakes": [
            "Using OR instead of AND, returning non-premium plans with low copay.",
            "Forgetting that plan_type values are lowercase strings.",
        ],
    },
    {
        "id": "interview-hc-003",
        "slug": "int-hc-doctor-count-per-specialty",
        "title": "Doctor Count per Specialty",
        "difficulty": "easy",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "Hospital leadership wants a breakdown of how many doctors "
            "practice in each specialty. Return each specialty and the "
            "number of doctors, sorted by doctor count descending."
        ),
        "schema_hint": ["doctors"],
        "concept_tags": ["SELECT", "GROUP BY", "COUNT", "ORDER BY"],
        "solution_query": (
            "SELECT specialty, COUNT(*) AS doctor_count\n"
            "FROM doctors\n"
            "GROUP BY specialty\n"
            "ORDER BY doctor_count DESC;"
        ),
        "hints": [
            "Group the doctors by their specialty.",
            "Use an aggregate function to count each group.",
            "Sort the result so the most popular specialty appears first.",
            "SELECT specialty, COUNT(*) FROM doctors GROUP BY specialty ORDER BY ...;",
        ],
        "explanation": (
            "1. GROUP BY specialty creates one row per specialty.\n"
            "2. COUNT(*) counts doctors in each specialty.\n"
            "3. ORDER BY doctor_count DESC puts the largest group first."
        ),
        "approach": [
            "Group the doctors table by specialty.",
            "Count records in each group.",
            "Order by count descending.",
        ],
        "common_mistakes": [
            "Selecting columns not in the GROUP BY without aggregation.",
            "Forgetting DESC, which would show smallest groups first.",
        ],
    },
    {
        "id": "interview-hc-004",
        "slug": "int-hc-cancelled-visits-count",
        "title": "Total Cancelled and No-Show Visits",
        "difficulty": "easy",
        "category": "WHERE",
        "dataset": "healthcare",
        "description": (
            "Operations wants to know how many visits were either cancelled "
            "or marked as no-shows. Return a single count of visits whose "
            "status is 'cancelled' or 'no_show'."
        ),
        "schema_hint": ["visits"],
        "concept_tags": ["SELECT", "WHERE", "IN", "COUNT"],
        "solution_query": (
            "SELECT COUNT(*) AS missed_visits\n"
            "FROM visits\n"
            "WHERE status IN ('cancelled', 'no_show');"
        ),
        "hints": [
            "You need to filter for two possible status values.",
            "The IN operator checks membership in a set of values.",
            "COUNT(*) counts all matching rows.",
            "WHERE status IN ('cancelled', 'no_show')",
        ],
        "explanation": (
            "1. WHERE status IN ('cancelled', 'no_show') matches both statuses.\n"
            "2. COUNT(*) returns the total number of matching visits."
        ),
        "approach": [
            "Use IN to check for multiple status values.",
            "Wrap in COUNT(*) to get a single number.",
        ],
        "common_mistakes": [
            "Using AND instead of OR/IN when checking one column for multiple values.",
            "Misspelling the status values.",
        ],
    },
    {
        "id": "interview-hc-005",
        "slug": "int-hc-recent-lab-results",
        "title": "Recent Abnormal Lab Results",
        "difficulty": "easy",
        "category": "WHERE",
        "dataset": "healthcare",
        "description": (
            "A clinical review board needs all abnormal lab results from "
            "2024 onward. Return the test_name, result_value, unit, and "
            "tested_at for abnormal results tested on or after '2024-01-01', "
            "ordered by tested_at descending."
        ),
        "schema_hint": ["lab_results"],
        "concept_tags": ["SELECT", "WHERE", "AND", "ORDER BY"],
        "solution_query": (
            "SELECT test_name, result_value, unit, tested_at\n"
            "FROM lab_results\n"
            "WHERE is_abnormal = 1\n"
            "  AND tested_at >= '2024-01-01'\n"
            "ORDER BY tested_at DESC;"
        ),
        "hints": [
            "Abnormal results are indicated by is_abnormal = 1.",
            "Combine the abnormality flag with a date filter using AND.",
            "Order by tested_at descending for most recent first.",
            "WHERE is_abnormal = 1 AND tested_at >= '2024-01-01'",
        ],
        "explanation": (
            "1. WHERE is_abnormal = 1 filters to abnormal results only.\n"
            "2. AND tested_at >= '2024-01-01' restricts to 2024 and later.\n"
            "3. ORDER BY tested_at DESC shows the most recent results first."
        ),
        "approach": [
            "Filter lab_results on is_abnormal and tested_at.",
            "Return the requested columns.",
            "Sort by date descending.",
        ],
        "common_mistakes": [
            "Using is_abnormal = 'true' instead of the integer 1.",
            "Forgetting DESC, which would show oldest results first.",
        ],
    },
    {
        "id": "interview-hc-006",
        "slug": "int-hc-department-budget-ranking",
        "title": "Departments Ordered by Budget",
        "difficulty": "easy",
        "category": "ORDER BY",
        "dataset": "healthcare",
        "description": (
            "The CFO wants a simple ranked list of departments by their "
            "budget. Return the department name, floor, and budget, sorted "
            "by budget from highest to lowest."
        ),
        "schema_hint": ["departments"],
        "concept_tags": ["SELECT", "ORDER BY"],
        "solution_query": (
            "SELECT name, floor, budget\n"
            "FROM departments\n"
            "ORDER BY budget DESC;"
        ),
        "hints": [
            "No filtering or grouping is needed here.",
            "Use ORDER BY with DESC for highest first.",
            "The departments table has name, floor, and budget columns.",
            "SELECT name, floor, budget FROM departments ORDER BY budget DESC;",
        ],
        "explanation": (
            "1. SELECT the three columns from departments.\n"
            "2. ORDER BY budget DESC sorts from highest to lowest budget."
        ),
        "approach": [
            "Select name, floor, and budget from departments.",
            "Order by budget descending.",
        ],
        "common_mistakes": [
            "Forgetting DESC, which defaults to ascending.",
            "Using GROUP BY when no aggregation is needed.",
        ],
    },
    {
        "id": "interview-hc-007",
        "slug": "int-hc-billing-pending-total",
        "title": "Total Pending Billing Amount",
        "difficulty": "easy",
        "category": "aggregate",
        "dataset": "healthcare",
        "description": (
            "The accounts receivable team needs the total dollar amount of "
            "all pending bills. Return a single value: the SUM of amount "
            "for billing records where status is 'pending'."
        ),
        "schema_hint": ["billing"],
        "concept_tags": ["SELECT", "WHERE", "SUM"],
        "solution_query": (
            "SELECT SUM(amount) AS total_pending\n"
            "FROM billing\n"
            "WHERE status = 'pending';"
        ),
        "hints": [
            "Filter to pending bills before summing.",
            "SUM(amount) adds up all matching values.",
            "This should return a single row, single column.",
            "SELECT SUM(amount) FROM billing WHERE status = 'pending';",
        ],
        "explanation": (
            "1. WHERE status = 'pending' filters to pending bills.\n"
            "2. SUM(amount) totals the amount column across all matching rows."
        ),
        "approach": [
            "Filter billing to pending status.",
            "Use SUM to aggregate the amount.",
        ],
        "common_mistakes": [
            "Using COUNT instead of SUM, which gives number of bills not dollar total.",
            "Forgetting the WHERE clause and summing all bills.",
        ],
    },
    {
        "id": "interview-hc-008",
        "slug": "int-hc-patient-age-groups",
        "title": "Patient Count by Birth Decade",
        "difficulty": "easy",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "A demographic study needs patients grouped by their birth "
            "decade (e.g., 1950, 1960, 1970). Return each decade and the "
            "number of patients born in that decade, sorted by decade."
        ),
        "schema_hint": ["patients"],
        "concept_tags": ["SELECT", "GROUP BY", "COUNT", "string functions"],
        "solution_query": (
            "SELECT (CAST(SUBSTR(date_of_birth, 1, 3) AS INTEGER) * 10) AS birth_decade,\n"
            "       COUNT(*) AS patient_count\n"
            "FROM patients\n"
            "GROUP BY birth_decade\n"
            "ORDER BY birth_decade;"
        ),
        "hints": [
            "Extract the first three characters of date_of_birth to get the century+decade prefix.",
            "Multiply by 10 to get the decade as a four-digit year.",
            "SUBSTR and CAST can parse text date components.",
            "CAST(SUBSTR(date_of_birth, 1, 3) AS INTEGER) * 10 gives the decade.",
        ],
        "explanation": (
            "1. SUBSTR(date_of_birth, 1, 3) extracts e.g. '198' from '1985-03-14'.\n"
            "2. CAST to INTEGER and multiply by 10 produces 1980.\n"
            "3. GROUP BY birth_decade groups patients into decades.\n"
            "4. COUNT(*) counts patients in each group."
        ),
        "approach": [
            "Derive the decade from the date_of_birth string.",
            "Group by the derived decade.",
            "Count patients per group and order by decade.",
        ],
        "common_mistakes": [
            "Trying to use YEAR() which is not available in SQLite.",
            "Extracting wrong substring positions from the date string.",
        ],
    },
    {
        "id": "interview-hc-009",
        "slug": "int-hc-prescriptions-with-no-refills",
        "title": "Prescriptions with Zero Refills",
        "difficulty": "easy",
        "category": "WHERE",
        "dataset": "healthcare",
        "description": (
            "The pharmacy wants to identify one-time prescriptions that "
            "have no refills. Return the medication, dosage, frequency, "
            "and start_date for prescriptions where refills is 0, ordered "
            "by start_date descending."
        ),
        "schema_hint": ["prescriptions"],
        "concept_tags": ["SELECT", "WHERE", "ORDER BY"],
        "solution_query": (
            "SELECT medication, dosage, frequency, start_date\n"
            "FROM prescriptions\n"
            "WHERE refills = 0\n"
            "ORDER BY start_date DESC;"
        ),
        "hints": [
            "Filter where refills equals zero.",
            "Refills is an integer column, compare with 0.",
            "Order by start_date descending for most recent first.",
            "WHERE refills = 0 ORDER BY start_date DESC;",
        ],
        "explanation": (
            "1. WHERE refills = 0 filters to prescriptions with no refills.\n"
            "2. ORDER BY start_date DESC shows the newest prescriptions first."
        ),
        "approach": [
            "Filter prescriptions on refills = 0.",
            "Select the requested columns.",
            "Order by start_date descending.",
        ],
        "common_mistakes": [
            "Using refills IS NULL instead of refills = 0.",
            "Forgetting to order the results.",
        ],
    },
    {
        "id": "interview-hc-010",
        "slug": "int-hc-visits-per-weekday",
        "title": "Visit Count by Day of Week",
        "difficulty": "easy",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "Scheduling wants to understand visit distribution across "
            "the week. Return the day of the week (0=Sunday through "
            "6=Saturday) and the number of visits on that day, sorted "
            "by visit count descending."
        ),
        "schema_hint": ["visits"],
        "concept_tags": ["SELECT", "GROUP BY", "COUNT", "date functions"],
        "solution_query": (
            "SELECT STRFTIME('%w', visit_date) AS day_of_week,\n"
            "       COUNT(*) AS visit_count\n"
            "FROM visits\n"
            "GROUP BY day_of_week\n"
            "ORDER BY visit_count DESC;"
        ),
        "hints": [
            "SQLite uses STRFTIME for date part extraction.",
            "'%w' format returns the day of the week (0=Sunday).",
            "Group by the extracted day of week.",
            "STRFTIME('%w', visit_date) gives the weekday number.",
        ],
        "explanation": (
            "1. STRFTIME('%w', visit_date) extracts the weekday number.\n"
            "2. GROUP BY day_of_week creates one row per weekday.\n"
            "3. COUNT(*) tallies visits per weekday.\n"
            "4. ORDER BY visit_count DESC shows busiest days first."
        ),
        "approach": [
            "Use STRFTIME to extract the weekday.",
            "Group and count by weekday.",
            "Sort by count descending.",
        ],
        "common_mistakes": [
            "Using DAYOFWEEK() which does not exist in SQLite.",
            "Confusing '%w' (weekday) with '%W' (week number).",
        ],
    },
    # --- MEDIUM (12 problems) ---
    {
        "id": "interview-hc-011",
        "slug": "int-hc-patient-visit-doctor-join",
        "title": "Patient Visit History with Doctor Details",
        "difficulty": "medium",
        "category": "JOIN",
        "dataset": "healthcare",
        "description": (
            "Build a patient visit history report. For each completed visit, "
            "return the patient's full name, the doctor's full name, "
            "the visit_date, and the diagnosis. Sort by visit_date descending."
        ),
        "schema_hint": ["patients", "visits", "doctors"],
        "concept_tags": ["JOIN", "WHERE", "string concatenation", "ORDER BY"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       v.visit_date,\n"
            "       v.diagnosis\n"
            "FROM visits v\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN doctors d ON v.doctor_id = d.id\n"
            "WHERE v.status = 'completed'\n"
            "ORDER BY v.visit_date DESC;"
        ),
        "hints": [
            "You need a three-table JOIN: visits, patients, doctors.",
            "Use || to concatenate first and last names.",
            "Filter for completed visits with WHERE.",
            "visits connects to patients via patient_id and to doctors via doctor_id.",
        ],
        "explanation": (
            "1. JOIN visits to patients on patient_id and to doctors on doctor_id.\n"
            "2. WHERE v.status = 'completed' filters to completed visits.\n"
            "3. String concatenation builds full names.\n"
            "4. ORDER BY v.visit_date DESC shows most recent first."
        ),
        "approach": [
            "Start from the visits table.",
            "JOIN patients and doctors on their respective foreign keys.",
            "Filter for completed status.",
            "Concatenate names and order by date.",
        ],
        "common_mistakes": [
            "Joining on wrong columns (e.g., patient.id = doctor.id).",
            "Forgetting to filter for completed visits only.",
        ],
    },
    {
        "id": "interview-hc-012",
        "slug": "int-hc-avg-prescriptions-per-visit",
        "title": "Average Prescriptions per Visit by Doctor",
        "difficulty": "medium",
        "category": "JOIN",
        "dataset": "healthcare",
        "description": (
            "Management wants to compare prescribing habits. For each doctor, "
            "calculate the average number of prescriptions per visit. Return "
            "the doctor's full name, total visits, total prescriptions, and "
            "the average prescriptions per visit (rounded to 2 decimals). "
            "Only include doctors who have at least one visit. Sort by average "
            "descending."
        ),
        "schema_hint": ["doctors", "visits", "prescriptions"],
        "concept_tags": ["JOIN", "GROUP BY", "COUNT", "ROUND", "subquery"],
        "solution_query": (
            "SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "       COUNT(DISTINCT v.id) AS total_visits,\n"
            "       COUNT(rx.id) AS total_prescriptions,\n"
            "       ROUND(1.0 * COUNT(rx.id) / COUNT(DISTINCT v.id), 2) AS avg_rx_per_visit\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "LEFT JOIN prescriptions rx ON v.id = rx.visit_id\n"
            "GROUP BY d.id, d.first_name, d.last_name\n"
            "ORDER BY avg_rx_per_visit DESC;"
        ),
        "hints": [
            "Use COUNT(DISTINCT v.id) to count unique visits per doctor.",
            "LEFT JOIN prescriptions to include visits with no prescriptions.",
            "Multiply by 1.0 to force floating-point division.",
            "ROUND(1.0 * COUNT(rx.id) / COUNT(DISTINCT v.id), 2) computes the average.",
        ],
        "explanation": (
            "1. JOIN doctors to visits to get each doctor's visits.\n"
            "2. LEFT JOIN prescriptions so visits without prescriptions still count.\n"
            "3. COUNT(DISTINCT v.id) avoids double-counting visits inflated by multiple prescriptions.\n"
            "4. Division gives average prescriptions per visit; ROUND to 2 decimals."
        ),
        "approach": [
            "Join doctors, visits, and prescriptions.",
            "Use COUNT(DISTINCT) for visits and COUNT for prescriptions.",
            "Divide to get the average and round.",
            "Group by doctor and sort by average descending.",
        ],
        "common_mistakes": [
            "Using COUNT(*) instead of COUNT(DISTINCT v.id), inflating visit counts.",
            "Integer division that truncates to 0 instead of using 1.0 multiplier.",
            "Forgetting LEFT JOIN and excluding doctors whose visits had no prescriptions.",
        ],
    },
    {
        "id": "interview-hc-013",
        "slug": "int-hc-billing-by-insurance-plan",
        "title": "Billing Breakdown by Insurance Plan Type",
        "difficulty": "medium",
        "category": "JOIN",
        "dataset": "healthcare",
        "description": (
            "Finance wants to see how billing is distributed across insurance "
            "plan types. For each plan_type, return the plan_type, total "
            "billed amount, total insurance_covered amount, total "
            "patient_responsibility, and the count of billing records. "
            "Sort by total billed descending."
        ),
        "schema_hint": ["billing", "visits", "patients", "insurance"],
        "concept_tags": ["JOIN", "GROUP BY", "SUM", "COUNT"],
        "solution_query": (
            "SELECT i.plan_type,\n"
            "       SUM(b.amount) AS total_billed,\n"
            "       SUM(b.insurance_covered) AS total_covered,\n"
            "       SUM(b.patient_responsibility) AS total_patient_resp,\n"
            "       COUNT(*) AS bill_count\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "JOIN insurance i ON p.insurance_id = i.id\n"
            "GROUP BY i.plan_type\n"
            "ORDER BY total_billed DESC;"
        ),
        "hints": [
            "You need to chain four tables: billing -> visits -> patients -> insurance.",
            "Use SUM for each monetary column.",
            "Group by plan_type to get one row per plan.",
            "billing connects to visits, visits to patients, patients to insurance.",
        ],
        "explanation": (
            "1. Chain JOINs from billing through visits and patients to insurance.\n"
            "2. GROUP BY i.plan_type aggregates by plan type.\n"
            "3. SUM computes totals for each monetary column.\n"
            "4. COUNT(*) gives the number of billing records per plan."
        ),
        "approach": [
            "Join billing to visits, visits to patients, patients to insurance.",
            "Group by plan_type.",
            "Aggregate monetary columns with SUM and count records.",
        ],
        "common_mistakes": [
            "Missing one of the intermediate JOINs in the chain.",
            "Grouping by provider_name instead of plan_type.",
        ],
    },
    {
        "id": "interview-hc-014",
        "slug": "int-hc-department-visit-performance",
        "title": "Department Visit Completion Rate",
        "difficulty": "medium",
        "category": "JOIN",
        "dataset": "healthcare",
        "description": (
            "Compare department performance by calculating the completion "
            "rate of visits. For each department, return the department name, "
            "total visits, completed visits, and the completion rate as a "
            "percentage (rounded to 1 decimal). Sort by completion rate "
            "descending."
        ),
        "schema_hint": ["departments", "doctors", "visits"],
        "concept_tags": ["JOIN", "GROUP BY", "CASE", "ROUND", "percentage"],
        "solution_query": (
            "SELECT dep.name AS department_name,\n"
            "       COUNT(*) AS total_visits,\n"
            "       SUM(CASE WHEN v.status = 'completed' THEN 1 ELSE 0 END) AS completed_visits,\n"
            "       ROUND(100.0 * SUM(CASE WHEN v.status = 'completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate\n"
            "FROM departments dep\n"
            "JOIN doctors d ON d.department_id = dep.id\n"
            "JOIN visits v ON v.doctor_id = d.id\n"
            "GROUP BY dep.id, dep.name\n"
            "ORDER BY completion_rate DESC;"
        ),
        "hints": [
            "Use CASE WHEN to conditionally count completed visits.",
            "Multiply by 100.0 for percentage.",
            "Chain departments -> doctors -> visits.",
            "SUM(CASE WHEN v.status = 'completed' THEN 1 ELSE 0 END) counts completed visits.",
        ],
        "explanation": (
            "1. JOIN departments to doctors to visits.\n"
            "2. COUNT(*) gives total visits per department.\n"
            "3. SUM(CASE ...) counts only completed visits.\n"
            "4. Dividing and multiplying by 100 gives the percentage."
        ),
        "approach": [
            "Join departments through doctors to visits.",
            "Use conditional aggregation for completed counts.",
            "Compute the percentage and round.",
        ],
        "common_mistakes": [
            "Using COUNT with a WHERE clause that filters out non-completed visits entirely.",
            "Integer division producing 0 instead of a decimal rate.",
        ],
    },
    {
        "id": "interview-hc-015",
        "slug": "int-hc-frequent-visitors",
        "title": "Patients with Visits in Multiple Months",
        "difficulty": "medium",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "Identify highly engaged patients. Find patients who have had "
            "visits in 3 or more distinct calendar months. Return the "
            "patient's first name, last name, and the number of distinct "
            "months they visited. Sort by distinct months descending."
        ),
        "schema_hint": ["patients", "visits"],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT", "STRFTIME"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       COUNT(DISTINCT STRFTIME('%Y-%m', v.visit_date)) AS distinct_months\n"
            "FROM patients p\n"
            "JOIN visits v ON p.id = v.patient_id\n"
            "GROUP BY p.id, p.first_name, p.last_name\n"
            "HAVING distinct_months >= 3\n"
            "ORDER BY distinct_months DESC;"
        ),
        "hints": [
            "Use STRFTIME('%Y-%m', visit_date) to extract year-month.",
            "COUNT(DISTINCT ...) counts unique months.",
            "HAVING filters groups after aggregation.",
            "COUNT(DISTINCT STRFTIME('%Y-%m', v.visit_date)) >= 3",
        ],
        "explanation": (
            "1. JOIN patients to visits.\n"
            "2. STRFTIME('%Y-%m', ...) extracts the year-month.\n"
            "3. COUNT(DISTINCT ...) counts unique months per patient.\n"
            "4. HAVING >= 3 keeps only patients with 3+ distinct months."
        ),
        "approach": [
            "Join patients to visits.",
            "Extract year-month from visit_date.",
            "Count distinct months per patient.",
            "Filter with HAVING and sort.",
        ],
        "common_mistakes": [
            "Using WHERE instead of HAVING to filter aggregated results.",
            "Counting visits instead of distinct months.",
        ],
    },
    {
        "id": "interview-hc-016",
        "slug": "int-hc-insurance-coverage-gap",
        "title": "Patient Out-of-Pocket Exceeding Insurance Coverage",
        "difficulty": "medium",
        "category": "JOIN",
        "dataset": "healthcare",
        "description": (
            "Find visits where the patient's responsibility exceeded the "
            "insurance-covered portion. Return the patient's full name, "
            "visit_date, amount, insurance_covered, patient_responsibility, "
            "and the difference (patient_responsibility - insurance_covered) "
            "as overpay_gap. Only include rows where the gap is positive. "
            "Sort by overpay_gap descending."
        ),
        "schema_hint": ["patients", "visits", "billing"],
        "concept_tags": ["JOIN", "WHERE", "arithmetic", "ORDER BY"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       v.visit_date,\n"
            "       b.amount,\n"
            "       b.insurance_covered,\n"
            "       b.patient_responsibility,\n"
            "       (b.patient_responsibility - b.insurance_covered) AS overpay_gap\n"
            "FROM billing b\n"
            "JOIN visits v ON b.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE b.patient_responsibility > b.insurance_covered\n"
            "ORDER BY overpay_gap DESC;"
        ),
        "hints": [
            "Compare patient_responsibility to insurance_covered in the WHERE clause.",
            "Subtract to compute the gap in the SELECT.",
            "Chain billing to visits to patients.",
            "WHERE b.patient_responsibility > b.insurance_covered",
        ],
        "explanation": (
            "1. JOIN billing -> visits -> patients.\n"
            "2. WHERE filters to rows where patient pays more than insurance.\n"
            "3. The computed column overpay_gap shows the difference.\n"
            "4. ORDER BY overpay_gap DESC shows the largest gaps first."
        ),
        "approach": [
            "Join billing to visits to patients.",
            "Filter for patient_responsibility > insurance_covered.",
            "Compute the difference and sort descending.",
        ],
        "common_mistakes": [
            "Reversing the subtraction order.",
            "Forgetting the WHERE filter and including negative gaps.",
        ],
    },
    {
        "id": "interview-hc-017",
        "slug": "int-hc-lab-abnormal-rate-by-test",
        "title": "Abnormal Result Rate by Lab Test",
        "difficulty": "medium",
        "category": "GROUP BY",
        "dataset": "healthcare",
        "description": (
            "The lab director wants to know the abnormality rate for each "
            "test. For each test_name, return the total number of results, "
            "the number of abnormal results, and the abnormal percentage "
            "(rounded to 1 decimal). Only include tests with at least 5 "
            "results. Sort by abnormal rate descending."
        ),
        "schema_hint": ["lab_results"],
        "concept_tags": ["GROUP BY", "SUM", "COUNT", "HAVING", "ROUND"],
        "solution_query": (
            "SELECT test_name,\n"
            "       COUNT(*) AS total_results,\n"
            "       SUM(is_abnormal) AS abnormal_count,\n"
            "       ROUND(100.0 * SUM(is_abnormal) / COUNT(*), 1) AS abnormal_rate\n"
            "FROM lab_results\n"
            "GROUP BY test_name\n"
            "HAVING total_results >= 5\n"
            "ORDER BY abnormal_rate DESC;"
        ),
        "hints": [
            "Since is_abnormal is 0 or 1, SUM gives the count of abnormals.",
            "Divide abnormal count by total and multiply by 100 for percentage.",
            "HAVING filters after GROUP BY.",
            "SUM(is_abnormal) counts abnormal results because it sums 1s and 0s.",
        ],
        "explanation": (
            "1. GROUP BY test_name groups all results by test.\n"
            "2. SUM(is_abnormal) counts abnormals (since the column is 0/1).\n"
            "3. Division by COUNT(*) and multiplication by 100 gives percentage.\n"
            "4. HAVING >= 5 excludes rare tests."
        ),
        "approach": [
            "Group by test_name.",
            "Count total and sum abnormals.",
            "Calculate percentage, filter with HAVING, sort.",
        ],
        "common_mistakes": [
            "Using COUNT(is_abnormal) which counts non-NULL values, not just 1s.",
            "Forgetting HAVING and including tests with very few results.",
        ],
    },
    {
        "id": "interview-hc-018",
        "slug": "int-hc-readmission-within-30-days",
        "title": "Patients with Visits Within 30 Days of a Previous Visit",
        "difficulty": "medium",
        "category": "self-join",
        "dataset": "healthcare",
        "description": (
            "Identify potential readmissions by finding patients who had "
            "two visits within 30 days of each other. Return the patient's "
            "first name, last name, the first visit date, the second visit "
            "date, and the number of days between them. Each pair should "
            "appear only once. Sort by days_between ascending."
        ),
        "schema_hint": ["patients", "visits"],
        "concept_tags": ["self-join", "JOIN", "JULIANDAY", "date arithmetic"],
        "solution_query": (
            "SELECT p.first_name, p.last_name,\n"
            "       v1.visit_date AS first_visit,\n"
            "       v2.visit_date AS second_visit,\n"
            "       CAST(JULIANDAY(v2.visit_date) - JULIANDAY(v1.visit_date) AS INTEGER) AS days_between\n"
            "FROM visits v1\n"
            "JOIN visits v2 ON v1.patient_id = v2.patient_id\n"
            "  AND v2.visit_date > v1.visit_date\n"
            "  AND JULIANDAY(v2.visit_date) - JULIANDAY(v1.visit_date) <= 30\n"
            "JOIN patients p ON v1.patient_id = p.id\n"
            "ORDER BY days_between ASC;"
        ),
        "hints": [
            "Self-join the visits table to itself on the same patient_id.",
            "Ensure v2.visit_date > v1.visit_date to avoid duplicates.",
            "Use JULIANDAY for date arithmetic in SQLite.",
            "JULIANDAY(v2.visit_date) - JULIANDAY(v1.visit_date) gives days between.",
        ],
        "explanation": (
            "1. Self-join visits on the same patient_id with v2 after v1.\n"
            "2. JULIANDAY difference calculates days between visits.\n"
            "3. Filter for pairs within 30 days.\n"
            "4. JOIN patients for name display."
        ),
        "approach": [
            "Self-join visits on patient_id with a date ordering constraint.",
            "Use JULIANDAY for day difference.",
            "Filter within 30 days and join patients for names.",
        ],
        "common_mistakes": [
            "Not constraining v2.visit_date > v1.visit_date, creating duplicate pairs.",
            "Using string comparison for date arithmetic instead of JULIANDAY.",
        ],
    },
    {
        "id": "interview-hc-019",
        "slug": "int-hc-top-diagnosis-per-department",
        "title": "Most Common Diagnosis per Department",
        "difficulty": "medium",
        "category": "subquery",
        "dataset": "healthcare",
        "description": (
            "For each department, find the most frequently occurring "
            "diagnosis. Return the department name, the top diagnosis, and "
            "its count. In case of ties, any one is acceptable."
        ),
        "schema_hint": ["departments", "doctors", "visits"],
        "concept_tags": ["JOIN", "GROUP BY", "subquery", "ranking"],
        "solution_query": (
            "SELECT department_name, diagnosis, diagnosis_count\n"
            "FROM (\n"
            "    SELECT dep.name AS department_name,\n"
            "           v.diagnosis,\n"
            "           COUNT(*) AS diagnosis_count,\n"
            "           ROW_NUMBER() OVER (PARTITION BY dep.id ORDER BY COUNT(*) DESC) AS rn\n"
            "    FROM departments dep\n"
            "    JOIN doctors d ON d.department_id = dep.id\n"
            "    JOIN visits v ON v.doctor_id = d.id\n"
            "    GROUP BY dep.id, dep.name, v.diagnosis\n"
            ") sub\n"
            "WHERE rn = 1;"
        ),
        "hints": [
            "Use ROW_NUMBER() OVER (PARTITION BY department ...) to rank diagnoses.",
            "Wrap in a subquery and filter where rn = 1.",
            "Join departments -> doctors -> visits to link diagnoses to departments.",
            "GROUP BY department and diagnosis to count occurrences.",
        ],
        "explanation": (
            "1. JOIN departments to doctors to visits.\n"
            "2. GROUP BY department and diagnosis to count each diagnosis per department.\n"
            "3. ROW_NUMBER() ranks diagnoses within each department by count.\n"
            "4. Outer query filters to rank = 1 (most common)."
        ),
        "approach": [
            "Join the three tables and group by department and diagnosis.",
            "Use ROW_NUMBER with PARTITION BY department.",
            "Filter to rank 1 in the outer query.",
        ],
        "common_mistakes": [
            "Using MAX(COUNT(*)) which is not valid in SQL.",
            "Forgetting to GROUP BY both department and diagnosis.",
        ],
    },
    {
        "id": "interview-hc-020",
        "slug": "int-hc-medication-overlap-detection",
        "title": "Patients on Multiple Concurrent Medications",
        "difficulty": "medium",
        "category": "self-join",
        "dataset": "healthcare",
        "description": (
            "Identify patients who have overlapping prescriptions (two different "
            "medications where one's date range overlaps with another). Return "
            "the patient's full name, medication_1, medication_2, and the "
            "overlap start date (later of the two start dates). Show each pair "
            "once only."
        ),
        "schema_hint": ["patients", "visits", "prescriptions"],
        "concept_tags": ["self-join", "JOIN", "date overlap", "MAX/MIN"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       rx1.medication AS medication_1,\n"
            "       rx2.medication AS medication_2,\n"
            "       MAX(rx1.start_date, rx2.start_date) AS overlap_start\n"
            "FROM prescriptions rx1\n"
            "JOIN visits v1 ON rx1.visit_id = v1.id\n"
            "JOIN prescriptions rx2 ON rx1.id < rx2.id\n"
            "JOIN visits v2 ON rx2.visit_id = v2.id\n"
            "  AND v1.patient_id = v2.patient_id\n"
            "JOIN patients p ON v1.patient_id = p.id\n"
            "WHERE rx1.medication <> rx2.medication\n"
            "  AND rx1.start_date <= rx2.end_date\n"
            "  AND rx2.start_date <= rx1.end_date\n"
            "ORDER BY patient_name, overlap_start;"
        ),
        "hints": [
            "Two date ranges overlap if start1 <= end2 AND start2 <= end1.",
            "Self-join prescriptions with rx1.id < rx2.id to avoid duplicates.",
            "Connect both prescriptions to the same patient via their visits.",
            "MAX(rx1.start_date, rx2.start_date) gives the overlap start.",
        ],
        "explanation": (
            "1. Self-join prescriptions on rx1.id < rx2.id for unique pairs.\n"
            "2. Connect both to the same patient via visits.\n"
            "3. Check overlap condition: start1 <= end2 AND start2 <= end1.\n"
            "4. Filter for different medications.\n"
            "5. MAX of start dates gives overlap start."
        ),
        "approach": [
            "Self-join prescriptions to find pairs for the same patient.",
            "Apply the date overlap condition.",
            "Use rx1.id < rx2.id to avoid duplicate pairs.",
        ],
        "common_mistakes": [
            "Missing the date overlap condition entirely.",
            "Not ensuring both prescriptions belong to the same patient.",
            "Getting duplicate pairs by not using id < id.",
        ],
    },
    {
        "id": "interview-hc-021",
        "slug": "int-hc-monthly-revenue-trend",
        "title": "Monthly Revenue with Month-over-Month Change",
        "difficulty": "medium",
        "category": "window functions",
        "dataset": "healthcare",
        "description": (
            "Build a monthly revenue trend report. For each month (YYYY-MM), "
            "show the total billing amount, and the change from the previous "
            "month. Return month, total_revenue, and revenue_change. Sort by "
            "month ascending."
        ),
        "schema_hint": ["billing"],
        "concept_tags": ["GROUP BY", "window functions", "LAG", "STRFTIME"],
        "solution_query": (
            "SELECT month,\n"
            "       total_revenue,\n"
            "       total_revenue - LAG(total_revenue) OVER (ORDER BY month) AS revenue_change\n"
            "FROM (\n"
            "    SELECT STRFTIME('%Y-%m', billed_at) AS month,\n"
            "           SUM(amount) AS total_revenue\n"
            "    FROM billing\n"
            "    GROUP BY month\n"
            ") monthly\n"
            "ORDER BY month;"
        ),
        "hints": [
            "First aggregate billing by month using STRFTIME.",
            "Then use LAG() to access the previous month's revenue.",
            "Subtracting LAG from current gives the change.",
            "LAG(total_revenue) OVER (ORDER BY month) accesses the prior row.",
        ],
        "explanation": (
            "1. Inner query groups billing by YYYY-MM and sums amounts.\n"
            "2. LAG(total_revenue) OVER (ORDER BY month) gets the previous month's total.\n"
            "3. Subtracting LAG from current gives month-over-month change.\n"
            "4. First month will have NULL change since there is no prior month."
        ),
        "approach": [
            "Aggregate billing by month in a subquery.",
            "Apply LAG window function for previous month value.",
            "Subtract to compute the change.",
        ],
        "common_mistakes": [
            "Trying to use LAG without a subquery, mixing aggregation and window functions.",
            "Using billed_at directly without extracting YYYY-MM.",
        ],
    },
    {
        "id": "interview-hc-022",
        "slug": "int-hc-doctor-patient-unique-diagnosis",
        "title": "Doctors Who Treated Every Blood Type",
        "difficulty": "medium",
        "category": "division",
        "dataset": "healthcare",
        "description": (
            "Find doctors who have treated patients of every blood type. "
            "Return the doctor's first name, last name, and the number of "
            "distinct blood types treated. Only include doctors whose "
            "distinct blood type count equals the total number of distinct "
            "blood types in the patients table."
        ),
        "schema_hint": ["doctors", "visits", "patients"],
        "concept_tags": ["JOIN", "GROUP BY", "HAVING", "COUNT DISTINCT", "subquery"],
        "solution_query": (
            "SELECT d.first_name, d.last_name,\n"
            "       COUNT(DISTINCT p.blood_type) AS blood_types_treated\n"
            "FROM doctors d\n"
            "JOIN visits v ON d.id = v.doctor_id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "GROUP BY d.id, d.first_name, d.last_name\n"
            "HAVING COUNT(DISTINCT p.blood_type) = (\n"
            "    SELECT COUNT(DISTINCT blood_type) FROM patients\n"
            ");"
        ),
        "hints": [
            "Count distinct blood types per doctor.",
            "Compare to total distinct blood types via a subquery in HAVING.",
            "Join doctors -> visits -> patients to connect doctors to blood types.",
            "HAVING COUNT(DISTINCT p.blood_type) = (SELECT COUNT(DISTINCT blood_type) FROM patients)",
        ],
        "explanation": (
            "1. JOIN doctors to visits to patients.\n"
            "2. GROUP BY doctor and count distinct blood types treated.\n"
            "3. HAVING compares each doctor's count to the total distinct blood types.\n"
            "4. Only doctors matching all blood types are returned."
        ),
        "approach": [
            "Join the three tables.",
            "Group by doctor and count distinct blood types.",
            "Use a subquery in HAVING to compare to the total.",
        ],
        "common_mistakes": [
            "Hard-coding the number of blood types instead of using a subquery.",
            "Using COUNT(blood_type) instead of COUNT(DISTINCT blood_type).",
        ],
    },
    # --- HARD (8 problems) ---
    {
        "id": "interview-hc-023",
        "slug": "int-hc-patient-visit-gap-analysis",
        "title": "Visit Gap Analysis with Window Functions",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "healthcare",
        "description": (
            "For each patient's visits (ordered by date), calculate the "
            "number of days since their previous visit. Return the patient's "
            "full name, visit_date, previous_visit_date, and days_since_last. "
            "Include only patients who have had at least 2 visits. Sort by "
            "days_since_last descending to highlight the largest gaps."
        ),
        "schema_hint": ["patients", "visits"],
        "concept_tags": ["window functions", "LAG", "JULIANDAY", "JOIN"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       v.visit_date,\n"
            "       LAG(v.visit_date) OVER (PARTITION BY v.patient_id ORDER BY v.visit_date) AS previous_visit_date,\n"
            "       CAST(JULIANDAY(v.visit_date) - JULIANDAY(\n"
            "           LAG(v.visit_date) OVER (PARTITION BY v.patient_id ORDER BY v.visit_date)\n"
            "       ) AS INTEGER) AS days_since_last\n"
            "FROM visits v\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "WHERE LAG(v.visit_date) OVER (PARTITION BY v.patient_id ORDER BY v.visit_date) IS NOT NULL\n"
            "ORDER BY days_since_last DESC;"
        ),
        "hints": [
            "LAG(visit_date) OVER (PARTITION BY patient_id ORDER BY visit_date) gets the prior visit.",
            "JULIANDAY difference calculates days between dates.",
            "Filter out rows where LAG is NULL (first visits).",
            "Wrap in a subquery if the WHERE on window function doesn't work.",
        ],
        "explanation": (
            "1. LAG partitioned by patient_id gets each patient's previous visit date.\n"
            "2. JULIANDAY difference computes the gap in days.\n"
            "3. Filtering out NULL LAG values removes first visits.\n"
            "4. ORDER BY days_since_last DESC highlights the longest gaps.\n"
            "Note: In SQLite, you may need to wrap the window function in a subquery "
            "to filter on it."
        ),
        "approach": [
            "Use LAG window function partitioned by patient.",
            "Compute day difference with JULIANDAY.",
            "Filter out first visits (NULL lag).",
            "Sort by gap descending.",
        ],
        "common_mistakes": [
            "Using LAG directly in WHERE which may not work; need a subquery.",
            "Forgetting PARTITION BY and computing LAG across all patients.",
        ],
    },
    {
        "id": "interview-hc-024",
        "slug": "int-hc-department-ranking-composite",
        "title": "Department Composite Performance Ranking",
        "difficulty": "hard",
        "category": "CTE",
        "dataset": "healthcare",
        "description": (
            "Create a composite department ranking. Using CTEs, compute "
            "for each department: (1) total visits, (2) total revenue from "
            "billing, (3) average doctor salary. Then rank departments by "
            "total revenue descending. Return department name, total_visits, "
            "total_revenue, avg_salary (rounded to 0 decimals), and the "
            "revenue rank."
        ),
        "schema_hint": ["departments", "doctors", "visits", "billing"],
        "concept_tags": ["CTE", "JOIN", "RANK", "window functions", "ROUND"],
        "solution_query": (
            "WITH dept_visits AS (\n"
            "    SELECT d.department_id,\n"
            "           COUNT(*) AS total_visits\n"
            "    FROM doctors d\n"
            "    JOIN visits v ON v.doctor_id = d.id\n"
            "    GROUP BY d.department_id\n"
            "),\n"
            "dept_revenue AS (\n"
            "    SELECT d.department_id,\n"
            "           SUM(b.amount) AS total_revenue\n"
            "    FROM doctors d\n"
            "    JOIN visits v ON v.doctor_id = d.id\n"
            "    JOIN billing b ON b.visit_id = v.id\n"
            "    GROUP BY d.department_id\n"
            "),\n"
            "dept_salary AS (\n"
            "    SELECT department_id,\n"
            "           ROUND(AVG(salary), 0) AS avg_salary\n"
            "    FROM doctors\n"
            "    GROUP BY department_id\n"
            ")\n"
            "SELECT dep.name AS department_name,\n"
            "       COALESCE(dv.total_visits, 0) AS total_visits,\n"
            "       COALESCE(dr.total_revenue, 0) AS total_revenue,\n"
            "       ds.avg_salary,\n"
            "       RANK() OVER (ORDER BY COALESCE(dr.total_revenue, 0) DESC) AS revenue_rank\n"
            "FROM departments dep\n"
            "LEFT JOIN dept_visits dv ON dep.id = dv.department_id\n"
            "LEFT JOIN dept_revenue dr ON dep.id = dr.department_id\n"
            "LEFT JOIN dept_salary ds ON dep.id = ds.department_id\n"
            "ORDER BY revenue_rank;"
        ),
        "hints": [
            "Use three CTEs: one for visits, one for revenue, one for salary.",
            "LEFT JOIN each CTE to departments so all departments appear.",
            "RANK() OVER (ORDER BY revenue DESC) creates the ranking.",
            "COALESCE handles departments with no visits or billing.",
        ],
        "explanation": (
            "1. CTE dept_visits counts visits per department.\n"
            "2. CTE dept_revenue sums billing amounts per department.\n"
            "3. CTE dept_salary averages doctor salary per department.\n"
            "4. Final query LEFT JOINs all three to departments.\n"
            "5. RANK() window function ranks by revenue descending."
        ),
        "approach": [
            "Build separate CTEs for each metric.",
            "LEFT JOIN all CTEs to the departments table.",
            "Use RANK() window function for the ranking.",
        ],
        "common_mistakes": [
            "Using INNER JOIN which drops departments with no visits.",
            "Forgetting COALESCE for NULL values from LEFT JOINs.",
            "Confusing RANK vs ROW_NUMBER when ties exist.",
        ],
    },
    {
        "id": "interview-hc-025",
        "slug": "int-hc-doctor-workload-percentile",
        "title": "Doctor Workload Percentile Ranking",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "healthcare",
        "description": (
            "Rank each doctor by workload (number of visits) within their "
            "department using PERCENT_RANK. Return the doctor's full name, "
            "department name, visit count, and their percentile rank "
            "(rounded to 2 decimals). Sort by department name, then percentile "
            "descending."
        ),
        "schema_hint": ["doctors", "departments", "visits"],
        "concept_tags": ["window functions", "PERCENT_RANK", "JOIN", "GROUP BY"],
        "solution_query": (
            "SELECT doctor_name, department_name, visit_count,\n"
            "       ROUND(PERCENT_RANK() OVER (\n"
            "           PARTITION BY department_name ORDER BY visit_count\n"
            "       ), 2) AS percentile_rank\n"
            "FROM (\n"
            "    SELECT d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "           dep.name AS department_name,\n"
            "           COUNT(v.id) AS visit_count\n"
            "    FROM doctors d\n"
            "    JOIN departments dep ON d.department_id = dep.id\n"
            "    LEFT JOIN visits v ON v.doctor_id = d.id\n"
            "    GROUP BY d.id, d.first_name, d.last_name, dep.name\n"
            ") sub\n"
            "ORDER BY department_name, percentile_rank DESC;"
        ),
        "hints": [
            "First aggregate visit counts per doctor in a subquery.",
            "Apply PERCENT_RANK() partitioned by department.",
            "LEFT JOIN visits so doctors with zero visits are included.",
            "PERCENT_RANK() returns a value between 0 and 1.",
        ],
        "explanation": (
            "1. Inner query counts visits per doctor via LEFT JOIN.\n"
            "2. PERCENT_RANK() partitioned by department ranks within department.\n"
            "3. ROUND to 2 decimals for readability.\n"
            "4. Sort by department then percentile descending."
        ),
        "approach": [
            "Aggregate visits per doctor in a subquery.",
            "Apply PERCENT_RANK window function partitioned by department.",
            "Sort by department and percentile.",
        ],
        "common_mistakes": [
            "Trying to use PERCENT_RANK with GROUP BY in the same query level.",
            "Using INNER JOIN and losing doctors with no visits.",
        ],
    },
    {
        "id": "interview-hc-026",
        "slug": "int-hc-patient-journey-cte",
        "title": "Complete Patient Journey Timeline",
        "difficulty": "hard",
        "category": "CTE",
        "dataset": "healthcare",
        "description": (
            "Build a comprehensive patient journey report using CTEs. For "
            "each patient, show: total visits, total prescriptions, total "
            "lab tests, total billed amount, and days between their first "
            "and last visit (patient tenure). Return patient full name, "
            "total_visits, total_prescriptions, total_lab_tests, "
            "total_billed, and tenure_days. Sort by tenure_days descending."
        ),
        "schema_hint": ["patients", "visits", "prescriptions", "lab_results", "billing"],
        "concept_tags": ["CTE", "JOIN", "LEFT JOIN", "aggregate", "JULIANDAY"],
        "solution_query": (
            "WITH visit_stats AS (\n"
            "    SELECT patient_id,\n"
            "           COUNT(*) AS total_visits,\n"
            "           MIN(visit_date) AS first_visit,\n"
            "           MAX(visit_date) AS last_visit\n"
            "    FROM visits\n"
            "    GROUP BY patient_id\n"
            "),\n"
            "rx_stats AS (\n"
            "    SELECT v.patient_id,\n"
            "           COUNT(rx.id) AS total_prescriptions\n"
            "    FROM visits v\n"
            "    JOIN prescriptions rx ON rx.visit_id = v.id\n"
            "    GROUP BY v.patient_id\n"
            "),\n"
            "lab_stats AS (\n"
            "    SELECT v.patient_id,\n"
            "           COUNT(lr.id) AS total_lab_tests\n"
            "    FROM visits v\n"
            "    JOIN lab_results lr ON lr.visit_id = v.id\n"
            "    GROUP BY v.patient_id\n"
            "),\n"
            "bill_stats AS (\n"
            "    SELECT v.patient_id,\n"
            "           SUM(b.amount) AS total_billed\n"
            "    FROM visits v\n"
            "    JOIN billing b ON b.visit_id = v.id\n"
            "    GROUP BY v.patient_id\n"
            ")\n"
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       COALESCE(vs.total_visits, 0) AS total_visits,\n"
            "       COALESCE(rs.total_prescriptions, 0) AS total_prescriptions,\n"
            "       COALESCE(ls.total_lab_tests, 0) AS total_lab_tests,\n"
            "       COALESCE(bs.total_billed, 0) AS total_billed,\n"
            "       CAST(JULIANDAY(vs.last_visit) - JULIANDAY(vs.first_visit) AS INTEGER) AS tenure_days\n"
            "FROM patients p\n"
            "LEFT JOIN visit_stats vs ON p.id = vs.patient_id\n"
            "LEFT JOIN rx_stats rs ON p.id = rs.patient_id\n"
            "LEFT JOIN lab_stats ls ON p.id = ls.patient_id\n"
            "LEFT JOIN bill_stats bs ON p.id = bs.patient_id\n"
            "WHERE vs.total_visits IS NOT NULL\n"
            "ORDER BY tenure_days DESC;"
        ),
        "hints": [
            "Use four CTEs: one each for visits, prescriptions, labs, and billing.",
            "Aggregate per patient_id in each CTE.",
            "LEFT JOIN all CTEs to patients.",
            "JULIANDAY(MAX) - JULIANDAY(MIN) gives tenure in days.",
        ],
        "explanation": (
            "1. Four CTEs aggregate different metrics per patient.\n"
            "2. LEFT JOIN all to patients to preserve patients across all CTEs.\n"
            "3. COALESCE handles patients with no prescriptions, labs, or bills.\n"
            "4. JULIANDAY difference of first and last visit gives tenure.\n"
            "5. Filter out patients with no visits."
        ),
        "approach": [
            "Create separate CTEs for each data domain.",
            "LEFT JOIN all CTEs to the patients table.",
            "Compute tenure from first/last visit dates.",
        ],
        "common_mistakes": [
            "Using INNER JOINs which drop patients missing any one metric.",
            "Counting across tables without separating into CTEs, causing row multiplication.",
            "Forgetting COALESCE for NULL aggregates.",
        ],
    },
    {
        "id": "interview-hc-027",
        "slug": "int-hc-running-abnormal-count",
        "title": "Cumulative Abnormal Lab Results per Patient Over Time",
        "difficulty": "hard",
        "category": "window functions",
        "dataset": "healthcare",
        "description": (
            "Track the accumulation of abnormal lab results for each patient "
            "over time. For each lab result, show the patient's full name, "
            "test_name, tested_at, is_abnormal, and a running count of "
            "abnormal results for that patient up to and including this test. "
            "Sort by patient last name, then tested_at."
        ),
        "schema_hint": ["patients", "visits", "lab_results"],
        "concept_tags": ["window functions", "SUM", "JOIN", "running total"],
        "solution_query": (
            "SELECT p.first_name || ' ' || p.last_name AS patient_name,\n"
            "       lr.test_name,\n"
            "       lr.tested_at,\n"
            "       lr.is_abnormal,\n"
            "       SUM(lr.is_abnormal) OVER (\n"
            "           PARTITION BY p.id\n"
            "           ORDER BY lr.tested_at\n"
            "           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
            "       ) AS cumulative_abnormal_count\n"
            "FROM lab_results lr\n"
            "JOIN visits v ON lr.visit_id = v.id\n"
            "JOIN patients p ON v.patient_id = p.id\n"
            "ORDER BY p.last_name, lr.tested_at;"
        ),
        "hints": [
            "SUM(is_abnormal) OVER (...) computes a running sum of 0s and 1s.",
            "PARTITION BY patient so the running total resets per patient.",
            "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW is the cumulative frame.",
            "Join lab_results -> visits -> patients to get patient info.",
        ],
        "explanation": (
            "1. JOIN lab_results to visits to patients.\n"
            "2. SUM(is_abnormal) as a window function with cumulative frame.\n"
            "3. PARTITION BY p.id resets the running total per patient.\n"
            "4. ORDER BY tested_at within the window ensures chronological accumulation."
        ),
        "approach": [
            "Join the three tables.",
            "Use SUM window function with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
            "Partition by patient and order by test date.",
        ],
        "common_mistakes": [
            "Omitting the frame clause, which may default to RANGE instead of ROWS.",
            "Forgetting PARTITION BY, computing a global running total.",
        ],
    },
    {
        "id": "interview-hc-028",
        "slug": "int-hc-cohort-first-visit-retention",
        "title": "Patient Cohort Retention Analysis",
        "difficulty": "hard",
        "category": "CTE",
        "dataset": "healthcare",
        "description": (
            "Perform a cohort retention analysis. Group patients by the "
            "month of their first visit (cohort_month). For each cohort, "
            "count the total patients and how many returned for a second "
            "visit within 90 days. Return cohort_month, cohort_size, "
            "returned_within_90_days, and retention_rate (percentage, "
            "rounded to 1 decimal). Sort by cohort_month."
        ),
        "schema_hint": ["visits"],
        "concept_tags": ["CTE", "GROUP BY", "JULIANDAY", "cohort analysis", "ROUND"],
        "solution_query": (
            "WITH first_visits AS (\n"
            "    SELECT patient_id,\n"
            "           MIN(visit_date) AS first_visit_date,\n"
            "           STRFTIME('%Y-%m', MIN(visit_date)) AS cohort_month\n"
            "    FROM visits\n"
            "    GROUP BY patient_id\n"
            "),\n"
            "return_visits AS (\n"
            "    SELECT fv.patient_id,\n"
            "           fv.cohort_month,\n"
            "           MIN(v.visit_date) AS second_visit_date\n"
            "    FROM first_visits fv\n"
            "    JOIN visits v ON v.patient_id = fv.patient_id\n"
            "      AND v.visit_date > fv.first_visit_date\n"
            "      AND JULIANDAY(v.visit_date) - JULIANDAY(fv.first_visit_date) <= 90\n"
            "    GROUP BY fv.patient_id, fv.cohort_month\n"
            ")\n"
            "SELECT fv.cohort_month,\n"
            "       COUNT(DISTINCT fv.patient_id) AS cohort_size,\n"
            "       COUNT(DISTINCT rv.patient_id) AS returned_within_90_days,\n"
            "       ROUND(100.0 * COUNT(DISTINCT rv.patient_id) / COUNT(DISTINCT fv.patient_id), 1) AS retention_rate\n"
            "FROM first_visits fv\n"
            "LEFT JOIN return_visits rv ON fv.patient_id = rv.patient_id\n"
            "GROUP BY fv.cohort_month\n"
            "ORDER BY fv.cohort_month;"
        ),
        "hints": [
            "CTE 1: find each patient's first visit date and cohort month.",
            "CTE 2: find patients who returned within 90 days of their first visit.",
            "LEFT JOIN CTE 2 to CTE 1 to include non-returners.",
            "JULIANDAY difference checks the 90-day window.",
        ],
        "explanation": (
            "1. first_visits CTE finds each patient's earliest visit and assigns a cohort.\n"
            "2. return_visits CTE finds patients who had another visit within 90 days.\n"
            "3. LEFT JOIN ensures patients who did not return are still counted in cohort_size.\n"
            "4. COUNT(DISTINCT) on each CTE's patient_id gives cohort and retention counts.\n"
            "5. Division gives the retention rate."
        ),
        "approach": [
            "Identify cohorts by first visit month.",
            "Find return visits within 90 days.",
            "LEFT JOIN and aggregate for retention rate.",
        ],
        "common_mistakes": [
            "Not excluding the first visit itself when looking for return visits.",
            "Using INNER JOIN which drops cohorts with zero retention.",
            "Counting all subsequent visits instead of unique patients.",
        ],
    },
    {
        "id": "interview-hc-029",
        "slug": "int-hc-doctor-revenue-vs-salary-ratio",
        "title": "Doctor Revenue-to-Salary Efficiency Ratio",
        "difficulty": "hard",
        "category": "CTE",
        "dataset": "healthcare",
        "description": (
            "Calculate each doctor's revenue-to-salary ratio to measure "
            "financial efficiency. Using a CTE, compute total revenue "
            "generated (sum of billing amounts for their visits), then "
            "divide by salary to get the ratio. Return doctor full name, "
            "department name, salary, total_revenue, revenue_to_salary_ratio "
            "(rounded to 2 decimals), and DENSE_RANK by ratio descending "
            "across the entire hospital. Sort by rank."
        ),
        "schema_hint": ["doctors", "departments", "visits", "billing"],
        "concept_tags": ["CTE", "JOIN", "DENSE_RANK", "window functions", "ROUND"],
        "solution_query": (
            "WITH doctor_revenue AS (\n"
            "    SELECT d.id AS doctor_id,\n"
            "           d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "           dep.name AS department_name,\n"
            "           d.salary,\n"
            "           COALESCE(SUM(b.amount), 0) AS total_revenue\n"
            "    FROM doctors d\n"
            "    JOIN departments dep ON d.department_id = dep.id\n"
            "    LEFT JOIN visits v ON v.doctor_id = d.id\n"
            "    LEFT JOIN billing b ON b.visit_id = v.id\n"
            "    GROUP BY d.id, d.first_name, d.last_name, dep.name, d.salary\n"
            ")\n"
            "SELECT doctor_name,\n"
            "       department_name,\n"
            "       salary,\n"
            "       total_revenue,\n"
            "       ROUND(total_revenue / salary, 2) AS revenue_to_salary_ratio,\n"
            "       DENSE_RANK() OVER (ORDER BY total_revenue / salary DESC) AS efficiency_rank\n"
            "FROM doctor_revenue\n"
            "ORDER BY efficiency_rank;"
        ),
        "hints": [
            "Use a CTE to compute total revenue per doctor.",
            "LEFT JOIN visits and billing to include doctors with zero revenue.",
            "Divide revenue by salary for the ratio.",
            "DENSE_RANK() OVER (ORDER BY ratio DESC) ranks all doctors.",
        ],
        "explanation": (
            "1. CTE joins doctors to departments, visits, and billing.\n"
            "2. LEFT JOINs ensure doctors without visits still appear.\n"
            "3. SUM(b.amount) gives total revenue per doctor.\n"
            "4. Outer query divides revenue by salary for the ratio.\n"
            "5. DENSE_RANK ranks all doctors by ratio descending."
        ),
        "approach": [
            "Build a CTE aggregating revenue per doctor.",
            "Compute ratio and rank in the outer query.",
            "Use DENSE_RANK for ranking with ties.",
        ],
        "common_mistakes": [
            "Integer division when salary is stored as REAL (not an issue here but common concern).",
            "Using INNER JOIN and dropping doctors with no billing.",
            "Confusing DENSE_RANK with ROW_NUMBER when ties exist.",
        ],
    },
    {
        "id": "interview-hc-030",
        "slug": "int-hc-comprehensive-hospital-kpi",
        "title": "Hospital KPI Dashboard with Multiple CTEs",
        "difficulty": "hard",
        "category": "CTE",
        "dataset": "healthcare",
        "description": (
            "Build a hospital-wide KPI report by department. For each "
            "department, compute: total doctors, total visits, total revenue, "
            "average bill per visit (rounded to 2 decimals), no-show rate "
            "(percentage of visits with status 'no_show', rounded to 1 "
            "decimal), and the name of the doctor with the most visits in "
            "that department. Return all metrics in a single result set "
            "sorted by total revenue descending."
        ),
        "schema_hint": ["departments", "doctors", "visits", "billing"],
        "concept_tags": ["CTE", "JOIN", "window functions", "ROW_NUMBER", "CASE", "ROUND"],
        "solution_query": (
            "WITH dept_doctors AS (\n"
            "    SELECT department_id, COUNT(*) AS total_doctors\n"
            "    FROM doctors\n"
            "    GROUP BY department_id\n"
            "),\n"
            "dept_visits AS (\n"
            "    SELECT d.department_id,\n"
            "           COUNT(*) AS total_visits,\n"
            "           ROUND(100.0 * SUM(CASE WHEN v.status = 'no_show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate\n"
            "    FROM doctors d\n"
            "    JOIN visits v ON v.doctor_id = d.id\n"
            "    GROUP BY d.department_id\n"
            "),\n"
            "dept_revenue AS (\n"
            "    SELECT d.department_id,\n"
            "           SUM(b.amount) AS total_revenue,\n"
            "           ROUND(AVG(b.amount), 2) AS avg_bill\n"
            "    FROM doctors d\n"
            "    JOIN visits v ON v.doctor_id = d.id\n"
            "    JOIN billing b ON b.visit_id = v.id\n"
            "    GROUP BY d.department_id\n"
            "),\n"
            "top_doctor AS (\n"
            "    SELECT department_id, doctor_name\n"
            "    FROM (\n"
            "        SELECT d.department_id,\n"
            "               d.first_name || ' ' || d.last_name AS doctor_name,\n"
            "               COUNT(v.id) AS visit_count,\n"
            "               ROW_NUMBER() OVER (PARTITION BY d.department_id ORDER BY COUNT(v.id) DESC) AS rn\n"
            "        FROM doctors d\n"
            "        JOIN visits v ON v.doctor_id = d.id\n"
            "        GROUP BY d.department_id, d.id, d.first_name, d.last_name\n"
            "    )\n"
            "    WHERE rn = 1\n"
            ")\n"
            "SELECT dep.name AS department_name,\n"
            "       COALESCE(dd.total_doctors, 0) AS total_doctors,\n"
            "       COALESCE(dv.total_visits, 0) AS total_visits,\n"
            "       COALESCE(dr.total_revenue, 0) AS total_revenue,\n"
            "       dr.avg_bill,\n"
            "       dv.no_show_rate,\n"
            "       td.doctor_name AS busiest_doctor\n"
            "FROM departments dep\n"
            "LEFT JOIN dept_doctors dd ON dep.id = dd.department_id\n"
            "LEFT JOIN dept_visits dv ON dep.id = dv.department_id\n"
            "LEFT JOIN dept_revenue dr ON dep.id = dr.department_id\n"
            "LEFT JOIN top_doctor td ON dep.id = td.department_id\n"
            "ORDER BY COALESCE(dr.total_revenue, 0) DESC;"
        ),
        "hints": [
            "Use four CTEs: doctor counts, visit stats, revenue stats, and top doctor.",
            "For top doctor, use ROW_NUMBER() OVER (PARTITION BY department ORDER BY visits DESC).",
            "LEFT JOIN all CTEs to departments.",
            "CASE WHEN v.status = 'no_show' computes the no-show rate.",
        ],
        "explanation": (
            "1. dept_doctors CTE counts doctors per department.\n"
            "2. dept_visits CTE counts visits and calculates no-show rate.\n"
            "3. dept_revenue CTE sums billing and averages per visit.\n"
            "4. top_doctor CTE uses ROW_NUMBER to find the busiest doctor per department.\n"
            "5. Final query LEFT JOINs all CTEs to departments for a complete dashboard."
        ),
        "approach": [
            "Decompose the problem into separate CTEs for each metric.",
            "Use ROW_NUMBER for finding the top doctor per department.",
            "LEFT JOIN everything to departments as the anchor table.",
            "Sort by total revenue descending.",
        ],
        "common_mistakes": [
            "Trying to compute all metrics in a single query without CTEs, causing cross-joins.",
            "Using INNER JOINs and losing departments with no visits.",
            "Forgetting COALESCE for departments with no data in a CTE.",
            "Not partitioning ROW_NUMBER by department.",
        ],
    },
]
