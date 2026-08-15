# GlueKPS - Decision Log

Decisions are append-only. New decisions should record the options considered, the chosen direction, and the reason. Deferred decisions remain visible rather than being silently resolved.

## Product Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 1 | Product boundary | Replace existing tools vs glue them together | Glue layer over existing tools | The user wants one coherent personal system without recreating Notion, Calendar, Toggl, Superlist, or YouTube Music. |
| 2 | Primary outcome | Generic productivity app vs clarified commitments and execution alignment | Turn vague intentions into verified commitments connected to planning, execution, time tracking, and review | This is the missing capability across the user's existing tools. |
| 3 | User base | Multi-user product vs private personal tool | Single user only | The system is for the builder's own life; collaboration adds no current value. |
| 4 | Canonical data store | Notion vs external apps vs personal database | Supabase PostgreSQL | It provides durable structured data, history, authentication, storage, APIs, and future search without making Notion a reliability bottleneck. |
| 5 | First vertical slice | Build every integration first vs prove the core loop | Capture -> transcription -> clarification -> confirmation -> canonical record -> Superlist projection | The system must first reliably convert vague input into useful action. |
| 6 | Working style | One-shot automation vs draft-first | Draft-first with human confirmation | AI can prepare the work, but the user remains the authority over commitments and meaning. |
| 7 | Confirmation | Large forms vs progressive questioning | One question at a time with concise proposal and one-tap actions | Reduces cognitive load while collecting the information that matters. |
| 8 | Bias to action | Ask until perfect vs act immediately vs safe action with preserved questions | Clarify material blockers; use a reversible provisional action when the user is depleted | Execution generates information, but important uncertainty must not be hidden. |
| 9 | Behavior support | Punitive enforcement vs reminders only vs supportive guardrails | Supportive, context-aware guardrails | The system can reduce friction and recover from escape without claiming to control behavior or provide clinical treatment. |
| 10 | Primary success measure | Task volume vs meaningful progress | Capture-to-action, plan adherence, focus-block attendance, recovery, and project progress | Checking tasks is not the same as moving outcomes forward. |

## Domain Model Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 11 | Core ontology | PARA only vs expanded model | Areas, Goals, Projects, Tasks/Subtasks, Captures, Routines, Events, Resources | Preserves PARA while representing goals, recurring behavior, time commitments, and raw input explicitly. |
| 12 | Project relationships | Force every project into an Area and Goal vs optional relationships | Area and Goal links are optional | Projects may be standalone; the assistant must not invent meaning. |
| 13 | Task ownership | Multiple owners/contexts vs one owner | Exactly one primary owner | The user wants simple execution without duplicate or ambiguous task placement. |
| 14 | Hierarchy | Shallow fixed depth vs unlimited nesting | Allow deep nesting when genuinely needed, stop at executable leaf | Real work can reveal more decomposition, but the assistant must avoid meaningless micro-tasks and endless automatic nesting. |
| 15 | Task quality | Vague task titles vs action and completion standard | Next action plus observable definition of done | The system exists to turn vague intentions into executable work. |
| 16 | Effort unit | Hours only vs focus sessions | Focus sessions first, time equivalent second | Planning should match the user's 25/5 and 50/10 execution model. |
| 17 | Goal quality | Permanent aspiration vs outcome and review horizon | Observable outcome plus review horizon, with exploratory goals allowed | Goals should be reviewable without forcing false precision at the start. |
| 18 | Archive | Hard deletion vs retain everything visibly vs non-destructive archive | Archive structured records, delete transient audio after processing | History remains safe and restorable while unnecessary raw audio is removed. |
| 19 | Lifecycle | Simple done/not-done vs explicit internal state machine | Detailed internal states with simple user-facing views | Automation needs lifecycle precision without creating user-facing complexity. |
| 20 | Versioning | Overwrite current record vs preserve changes | Version interpretations and meaningful plan changes | New information can change scope, priority, estimate, and intent; history must remain intact. |

