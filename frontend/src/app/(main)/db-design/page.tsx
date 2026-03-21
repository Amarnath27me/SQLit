"use client";

import { useState } from "react";
import ERBuilder from "@/components/db-design/ERBuilder";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface SolutionColumn {
  name: string;
  type: string;
  constraints: string;
}

interface SolutionTable {
  name: string;
  columns: SolutionColumn[];
}

interface DesignChallenge {
  id: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  scenario: string;
  requirements: string[];
  solution: SolutionTable[];
  relationships: string[];
}

interface NormForm {
  name: string;
  title: string;
  rule: string;
  example: string;
  violation: string;
}

interface RelationshipType {
  name: string;
  description: string;
  diagram: string[];
  example: string;
  implementation: string;
}

/* ------------------------------------------------------------------ */
/*  Design Challenges Data                                             */
/* ------------------------------------------------------------------ */

const CHALLENGES: DesignChallenge[] = [
  {
    id: "ch1",
    title: "Blog Platform",
    difficulty: "easy",
    scenario:
      "Design a schema for a blogging platform where users write posts, organize them into categories, and readers can leave comments.",
    requirements: [
      "Users have a name, email, and bio",
      "Posts have a title, body, publish date, and status (draft/published)",
      "Each post belongs to one author but can have multiple categories",
      "Readers can comment on posts with a name and message",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "bio", type: "TEXT", constraints: "" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "categories",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(50)", constraints: "UNIQUE NOT NULL" },
          { name: "slug", type: "VARCHAR(60)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "posts",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "author_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "body", type: "TEXT", constraints: "NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'draft'" },
          { name: "published_at", type: "TIMESTAMP", constraints: "" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "post_categories",
        columns: [
          { name: "post_id", type: "INT", constraints: "FK -> posts.id" },
          { name: "category_id", type: "INT", constraints: "FK -> categories.id" },
          { name: "", type: "", constraints: "PRIMARY KEY (post_id, category_id)" },
        ],
      },
      {
        name: "comments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "post_id", type: "INT", constraints: "FK -> posts.id NOT NULL" },
          { name: "author_name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "message", type: "TEXT", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [
      "users 1---* posts (one author, many posts)",
      "posts *---* categories (via post_categories junction table)",
      "posts 1---* comments (one post, many comments)",
    ],
  },
  {
    id: "ch2",
    title: "Library System",
    difficulty: "easy",
    scenario:
      "Design a schema for a public library that tracks books, members, and borrowing activity. The library may own multiple copies of the same book.",
    requirements: [
      "Books have ISBN, title, author, genre, and publication year",
      "The library can have multiple physical copies of each book",
      "Members have a name, email, phone, and membership date",
      "Track which member borrowed which copy, with due date and return date",
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
          { name: "pub_year", type: "INT", constraints: "" },
        ],
      },
      {
        name: "book_copies",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "book_id", type: "INT", constraints: "FK -> books.id NOT NULL" },
          { name: "condition", type: "VARCHAR(20)", constraints: "DEFAULT 'good'" },
          { name: "acquired_at", type: "DATE", constraints: "DEFAULT CURRENT_DATE" },
        ],
      },
      {
        name: "members",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "phone", type: "VARCHAR(20)", constraints: "" },
          { name: "member_since", type: "DATE", constraints: "DEFAULT CURRENT_DATE" },
        ],
      },
      {
        name: "borrowings",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "copy_id", type: "INT", constraints: "FK -> book_copies.id NOT NULL" },
          { name: "member_id", type: "INT", constraints: "FK -> members.id NOT NULL" },
          { name: "borrowed_at", type: "DATE", constraints: "NOT NULL DEFAULT CURRENT_DATE" },
          { name: "due_at", type: "DATE", constraints: "NOT NULL" },
          { name: "returned_at", type: "DATE", constraints: "" },
        ],
      },
    ],
    relationships: [
      "books 1---* book_copies (one title, many physical copies)",
      "members 1---* borrowings (one member, many borrowings over time)",
      "book_copies 1---* borrowings (each copy can be borrowed many times)",
    ],
  },
  {
    id: "ch3",
    title: "Social Media Platform",
    difficulty: "medium",
    scenario:
      "Design a schema for a Twitter-like social media app with posts, comments, likes, and a follower system.",
    requirements: [
      "Users have a username, display name, bio, and avatar URL",
      "Users can create short text posts (max 280 chars)",
      "Users can comment on posts",
      "Users can like posts",
      "Users can follow other users (asymmetric relationship)",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "username", type: "VARCHAR(30)", constraints: "UNIQUE NOT NULL" },
          { name: "display_name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "bio", type: "VARCHAR(160)", constraints: "" },
          { name: "avatar_url", type: "VARCHAR(500)", constraints: "" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
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
      "users 1---* posts (one user, many posts)",
      "users 1---* comments (one user, many comments)",
      "posts 1---* comments (one post, many comments)",
      "users *---* posts via likes (many-to-many through junction table)",
      "users *---* users via follows (self-referencing many-to-many)",
    ],
  },
  {
    id: "ch4",
    title: "Food Delivery App",
    difficulty: "medium",
    scenario:
      "Design a schema for a food delivery platform where restaurants list menu items, customers place orders, and drivers deliver them.",
    requirements: [
      "Restaurants have a name, address, cuisine type, and rating",
      "Each restaurant has menu items with name, description, price, and availability",
      "Customers place orders containing multiple menu items with quantities",
      "Orders track status: placed, preparing, picked_up, delivered",
      "Delivery drivers are assigned to orders",
    ],
    solution: [
      {
        name: "restaurants",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "address", type: "VARCHAR(300)", constraints: "NOT NULL" },
          { name: "cuisine_type", type: "VARCHAR(50)", constraints: "" },
          { name: "rating", type: "DECIMAL(2,1)", constraints: "DEFAULT 0.0" },
        ],
      },
      {
        name: "menu_items",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "restaurant_id", type: "INT", constraints: "FK -> restaurants.id NOT NULL" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
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
          { name: "phone", type: "VARCHAR(20)", constraints: "" },
          { name: "address", type: "VARCHAR(300)", constraints: "" },
        ],
      },
      {
        name: "drivers",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "phone", type: "VARCHAR(20)", constraints: "NOT NULL" },
          { name: "vehicle_type", type: "VARCHAR(30)", constraints: "" },
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
      "restaurants 1---* menu_items (one restaurant, many items)",
      "customers 1---* orders (one customer, many orders)",
      "restaurants 1---* orders (one restaurant, many orders)",
      "drivers 1---* orders (one driver, many deliveries)",
      "orders 1---* order_items (one order, many line items)",
      "menu_items 1---* order_items (one item can appear in many orders)",
    ],
  },
  {
    id: "ch5",
    title: "Hotel Booking System",
    difficulty: "medium",
    scenario:
      "Design a schema for a hotel chain that manages multiple properties, room types, and guest reservations.",
    requirements: [
      "Multiple hotels, each with a name, city, and star rating",
      "Each hotel defines room types (e.g., Single, Deluxe, Suite) with price per night",
      "Track individual rooms by room number",
      "Guests make reservations for a date range at a specific hotel and room type",
      "Support reservation statuses: confirmed, checked_in, checked_out, cancelled",
    ],
    solution: [
      {
        name: "hotels",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "city", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "star_rating", type: "INT", constraints: "CHECK (star_rating BETWEEN 1 AND 5)" },
        ],
      },
      {
        name: "room_types",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "hotel_id", type: "INT", constraints: "FK -> hotels.id NOT NULL" },
          { name: "name", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
          { name: "price_per_night", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "max_guests", type: "INT", constraints: "DEFAULT 2" },
        ],
      },
      {
        name: "rooms",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "hotel_id", type: "INT", constraints: "FK -> hotels.id NOT NULL" },
          { name: "room_type_id", type: "INT", constraints: "FK -> room_types.id NOT NULL" },
          { name: "room_number", type: "VARCHAR(10)", constraints: "NOT NULL" },
          { name: "floor", type: "INT", constraints: "" },
        ],
      },
      {
        name: "guests",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "phone", type: "VARCHAR(20)", constraints: "" },
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
          { name: "total_price", type: "DECIMAL(10,2)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [
      "hotels 1---* room_types (one hotel, many room types)",
      "hotels 1---* rooms (one hotel, many rooms)",
      "room_types 1---* rooms (one type, many rooms of that type)",
      "guests 1---* reservations (one guest, many reservations)",
      "rooms 1---* reservations (one room, many reservations over time)",
    ],
  },
  {
    id: "ch6",
    title: "E-Commerce Store",
    difficulty: "medium",
    scenario:
      "Design a schema for an online store with product catalog, customer accounts, orders, and reviews.",
    requirements: [
      "Products have a name, description, price, SKU, and stock quantity",
      "Products belong to hierarchical categories (categories can have parent categories)",
      "Customers can place orders with multiple products",
      "Customers can leave a star rating and review on products they purchased",
      "Track order status and shipping address",
    ],
    solution: [
      {
        name: "categories",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "parent_id", type: "INT", constraints: "FK -> categories.id (self-ref)" },
        ],
      },
      {
        name: "products",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "category_id", type: "INT", constraints: "FK -> categories.id" },
          { name: "name", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
          { name: "sku", type: "VARCHAR(50)", constraints: "UNIQUE NOT NULL" },
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
          { name: "password_hash", type: "VARCHAR(255)", constraints: "NOT NULL" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "orders",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "status", type: "VARCHAR(20)", constraints: "DEFAULT 'pending'" },
          { name: "shipping_address", type: "TEXT", constraints: "NOT NULL" },
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
      {
        name: "reviews",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "product_id", type: "INT", constraints: "FK -> products.id NOT NULL" },
          { name: "customer_id", type: "INT", constraints: "FK -> customers.id NOT NULL" },
          { name: "rating", type: "INT", constraints: "NOT NULL CHECK (rating BETWEEN 1 AND 5)" },
          { name: "comment", type: "TEXT", constraints: "" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [
      "categories 1---* categories (self-referencing hierarchy)",
      "categories 1---* products (one category, many products)",
      "customers 1---* orders (one customer, many orders)",
      "orders 1---* order_items (one order, many line items)",
      "products 1---* order_items (one product, many order appearances)",
      "customers 1---* reviews (one customer, many reviews)",
      "products 1---* reviews (one product, many reviews)",
    ],
  },
  {
    id: "ch7",
    title: "Multi-tenant SaaS (Project Management)",
    difficulty: "hard",
    scenario:
      "Design a schema for a multi-tenant project management tool (like Jira) where organizations manage projects, boards, tasks, and team members with roles.",
    requirements: [
      "Organizations have a name and subscription plan",
      "Users belong to organizations with a role (admin, member, viewer)",
      "Organizations have projects; projects have boards; boards have columns; columns have tasks",
      "Tasks have a title, description, assignee, priority, status, and due date",
      "Tasks support comments and an activity audit log",
    ],
    solution: [
      {
        name: "organizations",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "plan", type: "VARCHAR(20)", constraints: "DEFAULT 'free'" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
        ],
      },
      {
        name: "org_members",
        columns: [
          { name: "org_id", type: "INT", constraints: "FK -> organizations.id" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id" },
          { name: "role", type: "VARCHAR(20)", constraints: "NOT NULL DEFAULT 'member'" },
          { name: "", type: "", constraints: "PRIMARY KEY (org_id, user_id)" },
        ],
      },
      {
        name: "projects",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "org_id", type: "INT", constraints: "FK -> organizations.id NOT NULL" },
          { name: "name", type: "VARCHAR(150)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
        ],
      },
      {
        name: "boards",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "project_id", type: "INT", constraints: "FK -> projects.id NOT NULL" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "board_columns",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "board_id", type: "INT", constraints: "FK -> boards.id NOT NULL" },
          { name: "name", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "position", type: "INT", constraints: "NOT NULL DEFAULT 0" },
        ],
      },
      {
        name: "tasks",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "column_id", type: "INT", constraints: "FK -> board_columns.id NOT NULL" },
          { name: "assignee_id", type: "INT", constraints: "FK -> users.id" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
          { name: "priority", type: "VARCHAR(10)", constraints: "DEFAULT 'medium'" },
          { name: "due_date", type: "DATE", constraints: "" },
          { name: "position", type: "INT", constraints: "NOT NULL DEFAULT 0" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
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
      {
        name: "activity_log",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "org_id", type: "INT", constraints: "FK -> organizations.id NOT NULL" },
          { name: "user_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "entity_type", type: "VARCHAR(30)", constraints: "NOT NULL" },
          { name: "entity_id", type: "INT", constraints: "NOT NULL" },
          { name: "action", type: "VARCHAR(50)", constraints: "NOT NULL" },
          { name: "details", type: "JSONB", constraints: "" },
          { name: "created_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
        ],
      },
    ],
    relationships: [
      "organizations 1---* org_members, projects (scoping everything to an org)",
      "users *---* organizations via org_members (many-to-many with role)",
      "projects 1---* boards 1---* board_columns 1---* tasks (hierarchical)",
      "users 1---* tasks (assignee), task_comments, activity_log",
      "activity_log uses polymorphic entity_type + entity_id pattern",
    ],
  },
  {
    id: "ch8",
    title: "E-Learning Platform",
    difficulty: "hard",
    scenario:
      "Design a schema for an online learning platform where instructors create courses with modules and lessons, students enroll, take quizzes, and earn certificates.",
    requirements: [
      "Instructors create courses with a title, description, price, and level",
      "Courses contain ordered modules; modules contain ordered lessons",
      "Lessons can be video, text, or quiz type",
      "Quizzes have multiple-choice questions with one correct answer",
      "Students enroll in courses and their progress is tracked per-lesson",
      "Students earn a certificate upon completing all lessons",
    ],
    solution: [
      {
        name: "users",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "name", type: "VARCHAR(100)", constraints: "NOT NULL" },
          { name: "email", type: "VARCHAR(255)", constraints: "UNIQUE NOT NULL" },
          { name: "role", type: "VARCHAR(20)", constraints: "NOT NULL" },
        ],
      },
      {
        name: "courses",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "instructor_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "description", type: "TEXT", constraints: "" },
          { name: "price", type: "DECIMAL(10,2)", constraints: "DEFAULT 0.00" },
          { name: "level", type: "VARCHAR(20)", constraints: "DEFAULT 'beginner'" },
          { name: "published", type: "BOOLEAN", constraints: "DEFAULT FALSE" },
        ],
      },
      {
        name: "modules",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "course_id", type: "INT", constraints: "FK -> courses.id NOT NULL" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "position", type: "INT", constraints: "NOT NULL" },
        ],
      },
      {
        name: "lessons",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "module_id", type: "INT", constraints: "FK -> modules.id NOT NULL" },
          { name: "title", type: "VARCHAR(200)", constraints: "NOT NULL" },
          { name: "type", type: "VARCHAR(10)", constraints: "NOT NULL (video/text/quiz)" },
          { name: "content_url", type: "VARCHAR(500)", constraints: "" },
          { name: "content_text", type: "TEXT", constraints: "" },
          { name: "position", type: "INT", constraints: "NOT NULL" },
        ],
      },
      {
        name: "quiz_questions",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "lesson_id", type: "INT", constraints: "FK -> lessons.id NOT NULL" },
          { name: "question_text", type: "TEXT", constraints: "NOT NULL" },
          { name: "position", type: "INT", constraints: "NOT NULL" },
        ],
      },
      {
        name: "quiz_options",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "question_id", type: "INT", constraints: "FK -> quiz_questions.id NOT NULL" },
          { name: "option_text", type: "VARCHAR(300)", constraints: "NOT NULL" },
          { name: "is_correct", type: "BOOLEAN", constraints: "DEFAULT FALSE" },
        ],
      },
      {
        name: "enrollments",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "student_id", type: "INT", constraints: "FK -> users.id NOT NULL" },
          { name: "course_id", type: "INT", constraints: "FK -> courses.id NOT NULL" },
          { name: "enrolled_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "", type: "", constraints: "UNIQUE (student_id, course_id)" },
        ],
      },
      {
        name: "lesson_progress",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "enrollment_id", type: "INT", constraints: "FK -> enrollments.id NOT NULL" },
          { name: "lesson_id", type: "INT", constraints: "FK -> lessons.id NOT NULL" },
          { name: "completed", type: "BOOLEAN", constraints: "DEFAULT FALSE" },
          { name: "completed_at", type: "TIMESTAMP", constraints: "" },
          { name: "", type: "", constraints: "UNIQUE (enrollment_id, lesson_id)" },
        ],
      },
      {
        name: "certificates",
        columns: [
          { name: "id", type: "SERIAL", constraints: "PRIMARY KEY" },
          { name: "enrollment_id", type: "INT", constraints: "FK -> enrollments.id UNIQUE NOT NULL" },
          { name: "issued_at", type: "TIMESTAMP", constraints: "DEFAULT NOW()" },
          { name: "certificate_url", type: "VARCHAR(500)", constraints: "" },
        ],
      },
    ],
    relationships: [
      "users (instructor) 1---* courses",
      "courses 1---* modules 1---* lessons (ordered hierarchy)",
      "lessons (quiz type) 1---* quiz_questions 1---* quiz_options",
      "users (student) *---* courses via enrollments",
      "enrollments 1---* lesson_progress (track per-lesson completion)",
      "enrollments 1---1 certificates (issued on completion)",
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Normalization Guide Data                                           */
/* ------------------------------------------------------------------ */

const NORMAL_FORMS: NormForm[] = [
  {
    name: "1NF",
    title: "First Normal Form",
    rule: "Each column holds atomic (indivisible) values. No repeating groups or arrays within a single column.",
    example: "Instead of storing \"tags: sql,joins,database\" in one column, create a separate tags table with one tag per row.",
    violation: "A column storing comma-separated values like \"Math, Science, English\" for a student's subjects.",
  },
  {
    name: "2NF",
    title: "Second Normal Form",
    rule: "Must be in 1NF. Every non-key column must depend on the entire primary key, not just part of it.",
    example: "In a table with composite PK (student_id, course_id), the student_name depends only on student_id -- move it to a students table.",
    violation: "Table (student_id, course_id, student_name, grade) -- student_name only depends on student_id, not the full PK.",
  },
  {
    name: "3NF",
    title: "Third Normal Form",
    rule: "Must be in 2NF. No transitive dependencies -- non-key columns must not depend on other non-key columns.",
    example: "If orders has customer_id and customer_city, the city depends on the customer, not the order. Move city to the customers table.",
    violation: "Table orders (id, customer_id, customer_city) -- customer_city depends on customer_id, not on the order id.",
  },
  {
    name: "BCNF",
    title: "Boyce-Codd Normal Form",
    rule: "Must be in 3NF. Every determinant (column that uniquely determines another) must be a candidate key.",
    example: "If a professor can teach only one subject, and a subject can be taught by many professors, (student, subject) -> professor but professor -> subject creates a BCNF violation.",
    violation: "Rarely encountered in practice. Most 3NF schemas are already in BCNF.",
  },
];

const DENORMALIZATION_TIPS = [
  {
    title: "When to Denormalize",
    description: "Denormalize for read-heavy workloads where JOINs become a bottleneck. Common in analytics dashboards, search results, and reporting tables.",
  },
  {
    title: "Computed Columns",
    description: "Store pre-computed values like order_total or follower_count to avoid expensive COUNT/SUM queries on every read.",
  },
  {
    title: "Common Anti-Patterns",
    description: "Avoid: storing JSON blobs instead of proper tables, using EAV (Entity-Attribute-Value) pattern when a fixed schema works, creating \"god tables\" with 50+ columns.",
  },
];

/* ------------------------------------------------------------------ */
/*  Relationship Types Data                                            */
/* ------------------------------------------------------------------ */

const RELATIONSHIP_TYPES: RelationshipType[] = [
  {
    name: "One-to-One (1:1)",
    description: "Each row in Table A relates to exactly one row in Table B, and vice versa. Used to split a table for security or performance reasons.",
    diagram: [
      "users             user_profiles",
      "-------           ---------------",
      "id (PK)    <---   user_id (PK, FK)",
      "email             bio",
      "name              avatar_url",
    ],
    example: "A users table and a user_profiles table. Each user has exactly one profile. Splitting keeps the frequently-queried users table small.",
    implementation: "Put the FK on either side, with a UNIQUE constraint. Or use the same PK value in both tables (shared primary key).",
  },
  {
    name: "One-to-Many (1:N)",
    description: "Each row in Table A can relate to many rows in Table B, but each row in Table B relates to only one row in Table A. This is the most common relationship.",
    diagram: [
      "departments       employees",
      "-----------       ----------",
      "id (PK)    <---   department_id (FK)",
      "name              id (PK)",
      "                  name",
      "                  salary",
    ],
    example: "A departments table and an employees table. One department has many employees, but each employee belongs to one department.",
    implementation: "Add a FK column on the \"many\" side (employees.department_id references departments.id).",
  },
  {
    name: "Many-to-Many (M:N)",
    description: "Each row in Table A can relate to many rows in Table B, and vice versa. Requires a junction (bridge/join) table to resolve the relationship.",
    diagram: [
      "students          enrollments          courses",
      "---------         -----------          --------",
      "id (PK)   <---    student_id (FK)      id (PK)",
      "name              course_id (FK)  ---> name",
      "                  enrolled_at          credits",
      "                  PK(student_id,",
      "                     course_id)",
    ],
    example: "Students and courses. One student takes many courses, and one course has many students. The enrollments junction table connects them.",
    implementation: "Create a junction table with FKs to both sides. The composite PK (or UNIQUE constraint) prevents duplicate pairs. Add extra columns for relationship metadata (e.g., enrolled_at, grade).",
  },
];

/* ------------------------------------------------------------------ */
/*  Best Practices Data                                                */
/* ------------------------------------------------------------------ */

const BEST_PRACTICES = [
  {
    category: "Naming Conventions",
    tips: [
      "Use snake_case for table and column names (user_profiles, created_at)",
      "Table names should be plural nouns (users, orders, products)",
      "Foreign key columns should be named [singular_table]_id (user_id, order_id)",
      "Boolean columns should read as questions (is_active, has_verified, can_edit)",
      "Avoid reserved SQL keywords as names (order, user, group -- use orders, users, groups)",
    ],
  },
  {
    category: "Indexing Strategies",
    tips: [
      "Always index foreign key columns -- they are used in JOINs and lookups",
      "Add indexes on columns used in WHERE, ORDER BY, and GROUP BY clauses",
      "Use composite indexes for queries that filter on multiple columns, matching the column order",
      "Avoid over-indexing -- each index slows down INSERT/UPDATE operations",
      "Consider partial indexes for queries that filter on a subset (e.g., WHERE active = true)",
    ],
  },
  {
    category: "Data Type Selection",
    tips: [
      "Use SERIAL or BIGSERIAL for auto-incrementing primary keys (or UUID for distributed systems)",
      "Use VARCHAR(n) with a realistic limit, not TEXT for everything (it documents intent)",
      "Use DECIMAL(p,s) for monetary values -- never FLOAT or DOUBLE (precision loss)",
      "Use TIMESTAMP WITH TIME ZONE for dates/times that cross time zones",
      "Use BOOLEAN for true/false -- avoid INT with 0/1 convention",
    ],
  },
  {
    category: "Schema Design Tips",
    tips: [
      "Every table should have a primary key -- prefer surrogate keys (id) for stability",
      "Add created_at and updated_at timestamps to most tables for auditing",
      "Store computed values (totals, counts) only when query performance requires it",
      "Use CHECK constraints to enforce business rules at the database level",
      "Design for the queries you will run -- the access pattern matters more than the data model",
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  Difficulty badge component                                         */
/* ------------------------------------------------------------------ */

function DifficultyBadge({ level }: { level: "easy" | "medium" | "hard" }) {
  const styles = {
    easy: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
    medium: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    hard: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
  };
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide ${styles[level]}`}>
      {level}
    </span>
  );
}

/* ------------------------------------------------------------------ */
/*  Solution table renderer                                            */
/* ------------------------------------------------------------------ */

function SolutionSchema({ tables, relationships }: { tables: SolutionTable[]; relationships: string[] }) {
  return (
    <div className="space-y-4">
      {tables.map((table) => (
        <div
          key={table.name}
          className="overflow-hidden rounded-lg border border-[var(--color-border)]"
        >
          <div className="border-b border-[var(--color-border)] bg-[var(--color-accent)]/10 px-4 py-2">
            <span className="text-xs font-bold text-[var(--color-accent)]">{table.name}</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[var(--color-border)] bg-[var(--color-background)]">
                  <th className="px-4 py-1.5 font-medium text-[var(--color-text-muted)]">Column</th>
                  <th className="px-4 py-1.5 font-medium text-[var(--color-text-muted)]">Type</th>
                  <th className="px-4 py-1.5 font-medium text-[var(--color-text-muted)]">Constraints</th>
                </tr>
              </thead>
              <tbody>
                {table.columns.map((col, i) => (
                  <tr key={i} className="border-b border-[var(--color-border)] last:border-0">
                    <td className="px-4 py-1.5">
                      {col.name ? (
                        <span className="font-medium text-[var(--color-text-primary)]">
                          {col.constraints.includes("PRIMARY KEY") && !col.constraints.includes("(") && (
                            <span className="mr-1.5 text-amber-500" title="Primary Key">PK</span>
                          )}
                          {col.constraints.includes("FK") && (
                            <span className="mr-1.5 text-blue-500" title="Foreign Key">FK</span>
                          )}
                          {col.name}
                        </span>
                      ) : (
                        <span className="italic text-[var(--color-text-muted)]">--</span>
                      )}
                    </td>
                    <td className="px-4 py-1.5 text-[var(--color-text-secondary)]">{col.type}</td>
                    <td className="px-4 py-1.5 text-[var(--color-text-muted)]">{col.constraints}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}

      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
        <h5 className="text-xs font-semibold text-[var(--color-text-primary)]">Relationships</h5>
        <ul className="mt-2 space-y-1">
          {relationships.map((rel, i) => (
            <li key={i} className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]">
              <span className="mt-0.5 shrink-0 text-[var(--color-accent)]">--</span>
              <span className="font-mono">{rel}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Page Component                                                     */
/* ------------------------------------------------------------------ */

export default function DBDesignPage() {
  const [revealedSolutions, setRevealedSolutions] = useState<Set<string>>(new Set());
  const [activeSection, setActiveSection] = useState<"challenges" | "normalization" | "relationships" | "best-practices" | "er-builder">("challenges");

  const toggleSolution = (id: string) => {
    setRevealedSolutions((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const SECTIONS = [
    { key: "challenges" as const, label: "Design Challenges" },
    { key: "normalization" as const, label: "Normalization" },
    { key: "relationships" as const, label: "Relationships" },
    { key: "best-practices" as const, label: "Best Practices" },
    { key: "er-builder" as const, label: "ER Builder" },
  ];

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">Database Design</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          Learn to design effective database schemas. Practice with real-world scenarios, study normalization rules, and master relationship patterns.
        </p>
      </div>

      {/* Section Tabs */}
      <div className="mt-6 flex items-center gap-1 border-b border-[var(--color-border)]">
        {SECTIONS.map((s) => (
          <button
            key={s.key}
            onClick={() => setActiveSection(s.key)}
            className={`border-b-2 px-4 py-2 text-sm font-medium transition-colors ${
              activeSection === s.key
                ? "border-[var(--color-accent)] text-[var(--color-accent)]"
                : "border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* ============================================================ */}
      {/*  DESIGN CHALLENGES                                            */}
      {/* ============================================================ */}
      {activeSection === "challenges" && (
        <div className="mt-6 space-y-4">
          <p className="text-sm text-[var(--color-text-muted)]">
            Read the business scenario, think about what tables and columns you would need, then reveal the solution to compare.
          </p>

          {CHALLENGES.map((ch) => (
            <div
              key={ch.id}
              className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]"
            >
              {/* Challenge header */}
              <div className="flex items-center justify-between p-5">
                <div className="flex items-center gap-3">
                  <DifficultyBadge level={ch.difficulty} />
                  <span className="text-sm font-semibold text-[var(--color-text-primary)]">{ch.title}</span>
                </div>
                <button
                  onClick={() => toggleSolution(ch.id)}
                  className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                    revealedSolutions.has(ch.id)
                      ? "bg-[var(--color-accent)] text-white"
                      : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
                  }`}
                >
                  {revealedSolutions.has(ch.id) ? "Hide Solution" : "Show Solution"}
                </button>
              </div>

              {/* Scenario + Requirements */}
              <div className="border-t border-[var(--color-border)] px-5 pb-5 pt-4 space-y-3">
                <p className="text-sm text-[var(--color-text-secondary)]">{ch.scenario}</p>

                <div>
                  <h4 className="text-xs font-semibold text-[var(--color-text-primary)]">Requirements</h4>
                  <ul className="mt-2 space-y-1">
                    {ch.requirements.map((req, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-[var(--color-text-secondary)]">
                        <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
                        {req}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Revealed solution */}
                {revealedSolutions.has(ch.id) && (
                  <div className="mt-4 rounded-lg border border-dashed border-[var(--color-accent)]/30 bg-[var(--color-background)] p-4">
                    <h4 className="mb-3 text-xs font-bold uppercase tracking-wide text-[var(--color-accent)]">
                      Recommended Schema
                    </h4>
                    <SolutionSchema tables={ch.solution} relationships={ch.relationships} />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ============================================================ */}
      {/*  NORMALIZATION GUIDE                                          */}
      {/* ============================================================ */}
      {activeSection === "normalization" && (
        <div className="mt-6 space-y-6">
          {/* Normal Forms */}
          <div className="grid gap-4 sm:grid-cols-2">
            {NORMAL_FORMS.map((nf) => (
              <div
                key={nf.name}
                className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
              >
                <div className="flex items-center gap-2">
                  <span className="rounded-md bg-[var(--color-accent)]/10 px-2 py-1 text-xs font-bold text-[var(--color-accent)]">
                    {nf.name}
                  </span>
                  <span className="text-sm font-semibold text-[var(--color-text-primary)]">{nf.title}</span>
                </div>
                <p className="mt-3 text-sm text-[var(--color-text-secondary)]">{nf.rule}</p>

                <div className="mt-3 rounded-lg bg-[var(--color-background)] p-3">
                  <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400">Example Fix</p>
                  <p className="mt-1 text-xs text-[var(--color-text-secondary)]">{nf.example}</p>
                </div>

                <div className="mt-2 rounded-lg bg-red-50 p-3 dark:bg-red-950/30">
                  <p className="text-xs font-medium text-red-600 dark:text-red-400">Violation</p>
                  <p className="mt-1 text-xs text-[var(--color-text-secondary)]">{nf.violation}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Denormalization Tips */}
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
            <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Denormalization & Anti-Patterns</h3>
            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              {DENORMALIZATION_TIPS.map((tip, i) => (
                <div key={i} className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
                  <h4 className="text-xs font-semibold text-[var(--color-text-primary)]">{tip.title}</h4>
                  <p className="mt-2 text-xs leading-relaxed text-[var(--color-text-secondary)]">{tip.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/*  RELATIONSHIP TYPES                                           */}
      {/* ============================================================ */}
      {activeSection === "relationships" && (
        <div className="mt-6 space-y-6">
          {RELATIONSHIP_TYPES.map((rel) => (
            <div
              key={rel.name}
              className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
            >
              <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">{rel.name}</h3>
              <p className="mt-2 text-sm text-[var(--color-text-secondary)]">{rel.description}</p>

              {/* ASCII diagram */}
              <pre className="mt-4 overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-code-bg)] p-4 text-xs leading-relaxed text-emerald-700 dark:text-emerald-400">
                <code>{rel.diagram.join("\n")}</code>
              </pre>

              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <div className="rounded-lg bg-[var(--color-background)] p-3">
                  <p className="text-xs font-medium text-[var(--color-accent)]">Real-World Example</p>
                  <p className="mt-1 text-xs text-[var(--color-text-secondary)]">{rel.example}</p>
                </div>
                <div className="rounded-lg bg-[var(--color-background)] p-3">
                  <p className="text-xs font-medium text-[var(--color-accent)]">Implementation</p>
                  <p className="mt-1 text-xs text-[var(--color-text-secondary)]">{rel.implementation}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ============================================================ */}
      {/*  BEST PRACTICES                                               */}
      {/* ============================================================ */}
      {activeSection === "best-practices" && (
        <div className="mt-6 space-y-4">
          {BEST_PRACTICES.map((section) => (
            <div
              key={section.category}
              className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
            >
              <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">{section.category}</h3>
              <ul className="mt-3 space-y-2">
                {section.tips.map((tip, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-[var(--color-text-secondary)]">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {/* ============================================================ */}
      {/*  ER BUILDER                                                    */}
      {/* ============================================================ */}
      {activeSection === "er-builder" && <ERBuilder />}
    </div>
  );
}
