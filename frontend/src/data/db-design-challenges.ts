/* ── Database Design Challenges ── */

export interface SolutionColumn {
  name: string;
  type: string;
  constraints: string;
}

export interface SolutionTable {
  name: string;
  columns: SolutionColumn[];
}

export interface ValidationRule {
  check: string; // "table_exists" | "column_exists" | "has_pk" | "has_fk" | "relationship"
  table?: string;
  column?: string;
  targetTable?: string;
  message: string; // shown on success
  failMessage: string; // shown on failure
}

export interface DesignChallenge {
  id: string;
  title: string;
  level: "beginner" | "intermediate" | "advanced" | "expert";
  mode: "build" | "fix";
  scenario: string;
  requirements: string[];
  hints: string[];
  solution: SolutionTable[];
  relationships: string[];
  validationRules: ValidationRule[];
  learnings: string[];
  // For "fix" mode — the broken schema to start with
  brokenSchema?: SolutionTable[];
  brokenDescription?: string;
}

const CHALLENGES: DesignChallenge[] = [
  // ════════════════════════════════════════
  //  BEGINNER — Understand Tables (8)
  // ════════════════════════════════════════
  {
    id: "b1",
    title: "Store User Profiles",
    level: "beginner",
    mode: "build",
    scenario: "A startup needs to store user accounts. Each user has a name, email, and sign-up date.",
    requirements: [
      "Create a users table",
      "Each user must have a unique identifier",
      "Store name, email, and signup date",
      "Email must be unique",
    ],
    hints: [
      "Every table needs a primary key — usually an auto-incrementing id",
      "Use VARCHAR for text, TIMESTAMP for dates",
      "UNIQUE constraint prevents duplicate emails",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "table_exists", table: "users", message: "Users table created", failMessage: "Missing 'users' table" },
      { check: "has_pk", table: "users", message: "Primary key set", failMessage: "Users table needs a PRIMARY KEY" },
      { check: "column_exists", table: "users", column: "email", message: "Email column exists", failMessage: "Missing 'email' column" },
    ],
    learnings: ["Every table needs a PRIMARY KEY", "Use SERIAL for auto-incrementing IDs", "UNIQUE constraint prevents duplicates"],
  },
  {
    id: "b2",
    title: "Product Catalog",
    level: "beginner",
    mode: "build",
    scenario: "An online store needs a simple product list with name, price, and stock quantity.",
    requirements: [
      "Create a products table",
      "Each product has a unique ID",
      "Store name, price, and stock_quantity",
      "Price should be a decimal type",
    ],
    hints: [
      "Use DECIMAL(10,2) for money values — never FLOAT",
      "INT works well for stock quantity",
      "NOT NULL ensures required fields are always filled",
    ],
    solution: [
      {
        name: "products",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "stock_quantity", type: "INT", constraints: "DEFAULT 0" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "table_exists", table: "products", message: "Products table created", failMessage: "Missing 'products' table" },
      { check: "has_pk", table: "products", message: "Primary key set", failMessage: "Products needs a PRIMARY KEY" },
      { check: "column_exists", table: "products", column: "price", message: "Price column exists", failMessage: "Missing 'price' column" },
    ],
    learnings: ["Use DECIMAL for money — FLOAT causes rounding errors", "DEFAULT values handle optional fields", "NOT NULL enforces required data"],
  },
  {
    id: "b3",
    title: "Fix: Missing Primary Key",
    level: "beginner",
    mode: "fix",
    scenario: "A junior developer created this table but reports keep showing duplicate entries.",
    brokenDescription: "The employees table has no primary key, allowing duplicate rows.",
    brokenSchema: [
      {
        name: "employees",
        columns: [
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "department", type: "VARCHAR(50)", constraints: "" },
          { name: "salary", type: "DECIMAL(10,2)", constraints: "" },
          { name: "hire_date", type: "DATE", constraints: "" },
        ],
      },
    ],
    requirements: [
      "Identify why duplicate rows can appear",
      "Add a proper primary key",
      "Ensure each employee is uniquely identifiable",
    ],
    hints: [
      "Without a PRIMARY KEY, the database can't distinguish between rows",
      "Add an 'id' column with SERIAL PRIMARY KEY",
    ],
    solution: [
      {
        name: "employees",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "department", type: "VARCHAR(50)", constraints: "" },
          { name: "salary", type: "DECIMAL(10,2)", constraints: "" },
          { name: "hire_date", type: "DATE", constraints: "" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "has_pk", table: "employees", message: "Primary key added!", failMessage: "Still no PRIMARY KEY on employees" },
    ],
    learnings: ["Every table MUST have a primary key", "Without a PK, you can't uniquely identify or update rows", "SERIAL auto-generates unique IDs"],
  },
  {
    id: "b4",
    title: "Blog Posts",
    level: "beginner",
    mode: "build",
    scenario: "A personal blog needs to store articles with title, body, and publish status.",
    requirements: [
      "Create a posts table",
      "Store title, body text, and publish status",
      "Track when each post was created",
      "Status should default to 'draft'",
    ],
    hints: [
      "Use TEXT for the body — VARCHAR has a length limit",
      "VARCHAR(20) with DEFAULT 'draft' works for status",
    ],
    solution: [
      {
        name: "posts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "body", type: "TEXT", constraints: "NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'draft'" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "table_exists", table: "posts", message: "Posts table created", failMessage: "Missing 'posts' table" },
      { check: "has_pk", table: "posts", message: "Primary key set", failMessage: "Posts needs a PRIMARY KEY" },
      { check: "column_exists", table: "posts", column: "title", message: "Title column exists", failMessage: "Missing 'title' column" },
      { check: "column_exists", table: "posts", column: "body", message: "Body column exists", failMessage: "Missing 'body' column" },
    ],
    learnings: ["TEXT vs VARCHAR — use TEXT for unlimited length content", "DEFAULT values set automatic values for new rows"],
  },
  {
    id: "b5",
    title: "Fix: Wrong Data Types",
    level: "beginner",
    mode: "fix",
    scenario: "The finance team reports that transaction amounts show values like $99.99999999 instead of $100.00.",
    brokenDescription: "Money is stored as FLOAT which causes floating-point precision errors.",
    brokenSchema: [
      {
        name: "transactions",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "description", type: "VARCHAR(200)", constraints: "" },
          { name: "amount", type: "FLOAT", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    requirements: [
      "Fix the data type that causes precision errors",
      "Money should always show exact cents",
    ],
    hints: [
      "FLOAT uses binary representation — 0.1 can't be stored exactly",
      "DECIMAL(10,2) stores exact decimal values",
    ],
    solution: [
      {
        name: "transactions",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "description", type: "VARCHAR(200)", constraints: "" },
          { name: "amount", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "column_exists", table: "transactions", column: "amount", message: "Amount column exists", failMessage: "Missing 'amount' column" },
    ],
    learnings: ["NEVER use FLOAT for money", "DECIMAL(10,2) stores exact values with 2 decimal places", "This is a real-world bug that costs companies millions"],
  },
  {
    id: "b6",
    title: "Task Tracker",
    level: "beginner",
    mode: "build",
    scenario: "A team needs a simple task management board to track to-do items.",
    requirements: [
      "Create a tasks table",
      "Each task has a title and optional description",
      "Track priority (low, medium, high) and status (todo, in_progress, done)",
      "Record creation and completion dates",
    ],
    hints: [
      "Use VARCHAR for enum-like values (priority, status)",
      "completion date can be NULL until the task is done",
    ],
    solution: [
      {
        name: "tasks",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
          { name: "priority", type: "VARCHAR(10)", constraints: "DEFAULT 'medium'" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'todo'" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "completed_at", type: "TIMESTAMP", constraints: "" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "table_exists", table: "tasks", message: "Tasks table created", failMessage: "Missing 'tasks' table" },
      { check: "has_pk", table: "tasks", message: "Primary key set", failMessage: "Tasks needs a PRIMARY KEY" },
    ],
    learnings: ["Nullable columns are useful for optional/future data", "Enum-like values can use VARCHAR with application-level validation"],
  },
  {
    id: "b7",
    title: "Contact Book",
    level: "beginner",
    mode: "build",
    scenario: "Build a simple contacts table for a phone app.",
    requirements: [
      "Store first name, last name, phone, and email",
      "Phone and email should be optional",
      "Add a notes field for free-text",
    ],
    hints: [
      "Only first_name should be NOT NULL — everything else is optional",
      "Use TEXT for notes since length is unpredictable",
    ],
    solution: [
      {
        name: "contacts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "first_name", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "last_name", type: "VARCHAR(50)", constraints: "" },
          { name: "phone", type: "VARCHAR(20)", constraints: "" },
          { name: "email", type: "VARCHAR(255)", constraints: "" },
          { name: "notes", type: "TEXT", constraints: "" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "table_exists", table: "contacts", message: "Contacts table created", failMessage: "Missing 'contacts' table" },
      { check: "has_pk", table: "contacts", message: "Primary key set", failMessage: "Contacts needs a PRIMARY KEY" },
    ],
    learnings: ["Not every column needs NOT NULL — only truly required fields", "Design tables to match real-world data requirements"],
  },
  {
    id: "b8",
    title: "Fix: No Unique Constraint",
    level: "beginner",
    mode: "fix",
    scenario: "Users can register with the same email multiple times, causing login failures.",
    brokenDescription: "The accounts table allows duplicate emails because there's no UNIQUE constraint.",
    brokenSchema: [
      {
        name: "accounts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "username", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "NOT NULL" },
          { name: "password_hash", type: "VARCHAR(255)", constraints: "NOT NULL" },
        ],
      },
    ],
    requirements: [
      "Prevent duplicate email registrations",
      "Prevent duplicate usernames too",
    ],
    hints: [
      "Add UNIQUE constraint to both email and username",
      "UNIQUE can be added alongside NOT NULL",
    ],
    solution: [
      {
        name: "accounts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "username", type: "VARCHAR(50)", constraints: "UNIQUE NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "password_hash", type: "VARCHAR(255)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: [],
    validationRules: [
      { check: "column_exists", table: "accounts", column: "email", message: "Email column exists", failMessage: "Missing 'email' column" },
    ],
    learnings: ["UNIQUE constraints prevent duplicate values at the database level", "Always enforce uniqueness in the DB, not just the application"],
  },

  // ════════════════════════════════════════
  //  INTERMEDIATE — Relationships (10)
  // ════════════════════════════════════════
  {
    id: "i1",
    title: "Customers & Orders",
    level: "intermediate",
    mode: "build",
    scenario: "An e-commerce site needs to track which customers placed which orders.",
    requirements: [
      "Customers have name and email",
      "Orders have an amount and date",
      "Each order belongs to exactly one customer",
      "A customer can have many orders",
    ],
    hints: [
      "This is a one-to-many relationship: customers → orders",
      "The 'many' side (orders) gets the foreign key",
      "Add customer_id in orders that references customers.id",
    ],
    solution: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "total_amount", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: ["customers 1---* orders (one customer, many orders)"],
    validationRules: [
      { check: "table_exists", table: "customers", message: "Customers table created", failMessage: "Missing 'customers' table" },
      { check: "table_exists", table: "orders", message: "Orders table created", failMessage: "Missing 'orders' table" },
      { check: "has_fk", table: "orders", targetTable: "customers", message: "Foreign key relationship set!", failMessage: "Orders needs a foreign key to customers" },
    ],
    learnings: ["One-to-many: FK goes on the 'many' side", "The child table references the parent", "This is the most common relationship pattern"],
  },
  {
    id: "i2",
    title: "Authors & Books",
    level: "intermediate",
    mode: "build",
    scenario: "A bookstore needs to track books and their authors. Each book has exactly one author.",
    requirements: [
      "Authors have name and bio",
      "Books have title, ISBN, price, and publish year",
      "Each book belongs to one author",
      "An author can write many books",
    ],
    hints: [
      "One-to-many: authors → books",
      "ISBN should be UNIQUE",
    ],
    solution: [
      {
        name: "authors",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "bio", type: "TEXT", constraints: "" },
        ],
      },
      {
        name: "books",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "author_id", type: "INT", constraints: "FK -> authors.id NOT NULL" },
          { name: "title", type: "VARCHAR(300)", constraints: "NOT NULL" },
          { name: "isbn", type: "VARCHAR(13)", constraints: "UNIQUE NOT NULL" },
          { name: "price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "pub_year", type: "INT", constraints: "" },
        ],
      },
    ],
    relationships: ["authors 1---* books (one author, many books)"],
    validationRules: [
      { check: "table_exists", table: "authors", message: "Authors table created", failMessage: "Missing 'authors' table" },
      { check: "table_exists", table: "books", message: "Books table created", failMessage: "Missing 'books' table" },
      { check: "has_fk", table: "books", targetTable: "authors", message: "FK from books to authors", failMessage: "Books needs author_id FK" },
    ],
    learnings: ["Foreign keys enforce referential integrity", "You can't insert a book with a non-existent author_id"],
  },
  {
    id: "i3",
    title: "Fix: Missing Foreign Key",
    level: "intermediate",
    mode: "fix",
    scenario: "The orders table has a customer_id column but it's just a plain INT — there's no FK constraint. Orders reference deleted customers, causing report crashes.",
    brokenDescription: "customer_id exists but has no FOREIGN KEY constraint, allowing orphan records.",
    brokenSchema: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "NOT NULL" },
          { name: "total", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    requirements: [
      "Add proper FK constraint from orders.customer_id to customers.id",
      "This prevents orders from referencing non-existent customers",
    ],
    hints: [
      "Change customer_id constraint to include FK -> customers.id",
      "Without FK, the database can't enforce the relationship",
    ],
    solution: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "total", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: ["customers 1---* orders"],
    validationRules: [
      { check: "has_fk", table: "orders", targetTable: "customers", message: "FK constraint added!", failMessage: "orders.customer_id needs FK -> customers.id" },
    ],
    learnings: ["A column named 'customer_id' is NOT a foreign key without the constraint", "FKs prevent orphan records — data that references nothing"],
  },
  {
    id: "i4",
    title: "Departments & Employees",
    level: "intermediate",
    mode: "build",
    scenario: "An HR system tracks which department each employee belongs to.",
    requirements: [
      "Departments have a name and location",
      "Employees have name, email, hire_date, and salary",
      "Each employee belongs to one department",
      "A department can have many employees",
    ],
    hints: [
      "Classic one-to-many pattern",
      "department_id FK goes in the employees table",
    ],
    solution: [
      {
        name: "departments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "UNIQUE NOT NULL" },
          { name: "location", type: "VARCHAR(200)", constraints: "" },
        ],
      },
      {
        name: "employees",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "department_id", type: "INT", constraints: "FK -> departments.id NOT NULL" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "hire_date", type: "DATE", constraints: "NOT NULL" },
          { name: "salary", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: ["departments 1---* employees"],
    validationRules: [
      { check: "table_exists", table: "departments", message: "Departments table created", failMessage: "Missing 'departments' table" },
      { check: "table_exists", table: "employees", message: "Employees table created", failMessage: "Missing 'employees' table" },
      { check: "has_fk", table: "employees", targetTable: "departments", message: "FK relationship set", failMessage: "Employees needs FK to departments" },
    ],
    learnings: ["One-to-many is the most common relationship", "Always ask: which side is 'one' and which is 'many'?"],
  },
  {
    id: "i5",
    title: "Blog: Posts & Comments",
    level: "intermediate",
    mode: "build",
    scenario: "A blog platform needs users who write posts, and readers who comment on them.",
    requirements: [
      "Users have name and email",
      "Posts have title, body, and creation date",
      "Each post is written by one user",
      "Comments have text and creation date",
      "Each comment belongs to one post and one user",
    ],
    hints: [
      "Two one-to-many relationships from users",
      "Comments has TWO foreign keys: user_id and post_id",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "posts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "body", type: "TEXT", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "comments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "post_id", type: "INT", constraints: "FK -> posts.id NOT NULL" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "body", type: "TEXT", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: ["users 1---* posts", "users 1---* comments", "posts 1---* comments"],
    validationRules: [
      { check: "table_exists", table: "users", message: "Users table created", failMessage: "Missing 'users'" },
      { check: "table_exists", table: "posts", message: "Posts table created", failMessage: "Missing 'posts'" },
      { check: "table_exists", table: "comments", message: "Comments table created", failMessage: "Missing 'comments'" },
      { check: "has_fk", table: "posts", targetTable: "users", message: "Posts linked to users", failMessage: "Posts needs FK to users" },
      { check: "has_fk", table: "comments", targetTable: "posts", message: "Comments linked to posts", failMessage: "Comments needs FK to posts" },
    ],
    learnings: ["A table can have multiple foreign keys", "Comments need BOTH post_id and user_id to track who said what on which post"],
  },
  {
    id: "i6",
    title: "Fix: FK on Wrong Side",
    level: "intermediate",
    mode: "fix",
    scenario: "A developer put the foreign key on the wrong table. The schema says each department can only have ONE employee.",
    brokenDescription: "employee_id is on the departments table instead of department_id on employees.",
    brokenSchema: [
      {
        name: "departments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "employee_id", type: "INT", constraints: "FK -> employees.id" },
        ],
      },
      {
        name: "employees",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "salary", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
    ],
    requirements: [
      "Fix the FK so each employee belongs to one department",
      "A department should be able to have many employees",
    ],
    hints: [
      "The FK should be on the 'many' side",
      "Move the relationship: remove employee_id from departments, add department_id to employees",
    ],
    solution: [
      {
        name: "departments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "employees",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "department_id", type: "INT", constraints: "FK -> departments.id NOT NULL" },
          { name: "salary", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: ["departments 1---* employees"],
    validationRules: [
      { check: "has_fk", table: "employees", targetTable: "departments", message: "FK correctly on employees now", failMessage: "employees needs department_id FK" },
    ],
    learnings: ["FK ALWAYS goes on the 'many' side", "If departments has employee_id, it means 1 department = 1 employee — wrong!", "Think: which table has 'many' rows per parent?"],
  },
  {
    id: "i7",
    title: "School Classes",
    level: "intermediate",
    mode: "build",
    scenario: "A school needs to track teachers, subjects, and which teacher teaches which subject in which classroom.",
    requirements: [
      "Teachers have name, email, and subject specialization",
      "Classrooms have a room number and capacity",
      "Each class has a teacher, subject, classroom, and time slot",
    ],
    hints: [
      "The 'classes' table is the central table with multiple FKs",
      "A class connects a teacher to a room at a specific time",
    ],
    solution: [
      {
        name: "teachers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "specialization", type: "VARCHAR(100)", constraints: "" },
        ],
      },
      {
        name: "classrooms",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "room_number", type: "VARCHAR(10)", constraints: "UNIQUE NOT NULL" },
          { name: "capacity", type: "INT", constraints: "NOT NULL" },
        ],
      },
      {
        name: "classes",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "teacher_id", type: "INT", constraints: "FK -> teachers.id NOT NULL" },
          { name: "classroom_id", type: "INT", constraints: "FK -> classrooms.id NOT NULL" },
          { name: "subject", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "time_slot", type: "VARCHAR(50)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: ["teachers 1---* classes", "classrooms 1---* classes"],
    validationRules: [
      { check: "table_exists", table: "teachers", message: "Teachers table created", failMessage: "Missing 'teachers'" },
      { check: "table_exists", table: "classes", message: "Classes table created", failMessage: "Missing 'classes'" },
      { check: "has_fk", table: "classes", targetTable: "teachers", message: "Classes linked to teachers", failMessage: "Classes needs FK to teachers" },
    ],
    learnings: ["Central tables can have multiple FKs pointing to different parent tables", "This pattern is common in scheduling systems"],
  },

  // ════════════════════════════════════════
  //  ADVANCED — Real Systems (8)
  // ════════════════════════════════════════
  {
    id: "a1",
    title: "Students & Courses (Many-to-Many)",
    level: "advanced",
    mode: "build",
    scenario: "A university tracks which students enroll in which courses. One student takes many courses, one course has many students.",
    requirements: [
      "Students have name and student_number",
      "Courses have title, code, and credits",
      "Many-to-many: students enroll in courses",
      "Track enrollment date and grade",
    ],
    hints: [
      "Many-to-many requires a JUNCTION TABLE (bridge table)",
      "The junction table has two FKs: student_id and course_id",
      "Add extra columns (grade, enrolled_at) on the junction table",
    ],
    solution: [
      {
        name: "students",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "student_number", type: "VARCHAR(20)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "courses",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "code", type: "VARCHAR(10)", constraints: "UNIQUE NOT NULL" },
          { name: "credits", type: "INT", constraints: "NOT NULL" },
        ],
      },
      {
        name: "enrollments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "student_id", type: "INT", constraints: "FK -> students.id NOT NULL" },
          { name: "course_id", type: "INT", constraints: "FK -> courses.id NOT NULL" },
          { name: "enrolled_at", type: "DATE", constraints: "DEFAULT CURRENT_DATE" },
          { name: "grade", type: "VARCHAR(2)", constraints: "" },
        ],
      },
    ],
    relationships: [
      "students *---* courses (via enrollments junction table)",
      "students 1---* enrollments",
      "courses 1---* enrollments",
    ],
    validationRules: [
      { check: "table_exists", table: "students", message: "Students table created", failMessage: "Missing 'students'" },
      { check: "table_exists", table: "courses", message: "Courses table created", failMessage: "Missing 'courses'" },
      { check: "table_exists", table: "enrollments", message: "Junction table created!", failMessage: "Missing junction table (enrollments)" },
      { check: "has_fk", table: "enrollments", targetTable: "students", message: "Linked to students", failMessage: "Junction table needs FK to students" },
      { check: "has_fk", table: "enrollments", targetTable: "courses", message: "Linked to courses", failMessage: "Junction table needs FK to courses" },
    ],
    learnings: ["Many-to-many ALWAYS needs a junction/bridge table", "The junction table holds both FKs", "You can add extra data (grade, date) on the junction table"],
  },
  {
    id: "a2",
    title: "Social Media: Followers",
    level: "advanced",
    mode: "build",
    scenario: "Build a Twitter-like follow system where users can follow other users. Following is asymmetric (A follows B doesn't mean B follows A).",
    requirements: [
      "Users have username and display name",
      "Users can follow other users",
      "Following is one-directional",
      "A user can't follow themselves",
      "Track when the follow happened",
    ],
    hints: [
      "This is a self-referencing many-to-many",
      "The follows table has TWO FKs both pointing to users",
      "Use a composite PK to prevent duplicate follows",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "username", type: "VARCHAR(30)", constraints: "UNIQUE NOT NULL" },
          { name: "display_name", type: "VARCHAR(100)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "follows",
        columns: [
          { name: "follower_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "following_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "", type: "", constraints: "PRIMARY KEY (follower_id, following_id)" },
        ],
      },
    ],
    relationships: ["users *---* users (self-referencing via follows)"],
    validationRules: [
      { check: "table_exists", table: "users", message: "Users table created", failMessage: "Missing 'users'" },
      { check: "table_exists", table: "follows", message: "Follows junction table created", failMessage: "Missing 'follows' table" },
    ],
    learnings: ["Self-referencing many-to-many: both FKs point to the same table", "Composite PKs (two columns as PK) prevent duplicates", "Asymmetric relationships are directional"],
  },
  {
    id: "a3",
    title: "E-Commerce with Orders & Items",
    level: "advanced",
    mode: "build",
    scenario: "Design a complete order system where customers place orders containing multiple products with quantities.",
    requirements: [
      "Products have name, price, and stock",
      "Customers have name and email",
      "Orders track status and total amount",
      "Each order can contain multiple products with different quantities",
      "Store the unit price at time of order (prices can change later)",
    ],
    hints: [
      "Orders and products is many-to-many: one order has many products, one product appears in many orders",
      "The order_items junction table stores quantity and unit_price",
      "Store unit_price on order_items because product.price might change",
    ],
    solution: [
      {
        name: "products",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "stock_qty", type: "INT", constraints: "DEFAULT 0" },
        ],
      },
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'pending'" },
          { name: "total_amount", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "order_items",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "order_id", type: "INT", constraints: "FK -> orders.id NOT NULL" },
          { name: "product_id", type: "INT", constraints: "FK -> products.id NOT NULL" },
          { name: "quantity", type: "INT", constraints: "NOT NULL" },
          { name: "unit_price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: [
      "customers 1---* orders",
      "orders 1---* order_items",
      "products 1---* order_items",
    ],
    validationRules: [
      { check: "table_exists", table: "order_items", message: "Junction table for order items created", failMessage: "Missing 'order_items' table" },
      { check: "has_fk", table: "order_items", targetTable: "orders", message: "Linked to orders", failMessage: "order_items needs FK to orders" },
      { check: "has_fk", table: "order_items", targetTable: "products", message: "Linked to products", failMessage: "order_items needs FK to products" },
      { check: "column_exists", table: "order_items", column: "unit_price", message: "Stores price at time of purchase!", failMessage: "order_items should store unit_price (prices change)" },
    ],
    learnings: ["Always store prices on the order line item — product prices change over time", "This is called 'point-in-time data capture'", "order_items is both a junction table AND stores business data"],
  },
  {
    id: "a4",
    title: "Fix: Many-to-Many Without Junction",
    level: "advanced",
    mode: "fix",
    scenario: "A developer tried to model students-courses with a comma-separated list of course IDs in the students table. Queries are impossible.",
    brokenDescription: "course_ids is stored as a TEXT field with comma-separated values like '1,3,5'. You can't JOIN, filter, or aggregate properly.",
    brokenSchema: [
      {
        name: "students",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "course_ids", type: "TEXT", constraints: "" },
        ],
      },
      {
        name: "courses",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
        ],
      },
    ],
    requirements: [
      "Remove the comma-separated course_ids column",
      "Create a proper junction table for the many-to-many relationship",
    ],
    hints: [
      "NEVER store multiple values in one column",
      "Create an enrollments table with student_id and course_id",
    ],
    solution: [
      {
        name: "students",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "courses",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "enrollments",
        columns: [
          { name: "student_id", type: "INT", constraints: "FK -> students.id NOT NULL" },
          { name: "course_id", type: "INT", constraints: "FK -> courses.id NOT NULL" },
          { name: "", type: "", constraints: "PRIMARY KEY (student_id, course_id)" },
        ],
      },
    ],
    relationships: ["students *---* courses via enrollments"],
    validationRules: [
      { check: "table_exists", table: "enrollments", message: "Junction table created!", failMessage: "Need an enrollments junction table" },
    ],
    learnings: ["NEVER store comma-separated IDs in a column", "This violates First Normal Form (1NF)", "Always use a junction table for many-to-many"],
  },
  {
    id: "a5",
    title: "Library System",
    level: "advanced",
    mode: "build",
    scenario: "A library tracks books, physical copies, members, and borrowing history. One book title can have multiple copies.",
    requirements: [
      "Books have ISBN, title, author, and genre",
      "The library owns multiple physical copies of each book",
      "Members borrow specific copies, not book titles",
      "Track borrow date, due date, and return date",
    ],
    hints: [
      "Book vs Copy is a key distinction — copies are physical items",
      "Borrowings reference copies, not books",
      "returned_at being NULL means the book is still borrowed",
    ],
    solution: [
      {
        name: "books",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "isbn", type: "VARCHAR(13)", constraints: "UNIQUE NOT NULL" },
          { name: "title", type: "VARCHAR(300)", constraints: "NOT NULL" },
          { name: "author", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "genre", type: "VARCHAR(50)", constraints: "" },
        ],
      },
      {
        name: "book_copies",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "book_id", type: "INT", constraints: "FK -> books.id NOT NULL" },
          { name: "condition", type: "VARCHAR(20)", constraints: "DEFAULT 'good'" },
        ],
      },
      {
        name: "members",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "borrowings",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "copy_id", type: "INT", constraints: "FK -> book_copies.id NOT NULL" },
          { name: "member_id", type: "INT", constraints: "FK -> members.id NOT NULL" },
          { name: "borrowed_at", type: "DATE", constraints: "NOT NULL" },
          { name: "due_at", type: "DATE", constraints: "NOT NULL" },
          { name: "returned_at", type: "DATE", constraints: "" },
        ],
      },
    ],
    relationships: [
      "books 1---* book_copies",
      "members 1---* borrowings",
      "book_copies 1---* borrowings",
    ],
    validationRules: [
      { check: "table_exists", table: "book_copies", message: "Separate copies from books — great!", failMessage: "Need a 'book_copies' table (physical items)" },
      { check: "has_fk", table: "borrowings", targetTable: "book_copies", message: "Borrowings reference copies, not books", failMessage: "Borrowings should reference book_copies, not books" },
    ],
    learnings: ["Distinguish between abstract entities (book title) and physical entities (book copy)", "NULL columns can represent state (returned_at IS NULL = still borrowed)"],
  },
  {
    id: "a6",
    title: "Hotel Booking System",
    level: "advanced",
    mode: "build",
    scenario: "A hotel chain manages multiple properties, room types with pricing, and guest reservations.",
    requirements: [
      "Multiple hotels, each with name, city, and star rating",
      "Each hotel defines room types (Single, Deluxe, Suite) with price per night",
      "Track individual rooms by room number",
      "Guests make reservations for date ranges",
    ],
    hints: [
      "Hotels → room_types → rooms is a chain of one-to-many",
      "Reservations connect guests to specific rooms",
    ],
    solution: [
      {
        name: "hotels",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "city", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "star_rating", type: "INT", constraints: "" },
        ],
      },
      {
        name: "room_types",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "hotel_id", type: "INT", constraints: "FK -> hotels.id NOT NULL" },
          { name: "name", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "price_per_night", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "rooms",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "room_type_id", type: "INT", constraints: "FK -> room_types.id NOT NULL" },
          { name: "room_number", type: "VARCHAR(10)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "guests",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "reservations",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "guest_id", type: "INT", constraints: "FK -> guests.id NOT NULL" },
          { name: "room_id", type: "INT", constraints: "FK -> rooms.id NOT NULL" },
          { name: "check_in", type: "DATE", constraints: "NOT NULL" },
          { name: "check_out", type: "DATE", constraints: "NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'confirmed'" },
        ],
      },
    ],
    relationships: [
      "hotels 1---* room_types",
      "room_types 1---* rooms",
      "guests 1---* reservations",
      "rooms 1---* reservations",
    ],
    validationRules: [
      { check: "table_exists", table: "hotels", message: "Hotels table created", failMessage: "Missing 'hotels'" },
      { check: "table_exists", table: "room_types", message: "Room types separated from rooms", failMessage: "Need separate room_types table" },
      { check: "table_exists", table: "reservations", message: "Reservations table created", failMessage: "Missing 'reservations'" },
    ],
    learnings: ["Chain relationships: hotels → room_types → rooms", "Separate 'type' from 'instance' (room type vs actual room)"],
  },

  // ════════════════════════════════════════
  //  EXPERT — Real-World + Tradeoffs (6)
  // ════════════════════════════════════════
  {
    id: "e1",
    title: "Food Delivery Platform",
    level: "expert",
    mode: "build",
    scenario: "Design a food delivery system like Uber Eats. Restaurants list menu items, customers order, and drivers deliver.",
    requirements: [
      "Restaurants have menu items with prices and availability",
      "Customers place orders with multiple items and quantities",
      "Drivers are assigned to deliver orders",
      "Track order status: placed → preparing → picked_up → delivered",
      "Calculate order totals from line items",
    ],
    hints: [
      "This combines multiple patterns: one-to-many AND many-to-many",
      "order_items is the junction between orders and menu_items",
      "Think about who references whom",
    ],
    solution: [
      {
        name: "restaurants",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "address", type: "VARCHAR(300)", constraints: "NOT NULL" },
          { name: "cuisine_type", type: "VARCHAR(50)", constraints: "" },
        ],
      },
      {
        name: "menu_items",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "restaurant_id", type: "INT", constraints: "FK -> restaurants.id NOT NULL" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "is_available", type: "BOOLEAN", constraints: "DEFAULT TRUE" },
        ],
      },
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "address", type: "VARCHAR(300)", constraints: "" },
        ],
      },
      {
        name: "drivers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "phone", type: "VARCHAR(20)", constraints: "NOT NULL" },
          { name: "is_active", type: "BOOLEAN", constraints: "DEFAULT TRUE" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "restaurant_id", type: "INT", constraints: "FK -> restaurants.id NOT NULL" },
          { name: "driver_id", type: "INT", constraints: "FK -> drivers.id" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'placed'" },
          { name: "total_amount", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "order_items",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "order_id", type: "INT", constraints: "FK -> orders.id NOT NULL" },
          { name: "menu_item_id", type: "INT", constraints: "FK -> menu_items.id NOT NULL" },
          { name: "quantity", type: "INT", constraints: "NOT NULL DEFAULT 1" },
          { name: "unit_price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: [
      "restaurants 1---* menu_items",
      "customers 1---* orders",
      "restaurants 1---* orders",
      "drivers 1---* orders",
      "orders 1---* order_items",
      "menu_items 1---* order_items",
    ],
    validationRules: [
      { check: "table_exists", table: "restaurants", message: "Restaurants modeled", failMessage: "Missing 'restaurants'" },
      { check: "table_exists", table: "menu_items", message: "Menu items separated from restaurants", failMessage: "Missing 'menu_items'" },
      { check: "table_exists", table: "order_items", message: "Order items junction table exists", failMessage: "Missing 'order_items'" },
      { check: "has_fk", table: "orders", targetTable: "customers", message: "Orders linked to customers", failMessage: "Orders needs FK to customers" },
      { check: "has_fk", table: "orders", targetTable: "restaurants", message: "Orders linked to restaurants", failMessage: "Orders needs FK to restaurants" },
    ],
    learnings: [
      "Real systems combine multiple relationship patterns",
      "driver_id can be NULL (not yet assigned)",
      "Store unit_price on order_items — menu prices change",
    ],
  },
  {
    id: "e2",
    title: "Social Media Platform",
    level: "expert",
    mode: "build",
    scenario: "Design a Twitter-like platform with posts, comments, likes, and follows.",
    requirements: [
      "Users post short text messages",
      "Users comment on posts",
      "Users like posts (each user can like a post once)",
      "Users follow other users (asymmetric)",
    ],
    hints: [
      "Likes is a many-to-many junction with composite PK",
      "Follows is a self-referencing many-to-many",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "username", type: "VARCHAR(30)", constraints: "UNIQUE NOT NULL" },
          { name: "display_name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "bio", type: "VARCHAR(160)", constraints: "" },
        ],
      },
      {
        name: "posts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "content", type: "VARCHAR(280)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "comments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "post_id", type: "INT", constraints: "FK -> posts.id NOT NULL" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "content", type: "VARCHAR(280)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "likes",
        columns: [
          { name: "user_id", type: "INT", constraints: "FK -> users.id" },
          { name: "post_id", type: "INT", constraints: "FK -> posts.id" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "", type: "", constraints: "PRIMARY KEY (user_id, post_id)" },
        ],
      },
      {
        name: "follows",
        columns: [
          { name: "follower_id", type: "INT", constraints: "FK -> users.id" },
          { name: "following_id", type: "INT", constraints: "FK -> users.id" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "", type: "", constraints: "PRIMARY KEY (follower_id, following_id)" },
        ],
      },
    ],
    relationships: [
      "users 1---* posts",
      "users *---* posts via likes",
      "users *---* users via follows",
      "posts 1---* comments",
    ],
    validationRules: [
      { check: "table_exists", table: "likes", message: "Likes junction table created", failMessage: "Missing 'likes' table" },
      { check: "table_exists", table: "follows", message: "Follows self-referencing table created", failMessage: "Missing 'follows' table" },
    ],
    learnings: [
      "Composite primary keys prevent duplicate likes/follows",
      "Self-referencing relationships: both FKs point to the same table",
      "Junction tables can have extra columns (created_at)",
    ],
  },
  {
    id: "e3",
    title: "Fix: Everything in One Table",
    level: "expert",
    mode: "fix",
    scenario: "A developer put EVERYTHING in one giant table. It has 5000 rows with massive redundancy. Updating a restaurant's address requires changing hundreds of rows.",
    brokenDescription: "Orders, customers, and restaurants are all crammed into a single denormalized table.",
    brokenSchema: [
      {
        name: "order_data",
        columns: [
          { name: "order_id", type: "INT", constraints: "PRIMARY KEY" },
          { name: "customer_name", type: "VARCHAR(100)", constraints: "" },
          { name: "customer_email", type: "VARCHAR(255)", constraints: "" },
          { name: "restaurant_name", type: "VARCHAR(150)", constraints: "" },
          { name: "restaurant_address", type: "VARCHAR(300)", constraints: "" },
          { name: "item_name", type: "VARCHAR(100)", constraints: "" },
          { name: "item_price", type: "DECIMAL(10,2)", constraints: "" },
          { name: "quantity", type: "INT", constraints: "" },
          { name: "order_date", type: "TIMESTAMP", constraints: "" },
        ],
      },
    ],
    requirements: [
      "Normalize into proper separate tables",
      "Eliminate data redundancy",
      "Use foreign keys to connect tables",
      "Ensure updating a restaurant name only requires changing ONE row",
    ],
    hints: [
      "Identify the distinct entities: customers, restaurants, orders, order_items",
      "Each entity gets its own table with a PK",
      "Replace repeated data with foreign key references",
    ],
    solution: [
      {
        name: "customers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "restaurants",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "address", type: "VARCHAR(300)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "restaurant_id", type: "INT", constraints: "FK -> restaurants.id NOT NULL" },
          { name: "order_date", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "order_items",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "order_id", type: "INT", constraints: "FK -> orders.id NOT NULL" },
          { name: "item_name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "item_price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "quantity", type: "INT", constraints: "NOT NULL" },
        ],
      },
    ],
    relationships: [
      "customers 1---* orders",
      "restaurants 1---* orders",
      "orders 1---* order_items",
    ],
    validationRules: [
      { check: "table_exists", table: "customers", message: "Customers separated!", failMessage: "Need separate 'customers' table" },
      { check: "table_exists", table: "restaurants", message: "Restaurants separated!", failMessage: "Need separate 'restaurants' table" },
      { check: "table_exists", table: "orders", message: "Orders table created", failMessage: "Need separate 'orders' table" },
    ],
    learnings: [
      "Denormalized data causes update anomalies — changing one fact requires updating many rows",
      "Normalization eliminates redundancy",
      "Each fact should be stored in exactly ONE place",
    ],
  },
  {
    id: "e4",
    title: "Project Management Tool",
    level: "expert",
    mode: "build",
    scenario: "Design a Jira-like project management system with teams, projects, sprints, and tasks.",
    requirements: [
      "Teams contain multiple members (users)",
      "Projects belong to teams",
      "Sprints belong to projects and have start/end dates",
      "Tasks belong to sprints, have assignees, status, and priority",
      "Tasks can have comments from any team member",
    ],
    hints: [
      "team_members is a many-to-many junction between teams and users",
      "tasks has FKs to both sprints and users (assignee)",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "teams",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "team_members",
        columns: [
          { name: "team_id", type: "INT", constraints: "FK -> teams.id NOT NULL" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "role", type: "VARCHAR(50)", constraints: "DEFAULT 'member'" },
          { name: "", type: "", constraints: "PRIMARY KEY (team_id, user_id)" },
        ],
      },
      {
        name: "projects",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "team_id", type: "INT", constraints: "FK -> teams.id NOT NULL" },
          { name: "name", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
        ],
      },
      {
        name: "sprints",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "project_id", type: "INT", constraints: "FK -> projects.id NOT NULL" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "start_date", type: "DATE", constraints: "NOT NULL" },
          { name: "end_date", type: "DATE", constraints: "NOT NULL" },
        ],
      },
      {
        name: "tasks",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "sprint_id", type: "INT", constraints: "FK -> sprints.id NOT NULL" },
          { name: "assignee_id", type: "INT", constraints: "FK -> users.id" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'todo'" },
          { name: "priority", type: "VARCHAR(10)", constraints: "DEFAULT 'medium'" },
        ],
      },
      {
        name: "task_comments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "task_id", type: "INT", constraints: "FK -> tasks.id NOT NULL" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "body", type: "TEXT", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [
      "users *---* teams via team_members",
      "teams 1---* projects",
      "projects 1---* sprints",
      "sprints 1---* tasks",
      "users 1---* tasks (assignee)",
      "tasks 1---* task_comments",
    ],
    validationRules: [
      { check: "table_exists", table: "team_members", message: "Team membership modeled!", failMessage: "Need team_members junction table" },
      { check: "table_exists", table: "sprints", message: "Sprints table created", failMessage: "Missing 'sprints'" },
      { check: "table_exists", table: "tasks", message: "Tasks table created", failMessage: "Missing 'tasks'" },
    ],
    learnings: [
      "Complex systems are just combinations of simple patterns",
      "Chain: teams → projects → sprints → tasks",
      "team_members is many-to-many; tasks.assignee_id is one-to-many",
    ],
  },
];

export default CHALLENGES;