## Interaction and Voice Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 21 | Voice interaction | Fully live voice vs turn-based | Turn-based complete-ramble capture first | It preserves the entire initial thought and is cheaper and simpler to operate. |
| 22 | Text input | Voice-only vs equal text/voice vs voice-first fallback | Voice-first with text fallback | Voice supports the intended behavior, while text prevents abandonment when speaking is inconvenient. |
| 23 | Language | Multilingual from day one vs English first | English only initially | The user is comfortable rambling in English; a narrow language scope improves initial ASR reliability. |
| 24 | Capture access | Laptop only vs Android-only vs both | Full workflow on Android and laptop | Thoughts, planning, clarification, and execution can happen in different contexts and devices. |
| 25 | Offline behavior | Offline queue vs online-only | Online-only initially | Infrastructure should focus on a working system before offline synchronization is introduced. |
| 26 | Depleted state | Infer from silence vs explicit mode | Voice phrase and visible "I am stuck" action | Explicit activation is more reliable than guessing the user's mental state. |
| 27 | Provisional action | Stop until all questions are answered vs proceed permanently | One time-boxed provisional focus session followed by review | It creates action without silently committing to an uncertain plan. |

## Planning, Focus, and Behavior Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 28 | Daily planning | Static to-do list vs constraint-based plan | Constraint-based plan with evening draft and morning confirmation | Calendar, capacity, energy, routines, and real-life changes must shape the plan. |
| 29 | Capacity | Fill every available minute vs reserve slack | Reserve approximately 30-40% of realistic capacity | Work expands, ordinary life intervenes, and unrealistic plans create guilt. |
| 30 | Routine representation | Calendar event for everything vs tasks only vs mixed | Routine instances/tasks by default; events only for protected or time-critical routines | Keeps the calendar readable while retaining daily-life work. |
| 31 | Focus calendar display | One event per Pomodoro interval vs one overall block | One overall focus block | Calendar should show planned commitment without work-break fragmentation. |
| 32 | Toggl role | Net productive minutes vs overall block attendance | Overall focus-block attendance | Visual comparison of planned Calendar blocks and actual focus presence is more useful to the user. |
| 33 | Focus timer | External paid app vs Toggl-only vs built into GlueKPS | Built-in timer synchronized to Toggl | Avoids another dependency while retaining Toggl records. |
| 34 | Music | Playback API vs no music support vs stored links | Focus profiles with playlist URLs and open actions | YouTube Music playback control is unnecessary and uncertain. |
| 35 | Music default | Automatic mood switching vs fixed default | Hans Zimmer default; suggestions require approval | The user's known default should not be silently overridden. |
| 36 | Reminder ownership | Google Calendar for all reminders vs app for all reminders vs split | GlueKPS owns planning/routine/focus/recovery; Calendar owns actual events | Context-aware actions require the GlueKPS domain model. |
| 37 | Reminder interaction | Swipe-away notifications vs explicit state | Done, Snooze, Reschedule, Skip, Not relevant | Dismissal without state creates no learning and repeats failed timing. |
| 38 | Sleep support | Strict target immediately vs ignore sleep vs baseline-first | Manual one-tap logs and gradual baseline-based adjustment | The user has no sleep device and needs a realistic, non-punitive path. |
| 39 | Review rhythm | Review only when problems occur vs daily/weekly/quarterly | Before-day draft, during-day check-ins, end-day, weekly, quarterly | Each review horizon serves a different kind of adjustment. |

## Integration Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 40 | Superlist role | Canonical task database vs execution projection | Confirmed tasks, routine instances, and active project containers only | Superlist stays clean while Supabase preserves context and history. |
| 41 | Superlist lists | Create/delete lists vs use legacy lists | Use only the user's existing 52 lists | The user's legacy free plan has unlimited existing lists but cannot create more under current limits. |
| 42 | Superlist safety | Automatic list management vs user-controlled mapping | Never create, delete, rename, or auto-reassign lists; require explicit mappings | Protects the user's existing setup from destructive or incorrect automation. |
| 43 | Superlist status | Ignore external status vs simple bidirectional status | Superlist owns completed/postponed/skipped execution status | Its execution state is useful and should flow back without moving canonical meaning. |
| 44 | Calendar authority | App-only vs Calendar-only vs bidirectional | App proposes/creates; Calendar owns final timing and changes | Real-world reschedules and cancellations happen in Calendar. |
| 45 | Toggl authority | GlueKPS-only vs Toggl net time vs Toggl overall focus block | Toggl overall focus-block attendance | Keeps reports visually comparable with Calendar. |
| 46 | Notion role | Canonical database vs two-way editing vs controlled projection | One-way projection initially | Notion remains useful as the second brain without becoming a synchronization bottleneck. |
| 47 | Sync confirmation | Confirm every API field vs automatic after proposal approval | Confirm once, then synchronize; destructive changes require separate confirmation | Avoids repetitive approvals while protecting irreversible actions. |
| 48 | Sync failures | Drop or overwrite vs durable retry | Pending/failed durable operations with retries and idempotency | Confirmed user decisions must not silently disappear. |
| 49 | Sync conflicts | Last write wins vs silent merge vs user resolution | Preserve both versions and ask the user | Meaningful plan changes cannot be safely overwritten without context. |

