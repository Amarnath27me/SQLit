"""
E-Commerce Dataset Seed Script
Generates ~4500 rows across 8 tables with realistic data using Faker.
Includes intentional NULLs, duplicate emails, mismatched totals, and date gaps
for the Data Debugging mode.
"""

import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CATEGORY_DATA = [
    ("Smartphones", "Mobile phones and accessories"),
    ("Laptops & Computers", "Notebooks, desktops, and peripherals"),
    ("Audio & Headphones", "Speakers, headphones, and audio equipment"),
    ("Televisions", "Smart TVs and home theater displays"),
    ("Cameras", "Digital cameras, lenses, and accessories"),
    ("Men's Clothing", "Shirts, pants, jackets, and menswear"),
    ("Women's Clothing", "Dresses, tops, skirts, and womenswear"),
    ("Footwear", "Shoes, sneakers, boots, and sandals"),
    ("Kitchen Appliances", "Blenders, mixers, coffee makers, and cookware"),
    ("Home Furniture", "Tables, chairs, shelves, and decor"),
    ("Bedding & Bath", "Sheets, towels, pillows, and bathroom essentials"),
    ("Fitness & Sports", "Exercise equipment and activewear"),
    ("Books", "Fiction, non-fiction, and educational books"),
    ("Toys & Games", "Board games, puzzles, and children's toys"),
    ("Beauty & Personal Care", "Skincare, haircare, and grooming products"),
]

