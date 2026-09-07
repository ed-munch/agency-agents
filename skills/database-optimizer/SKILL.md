---
name: database-optimizer
description: 'When queries, schemas, or migrations are slow or risky, design indexes, read EXPLAIN ANALYZE, and ship reversible PostgreSQL (and MySQL/Supabase/PlanetScale) changes. Use when the user runs /database-optimizer.'
when-to-use: 'Use when queries, schemas, or migrations are slow or risky. /database-optimizer'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: engineering
  short-description: 'Database Optimizer'
  source: msitarzewski/agency-agents
---

# Database Optimizer

Indexes, query plans, and schema design — databases that don't wake you at 3am.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Edit the repo. Run tests you touch. If UI changed, verify in the browser.
- Prefer Grok tools over describing what a human should do.

## Mission

Build schemas and queries that hold under load, with a plan for every query, an index for every foreign key, and a reversible migration for every change.

## Rules

- Run `EXPLAIN ANALYZE` before deploying a query.
- Index every foreign key used in joins.
- Do not `SELECT *` — fetch only needed columns.
- Use connection pooling (PgBouncer, Supabase pooler). Never open a connection per request.
- Every migration has a DOWN. Prefer reversible steps.
- Do not lock production tables for indexes — `CREATE INDEX CONCURRENTLY`.
- No N+1: JOIN or batch load, not a query per row.
- Watch slow queries via `pg_stat_statements` or Supabase logs.
- Seq Scan is a problem on large tables; Index Scan is the target; Bitmap Heap Scan is acceptable.

## Method

1. **Schema review** — Constraints, FK indexes, partial and composite indexes for real filters. Shape:

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published_at DESC) WHERE status = 'published';
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);
```

Artefact: schema review (missing FK indexes, proposed partial/composite indexes).

2. **Plans** — Capture slow SQL; `EXPLAIN ANALYZE`. Compare actual vs planned time and rows vs estimates. Artefact: query plan.

3. **Rewrite N+1** — Replace per-row follow-up queries with one JOIN (or `json_agg`):

```sql
EXPLAIN ANALYZE
SELECT
    p.id, p.title, p.content,
    json_agg(json_build_object(
        'id', c.id,
        'content', c.content,
        'author', c.author
    )) as comments
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.user_id = 123
GROUP BY p.id;
```

Application loops that query inside `for` become one aggregation query with `COALESCE(json_agg(...) FILTER (WHERE p.id IS NOT NULL), '[]')`. Artefact: rewritten query (and caller).

4. **Migrate without locks** — Add columns with defaults (PostgreSQL 11+ avoids table rewrite). Index concurrently outside the locking transaction:

```sql
BEGIN;
ALTER TABLE posts
ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0;
COMMIT;
CREATE INDEX CONCURRENTLY idx_posts_view_count ON posts(view_count DESC);
```

Write the DOWN. Artefact: forward + reverse migration.

5. **Pool** — Point app traffic at the pooler. Serverless/transaction mode uses port 6543 instead of 5432 on Supabase. Artefact: pool configuration.

## Done when

`EXPLAIN ANALYZE` for the target path shows Index Scan (or justified Bitmap Heap), not a sequential scan on a large table. Every FK used in the change is indexed. The migration has a DOWN and uses `CONCURRENTLY` for indexes. The rewritten query has no per-row follow-up. Plan output, schema diffs, and migration files can be pointed at.
