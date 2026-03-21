// Dataset schema definitions for all 3 datasets

interface Column {
  name: string;
  type: string;
  isPrimaryKey: boolean;
  isForeignKey: boolean;
  references?: string;
  nullable: boolean;
}

interface Table {
  name: string;
  columns: Column[];
  sampleRows: Record<string, unknown>[];
}

function pk(name: string, type = "INT"): Column {
  return { name, type, isPrimaryKey: true, isForeignKey: false, nullable: false };
}
function col(name: string, type = "TEXT", nullable = false): Column {
  return { name, type, isPrimaryKey: false, isForeignKey: false, nullable };
}
function fk(name: string, ref: string, type = "INT", nullable = false): Column {
  return { name, type, isPrimaryKey: false, isForeignKey: true, references: ref, nullable };
}

export const DATASET_SCHEMAS: Record<string, Table[]> = {
  ecommerce: [
    {
      name: "customers", sampleRows: [],
      columns: [pk("id"), col("first_name"), col("last_name"), col("email"), col("phone", "TEXT", true), col("city"), col("state"), col("country"), col("created_at", "TIMESTAMP")],
    },
    {
      name: "categories", sampleRows: [],
      columns: [pk("id"), col("name"), col("description", "TEXT", true)],
    },
    {
      name: "products", sampleRows: [],
      columns: [pk("id"), col("name"), fk("category_id", "categories.id"), col("price", "REAL"), col("cost", "REAL"), col("stock_quantity", "INT"), col("created_at", "TIMESTAMP")],
    },
    {
      name: "orders", sampleRows: [],
      columns: [pk("id"), fk("customer_id", "customers.id"), col("order_date"), col("status"), col("total_amount", "REAL")],
    },
    {
      name: "order_items", sampleRows: [],
      columns: [pk("id"), fk("order_id", "orders.id"), fk("product_id", "products.id"), col("quantity", "INT"), col("unit_price", "REAL"), col("discount", "REAL")],
    },
    {
      name: "payments", sampleRows: [],
      columns: [pk("id"), fk("order_id", "orders.id"), col("payment_date"), col("amount", "REAL"), col("method"), col("status")],
    },
    {
      name: "reviews", sampleRows: [],
      columns: [pk("id"), fk("product_id", "products.id"), fk("customer_id", "customers.id"), col("rating", "INT"), col("comment", "TEXT", true), col("review_date")],
    },
    {
      name: "shipping", sampleRows: [],
      columns: [pk("id"), fk("order_id", "orders.id"), col("shipping_date"), col("delivery_date", "TEXT", true), col("carrier"), col("tracking_number"), col("status")],
    },
  ],
  finance: [
    {
      name: "customers", sampleRows: [],
      columns: [pk("id"), col("first_name"), col("last_name"), col("email"), col("phone", "TEXT", true), col("date_of_birth"), col("city"), col("state"), col("country"), col("created_at", "TIMESTAMP")],
    },
    {
      name: "accounts", sampleRows: [],
      columns: [pk("id"), fk("customer_id", "customers.id"), col("account_type"), col("balance", "REAL"), col("currency"), col("opened_at"), col("status")],
    },
    {
      name: "transactions", sampleRows: [],
      columns: [pk("id"), fk("account_id", "accounts.id"), col("transaction_date"), col("type"), col("amount", "REAL"), col("balance_after", "REAL"), col("description"), col("reference_number")],
    },
    {
      name: "cards", sampleRows: [],
      columns: [pk("id"), fk("account_id", "accounts.id"), col("card_number"), col("card_type"), col("expiry_date"), col("status"), col("credit_limit", "REAL", true), col("issued_at")],
    },
    {
      name: "loans", sampleRows: [],
      columns: [pk("id"), fk("customer_id", "customers.id"), col("loan_type"), col("principal", "REAL"), col("interest_rate", "REAL"), col("term_months", "INT"), col("start_date"), col("status")],
    },
    {
      name: "payments", sampleRows: [],
      columns: [pk("id"), fk("loan_id", "loans.id"), col("payment_date"), col("amount", "REAL"), col("principal_paid", "REAL"), col("interest_paid", "REAL"), col("remaining_balance", "REAL")],
    },
    {
      name: "branches", sampleRows: [],
      columns: [pk("id"), col("name"), col("city"), col("state"), col("manager_name"), col("opened_at")],
    },
  ],
  healthcare: [
    {
      name: "patients", sampleRows: [],
      columns: [pk("id"), col("first_name"), col("last_name"), col("date_of_birth"), col("gender"), col("email"), col("phone", "TEXT", true), col("blood_type"), col("city"), col("state"), fk("insurance_id", "insurance.id", "INT", true), col("created_at", "TIMESTAMP")],
    },
    {
      name: "doctors", sampleRows: [],
      columns: [pk("id"), col("first_name"), col("last_name"), col("specialty"), fk("department_id", "departments.id"), col("email"), col("phone"), col("hire_date"), col("salary", "REAL")],
    },
    {
      name: "departments", sampleRows: [],
      columns: [pk("id"), col("name"), col("floor", "INT"), fk("head_doctor_id", "doctors.id", "INT", true), col("budget", "REAL")],
    },
    {
      name: "visits", sampleRows: [],
      columns: [pk("id"), fk("patient_id", "patients.id"), fk("doctor_id", "doctors.id"), col("visit_date"), col("diagnosis"), col("notes", "TEXT", true), col("follow_up_date", "TEXT", true), col("status")],
    },
    {
      name: "prescriptions", sampleRows: [],
      columns: [pk("id"), fk("visit_id", "visits.id"), col("medication"), col("dosage"), col("frequency"), col("start_date"), col("end_date"), col("refills", "INT")],
    },
    {
      name: "insurance", sampleRows: [],
      columns: [pk("id"), col("provider_name"), col("plan_type"), col("coverage_amount", "REAL"), col("copay", "REAL"), col("deductible", "REAL")],
    },
    {
      name: "lab_results", sampleRows: [],
      columns: [pk("id"), fk("visit_id", "visits.id"), col("test_name"), col("result_value"), col("unit"), col("reference_range"), col("is_abnormal", "INT"), col("tested_at")],
    },
    {
      name: "billing", sampleRows: [],
      columns: [pk("id"), fk("visit_id", "visits.id"), col("amount", "REAL"), col("insurance_covered", "REAL"), col("patient_responsibility", "REAL"), col("status"), col("billed_at"), col("paid_at", "TEXT", true)],
    },
  ],
};

export function getSchemaForDataset(dataset: string): Table[] {
  return DATASET_SCHEMAS[dataset] || DATASET_SCHEMAS.ecommerce;
}
