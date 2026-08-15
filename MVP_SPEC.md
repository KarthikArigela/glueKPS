https://linear.app/karthik-arigela-personal/document/spec-gluekps-mvp-task-clarifier-superlist-projection-205204d31306

# [Spec] GlueKPS MVP: Task Clarifier + Superlist Projection

## Problem Statement

The user captures vague intentions (text rambles) but has no reliable way to turn them into executable, structured commitments that sync to their execution tool (Superlist). Existing tools each solve only part: Superlist manages tasks, but lacks the reasoning layer to decompose vague input into clear next actions with definitions of done. The user wants a **task clarifier** — a system that takes a raw capture, asks focused clarifying questions one at a time, decomposes work to leaf tasks that fit a single focused session, and projects confirmed tasks to Superlist.

## Solution

A **text-first, web-only MVP** that implements the core clarifier loop:

1. **Capture** — User pastes/types a raw thought
2. **Clarify** — LLM-driven conversation asks one question at a time until the leaf rule is satisfied
3. **Propose** — Structured tree (Project → Tasks → Subtasks) with next action, DoD, session estimate
4. **Confirm** — User approves/edits/saves-for-later/discards; approval persists to Supabase and triggers Superlist projection
5. **Project** — Confirmed tasks flow to Superlist via MCP (outbound-only): Projects → mapped lists, Tasks/Subtasks → nested under parent, Standalone tasks → built-in Inbox
6. **Track** — Sync status visible in web UI; durable retry with idempotency

## User Stories

### Capture & Input

1. As the sole user, I want to paste or type a complete English text capture, so that I can record thoughts without voice infrastructure.
2. As the sole user, I want my raw capture preserved verbatim, so that original intent remains auditable.
3. As the sole user, I want to see all my captures in a list, so that nothing silently disappears.

### Clarification Conversation

4. As the sole user, I want the system to classify my capture as a Project, Task, or Not actionable, so that I don't have to understand the ontology upfront.
5. As the sole user, I want the assistant to ask one useful clarification question at a time, so that the conversation remains manageable.
6. As the sole user, I want the assistant to ask about why, what, how, where, when, dependencies, resources, and success criteria when those details matter, so that vague intentions become executable.
7. As the sole user, I want the assistant to distinguish important missing information from optional information, so that it does not guess dangerously or interrogate endlessly.
8. As the sole user, I want the conversation to be resumable — I can answer, walk away, and return later to the same thread, so that clarification fits my schedule.
9. As the sole user, I want concise reasoning for the assistant's classification and questions, so that I can correct it without reading unnecessary model output.

### Decomposition & Leaf Rule

10. As the sole user, I want the system to decompose work until every leaf fits one 25/5 or 50/10 focused session, has one observable outcome, and has no unresolved blocking dependency, so that the breakdown is actionable without meaningless micro-tasks.
11. As the sole user, I want the leaf rule enforced at confirmation time — the proposal won't approve if a leaf violates it — so that I'm forced to clarify sufficiently upfront.
12. As the sole user, I want the assistant to propose a first executable action even when the complete path is unknown, so that information can be discovered through action.

### Proposal & Confirmation

13. As the sole user, I want a structured proposal card showing the full tree (Project → Tasks → Subtasks) with title, next action, definition of done, and session estimate, so that I can review before committing.
14. As the sole user, I want to edit any field inline on the proposal card, so that I can fix details without restarting clarification.
15. As the sole user, I want one-tap actions: **Approve & Save**, **Edit**, **Save for later**, **Discard**, **Not sure yet**, so that confirmation requires little effort.
16. As the sole user, I want the destination Superlist list picker (for Projects) integrated into the confirmation view, so that mapping is decided at commit time.
17. As the sole user, I want "Not sure yet" to reopen clarification with another question, so that uncertainty doesn't force a bad commit.

### Superlist Projection

18. As the sole user, I want confirmed Projects projected to a specific existing Superlist list (chosen from my 52 legacy lists), so that the list is the project.
19. As the sole user, I want the full tree (Tasks and Subtasks nested) projected into that list, so that the Superlist view mirrors the decomposition.
20. As the sole user, I want confirmed standalone Tasks (no Project) projected to Superlist's built-in Inbox, so that every executable item is visible in my execution tool.
21. As the sole user, I want projection to happen immediately per-task as each is confirmed, so that a confirmed leaf doesn't wait for siblings.
22. As the sole user, I want the integration to never create, delete, or rename Superlist lists, so that my existing 52-list setup cannot be damaged.
23. As the sole user, I want projection to be durable — retried on failure with idempotency — so that confirmed work is not silently discarded.