PRODUCT_TEMPLATES = {
    "Smartphones": [
        ("Galaxy Pro Max 15", 999.99, 650.00),
        ("iPhone Ultra 16", 1199.99, 780.00),
        ("Pixel 9 Pro", 899.99, 580.00),
        ("OnePlus Nord CE 5", 349.99, 210.00),
        ("Xiaomi Redmi Note 14", 249.99, 150.00),
        ("Samsung Galaxy A55", 449.99, 270.00),
        ("Motorola Edge 50", 599.99, 380.00),
        ("Sony Xperia 5 VI", 949.99, 620.00),
        ("Phone Case - Universal Silicone", 14.99, 3.50),
        ("Tempered Glass Screen Protector", 9.99, 1.80),
        ("Wireless Charging Pad", 29.99, 12.00),
        ("USB-C Fast Charger 65W", 24.99, 8.50),
        ("Car Phone Mount", 19.99, 5.00),
    ],
    "Laptops & Computers": [
        ("MacBook Air M4 13-inch", 1299.99, 890.00),
        ("Dell XPS 15", 1499.99, 980.00),
        ("ThinkPad X1 Carbon Gen 12", 1649.99, 1050.00),
        ("HP Spectre x360 16", 1399.99, 900.00),
        ("ASUS ROG Strix G16 Gaming", 1799.99, 1200.00),
        ("Acer Chromebook Spin 714", 599.99, 350.00),
        ("Wireless Mouse - Ergonomic", 39.99, 14.00),
        ("Mechanical Keyboard RGB", 89.99, 35.00),
        ("USB-C Hub 7-in-1", 49.99, 18.00),
        ("Laptop Stand Adjustable", 34.99, 12.00),
        ("27-inch 4K Monitor", 449.99, 280.00),
        ("External SSD 1TB", 89.99, 45.00),
        ("Webcam 1080p HD", 59.99, 22.00),
    ],
    "Audio & Headphones": [
        ("AirPods Pro 3", 249.99, 140.00),
        ("Sony WH-1000XM6", 349.99, 200.00),
        ("Bose QuietComfort Ultra", 379.99, 220.00),
        ("JBL Flip 7 Bluetooth Speaker", 129.99, 65.00),
        ("Samsung Galaxy Buds3 Pro", 229.99, 120.00),
        ("Sennheiser HD 660S2", 499.99, 300.00),
        ("Soundbar 2.1 Channel", 199.99, 95.00),
        ("Portable DAC Amplifier", 149.99, 70.00),
        ("Audio Technica AT2020 Mic", 99.99, 48.00),
        ("Earbuds - Budget Wired", 12.99, 3.00),
    ],
    "Televisions": [
        ("Samsung 65-inch OLED 4K", 1799.99, 1100.00),
        ("LG 55-inch QNED Smart TV", 799.99, 480.00),
        ("Sony Bravia 75-inch", 2499.99, 1600.00),
        ("TCL 50-inch 4K Roku TV", 329.99, 190.00),
        ("Hisense 43-inch Smart TV", 249.99, 140.00),
        ("Fire TV Stick 4K Max", 54.99, 25.00),
        ("Universal TV Wall Mount", 39.99, 14.00),
        ("HDMI Cable 6ft Premium", 12.99, 3.00),
    ],
    "Cameras": [
        ("Canon EOS R6 Mark III", 2499.99, 1650.00),
        ("Sony A7 IV Mirrorless", 2199.99, 1400.00),
        ("Nikon Z8", 3499.99, 2300.00),
        ("GoPro Hero 13 Black", 399.99, 240.00),
        ("DJI Mini 4 Pro Drone", 759.99, 480.00),
        ("Camera Tripod Professional", 79.99, 30.00),
        ("SD Card 256GB UHS-II", 44.99, 18.00),
        ("Camera Backpack Large", 69.99, 25.00),
    ],
    "Men's Clothing": [
        ("Classic Oxford Button-Down Shirt", 59.99, 18.00),
        ("Slim Fit Chino Pants", 49.99, 15.00),
        ("Wool Blend Blazer", 149.99, 55.00),
        ("Casual Crew Neck T-Shirt", 19.99, 5.00),
        ("Denim Jacket Vintage Wash", 79.99, 28.00),
        ("Fleece Pullover Hoodie", 44.99, 14.00),
        ("Lightweight Down Vest", 89.99, 32.00),
        ("Linen Summer Shorts", 34.99, 10.00),
    ],
    "Women's Clothing": [
        ("Floral Wrap Midi Dress", 69.99, 22.00),
        ("High-Waist Yoga Leggings", 39.99, 11.00),
        ("Cashmere V-Neck Sweater", 129.99, 48.00),
        ("Silk Blouse Classic Fit", 89.99, 30.00),
        ("Relaxed Fit Wide-Leg Jeans", 59.99, 18.00),
        ("Puffer Jacket Cropped", 99.99, 35.00),
        ("Cotton Tank Top 3-Pack", 24.99, 7.00),
        ("Pleated Midi Skirt", 54.99, 17.00),
    ],
    "Footwear": [
        ("Nike Air Max 90", 129.99, 55.00),
        ("Adidas Ultraboost Light", 189.99, 80.00),
        ("New Balance 990v6", 199.99, 90.00),
        ("Leather Chelsea Boots", 149.99, 60.00),
        ("Canvas Slip-On Sneakers", 49.99, 15.00),
        ("Running Shoes Lightweight", 89.99, 35.00),
        ("Hiking Boots Waterproof", 139.99, 55.00),
        ("Sandals Comfort Slide", 34.99, 10.00),
    ],
    "Kitchen Appliances": [
        ("Instant Pot Duo 8-Quart", 89.99, 40.00),
        ("KitchenAid Stand Mixer", 349.99, 200.00),
        ("Ninja Blender Pro 1200W", 79.99, 35.00),
        ("Breville Barista Express", 699.99, 420.00),
        ("Air Fryer XL 5.8 Quart", 69.99, 28.00),
        ("Toaster Oven Convection", 59.99, 24.00),
        ("Cast Iron Skillet 12-inch", 39.99, 15.00),
        ("Chef Knife Set 8-Piece", 129.99, 50.00),
        ("Non-Stick Cookware Set 10pc", 149.99, 60.00),
    ],
    "Home Furniture": [
        ("Ergonomic Office Chair", 299.99, 140.00),
        ("Standing Desk Electric 60-inch", 499.99, 250.00),
        ("Bookshelf 5-Tier Walnut", 179.99, 70.00),
        ("Coffee Table Modern Glass", 249.99, 100.00),
        ("Dining Table Set 4-Seater", 599.99, 280.00),
        ("Floating Wall Shelves Set of 3", 49.99, 16.00),
        ("Floor Lamp Arc Modern", 129.99, 48.00),
        ("Area Rug 8x10 Abstract", 199.99, 75.00),
    ],
    "Bedding & Bath": [
        ("Queen Sheet Set 1000TC Egyptian Cotton", 89.99, 30.00),
        ("Memory Foam Pillow 2-Pack", 49.99, 18.00),
        ("Weighted Blanket 15lb", 59.99, 22.00),
        ("Bath Towel Set 6-Piece", 44.99, 14.00),
        ("Down Alternative Comforter", 79.99, 28.00),
        ("Shower Curtain Fabric", 24.99, 7.00),
        ("Mattress Topper Gel Memory Foam", 129.99, 50.00),
    ],
    "Fitness & Sports": [
        ("Adjustable Dumbbell Set 50lb", 299.99, 150.00),
        ("Yoga Mat Premium 6mm", 34.99, 10.00),
        ("Resistance Bands Set of 5", 19.99, 5.00),
        ("Fitness Tracker Band", 49.99, 20.00),
        ("Jump Rope Speed Cable", 14.99, 4.00),
        ("Foam Roller 18-inch", 24.99, 8.00),
        ("Pull-Up Bar Doorway", 29.99, 11.00),
        ("Gym Bag Duffle Large", 39.99, 14.00),
    ],
    "Books": [
        ("The Art of Problem Solving", 24.99, 8.00),
        ("Data Science from Scratch", 39.99, 14.00),
        ("Modern Classic Novel Collection", 49.99, 16.00),
        ("Cookbook: World Flavors", 29.99, 10.00),
        ("Mindfulness and Meditation Guide", 18.99, 6.00),
        ("History of Innovation", 34.99, 12.00),
        ("Children's Illustrated Atlas", 22.99, 8.00),
    ],
    "Toys & Games": [
        ("LEGO Creator Expert Set", 129.99, 65.00),
        ("Board Game Strategy Collection", 44.99, 18.00),
        ("1000-Piece Jigsaw Puzzle", 19.99, 6.00),
        ("Remote Control Car 4WD", 59.99, 24.00),
        ("Building Blocks Mega Set", 34.99, 12.00),
        ("Card Game Party Pack", 14.99, 4.00),
        ("Plush Toy Giant Bear", 29.99, 10.00),
    ],
    "Beauty & Personal Care": [
        ("Vitamin C Serum 30ml", 24.99, 6.00),
        ("Electric Toothbrush Sonic", 49.99, 18.00),
        ("Hair Dryer Professional 1875W", 69.99, 28.00),
        ("Moisturizer SPF 30 Daily", 19.99, 5.00),
        ("Beard Trimmer Cordless", 39.99, 15.00),
        ("Shampoo & Conditioner Set", 29.99, 9.00),
        ("Nail Care Kit 12-Piece", 14.99, 4.00),
        ("Perfume Eau de Toilette 100ml", 79.99, 30.00),
    ],
}

