---
name: Keep refetchOnMount always for editor queries — canonical source only
description: Keep refetchOnMount "always" only in article-editing-provider.tsx; remove from page.tsx and editing-session-provider. Editor must always wait for fresh data (isFetching gate stays).
type: feedback
---

Keep `refetchOnMount: "always"` ONLY in `article-editing-provider.tsx` — the canonical owner of editor content. Remove it from `page.tsx` and `editing-session-provider.tsx` since React Query deduplicates by key and the single "always" flag on the canonical source still triggers a refetch for all observers.

The editor must always wait for fresh network data before rendering (the `isFetching` gate in article-editing-provider Effect A must stay). Do NOT switch to `isLoading` — user explicitly chose fresh data over faster rendering from cache on 2026-04-03.

Also keep `refetchOnWindowFocus: true` in the global React Query config.

**Why:** Editor data must be fresh to avoid editing stale content. But having `refetchOnMount: "always"` on 3+ components for the same query key is redundant and creates unnecessary competing requests.

**How to apply:** When touching article/video data fetching, ensure `article-editing-provider.tsx` retains `refetchOnMount: "always"`. Other consumers of the same query key should use default refetch behavior.
