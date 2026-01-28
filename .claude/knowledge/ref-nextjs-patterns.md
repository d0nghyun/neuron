# Next.js Patterns Reference

Quick reference for Next.js 15+ best practices and patterns.

## Overview

This document captures Next.js patterns learned from production development, focusing on Next.js 15+ with App Router and advanced features like cacheComponents.

## Route Segment Config Compatibility

| Feature | Compatible with cacheComponents? | Alternative |
|---------|----------------------------------|-------------|
| `dynamic = 'force-dynamic'` | NO | Use Suspense pattern |
| `dynamicParams = true/false` | NO | Use Suspense pattern |
| `revalidate = 0` | NO | Use Suspense pattern |
| Manual cache control | YES | Use in data fetching functions |

## Suspense Pattern for Dynamic Routes

When `nextConfig.cacheComponents: true` is enabled, use this pattern:

**WRONG - params await outside Suspense:**
```tsx
export default async function Page({ params }) {
  const { id } = await params;
  return <Suspense><Content id={id} /></Suspense>;
}
```

**CORRECT - params passed to async component inside Suspense:**
```tsx
export default function Page({ params }) {
  return <Suspense fallback={<LoadingSkeleton />}>
    <Content params={params} />
  </Suspense>;
}

async function Content({ params }) {
  const { id } = await params;
  // ... data fetching here
}
```

**Why:** Route segment configs are incompatible with cacheComponents. The params must be awaited inside the Suspense boundary, not before.

## Type Naming Conventions

When both Drizzle DB schema and Zod schema export types:

| Source | Naming | Example |
|--------|--------|---------|
| Drizzle schema | Add `Entity` suffix | `PortfolioAlphaEntity` |
| Zod schema | Keep original name | `PortfolioAlpha` |

**Reason:** Avoids TS2308 type collision errors when both are imported together.

**Example:**
```typescript
// schema.ts (Drizzle)
export type PortfolioAlphaEntity = typeof portfolioAlphas.$inferSelect;

// portfolio.schema.ts (Zod)
export const PortfolioAlphaSchema = z.object({ ... });
export type PortfolioAlpha = z.infer<typeof PortfolioAlphaSchema>;
```

## Loading States

Always provide loading skeletons for pages with async data:

```tsx
export default function Page({ params }) {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Content params={params} />
    </Suspense>
  );
}
```

## Mock Data Strategy

For rapid prototyping with demo deadlines:

| Phase | Approach | Refactor After |
|-------|----------|----------------|
| Prototyping | Mock data in route handlers | Move to proper use cases + repositories |
| Demo | Frontend + API routes working | Connect real data sources |
| Production | Full architecture | Performance optimization |

**Note:** Mock data in route handlers is acceptable for demos but should be refactored to proper domain/application layers for production.

## Related

- Next.js App Router docs: https://nextjs.org/docs/app
- Next.js caching: https://nextjs.org/docs/app/building-your-application/caching