ORDER_STATUSES = ["pending", "shipped", "delivered", "cancelled", "returned"]
ORDER_STATUS_WEIGHTS = [0.10, 0.15, 0.55, 0.12, 0.08]

PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer"]
PAYMENT_METHOD_WEIGHTS = [0.45, 0.25, 0.20, 0.10]

PAYMENT_STATUSES = ["completed", "pending", "failed", "refunded"]
PAYMENT_STATUS_WEIGHTS = [0.75, 0.10, 0.08, 0.07]

SHIPPING_CARRIERS = ["FedEx", "UPS", "USPS", "DHL", "Amazon Logistics"]
SHIPPING_STATUSES = ["processing", "shipped", "in_transit", "delivered", "returned"]
SHIPPING_STATUS_WEIGHTS = [0.08, 0.12, 0.15, 0.58, 0.07]

# Rating distribution skewed toward 4-5
RATING_WEIGHTS = [0.05, 0.08, 0.12, 0.30, 0.45]  # 1-star through 5-star

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]


def _sql_str(val):
    """Escape a value for SQL insertion."""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val).replace("'", "''")
    return f"'{s}'"


def _sql_row(values):
    """Format a row of values for INSERT."""
    return "(" + ", ".join(_sql_str(v) for v in values) + ")"


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_customers(n=500):
    """Generate customer records. ~20 will have intentionally duplicate emails."""
    rows = []
    emails_pool = []

    for i in range(1, n + 1):
        first = fake.first_name()
        last = fake.last_name()
        email = f"{first.lower()}.{last.lower()}@{fake.free_email_domain()}"
        phone = fake.phone_number() if random.random() > 0.05 else None
        city = fake.city()
        state = random.choice(US_STATES)
        country = "US"
        created = fake.date_time_between(
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2025, 12, 31),
        ).strftime("%Y-%m-%d %H:%M:%S")

        rows.append((i, first, last, email, phone, city, state, country, created))
        emails_pool.append(email)

    # Introduce ~20 duplicate emails (overwrite emails for customers 481-500)
    duplicate_sources = random.sample(emails_pool[:460], 20)
    for idx, dup_email in enumerate(duplicate_sources):
        row_idx = 480 + idx  # rows index 480..499 -> customer ids 481..500
        r = list(rows[row_idx])
        r[3] = dup_email
        rows[row_idx] = tuple(r)

    return rows


