"""
Healthcare Dataset Seed Script
Generates ~4000 rows across 8 tables with realistic data.
Includes intentional NULLs, duplicate emails, date gaps, and overdue billing
for the Data Debugging mode.
"""

import random
from datetime import datetime, timedelta

random.seed(42)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INSURANCE_DATA = [
    ("Blue Cross Blue Shield", "premium", 500000, 30, 1000),
    ("Aetna", "standard", 300000, 40, 2000),
    ("UnitedHealthcare", "premium", 600000, 25, 750),
    ("Cigna", "standard", 350000, 35, 1500),
    ("Humana", "basic", 150000, 50, 3000),
    ("Kaiser Permanente", "premium", 550000, 20, 500),
    ("Anthem", "standard", 320000, 40, 1800),
    ("Molina Healthcare", "basic", 120000, 55, 3500),
    ("Centene", "basic", 100000, 60, 4000),
    ("WellCare", "standard", 280000, 45, 2200),
    ("Medicare Part A", "standard", 400000, 0, 1600),
    ("Medicare Part B", "premium", 450000, 20, 800),
    ("Medicaid", "basic", 200000, 5, 500),
    ("TriCare", "premium", 500000, 15, 600),
    ("Oscar Health", "standard", 300000, 35, 1900),
]

DEPARTMENT_DATA = [
    (1, "Cardiology", 3, 2500000),
    (2, "Neurology", 4, 2200000),
    (3, "Orthopedics", 2, 1800000),
    (4, "Pediatrics", 1, 1500000),
    (5, "Oncology", 5, 3000000),
    (6, "Emergency", 1, 4000000),
    (7, "Radiology", 2, 1200000),
    (8, "Dermatology", 3, 900000),
    (9, "Psychiatry", 4, 1100000),
    (10, "General Medicine", 1, 1600000),
]

SPECIALTIES_BY_DEPT = {
    1: ["Cardiologist", "Interventional Cardiologist", "Electrophysiologist"],
    2: ["Neurologist", "Neurosurgeon", "Neuro-oncologist"],
    3: ["Orthopedic Surgeon", "Sports Medicine Specialist", "Spine Surgeon"],
    4: ["Pediatrician", "Neonatologist", "Pediatric Surgeon"],
    5: ["Oncologist", "Radiation Oncologist", "Surgical Oncologist"],
    6: ["Emergency Physician", "Trauma Surgeon", "Critical Care Specialist"],
    7: ["Radiologist", "Interventional Radiologist", "Nuclear Medicine Specialist"],
    8: ["Dermatologist", "Cosmetic Dermatologist", "Dermatopathologist"],
    9: ["Psychiatrist", "Child Psychiatrist", "Addiction Psychiatrist"],
    10: ["General Practitioner", "Family Medicine Physician", "Internal Medicine Physician"],
}

DOC_FIRST = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen", "Daniel",
    "Lisa", "Matthew", "Nancy", "Anthony", "Betty", "Mark", "Margaret",
    "Donald", "Sandra", "Steven", "Ashley", "Andrew", "Dorothy", "Paul",
    "Kimberly", "Joshua", "Emily", "Kenneth", "Donna", "Kevin", "Michelle",
    "Brian", "Carol", "George", "Amanda", "Timothy", "Melissa", "Ronald",
    "Deborah",
]
DOC_LAST = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts",
]

PAT_FIRST = [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "Logan", "Mia", "Lucas", "Charlotte", "Aiden", "Amelia",
    "Jackson", "Harper", "Sebastian", "Evelyn", "Jack", "Abigail", "Owen",
    "Emily", "Luke", "Ella", "Henry", "Grace", "Alexander", "Chloe",
    "Benjamin", "Aria", "Caleb", "Scarlett", "Ryan", "Victoria", "Nathan",
    "Madison", "Carter", "Luna", "Dylan", "Layla", "Samuel", "Penelope",
    "John", "Riley", "Gabriel", "Zoey", "Anthony", "Nora", "Isaac", "Lily",
    "Leo", "Hannah", "Daniel", "Eleanor", "Matthew", "Hazel", "Jayden",
    "Aurora", "David",
]
PAT_LAST = [
    "Anderson", "Baker", "Campbell", "Davis", "Edwards", "Foster", "Garcia",
    "Harris", "Irving", "Jackson", "Kelly", "Lambert", "Mitchell", "Nelson",
    "Owens", "Parker", "Quinn", "Reynolds", "Stewart", "Turner", "Underwood",
    "Vasquez", "Walker", "Xavier", "Young", "Zimmerman", "Abbott", "Blake",
    "Collins", "Dixon", "Ellis", "Fletcher", "Gibson", "Hughes", "Ingram",
    "Jensen", "Knox", "Lawson", "Morgan", "Nash", "Oliver", "Peters",
    "Richards", "Shaw", "Tucker", "Upton", "Vaughn", "Watson", "York",
    "Zane",
]

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"),
    ("Indianapolis", "IN"), ("San Francisco", "CA"), ("Seattle", "WA"),
    ("Denver", "CO"), ("Washington", "DC"), ("Nashville", "TN"),
    ("Oklahoma City", "OK"), ("El Paso", "TX"), ("Boston", "MA"),
    ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"),
    ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"),
]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