## Security and AI Provider Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 50 | Cloud posture | Local/self-hosted vs managed cloud | Managed Supabase and hosted APIs | Reliable access from Android and laptop is a primary requirement. |
| 51 | Privacy boundary | Zero-knowledge cloud vs strong cloud security with selective disclosure | Strong cloud security with selective AI disclosure | Hosted AI requires selected content to be readable during processing; unnecessary exposure is still minimized. |
| 52 | Authentication | None vs password-only vs hosted identity | Supabase Auth with Google sign-in and passkeys | Single-user secure cross-device access without building identity infrastructure. |
| 53 | AI hosting | Local models/fine-tuning vs hosted APIs | Hosted APIs only | The user wants to use OpenRouter and other hosted providers, not operate models. |
| 54 | AI routing | Hardcode one provider vs provider-neutral interface | OpenAI-compatible provider adapter | Cost, quality, quotas, and availability may change. |
| 55 | AI metadata | Discard operation metadata vs record it | Provider, model, latency, cost, and confidence metadata | Enables quality and cost optimization without retaining raw audio. |
| 56 | AI sensitivity | Send everything automatically vs block everything vs tiers | Normal, Sensitive, Highly private gating | Allows useful automation while preserving control over intimate content. |
| 57 | ASR | Build ASR infrastructure vs free/low-cost hosted transcription | Low-cost hosted ASR behind an adapter | Capability can be tested without operating a speech model. |

## Technical Stack Decisions

| # | Decision | Options Considered | Chosen | Rationale |
|---|---|---|---|---|
| 58 | Architecture shape | Microservices vs modular monolith | Modular monolith | Clear internal boundaries without early deployment and debugging overhead. |
| 59 | Web client | React alternatives vs Next.js | Next.js, React, TypeScript, App Router, Tailwind, shadcn/ui | Supports the full desktop and mobile web experience with a mature UI stack. |
| 60 | Mobile client | Native Android vs React Native/Expo | React Native, Expo, Expo Router plus small native Android extensions | Provides cross-device shared UI and access to required Android capabilities. |
| 61 | Backend | Next-only API vs FastAPI | FastAPI with asyncio and Pydantic | Matches the user's learning path and gives a clear AI/orchestration boundary. |
| 62 | Persistence | SQLite vs managed relational database | Supabase PostgreSQL day one | Personal context, history, relationships, and sync records need durable relational storage. |
| 63 | Validation | Loose model output vs typed contracts | Pydantic validation before persistence | LLM output must not directly mutate canonical data. |
| 64 | Search | Vector database immediately vs relational search first | PostgreSQL full-text first; pgvector when justified | Avoids premature retrieval infrastructure. |
| 65 | Deployment | Local-only vs managed deployment | Vercel for web, Cloud Run for FastAPI, Supabase managed | Reliable multi-device access and a production-shaped learning path. |
| 66 | Infrastructure | Add services broadly vs minimal services | No Redis/Kafka/Kubernetes/microservices initially | Cost and operational complexity are not justified before a concrete need. |
| 67 | Documentation | Minimal code only vs learning-oriented docs | Brief rationale, acceptance criteria, and verification in tickets | The user is learning system design and wants decisions understandable. |

## Deferred Decisions

| # | Deferred Decision | Current Direction |
|---|---|---|
| D1 | Backups and portable export | Required later; not a first working-system milestone. |
| D2 | Offline capture and synchronization | Online-only first; revisit after reliable online flow. |
| D3 | Fully live interruptible voice | Turn-based first; revisit after capture and clarification work. |
| D4 | Deep semantic retrieval | Add pgvector only after search needs are proven. |
| D5 | TTS spoken responses | Optional after the turn-based voice capture loop is reliable. |
| D6 | YouTube Music playback control | Do not depend on it; stored links are sufficient initially. |
| D7 | Full Notion bidirectional editing | One-way projection first. |
| D8 | More advanced model routing, fallback, and cost optimization | Provider adapter and operation metadata first; optimize from evidence. |
| D9 | Device-level behavior enforcement | Continue using StayFree and Android controls. |
| D10 | Medical or clinical sleep intervention | Out of scope; only lightweight self-tracking and planning support. |