def generate_categories():
    """Generate category records from the predefined list."""
    rows = []
    for i, (name, desc) in enumerate(CATEGORY_DATA, start=1):
        rows.append((i, name, desc))
    return rows


def generate_products():
    """Generate product records from templates, mapped to categories."""
    rows = []
    pid = 1
    cat_names = [c[0] for c in CATEGORY_DATA]

    for cat_id, cat_name in enumerate(cat_names, start=1):
        templates = PRODUCT_TEMPLATES.get(cat_name, [])
        for name, price, cost in templates:
            stock = random.randint(0, 500)
            created = fake.date_time_between(
                start_date=datetime(2022, 1, 1),
                end_date=datetime(2025, 6, 30),
            ).strftime("%Y-%m-%d %H:%M:%S")
            rows.append((pid, name, cat_id, round(price, 2), round(cost, 2), stock, created))
            pid += 1

    # Pad to ~200 with extra variants
    while len(rows) < 200:
        cat_id = random.randint(1, len(CATEGORY_DATA))
        cat_name = cat_names[cat_id - 1]
        templates = PRODUCT_TEMPLATES.get(cat_name, [])
        if templates:
            base_name, base_price, base_cost = random.choice(templates)
            variant = random.choice(["- Black", "- White", "- Blue", "- Limited Edition", "- Bundle"])
            price = round(base_price * random.uniform(0.85, 1.15), 2)
            cost = round(base_cost * random.uniform(0.90, 1.10), 2)
        else:
            base_name = f"Generic Product {len(rows)}"
            price = round(random.uniform(9.99, 299.99), 2)
            cost = round(price * random.uniform(0.35, 0.65), 2)
            variant = ""

        name = f"{base_name} {variant}".strip()
        stock = random.randint(0, 500)
        created = fake.date_time_between(
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2025, 6, 30),
        ).strftime("%Y-%m-%d %H:%M:%S")
        rows.append((pid, name, cat_id, price, cost, stock, created))
        pid += 1

    return rows


def generate_orders_and_items(n_orders=1000, products=None):
    """
    Generate orders and order_items together so we can create intentional
    mismatches. Returns (order_rows, item_rows).
    """
    order_rows = []
    item_rows = []
    item_id = 1

    product_ids = [p[0] for p in products]
    product_prices = {p[0]: p[3] for p in products}

    # Create date range with intentional gaps
    base_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    # Generate order dates -- skip some days intentionally for gap debugging
    gap_days = set()
    # Create ~15 gap windows of 2-5 days each
    for _ in range(15):
        gap_start = random.randint(30, (end_date - base_date).days - 30)
        gap_len = random.randint(2, 5)
        for d in range(gap_len):
            gap_days.add(gap_start + d)

    # Collect all possible days, remove gap days
    all_days = []
    for day_offset in range((end_date - base_date).days + 1):
        if day_offset not in gap_days:
            all_days.append(base_date + timedelta(days=day_offset))

    # Decide which orders will have mismatched totals (~50 orders)
    mismatch_orders = set(random.sample(range(1, n_orders + 1), min(50, n_orders)))

    for oid in range(1, n_orders + 1):
        customer_id = random.randint(1, 500)
        order_date = random.choice(all_days)
        status = random.choices(ORDER_STATUSES, weights=ORDER_STATUS_WEIGHTS, k=1)[0]

        # Generate 1-5 items for this order
        n_items = random.choices([1, 2, 3, 4, 5], weights=[0.30, 0.35, 0.20, 0.10, 0.05], k=1)[0]
        selected_products = random.sample(product_ids, min(n_items, len(product_ids)))

        real_total = 0.0
        for prod_id in selected_products:
            qty = random.choices([1, 2, 3, 4], weights=[0.50, 0.30, 0.15, 0.05], k=1)[0]
            unit_price = product_prices[prod_id]
            discount = 0.0
            if random.random() < 0.20:
                discount = round(random.choice([0.05, 0.10, 0.15, 0.20, 0.25]) * unit_price, 2)

            line_total = round(qty * unit_price - discount, 2)
            real_total += line_total

            item_rows.append((item_id, oid, prod_id, qty, unit_price, discount))
            item_id += 1

        real_total = round(real_total, 2)

        # Intentional mismatch: adjust total_amount by a random offset
        if oid in mismatch_orders:
            offset = round(random.uniform(-25.0, 50.0), 2)
            if offset == 0:
                offset = 5.99
            total_amount = round(real_total + offset, 2)
        else:
            total_amount = real_total

        order_rows.append((
            oid, customer_id,
            order_date.strftime("%Y-%m-%d"),
            status, total_amount,
        ))

    return order_rows, item_rows