DIAGNOSES = [
    "Hypertension", "Type 2 Diabetes", "Upper Respiratory Infection",
    "Migraine", "Anxiety Disorder", "Major Depressive Disorder", "Asthma",
    "Allergic Rhinitis", "Lower Back Pain", "Osteoarthritis",
    "Hyperlipidemia", "Urinary Tract Infection",
    "Gastroesophageal Reflux", "Iron Deficiency Anemia",
    "Hypothyroidism", "Atrial Fibrillation", "Chronic Kidney Disease",
    "Pneumonia", "Bronchitis", "Skin Rash", "Contact Dermatitis",
    "Eczema", "Psoriasis", "Insomnia", "Sleep Apnea", "Obesity",
    "Vitamin D Deficiency", "Osteoporosis", "Gout", "Conjunctivitis",
    "Sinusitis", "Otitis Media", "Strep Throat", "Influenza", "COVID-19",
    "Concussion", "Fracture", "Sprain", "Tendinitis",
    "Carpal Tunnel Syndrome",
]

VISIT_STATUSES = [
    "completed", "completed", "completed", "completed", "completed",
    "completed", "completed", "scheduled", "cancelled", "no_show",
]

MEDICATIONS = [
    ("Lisinopril", "10mg", "Once daily"),
    ("Metformin", "500mg", "Twice daily"),
    ("Atorvastatin", "20mg", "Once daily at bedtime"),
    ("Amoxicillin", "500mg", "Three times daily"),
    ("Omeprazole", "20mg", "Once daily before breakfast"),
    ("Levothyroxine", "50mcg", "Once daily on empty stomach"),
    ("Amlodipine", "5mg", "Once daily"),
    ("Metoprolol", "25mg", "Twice daily"),
    ("Sertraline", "50mg", "Once daily"),
    ("Gabapentin", "300mg", "Three times daily"),
    ("Prednisone", "10mg", "Once daily with food"),
    ("Ibuprofen", "400mg", "Every 6 hours as needed"),
    ("Acetaminophen", "500mg", "Every 4-6 hours as needed"),
    ("Albuterol", "2 puffs", "Every 4-6 hours as needed"),
    ("Fluticasone", "50mcg", "Two sprays each nostril daily"),
    ("Azithromycin", "250mg", "Once daily for 5 days"),
    ("Ciprofloxacin", "500mg", "Twice daily"),
    ("Warfarin", "5mg", "Once daily"),
    ("Hydrochlorothiazide", "25mg", "Once daily"),
    ("Losartan", "50mg", "Once daily"),
    ("Clopidogrel", "75mg", "Once daily"),
    ("Pantoprazole", "40mg", "Once daily"),
    ("Escitalopram", "10mg", "Once daily"),
    ("Tramadol", "50mg", "Every 6 hours as needed"),
    ("Montelukast", "10mg", "Once daily at bedtime"),
]

