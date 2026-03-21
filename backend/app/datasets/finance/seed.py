"""
Finance Dataset Seed Script
Generates ~4000 rows across 7 tables with realistic data.
Uses random with seed(42) for reproducible output. Includes intentional
data quality issues:
  - ~5% NULLs in phone fields
  - ~15 duplicate customer emails for debugging
  - Some transactions with incorrect balance_after values
  - Date gaps in transaction history (missing days)
"""

import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Deterministic seeds
# ---------------------------------------------------------------------------
_RNG = random.Random(42)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen",
    "Charles", "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony",
    "Margaret", "Mark", "Sandra", "Donald", "Ashley", "Steven", "Dorothy",
    "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna", "Kenneth",
    "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca",
    "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob",
    "Kathleen", "Gary", "Amy", "Nicholas", "Angela", "Eric", "Shirley",
    "Jonathan", "Anna", "Stephen", "Brenda", "Larry", "Pamela", "Justin",
    "Emma", "Scott", "Nicole", "Brandon", "Helen", "Benjamin", "Samantha",
    "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Carolyn", "Patrick", "Janet", "Jack",
    "Catherine", "Dennis", "Maria", "Jerry", "Heather",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Turner", "Phillips", "Evans", "Collins",
    "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan", "Peterson",
    "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard",
    "Ward", "Cox", "Diaz", "Richardson", "Wood", "Watson", "Brooks",
    "Bennett", "Gray", "James", "Reyes", "Cruz", "Hughes", "Price",
    "Myers", "Long", "Foster", "Sanders", "Ross", "Morales", "Powell",
    "Sullivan", "Russell", "Ortiz", "Jenkins", "Gutierrez", "Perry",
    "Butler", "Barnes", "Fisher", "Henderson", "Coleman",
]

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"),
    ("Indianapolis", "IN"), ("San Francisco", "CA"), ("Seattle", "WA"),
    ("Denver", "CO"), ("Nashville", "TN"), ("Oklahoma City", "OK"),
    ("El Paso", "TX"), ("Washington", "DC"), ("Boston", "MA"),
    ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"),
    ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"),
    ("Albuquerque", "NM"), ("Tucson", "AZ"), ("Fresno", "CA"),
    ("Mesa", "AZ"), ("Sacramento", "CA"), ("Atlanta", "GA"),
    ("Kansas City", "MO"), ("Omaha", "NE"), ("Miami", "FL"),
    ("Tampa", "FL"),
]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]

BRANCH_DATA = [
    (1, "Main Street Branch", "New York", "NY", "Robert Chen", "2018-03-15"),
    (2, "Downtown Financial Center", "Chicago", "IL", "Sarah Mitchell", "2019-06-01"),
    (3, "Westside Branch", "Los Angeles", "CA", "Michael Torres", "2019-09-20"),
    (4, "Harbor View Branch", "San Francisco", "CA", "Jennifer Walsh", "2020-01-10"),
    (5, "Lakefront Office", "Seattle", "WA", "David Kumar", "2020-05-22"),
    (6, "Sunbelt Branch", "Phoenix", "AZ", "Amanda Rodriguez", "2020-08-14"),
    (7, "Capital District Branch", "Washington", "DC", "Thomas Jefferson", "2021-02-01"),
    (8, "Lone Star Branch", "Houston", "TX", "Patricia Gonzalez", "2021-07-19"),
    (9, "Gateway Branch", "Denver", "CO", "Christopher Lee", "2022-01-05"),
    (10, "Peachtree Branch", "Atlanta", "GA", "Lisa Franklin", "2022-06-30"),
]

ACCOUNT_TYPES = ["checking", "savings", "investment", "credit"]
ACCOUNT_STATUSES = ["active"] * 7 + ["closed", "frozen"]

TX_TYPES = ["deposit", "withdrawal", "transfer", "fee", "interest"]
TX_DESCRIPTIONS = {
    "deposit": [
        "Direct deposit - Payroll", "ATM deposit", "Mobile check deposit",
        "Wire transfer in", "Cash deposit",
    ],
    "withdrawal": [
        "ATM withdrawal", "Debit purchase", "Wire transfer out",
        "Check payment", "Online bill pay",
    ],
    "transfer": [
        "Transfer to savings", "Transfer from checking", "Internal transfer",
        "Zelle transfer", "Account transfer",
    ],
    "fee": [
        "Monthly maintenance fee", "Overdraft fee", "Wire transfer fee",
        "ATM fee", "Late payment fee",
    ],
    "interest": [
        "Monthly interest", "Savings interest", "Investment dividend",
        "Interest payment", "Quarterly interest",
    ],
}