### Sync & Visibility

24. As the sole user, I want a simple Active view listing confirmed items with sync status (Synced / Pending / Failed), so that I know what's landed in Superlist.
25. As the sole user, I want failed syncs to be retryable manually, so that transient errors don't block me.

### Auth & Data

26. As the sole user, I want Google sign-in via Supabase Auth, so that access is convenient and secure.
27. As the sole user, I want Row Level Security on all my data, so that database access is restricted to my account.
28. As the sole user, I want AI operation metadata (provider, model, latency, cost, confidence) recorded, so that quality and spending can be improved.

## Implementation Decisions

### Architecture

* **Monorepo**: pnpm/Turborepo with three workspaces — `apps/web` (Next.js), `apps/api` (FastAPI), `packages/contracts` (shared TypeScript types).
* **Modular monolith** — single FastAPI process, clear internal boundaries (captures, clarifier, superlist, sync).
* **Canonical data store**: Supabase PostgreSQL (7 tables, RLS on `user_id = auth.uid()`).
* **AI provider**: OpenRouter via OpenAI-compatible adapter; default model `deepseek/deepseek-v4-flash`; operation metadata recorded per call.
* **Superlist integration**: FastAPI acts as MCP client to `https://app.superlist.com/mcp` using Python `mcp` SDK; dynamic OAuth 2.0 (PKCE) with encrypted refresh token storage; outbound-only projection (no read-back in MVP).
* **Auth**: Supabase Auth with Google sign-in; JWT verification middleware on API; protected routes on web.

### Domain Model (MVP Subset)

* **Capture** — raw text, kind (project/task/not-actionable), lifecycle state (captured/clarifying/proposed/confirmed/saved-later/discarded)
* **Conversation** — message history per capture for resumable clarification
* **Project** — finite container with title, purpose, mapped to one Superlist list
* **Task/Subtask** — executable leaf with next action, definition of done, session estimate (25/50 min), hierarchy via `parent_task_id`
* **ProjectListMapping** — project_id → superlist_list_id (derived available lists = all Superlist lists minus Archive minus active mappings)
* **SyncOperation** — durable outbound projection record with status, retries, idempotency key
* **AIOperation** — provider, model, latency, cost, confidence per AI call

**Excluded from MVP**: Area, Goal, Routine, Event, Resource, version history, archival, deeper decomposition on request, Calendar/Toggl/Focus sessions, voice/ASR, read-back from Superlist.

### Clarification Engine