def generate_payments(orders):
    """Generate payments. ~90% of non-cancelled orders get a payment."""
    rows = []
    pid = 1

    for order in orders:
        oid, _, order_date_str, status, total_amount = order

        # Skip some orders (cancelled mostly, but a few others too)
        if status == "cancelled" and random.random() < 0.70:
            continue
        if status != "cancelled" and random.random() < 0.05:
            continue

        order_date = datetime.strptime(order_date_str, "%Y-%m-%d")
        pay_date = order_date + timedelta(days=random.randint(0, 3))

        method = random.choices(PAYMENT_METHODS, weights=PAYMENT_METHOD_WEIGHTS, k=1)[0]
        pay_status = random.choices(PAYMENT_STATUSES, weights=PAYMENT_STATUS_WEIGHTS, k=1)[0]

        # Payment amount usually matches order, sometimes slightly off
        amount = total_amount
        if random.random() < 0.03:
            amount = round(amount + random.uniform(-5.0, 5.0), 2)

        rows.append((pid, oid, pay_date.strftime("%Y-%m-%d"), amount, method, pay_status))
        pid += 1

    return rows


def generate_reviews(products, n=600):
    """Generate product reviews with rating distribution skewed to 4-5."""
    rows = []
    product_ids = [p[0] for p in products]

    for rid in range(1, n + 1):
        prod_id = random.choice(product_ids)
        cust_id = random.randint(1, 500)
        rating = random.choices([1, 2, 3, 4, 5], weights=RATING_WEIGHTS, k=1)[0]

        # ~5% NULL comments
        if random.random() < 0.05:
            comment = None
        else:
            comment = _generate_review_comment(rating)

        review_date = fake.date_time_between(
            start_date=datetime(2023, 3, 1),
            end_date=datetime(2025, 12, 31),
        ).strftime("%Y-%m-%d")

        rows.append((rid, prod_id, cust_id, rating, comment, review_date))

    return rows


def _generate_review_comment(rating):
    """Generate a plausible review comment based on rating."""
    positive = [
        "Excellent product, highly recommend!",
        "Great quality for the price.",
        "Exactly what I was looking for.",
        "Very happy with this purchase.",
        "Works perfectly, fast shipping too.",
        "Love it! Will buy again.",
        "Superb craftsmanship and design.",
        "Exceeded my expectations.",
        "Best purchase I have made this year.",
        "Five stars, absolutely worth it.",
    ]
    neutral = [
        "Decent product, nothing special.",
        "It is okay for the price.",
        "Average quality, does the job.",
        "Not bad, but could be better.",
        "Meets expectations, no more no less.",
        "Functional but unimpressive.",
        "Would consider alternatives next time.",
    ]
    negative = [
        "Disappointing quality, would not recommend.",
        "Broke after a week of use.",
        "Not worth the money.",
        "Poor packaging, arrived damaged.",
        "Does not match the description at all.",
        "Very flimsy material.",
        "Returned it immediately.",
    ]

    if rating >= 4:
        return random.choice(positive)
    elif rating == 3:
        return random.choice(neutral)
    else:
        return random.choice(negative)


