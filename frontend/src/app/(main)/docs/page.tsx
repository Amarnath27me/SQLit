import Link from "next/link";

const DOC_SECTIONS = [
  {
    title: "Fundamentals",
    description: "SELECT, FROM, WHERE — the building blocks of every query",
    topics: [
      { slug: "select", title: "SELECT Statements", description: "Retrieve data from tables" },
      { slug: "where", title: "WHERE Clause", description: "Filter rows with conditions" },
      { slug: "operators", title: "Operators", description: "AND, OR, NOT, IN, BETWEEN, LIKE" },
      { slug: "order-by", title: "ORDER BY", description: "Sort your results" },
      { slug: "limit-offset", title: "LIMIT & OFFSET", description: "Paginate result sets" },
      { slug: "distinct", title: "DISTINCT", description: "Remove duplicate rows" },
    ],
  },
  {
    title: "Aggregations",
    description: "Summarize data with grouping and aggregate functions",
    topics: [
      { slug: "count", title: "COUNT", description: "Count rows and values" },
      { slug: "sum-avg", title: "SUM & AVG", description: "Calculate totals and averages" },
      { slug: "min-max", title: "MIN & MAX", description: "Find extreme values" },
      { slug: "group-by", title: "GROUP BY", description: "Group rows for aggregation" },
      { slug: "having", title: "HAVING", description: "Filter groups after aggregation" },
    ],
  },
  {
    title: "Joins",
    description: "Combine data from multiple tables",
    topics: [
      { slug: "inner-join", title: "INNER JOIN", description: "Matching rows from both tables" },
      { slug: "left-join", title: "LEFT JOIN", description: "All rows from left, matching from right" },
      { slug: "right-join", title: "RIGHT JOIN", description: "All rows from right, matching from left" },
      { slug: "full-join", title: "FULL OUTER JOIN", description: "All rows from both tables" },
      { slug: "self-join", title: "Self Join", description: "Join a table to itself" },
      { slug: "cross-join", title: "CROSS JOIN", description: "Cartesian product of two tables" },
    ],
  },
  {
    title: "Subqueries",
    description: "Queries within queries for complex logic",
    topics: [
      { slug: "scalar-subquery", title: "Scalar Subqueries", description: "Single value subqueries" },
      { slug: "derived-tables", title: "Derived Tables", description: "Subqueries in FROM clause" },
      { slug: "correlated", title: "Correlated Subqueries", description: "Row-by-row evaluation" },
      { slug: "exists", title: "EXISTS & NOT EXISTS", description: "Test for row existence" },
    ],
  },
  {
    title: "Window Functions",
    description: "Calculations across sets of rows related to the current row",
    topics: [
      { slug: "row-number", title: "ROW_NUMBER", description: "Assign sequential numbers" },
      { slug: "rank-dense-rank", title: "RANK & DENSE_RANK", description: "Rank with tie handling" },
      { slug: "lag-lead", title: "LAG & LEAD", description: "Access previous/next rows" },
      { slug: "running-totals", title: "Running Totals", description: "Cumulative calculations" },
      { slug: "ntile", title: "NTILE", description: "Divide rows into buckets" },
    ],
  },
  {
    title: "Advanced",
    description: "CTEs, CASE expressions, date functions, and more",
    topics: [
      { slug: "cte", title: "Common Table Expressions", description: "WITH clause for readable queries" },
      { slug: "recursive-cte", title: "Recursive CTEs", description: "Hierarchical data traversal" },
      { slug: "case", title: "CASE Expressions", description: "Conditional logic in SQL" },
      { slug: "union", title: "UNION & INTERSECT", description: "Combine result sets" },
      { slug: "date-functions", title: "Date Functions", description: "Work with dates and timestamps" },
      { slug: "string-functions", title: "String Functions", description: "Text manipulation" },
    ],
  },
];

export default function DocsPage() {
  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-bold">Documentation</h1>
        <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
          Comprehensive SQL reference from fundamentals to advanced topics.
          Each page includes syntax, real examples, common mistakes, and links
          to practice problems.
        </p>
      </div>

      <div className="mt-10 space-y-10">
        {DOC_SECTIONS.map((section) => (
          <div key={section.title}>
            <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
              {section.title}
            </h2>
            <p className="mt-1 text-sm text-[var(--color-text-muted)]">
              {section.description}
            </p>

            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {section.topics.map((topic) => (
                <Link
                  key={topic.slug}
                  href={`/docs/${topic.slug}`}
                  className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 transition-all hover:border-[var(--color-accent)] hover:shadow-sm"
                >
                  <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                    {topic.title}
                  </h3>
                  <p className="mt-1 text-xs text-[var(--color-text-muted)]">
                    {topic.description}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
