// === Problem Types ===

export type Difficulty = "easy" | "medium" | "hard";
export type Dialect = "postgresql" | "mysql";
export type Dataset = "ecommerce" | "finance" | "healthcare";

export type ProblemCategory =
  | "select"
  | "where"
  | "aggregation"
  | "joins"
  | "subqueries"
  | "window-functions"
  | "cte"
  | "advanced";

export interface Problem {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: ProblemCategory;
  dataset: Dataset;
  description: string;
  businessScenario: string;
  task: string;
  conceptTags: string[];
  acceptanceRate: number;
  schema: TableSchema[];
  hints: string[];
  explanation: string;
  approach: string;
  commonMistakes: string[];
}

export interface TableSchema {
  name: string;
  columns: ColumnDef[];
  sampleRows: Record<string, unknown>[];
}

export interface ColumnDef {
  name: string;
  type: string;
  isPrimaryKey: boolean;
  isForeignKey: boolean;
  references?: string; // "table.column"
  nullable: boolean;
}

// === Query Execution Types ===

export interface QueryRequest {
  query: string;
  problemId: string;
  dialect: Dialect;
  dataset: Dataset;
}

export interface QueryResult {
  success: boolean;
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

export interface QueryResponse {
  status: "accepted" | "wrong_answer" | "error";
  userResult: QueryResult | null;
  expectedResult: QueryResult | null;
  diff: ResultDiff | null;
  error: string | null;
  xpEarned: number;
}

export interface ResultDiff {
  matchingRows: number;
  totalExpectedRows: number;
  mismatchedRows: number[];
  mismatchedColumns: string[];
}

// === User Types ===

export interface User {
  id: string;
  displayName: string;
  email: string;
  avatar: string | null;
  xp: number;
  level: number;
  streak: number;
  solvedProblems: string[];
}

// === Gamification ===

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt: string | null;
}
