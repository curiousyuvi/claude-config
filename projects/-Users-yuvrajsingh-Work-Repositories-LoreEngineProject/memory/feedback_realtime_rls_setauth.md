---
name: feedback-realtime-rls-setauth
description: Supabase Realtime with @supabase/ssr cookie sessions needs an explicit setAuth(token) before subscribing — otherwise RLS-protected channels drop every event silently.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---

When subscribing to Supabase Realtime `postgres_changes` on an RLS-protected table in this project (anything keyed off `user_has_project_access` / `project_memberships`), you MUST call `supabase.realtime.setAuth(token)` with the current access token BEFORE `.subscribe()`. Also wire `onAuthStateChange` to re-call setAuth on token refresh.

**Why:** `@supabase/ssr`'s `createBrowserClient` stores the session in cookies. Cookie-based sessions don't auto-propagate to the realtime websocket — the websocket connects as anon, RLS policies fail silently, and every `postgres_changes` event is dropped. Symptom: initial `.select()` returns correct data (fetch carries cookies), but no live updates ever arrive; reload "magically fixes it" because it re-runs the initial fetch with the now-updated row. We hit this on the import-progress page (2026-05-26).

**How to apply:** In any custom hook that opens a Realtime channel, do `const { data } = await supabase.auth.getSession(); supabase.realtime.setAuth(data.session.access_token)` before `.subscribe()`. See `app/hooks/use-realtime-job.ts` for the canonical pattern. Also remember REPLICA IDENTITY FULL + publication membership are required on the DB side — see [[reference-design-system]] adjacent migration `20260526040001_realtime_publications.sql` for that piece.
