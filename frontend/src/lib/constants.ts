export const XP_REWARDS = {
  easy: 10,
  medium: 25,
  hard: 50,
} as const;

export const STREAK_MULTIPLIERS = {
  3: 1.2,
  7: 1.5,
  30: 2.0,
} as const;

export const QUERY_LIMITS = {
  timeoutMs: 3000,
  maxRows: 1000,
  ratePerMinute: 20,
} as const;

export const DATASETS = [
  { id: "ecommerce", name: "E-Commerce", tables: 8, rows: "~4,500" },
  { id: "finance", name: "Finance", tables: 7, rows: "~4,000" },
  { id: "healthcare", name: "Healthcare", tables: 8, rows: "~4,000" },
] as const;

export const DIALECTS = [
  { id: "postgresql", name: "PostgreSQL" },
  { id: "mysql", name: "MySQL" },
] as const;