def generate_shipping(orders, n_target=800):
    """Generate shipping records for a subset of orders."""
    rows = []
    sid = 1

    # Pick orders that are not 'pending' or 'cancelled' mostly
    eligible = [
        o for o in orders
        if o[3] in ("shipped", "delivered", "returned")
    ]
    # Also include some pending ones (processing state)
    pending_orders = [o for o in orders if o[3] == "pending"]
    eligible += random.sample(pending_orders, min(len(pending_orders), 50))

    random.shuffle(eligible)
    selected = eligible[:n_target]

    for order in selected:
        oid, _, order_date_str, order_status, _ = order
        order_date = datetime.strptime(order_date_str, "%Y-%m-%d")

        ship_date = order_date + timedelta(days=random.randint(0, 5))
        carrier = random.choice(SHIPPING_CARRIERS)
        tracking = fake.bothify(text="??########??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        ship_status = random.choices(SHIPPING_STATUSES, weights=SHIPPING_STATUS_WEIGHTS, k=1)[0]

        # delivery_date: NULL ~5% of the time, or if not yet delivered
        if ship_status in ("processing", "shipped", "in_transit") or random.random() < 0.05:
            delivery_date = None
        else:
            delivery_date = (ship_date + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")

        rows.append((
            sid, oid, ship_date.strftime("%Y-%m-%d"),
            delivery_date, carrier, tracking, ship_status,
        ))
        sid += 1

    return rows


# ---------------------------------------------------------------------------
# SQL generation
# ---------------------------------------------------------------------------

def _build_insert(table, columns, rows):
    """Build INSERT statements in batches of 50 rows."""
    if not rows:
        return ""

    col_list = ", ".join(columns)
    statements = []

    for i in range(0, len(rows), 50):
        batch = rows[i:i + 50]
        values = ",\n  ".join(_sql_row(r) for r in batch)
        statements.append(f"INSERT INTO {table} ({col_list}) VALUES\n  {values};")

    return "\n".join(statements)


def generate_seed_sql():
    """Generate the complete seed SQL string."""
    lines = [
        "-- E-Commerce Dataset Seed Data",
        "-- Generated with Faker (seed=42)",
        f"-- ~4500 total rows across 8 tables",
        "",
    ]

    # Categories
    categories = generate_categories()
    lines.append("-- Categories (~15 rows)")
    lines.append(_build_insert(
        "categories", ["id", "name", "description"], categories
    ))
    lines.append("")

    # Products
    products = generate_products()
    lines.append(f"-- Products (~{len(products)} rows)")
    lines.append(_build_insert(
        "products",
        ["id", "name", "category_id", "price", "cost", "stock_quantity", "created_at"],
        products,
    ))
    lines.append("")

    # Customers
    customers = generate_customers(500)
    lines.append(f"-- Customers (~{len(customers)} rows)")
    lines.append(_build_insert(
        "customers",
        ["id", "first_name", "last_name", "email", "phone", "city", "state", "country", "created_at"],
        customers,
    ))
    lines.append("")

    # Orders and Order Items
    orders, order_items = generate_orders_and_items(1000, products)
    lines.append(f"-- Orders (~{len(orders)} rows)")
    lines.append(_build_insert(
        "orders",
        ["id", "customer_id", "order_date", "status", "total_amount"],
        orders,
    ))
    lines.append("")

    lines.append(f"-- Order Items (~{len(order_items)} rows)")
    lines.append(_build_insert(
        "order_items",
        ["id", "order_id", "product_id", "quantity", "unit_price", "discount"],
        order_items,
    ))
    lines.append("")

    # Payments
    payments = generate_payments(orders)
    lines.append(f"-- Payments (~{len(payments)} rows)")
    lines.append(_build_insert(
        "payments",
        ["id", "order_id", "payment_date", "amount", "method", "status"],
        payments,
    ))
    lines.append("")

    # Reviews
    reviews = generate_reviews(products, 600)
    lines.append(f"-- Reviews (~{len(reviews)} rows)")
    lines.append(_build_insert(
        "reviews",
        ["id", "product_id", "customer_id", "rating", "comment", "review_date"],
        reviews,
    ))
    lines.append("")

    # Shipping
    shipping = generate_shipping(orders, 800)
    lines.append(f"-- Shipping (~{len(shipping)} rows)")
    lines.append(_build_insert(
        "shipping",
        ["id", "order_id", "shipping_date", "delivery_date", "carrier", "tracking_number", "status"],
        shipping,
    ))
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_seed_sql())
