---
name: Use yarn for Prisma type generation
description: Run "yarn" instead of "npx prisma generate" or "npx prisma migrate dev" to regenerate Prisma types. User will push schema changes to remote manually.
type: feedback
---

When Prisma schema changes are made, run `yarn` (not `npx prisma generate` or `npx prisma migrate dev`) to regenerate types. The user will handle pushing schema migrations to the remote database themselves.

**Why:** The project's yarn postinstall hook runs prisma generate automatically. Direct prisma commands may not work correctly in this setup.

**How to apply:** After modifying `prisma/schema.prisma`, just run `yarn` to get updated TypeScript types.