CARD_STATUSES = ["active"] * 4 + ["blocked", "expired"]
LOAN_TYPES = ["personal", "mortgage", "auto", "business"]
LOAN_STATUSES = ["active"] * 3 + ["paid", "defaulted"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sq(s: str) -> str:
    """SQL-escape single quotes."""
    return s.replace("'", "''")


def _rand_date(start: str, end: str) -> str:
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    delta = (e - s).days
    return (s + timedelta(days=_RNG.randint(0, max(delta, 1)))).strftime("%Y-%m-%d")


def _rand_datetime(start: str, end: str) -> str:
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    delta = int((e - s).total_seconds())
    return (s + timedelta(seconds=_RNG.randint(0, max(delta, 1)))).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_seed_sql() -> str:  # noqa: C901 — long but straightforward
    lines: list[str] = [
        "-- Finance Dataset Seed Data",
        "-- ~4000 rows across 7 tables with intentional data quality issues",
        "",
    ]

    # Reset RNG each call for reproducibility
    rng = random.Random(42)

    # ---- BRANCHES (10) ----
    lines.append("-- Branches")
    for b in BRANCH_DATA:
        lines.append(
            f"INSERT INTO branches VALUES ({b[0]}, '{_sq(b[1])}', "
            f"'{_sq(b[2])}', '{_sq(b[3])}', '{_sq(b[4])}', '{b[5]}');"
        )
    lines.append("")

    # ---- CUSTOMERS (400) ----
    lines.append("-- Customers")
    used_emails: list[str] = []
    dup_indices = set(rng.sample(range(20, 400), 15))

    for i in range(1, 401):
        fn = rng.choice(FIRST_NAMES)
        ln = rng.choice(LAST_NAMES)

        if i in dup_indices and len(used_emails) >= 20:
            email = rng.choice(used_emails[:20])
        else:
            domain = rng.choice(EMAIL_DOMAINS)
            email = f"{fn.lower()}.{ln.lower()}{rng.randint(1, 999)}@{domain}"
        used_emails.append(email)

        # ~5% NULL phones
        if rng.random() < 0.05:
            phone = "NULL"
        else:
            phone = (
                f"'+1-{rng.randint(200,999)}-{rng.randint(100,999)}"
                f"-{rng.randint(1000,9999)}'"
            )

        # inline date generation for dob
        s = datetime(1955, 1, 1)
        e = datetime(2000, 12, 31)
        dob = (s + timedelta(days=rng.randint(0, (e - s).days))).strftime("%Y-%m-%d")

        city, state = rng.choice(CITIES_STATES)

        s2 = datetime(2022, 1, 1)
        e2 = datetime(2024, 12, 31)
        created = (
            s2 + timedelta(seconds=rng.randint(0, int((e2 - s2).total_seconds())))
        ).strftime("%Y-%m-%d %H:%M:%S")

        lines.append(
            f"INSERT INTO customers VALUES ({i}, '{_sq(fn)}', '{_sq(ln)}', "
            f"'{_sq(email)}', {phone}, '{dob}', '{_sq(city)}', '{state}', "
            f"'US', '{created}');"
        )
    lines.append("")

    # ---- ACCOUNTS (600) ----
    lines.append("-- Accounts")
    accounts: list[tuple] = []

    for i in range(1, 601):
        cust_id = rng.randint(1, 400)
        atype = rng.choice(ACCOUNT_TYPES)

        if atype == "checking":
            balance = round(rng.uniform(100, 25000), 2)
        elif atype == "savings":
            balance = round(rng.uniform(500, 100000), 2)
        elif atype == "investment":
            balance = round(rng.uniform(1000, 500000), 2)
        else:
            balance = round(rng.uniform(-5000, 0), 2)

        opened = (
            datetime(2022, 1, 1)
            + timedelta(days=rng.randint(0, (datetime(2025, 6, 30) - datetime(2022, 1, 1)).days))
        ).strftime("%Y-%m-%d")
        status = rng.choice(ACCOUNT_STATUSES)

        accounts.append((i, cust_id, atype, balance, status))
        lines.append(
            f"INSERT INTO accounts VALUES ({i}, {cust_id}, '{atype}', "
            f"{balance}, 'USD', '{opened}', '{status}');"
        )
    lines.append("")

    # ---- TRANSACTIONS (2000) ----
    lines.append("-- Transactions")

    # Build date list with gaps
    all_dates = []
    cur = datetime(2022, 1, 1)
    end_dt = datetime(2025, 9, 30)
    while cur <= end_dt:
        all_dates.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)
    gap_indices = sorted(rng.sample(range(len(all_dates)), 60))
    gap_dates = {all_dates[gi] for gi in gap_indices}
    available_dates = [d for d in all_dates if d not in gap_dates]

    for i in range(1, 2001):
        acc_id = rng.randint(1, 600)
        tx_date = rng.choice(available_dates)
        ttype = rng.choice(TX_TYPES)

        if ttype == "deposit":
            amount = round(rng.uniform(50, 10000), 2)
        elif ttype == "withdrawal":
            amount = round(rng.uniform(10, 5000), 2)
        elif ttype == "transfer":
            amount = round(rng.uniform(25, 8000), 2)
        elif ttype == "fee":
            amount = round(rng.uniform(5, 75), 2)
        else:
            amount = round(rng.uniform(0.5, 500), 2)

        base_balance = accounts[acc_id - 1][3]
        if ttype in ("deposit", "interest"):
            balance_after = round(base_balance + amount, 2)
        else:
            balance_after = round(base_balance - amount, 2)

        # ~3% intentionally wrong balance_after
        if rng.random() < 0.03:
            balance_after = round(balance_after + rng.uniform(-500, 500), 2)

        desc = rng.choice(TX_DESCRIPTIONS[ttype])
        ref = f"TXN{i:07d}{rng.randint(100, 999)}"

        lines.append(
            f"INSERT INTO transactions VALUES ({i}, {acc_id}, '{tx_date}', "
            f"'{ttype}', {amount}, {balance_after}, '{_sq(desc)}', '{ref}');"
        )
    lines.append("")

    # ---- CARDS (300) ----
    lines.append("-- Cards")

    for i in range(1, 301):
        acc_id = rng.randint(1, 600)
        card_num = (
            f"{rng.randint(4000,5999)}-{rng.randint(1000,9999)}-"
            f"{rng.randint(1000,9999)}-{rng.randint(1000,9999)}"
        )
        ctype = rng.choice(["debit", "credit"])

        exp_year = rng.randint(2024, 2028)
        exp_month = rng.randint(1, 12)
        expiry = f"{exp_year}-{exp_month:02d}"

        status = rng.choice(CARD_STATUSES)
        if exp_year < 2025 or (exp_year == 2025 and exp_month < 6):
            if rng.random() < 0.5:
                status = "expired"

        if ctype == "credit":
            credit_limit = rng.choice([2000, 5000, 7500, 10000, 15000, 25000, 50000])
            cl_str = str(float(credit_limit))
        else:
            cl_str = "NULL"

        issued = (
            datetime(2022, 1, 1)
            + timedelta(days=rng.randint(0, (datetime(2025, 3, 31) - datetime(2022, 1, 1)).days))
        ).strftime("%Y-%m-%d")

        lines.append(
            f"INSERT INTO cards VALUES ({i}, {acc_id}, '{card_num}', "
            f"'{ctype}', '{expiry}', '{status}', {cl_str}, '{issued}');"
        )
    lines.append("")

    # ---- LOANS (200) ----
    lines.append("-- Loans")
    loans: list[tuple] = []

    for i in range(1, 201):
        cust_id = rng.randint(1, 400)
        ltype = rng.choice(LOAN_TYPES)

        if ltype == "personal":
            principal = round(rng.uniform(1000, 50000), 2)
            rate = round(rng.uniform(5.0, 18.0), 2)
            term = rng.choice([12, 24, 36, 48, 60])
        elif ltype == "mortgage":
            principal = round(rng.uniform(100000, 750000), 2)
            rate = round(rng.uniform(3.0, 7.5), 2)
            term = rng.choice([180, 240, 360])
        elif ltype == "auto":
            principal = round(rng.uniform(5000, 65000), 2)
            rate = round(rng.uniform(3.5, 12.0), 2)
            term = rng.choice([24, 36, 48, 60, 72])
        else:
            principal = round(rng.uniform(10000, 500000), 2)
            rate = round(rng.uniform(4.0, 15.0), 2)
            term = rng.choice([12, 24, 36, 60, 84, 120])

        start = (
            datetime(2022, 1, 1)
            + timedelta(days=rng.randint(0, (datetime(2025, 1, 31) - datetime(2022, 1, 1)).days))
        ).strftime("%Y-%m-%d")
        status = rng.choice(LOAN_STATUSES)

        loans.append((i, cust_id, ltype, principal, rate, term, start, status))
        lines.append(
            f"INSERT INTO loans VALUES ({i}, {cust_id}, '{ltype}', "
            f"{principal}, {rate}, {term}, '{start}', '{status}');"
        )
    lines.append("")

    # ---- PAYMENTS (400) ----
    lines.append("-- Loan Payments")

    for i in range(1, 401):
        loan = loans[rng.randint(0, len(loans) - 1)]
        loan_id = loan[0]
        principal_orig = loan[3]

        pay_date = (
            datetime(2022, 3, 1)
            + timedelta(days=rng.randint(0, (datetime(2025, 9, 30) - datetime(2022, 3, 1)).days))
        ).strftime("%Y-%m-%d")

        payment_amount = round(rng.uniform(200, 5000), 2)
        interest_paid = round(payment_amount * rng.uniform(0.1, 0.5), 2)
        principal_paid = round(payment_amount - interest_paid, 2)
        remaining = round(principal_orig - principal_paid * rng.randint(1, 10), 2)
        if remaining < 0:
            remaining = 0.0

        lines.append(
            f"INSERT INTO payments VALUES ({i}, {loan_id}, '{pay_date}', "
            f"{payment_amount}, {principal_paid}, {interest_paid}, {remaining});"
        )
    lines.append("")

    return "\n".join(lines)