* **One-question-at-a-time loop** driven by LLM via `ProviderAdapter`.
* **Classification turn** → determines kind (project/task/not-actionable) + first question.
* **Clarification turns** → each user answer appended; engine decides next question or proposal.
* **Proposal generation** → full tree built when leaf rule satisfied.
* **Leaf rule validator** (pure function): every leaf must have estimate ≤ 1 session, next_action present, definition_of_done present, no known blocker.
* **Not actionable** = terminal state; never produces proposal; stored in Supabase, no UI.
* Exploration leaves: When the user cannot provide outcome information because the path is genuinely unknown (e.g., "learn AI", the outcome isn't knowable yet), the clarifier does not interrogate endlessly. It converts the unknown into an exploration leaf: a task with *question, scope, stopping rule, and expected output* (e.g., "Research what becoming productive-with-AI requires; scope = 60 min / 3 sources; stopping rule = list top skills + pick one; output = a short decision note"). This leaf satisfies the leaf rule — it has a definition of done — and satisfies the first-executable-action story without producing slop. The unresolved questions remain noted in the conversation but are not blockers for confirmation.

### Confirmation Actions

| Action | Effect |
| -- | -- |
| **Approve & Save** | Persist Project+Task tree; create `project_list_mapping` (if Project); create `sync_operations`; capture state → confirmed |
| **Edit** | Apply inline edits; return updated proposal (no persistence) |
| **Save for later** | Capture state → saved_later |
| **Discard** | Capture state → discarded |
| **Not sure yet** | Capture state → clarifying; engine re-enters loop |

### Superlist Projection Details

* **Project** → mapped list (user picks from available lists at confirm time).
* **Tasks/Subtasks** → created in that list; subtasks nest under parent task via Superlist MCP `create_subtask`.
* **Standalone Task** → Superlist built-in Inbox (zero list slots consumed; movable to a list later via Superlist's native move).
* **Idempotency** — `idempotency_key = capture_id + task_index` prevents duplicates on retry.
* **Archive list** — exists in Superlist; excluded from available lists; archival flow deferred entirely.

### Web UI (3 Views)

1. `/capture` — New Capture: textarea + submit + "Connect Superlist" button.
2. `/capture/{id}/clarify` — Clarification thread (Mode A: conversation bubbles; Mode B: proposal card with tree renderer, inline editing, destination dropdown, 5 action buttons).
3. `/active` — Active items list: type badge, title, sync status chip (Synced/Pending/Failed); polls every 10s.

### Testing Strategy (Two Layers)

1. **Primary product seam test** — end-to-end pipeline with fakes (`FakeProviderAdapter`, `FakeSuperlistMCPClient`, in-memory DB): capture → fake clarification → valid proposal → confirm → asserts: verbatim capture stored, tree persisted, sync ops created, projection emitted, idempotent on replay.
2. **Pure logic unit tests** — leaf-rule validator (violations for oversize/missing fields/blocker), LLM output validation (Pydantic schema acceptance/rejection, retry on malformed JSON).

* **No E2E browser tests, no live Superlist/OpenRouter tests in CI** — live integration is manual, gated by env.

### Repo Structure

``` 
glueKPS/
├── frontend/         # Next.js 14, Tailwind, shadcn/ui, Supabase client        
└── backend/          # FastAPI, SQLAlchemy async, Pydantic, Supabase
```

### Secrets (`.env.example` at root + per app)

* `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
* `OPENROUTER_API_KEY`
* `SUPERLIST_CLIENT_ID`, `SUPERLIST_CLIENT_SECRET` (MCP OAuth dynamic client)
* `ENCRYPTION_KEY` (for stored refresh tokens)
* `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_API_URL`

## Testing Decisions

* **What makes a good test**: Verifies externally observable behavior at the highest practical seam (the capture→confirm→project pipeline). Does not assert internal implementation details, exact prompts, or framework structure.
* **Modules tested**:
  * Clarification engine (classification, multi-turn, leaf rule, proposal building)
  * Confirmation endpoint (all 5 actions, persistence, sync op creation)
  * Superlist MCP client (list, create task, create subtask, OAuth flow)
  * Sync worker (poll, retry with backoff, idempotency)
  * Leaf rule validator (pure logic edge cases)
  * LLM output validation (Pydantic schemas)
* **Prior art**: The spec's "Primary Product Seam" test pattern; adapter contract tests with fakes for external services.

## Out of Scope

* Voice capture, ASR/transcription, audio lifecycle
* Android/Expo mobile client
* Google Calendar, Toggl, Notion, YouTube Music integrations
* Focus sessions, Pomodoro timer, focus profiles
* Routines, routine instances, routine reviews
* Sleep tracking, bedtime/wake logging
* Daily/weekly/quarterly reviews
* Archival flow (completed/superseded/abandoned → Archive list + list renaming)
* Deeper decomposition on request after execution
* Version history / supersede chains / diffing
* Full bidirectional Superlist sync (read-back of completed/postponed/skipped)
* Live SuperList/OpenRouter tests in CI
* E2E browser test suite
* Passkey authentication
* pgvector / semantic search
* Redis, Kafka, Kubernetes, microservices
* Multi-user, sharing, collaboration

## Further Notes

* The Linear project `GlueKPS` (KAR) contains 13 tracer-bullet tickets ([KAR-5] through [KAR-17]) covering every implementation slice.
* The first vertical slice to prove is: **capture → clarification → proposal → confirm → persist → project to Superlist**.
* Superlist MCP is the only programmatic surface — no REST API exists. The dynamic OAuth flow is the main integration risk; de-risk early with a spike.
* All decisions are recorded in the grilling session; this spec synthesizes them without re-interviewing.
* Domain vocabulary follows `CONTEXT.md` (Capture, Project, Task, Subtask, Area, Goal, Routine, Event, Resource, Projection, Sync Operation, Focus Block, etc.).