LAB_TESTS = [
    ("Complete Blood Count", 14.2, "g/dL", "12.0-17.5"),
    ("Hemoglobin A1C", 6.8, "%", "4.0-5.6"),
    ("Fasting Glucose", 110.0, "mg/dL", "70-100"),
    ("Total Cholesterol", 195.0, "mg/dL", "< 200"),
    ("LDL Cholesterol", 130.0, "mg/dL", "< 100"),
    ("HDL Cholesterol", 55.0, "mg/dL", "> 40"),
    ("Triglycerides", 150.0, "mg/dL", "< 150"),
    ("TSH", 2.5, "mIU/L", "0.4-4.0"),
    ("Creatinine", 1.1, "mg/dL", "0.7-1.3"),
    ("BUN", 18.0, "mg/dL", "7-20"),
    ("Sodium", 140.0, "mEq/L", "136-145"),
    ("Potassium", 4.2, "mEq/L", "3.5-5.0"),
    ("ALT", 32.0, "U/L", "7-56"),
    ("AST", 28.0, "U/L", "10-40"),
    ("White Blood Cell Count", 7.5, "K/uL", "4.5-11.0"),
    ("Platelet Count", 250.0, "K/uL", "150-400"),
    ("Vitamin D", 22.0, "ng/mL", "30-100"),
    ("Iron", 80.0, "mcg/dL", "60-170"),
    ("Ferritin", 45.0, "ng/mL", "12-300"),
    ("PSA", 3.2, "ng/mL", "< 4.0"),
    ("Uric Acid", 7.5, "mg/dL", "3.5-7.2"),
    ("C-Reactive Protein", 0.8, "mg/L", "< 3.0"),
    ("Prothrombin Time", 12.5, "seconds", "11.0-13.5"),
    ("Blood Urea Nitrogen", 15.0, "mg/dL", "6-20"),
    ("Calcium", 9.5, "mg/dL", "8.5-10.5"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _esc(s: str) -> str:
    """Escape single quotes for SQL."""
    return s.replace("'", "''")


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_seed_sql() -> str:  # noqa: C901 — long but straightforward
    random.seed(42)
    out: list[str] = []

    out.append("-- ============================================================")
    out.append("-- Healthcare Seed Data  (~4000 rows across 8 tables)")
    out.append("-- ============================================================\n")

    # ---- Insurance (15) ----
    out.append("-- Insurance Plans (15)")
    for i, (name, plan, cov, copay, ded) in enumerate(INSURANCE_DATA, 1):
        out.append(
            f"INSERT INTO insurance VALUES "
            f"({i}, '{_esc(name)}', '{plan}', {cov}, {copay}, {ded});"
        )

    # ---- Departments (10) — head_doctor_id set to NULL initially ----
    out.append("\n-- Departments (10)")
    for did, name, floor, budget in DEPARTMENT_DATA:
        out.append(
            f"INSERT INTO departments VALUES "
            f"({did}, '{_esc(name)}', {floor}, NULL, {budget});"
        )

    # ---- Doctors (50) ----
    out.append("\n-- Doctors (50)")
    for i in range(1, 51):
        fn = DOC_FIRST[(i - 1) % len(DOC_FIRST)]
        ln = DOC_LAST[(i - 1) % len(DOC_LAST)]
        dept_id = ((i - 1) % 10) + 1
        specs = SPECIALTIES_BY_DEPT[dept_id]
        spec = specs[(i - 1) % len(specs)]
        email = f"{fn.lower()}.{ln.lower()}{i}@hospital.org"
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        hire = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
        salary = round(random.uniform(180000, 450000), 2)
        out.append(
            f"INSERT INTO doctors VALUES "
            f"({i}, '{fn}', '{ln}', '{_esc(spec)}', {dept_id}, "
            f"'{email}', '{phone}', '{hire:%Y-%m-%d}', {salary});"
        )

    # Update department heads (first doctor per department)
    out.append("\n-- Set department heads")
    for dept_id in range(1, 11):
        out.append(
            f"UPDATE departments SET head_doctor_id = {dept_id} "
            f"WHERE id = {dept_id};"
        )

    # ---- Patients (300) ----
    out.append("\n-- Patients (300)")
    patient_emails: list[str] = []
    for i in range(1, 301):
        fn = PAT_FIRST[(i - 1) % len(PAT_FIRST)]
        ln = PAT_LAST[(i - 1) % len(PAT_LAST)]
        dob = datetime(1940, 1, 1) + timedelta(days=random.randint(0, 25000))
        gender = random.choices(["M", "F", "Other"], weights=[45, 45, 10])[0]
        email = f"{fn.lower()}.{ln.lower()}{i}@email.com"
        patient_emails.append(email)
        if random.random() < 0.05:
            phone_val = "NULL"
        else:
            phone_val = (
                f"'555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'"
            )
        bt = random.choice(BLOOD_TYPES)
        ci = random.randint(0, len(CITIES_STATES) - 1)
        city, state = CITIES_STATES[ci]
        ins_choices = list(range(1, 16)) + [None]
        ins_id = random.choice(ins_choices)
        ins_str = "NULL" if ins_id is None else str(ins_id)
        created = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
        out.append(
            f"INSERT INTO patients VALUES "
            f"({i}, '{fn}', '{ln}', '{dob:%Y-%m-%d}', '{gender}', "
            f"'{email}', {phone_val}, '{bt}', '{_esc(city)}', '{state}', "
            f"{ins_str}, '{created:%Y-%m-%d}');"
        )

    # Intentional duplicate emails (~10)
    out.append("\n-- Duplicate emails for debugging")
    dup_targets = random.sample(range(10, 300), 10)
    dup_sources = random.sample(range(0, 10), 10)
    for tgt, src in zip(dup_targets, dup_sources):
        out.append(
            f"UPDATE patients SET email = '{patient_emails[src]}' "
            f"WHERE id = {tgt + 1};"
        )

    # ---- Visits (1500) ----
    out.append("\n-- Visits (1500)")
    visit_dates: list[datetime] = []
    for i in range(1, 1501):
        pid = random.randint(1, 300)
        did = random.randint(1, 50)
        vd = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1400))
        visit_dates.append(vd)
        diag = random.choice(DIAGNOSES)
        status = random.choice(VISIT_STATUSES)
        if random.random() < 0.15:
            notes_val = "NULL"
        else:
            notes_val = (
                f"'Patient presented with symptoms of {diag.lower()}. "
                f"Vitals recorded.'"
            )
        follow_up = "NULL"
        if status == "completed" and random.random() < 0.4:
            fu = vd + timedelta(days=random.randint(7, 90))
            follow_up = f"'{fu:%Y-%m-%d}'"
        out.append(
            f"INSERT INTO visits VALUES "
            f"({i}, {pid}, {did}, '{vd:%Y-%m-%d}', '{_esc(diag)}', "
            f"{notes_val}, {follow_up}, '{status}');"
        )

    # ---- Prescriptions (800) ----
    out.append("\n-- Prescriptions (800)")
    for i in range(1, 801):
        vid = random.randint(1, 1200)  # keep within completed range roughly
        med, dos, freq = random.choice(MEDICATIONS)
        sd = visit_dates[vid - 1]
        ed = sd + timedelta(days=random.choice([7, 14, 30, 60, 90, 180, 365]))
        refills = random.choice([0, 0, 1, 2, 3, 5])
        out.append(
            f"INSERT INTO prescriptions VALUES "
            f"({i}, {vid}, '{_esc(med)}', '{dos}', '{freq}', "
            f"'{sd:%Y-%m-%d}', '{ed:%Y-%m-%d}', {refills});"
        )

    # ---- Lab Results (600) ----
    out.append("\n-- Lab Results (600)")
    for i in range(1, 601):
        vid = random.randint(1, 1500)
        test_name, base_val, unit, ref = random.choice(LAB_TESTS)
        variation = base_val * random.uniform(-0.3, 0.3)
        val = round(base_val + variation, 1)
        is_abn = 1 if random.random() < 0.10 else 0
        td = visit_dates[vid - 1]
        tested = td + timedelta(hours=random.randint(0, 48))
        out.append(
            f"INSERT INTO lab_results VALUES "
            f"({i}, {vid}, '{_esc(test_name)}', '{val}', '{unit}', "
            f"'{ref}', {is_abn}, '{tested:%Y-%m-%d %H:%M:%S}');"
        )

    # ---- Billing (500) ----
    out.append("\n-- Billing (500)")
    bill_statuses = [
        "paid", "paid", "paid", "pending", "overdue", "insurance_processing",
    ]
    for i in range(1, 501):
        vid = random.randint(1, 1500)
        amount = round(random.uniform(75, 5000), 2)
        ins_pct = random.uniform(0.3, 0.9)
        ins_covered = round(amount * ins_pct, 2)
        pat_resp = round(amount - ins_covered, 2)
        bstatus = random.choice(bill_statuses)
        bd = visit_dates[vid - 1]
        billed = bd + timedelta(days=random.randint(0, 7))
        if bstatus == "paid":
            paid = billed + timedelta(days=random.randint(1, 60))
            paid_str = f"'{paid:%Y-%m-%d}'"
        else:
            paid_str = "NULL"
        out.append(
            f"INSERT INTO billing VALUES "
            f"({i}, {vid}, {amount}, {ins_covered}, {pat_resp}, "
            f"'{bstatus}', '{billed:%Y-%m-%d}', {paid_str});"
        )

    return "\n".join(out) + "\n"
