# Spec: GlueKPS - Personal Knowledge and Productivity System

## Problem Statement

The user wants one dependable personal system that turns vague intentions, rambling thoughts, and changing plans into clear, executable commitments without recreating the tools they already use.

Existing tools each solve only part of the problem:

- Google Calendar manages scheduled time.
- Notion stores long-form knowledge and the second brain.
- Toggl Track records time blocks.
- Superlist manages practical tasks.
- YouTube Music provides focus music.
- StayFree and Android controls provide device-level blocking.

The missing layer is the glue and reasoning system. It must preserve the user's original intent, ask useful questions, distinguish tasks from projects and areas, decompose work to a realistic focused-session unit, schedule it, support execution, record what actually happened, and replan when new information changes the work.

The user commonly encounters these failure modes:

- Vague items such as "Learn AI" or "Read OpenAI Developer Documentation" do not define a next action or success criterion.
- A task is actually a project, or an ongoing area of responsibility is treated as a task.
- The user's goal and the task selected do not align.
- New information changes the scope, priority, estimate, or definition of done.
- Plans fill all available time and become impossible when ordinary life intervenes.
- Difficulty triggers an escape loop: discomfort, random work or unnecessary content consumption, loss of context, and stalled progress.
- Generic reminders are dismissed without an explicit decision.
- Sleep and wake drift changes the entire day.
- Existing voice-typing tools have limits and do not preserve the workflow's context, confirmation, history, or interpretation.

## Solution

GlueKPS is a single-user, online-first personal operating system with a responsive web client and a full-featured Android client. Both clients use one shared backend and support the complete core workflow, while each is optimized for its context.

The system provides a voice-first and text-capable capture surface. A user can record a complete English ramble, receive a transcription and structured interpretation, answer concise clarifying questions, and confirm a proposed result. The original capture is preserved until transcription and interpretation are confirmed; raw audio is then deleted.

The system classifies confirmed information into a small canonical model:

- Areas: ongoing responsibilities.
- Goals: desired outcomes with a review horizon.
- Projects: finite efforts, optionally linked to an area or goal.
- Tasks and subtasks: executable work with one primary owner.
- Captures: raw or unprocessed inputs.
- Routines: recurring behaviors, metrics, and review cycles.
- Events: time-bound commitments.
- Resources: reference knowledge.

Supabase PostgreSQL is the canonical source of truth. Notion, Superlist, Google Calendar, and Toggl are connected according to explicit authority and projection rules. The assistant uses hosted AI APIs, primarily through provider-neutral OpenAI-compatible interfaces such as OpenRouter and low-cost hosted ASR providers. It does not fine-tune, self-host, or operate a local LLM.

The first complete vertical slice is:

> Android or web capture -> transcription -> progressive clarification -> confirmation -> canonical Supabase record -> optional Superlist projection.

## User Stories

### Capture and Voice Interaction

1. As the sole user, I want to capture a complete English voice ramble from Android, so that I can record thoughts while walking or away from my laptop.
2. As the sole user, I want the Android home-screen widget to start recording immediately, so that capture has very low friction.
3. As the sole user, I want lock-screen access where Android supports it, so that I can capture without navigating through the app.
4. As the sole user, I want text input as a fallback, so that the system remains usable when speaking is inconvenient.
5. As the sole user, I want voice and text to use the same processing pipeline, so that the system behaves consistently.
6. As the sole user, I want turn-based voice interaction first, so that the complete thought is captured before interpretation.
7. As the sole user, I want silence detection to optionally stop recording, so that I do not need to operate the phone precisely while speaking.
8. As the sole user, I want the raw voice recording preserved until transcription and interpretation are confirmed, so that meaningful input is not lost prematurely.
9. As the sole user, I want raw audio deleted after confirmation, so that unnecessary sensitive data is not retained.
10. As the sole user, I want the app to show whether a capture is queued, processing, clarifying, confirmed, or failed, so that an input never silently disappears.
11. As the sole user, I want the system to remain English-only initially, so that transcription quality is prioritized.
12. As the sole user, I want existing voice-typing tools to remain optional fallback inputs, so that I am not forced to depend on their quotas.

### Interpretation and Clarification

13. As the sole user, I want the assistant to decide whether an input is a capture, task, project, area, goal, routine, event, resource, or transient thought, so that I do not have to understand the ontology before using it.
14. As the sole user, I want concise reasoning for the assistant's classification, so that I can correct it without reading unnecessary model output.
15. As the sole user, I want the assistant to ask one useful clarification question at a time, so that the conversation remains manageable.
16. As the sole user, I want the assistant to ask about why, what, how, where, when, dependencies, resources, and success criteria when those details matter, so that vague intentions become executable.
17. As the sole user, I want the assistant to distinguish important missing information from optional information, so that it does not either guess dangerously or interrogate endlessly.
18. As the sole user, I want the assistant to preserve uncertainty instead of inventing details, so that the final plan remains honest.
19. As the sole user, I want the assistant to ask whether an item is a task, project, or area when the scope is ambiguous, so that the structure reflects reality.
20. As the sole user, I want the assistant to recognize when a project has no obvious goal or area, so that it does not invent a false relationship.
21. As the sole user, I want the assistant to propose a first executable action even when the complete path is unknown, so that information can be discovered through action.
22. As the sole user, I want the assistant to continue unresolved questions after a provisional action, so that action does not erase necessary clarification.
23. As the sole user, I want the assistant to provide a concise proposal before changing my system, so that I confirm the meaning rather than merely the wording.

### Confirmation and Human Control

24. As the sole user, I want every capture preserved verbatim, so that the original intent remains auditable.
25. As the sole user, I want the assistant to propose type, title, purpose, next action, success criteria, estimate, deadline, dependencies, tools, and destination, so that confirmation is easy.
26. As the sole user, I want one-tap actions such as Approve, Edit, Defer, Discard, and Not sure yet, so that confirmation requires little effort.
27. As the sole user, I want confirmed changes to synchronize automatically to authorized external systems, so that I do not approve the same change repeatedly.
28. As the sole user, I want destructive operations and external deletions to require separate confirmation, so that automation cannot cause irreversible loss.
29. As the sole user, I want the assistant to preserve every meaningful interpretation and plan change, so that learning is not lost when the plan changes.
30. As the sole user, I want the current view to show the latest interpretation while retaining prior versions underneath, so that daily use stays simple without losing history.

### Domain Model and Task Quality

31. As the sole user, I want an Area to represent an ongoing responsibility without an end condition, so that ongoing life responsibilities are not forced into projects.
32. As the sole user, I want a Goal to represent a desired outcome with an observable condition and review horizon, so that aspirations do not remain permanently vague.
33. As the sole user, I want a Project to represent finite work, optionally linked to an Area or Goal, so that projects can stand alone when appropriate.
34. As the sole user, I want every task to have exactly one primary owner, so that execution does not become ambiguous.
35. As the sole user, I want a task to have a clear next action and definition of done, so that I know how to begin and how to finish.
36. As the sole user, I want exploratory work to use a question, scope, stopping rule, and expected output, so that research does not pretend to have a known outcome.
37. As the sole user, I want tasks decomposed only until they fit one 25/5 or 50/10 focused work session, so that the breakdown is actionable without meaningless micro-tasks.
38. As the sole user, I want to request deeper decomposition after attempting a task, so that new information can improve the plan without endless initial nesting.
39. As the sole user, I want parent tasks and projects to act as containers while executable leaf tasks receive scheduling and tracking, so that time is attached to real work.
40. As the sole user, I want effort estimated primarily in focus sessions, with equivalent time stored for integrations, so that planning matches how I work.
41. As the sole user, I want estimates revised using actual progress, so that the system learns when work is larger or smaller than expected.
42. As the sole user, I want importance and urgency separated, so that subjective claims that everything is important do not distort priorities.
43. As the sole user, I want dependencies, resources, tools, context, location, and deadlines represented when relevant, so that I can start without avoidable friction.

### Lifecycle and Replanning

44. As the sole user, I want captures to move through explicit lifecycle states, so that unprocessed inputs do not disappear.
45. As the sole user, I want tasks to be marked confirmed, planned, in progress, blocked, waiting, completed, superseded, or archived, so that the next system behavior is clear.
46. As the sole user, I want projects and goals to support active, paused, achieved, abandoned, replaced, completed, and archived outcomes, so that old commitments stop appearing active.
47. As the sole user, I want the interface to expose simple views rather than every internal state, so that lifecycle precision does not create cognitive load.
48. As the sole user, I want new information to mark affected work stale, blocked, superseded, or needing review, so that outdated plans do not continue silently.
49. As the sole user, I want the assistant to explain what changed and why, so that replanning is understandable.
50. As the sole user, I want downstream effects on calendar events, routines, estimates, and related projects shown before confirmation, so that I understand the impact of a change.
51. As the sole user, I want provisional actions time-boxed to one focus session, so that a temporary assumption does not silently become a long-term plan.
52. As the sole user, I want a provisional action reviewed at the end of its timebox, so that the plan improves from execution evidence.
53. As the sole user, I want an explicit voice phrase or button for "I am stuck" or "Move me forward," so that I can switch from clarification to action when my capacity is depleted.
54. As the sole user, I want the rescue mode to identify the blocker, shrink the next action, offer a 5-10 minute rescue or one focus session, and record the interruption, so that difficulty leads to recovery instead of escape.

### Planning, Calendar, and Routines

55. As the sole user, I want evening or previous-day planning to create a draft for tomorrow, so that I can approach the next day intentionally.
56. As the sole user, I want morning planning to confirm wake time, capacity, energy, and constraints, so that the final plan reflects reality.
57. As the sole user, I want planning to use fixed calendar commitments, available windows, estimates, dependencies, deadlines, energy, meals, commute, routines, and recovery time, so that the plan is realistic.
58. As the sole user, I want the planner to reserve roughly 30-40% of realistic capacity, so that ordinary life and overruns do not destroy the day.
59. As the sole user, I want the planner to replan when my day shifts, so that a late start does not create an impossible schedule.
60. As the sole user, I want ordinary routines such as hydration, hygiene, skin care, family time, and hair care represented as routine instances or tasks rather than calendar events by default, so that the calendar remains readable.
61. As the sole user, I want routines to support full and minimum viable versions, so that difficult days preserve continuity without creating guilt.
62. As the sole user, I want routine instances to support Completed, Partial, Skipped, and Deferred, so that adherence is measured with nuance.
63. As the sole user, I want only time-critical or protected personal commitments to become calendar events, so that routine tracking does not clutter the calendar.
64. As the sole user, I want Google Calendar to own final event time, duration, conflict, cancellation, and rescheduling, so that real-world schedule changes flow back into the system.
65. As the sole user, I want a focus block to appear as one calendar block, so that Pomodoro breaks do not fragment the calendar.

### Focus Sessions and Music

66. As the sole user, I want the app to provide a built-in 25/5 or 50/10 focus timer, so that I do not need another paid focus app.
67. As the sole user, I want a focus session linked to one executable task, so that the session has a clear purpose.
68. As the sole user, I want the focus timer to privately record work intervals, breaks, interruptions, and completed cycles, so that reviews can inspect what happened without cluttering external tools.
69. As the sole user, I want Toggl to record one overall focus-block entry including planned breaks, so that its visual report can be compared with the calendar block.
70. As the sole user, I want the app to calculate net work and break time internally, so that Toggl can stay clean while detailed analysis remains available.
71. As the sole user, I want each focus session to ask my mood and context before starting, so that the assistant can help prevent avoidance.
72. As the sole user, I want Hans Zimmer OST to be the default focus profile, so that the highest-focus mode starts automatically.
73. As the sole user, I want the assistant to suggest Anirudh OST, TFI OST, Focus OST, or curated non-lyrical playlists when I describe low attention, boredom, or a need for a more entertaining work-compatible mode, so that I have a compromise instead of abandoning work.
74. As the sole user, I want to approve or override the suggested playlist before playback, so that the assistant never silently changes my music.
75. As the sole user, I want Liked Music and High Octane Playlist excluded from focus profiles, so that lyrical commute music is not mixed into work sessions.
76. As the sole user, I want playlists represented as stored YouTube Music URLs and open actions, so that the system does not depend on playback APIs.

### Sleep, Behavior, and Reminders

77. As the sole user, I want sleep and wake consistency treated as a first-class objective, so that late nights and late waking do not repeatedly destroy the day.
78. As the sole user, I want the system to learn my baseline before setting strict sleep targets, so that schedule changes are gradual and realistic.
79. As the sole user, I want one-tap bedtime and wake-time logging, so that sleep data can be collected without a watch or dedicated tracker.
80. As the sole user, I want optional phone activity signals used only as supporting estimates, so that manual logs remain correctable and understandable.
81. As the sole user, I want planning, routine, focus, and recovery reminders owned by GlueKPS, so that Google Calendar does not become a noisy generic reminder system.
82. As the sole user, I want actual calendar-event notifications to remain with Google Calendar, so that each system has a clear reminder responsibility.
83. As the sole user, I want reminders to provide Done, Snooze, Reschedule, Skip, or Not relevant actions, so that dismissal does not leave the system ignorant.
84. As the sole user, I want ignored reminders followed up at a suitable later interaction with a limit on repetition, so that the system helps without becoming notification spam.
85. As the sole user, I want repeated reminder dismissal to trigger a timing or routine review, so that the system changes the plan instead of repeating a failed prompt.
86. As the sole user, I want a supportive rather than punitive behavior system, so that setbacks become data and recovery rather than guilt.

### Reviews and Success

87. As the sole user, I want brief during-day check-ins at session start, session end, or meaningful drift, so that the system does not create another large task.
88. As the sole user, I want an end-of-day review to reconcile actual focus blocks, unfinished work, distractions, and changed assumptions, so that tomorrow benefits from evidence.
89. As the sole user, I want a weekly review to inspect project progress, recurring escape patterns, reminder failures, estimates, and plan adjustments, so that the system improves.
90. As the sole user, I want a quarterly review to revisit goals, areas, and quarterly quests, so that higher-level direction remains current.
91. As the sole user, I want the system to measure capture-to-action conversion, so that capture is not mistaken for progress.
92. As the sole user, I want the system to measure planned versus completed or consciously rescheduled commitments, so that planning quality is visible.
93. As the sole user, I want focus-block attendance and internal net-work data separated, so that both consistency and productive time are understandable.
94. As the sole user, I want stuck recoveries, escape episodes, and their triggers reviewed, so that behavior patterns can improve iteratively.
95. As the sole user, I want project progress, not task-count volume, to be a primary success signal, so that the system does not reward meaningless checking.

### Integrations and Data Ownership

96. As the sole user, I want Supabase PostgreSQL to be the canonical source of truth, so that integrations cannot erase the history or meaning of my plans.
97. As the sole user, I want every important interpretation and plan change versioned, so that the system retains context over time.
98. As the sole user, I want Superlist to receive only confirmed executable tasks, routine instances, and active project containers when useful, so that it stays clean.
99. As the sole user, I want Superlist to use only the existing 52 lists, so that the system respects my legacy free personal plan.
100. As the sole user, I want the integration to never create, delete, rename, or automatically reassign Superlist lists, so that my existing setup cannot be damaged.
101. As the sole user, I want explicit mappings from Supabase projects to existing Superlist lists, so that the assistant does not guess destinations.
102. As the sole user, I want Superlist to own simple execution state such as completed, postponed, or skipped, so that those changes flow back to the canonical record.
103. As the sole user, I want goals, areas, captures, resources, full project metadata, and history kept in Supabase rather than Superlist, so that the task app remains focused.
104. As the sole user, I want Google Calendar synchronized bidirectionally for event timing and changes, so that calendar reality is represented correctly.
105. As the sole user, I want Toggl to track overall focus-block attendance, so that it can be compared visually with planned calendar blocks.
106. As the sole user, I want Notion to receive a controlled one-way projection initially, so that direct Notion edits do not silently overwrite canonical meaning.
107. As the sole user, I want YouTube Music represented by URLs and focus profiles, so that playback integration remains optional.
108. As the sole user, I want confirmed outbound changes synchronized automatically, so that the system does not ask me to approve the same decision twice.
109. As the sole user, I want failed synchronizations preserved as pending or failed operations and retried, so that confirmed work is not silently discarded.
110. As the sole user, I want external conflicts to preserve both versions and require resolution, so that no system silently overwrites the other.

### Security and Access

111. As the sole user, I want private authenticated access from Android and laptop, so that personal information is not publicly exposed.
112. As the sole user, I want Google sign-in and passkey support, so that access is convenient and phishing-resistant.
113. As the sole user, I want Supabase Row Level Security applied to all personal data, so that database access is restricted to my account.
114. As the sole user, I want sensitive captures gated before external AI processing, so that I control disclosure.
115. As the sole user, I want normal, sensitive, and highly private processing categories, so that AI access can be proportionate to the content.
116. As the sole user, I want AI operations to record provider, model, latency, cost, and confidence metadata, so that quality and spending can be improved.
117. As the sole user, I want raw audio sent only for transcription and interpretation, then removed, so that storage exposure is minimized.
118. As the sole user, I want online-only operation initially, so that infrastructure stays focused on a working system before offline synchronization is attempted.

## Implementation Decisions

### Product Boundary

- GlueKPS is a private, single-user system. Multi-user workspaces, sharing, collaboration, and public onboarding are out of scope.
- The product is a glue layer, not a replacement for Notion, Google Calendar, Toggl, Superlist, or YouTube Music.
- The system's canonical record is the structured personal context and history in Supabase.
- The first vertical slice is capture, transcription, clarification, confirmation, persistence, and a controlled Superlist projection.
- Product development follows a product brief/PRD, domain glossary, technical architecture, milestone plan, Linear tracer-bullet tickets, implementation, and verification.

### Client Architecture

- Web: Next.js, React, TypeScript, App Router, Tailwind CSS, and shadcn/ui.
- Mobile: React Native, Expo, and Expo Router.
- Both clients support the complete core workflow: capture, clarification, planning, review, task editing, and focus sessions.
- Mobile is optimized for voice capture, walking thoughts, reminders, quick clarification, recovery, routines, and focus controls.
- Laptop is optimized for hierarchy editing, calendar comparison, detailed project work, and reviews.
- Android-native capabilities such as the home-screen widget, lock-screen access where supported, notifications, audio recording, and the focus timer may use Expo config plugins or small native modules.
- Shared TypeScript packages hold domain types, validation contracts, API clients, and synchronization models.
- Use a pnpm/Turborepo monorepo if the application repository is created as a new multi-package project.

### Backend Architecture

- Use a modular monolith rather than microservices.
- FastAPI is the canonical domain API from the beginning.
- Python uses asyncio and Pydantic. SQLAlchemy 2.x with an async PostgreSQL driver is preferred unless SQLModel is deliberately chosen for its learning value and remains adequate for the schema.
- Keep modules organized by domain boundary: captures, interpretation, clarification, planning, domain entities, focus, routines, reviews, and integrations.
- Do not duplicate core business rules separately in web and mobile clients.
- Use background processing for transcription, model interpretation, synchronization retries, and scheduled reminders where asynchronous work is required.
- Keep the first implementation free of Redis, Kafka, Kubernetes, and unnecessary service decomposition.

### Database and Storage

- Use Supabase PostgreSQL as the canonical database from day one.
- Use Supabase Auth, PostgreSQL Row Level Security, and Supabase Storage.
- Preserve raw captures, structured interpretations, confirmations, version history, lifecycle changes, sync operations, and external identifiers.
- Store raw audio temporarily and delete it after confirmed transcription and interpretation.
- Use PostgreSQL full-text search first. Add pgvector only when semantic retrieval provides a demonstrated benefit.
- Backups and portable export are required later but are not part of the first working system.

### AI and Voice

- Use hosted APIs only. No local LLM, self-hosted model, fine-tuning, or model-serving infrastructure.
- Use an OpenAI-compatible provider adapter so OpenRouter and other hosted providers can be changed by configuration.
- Prefer low-cost or free hosted models and ASR providers after validating capability.
- Use English-only voice input initially.
- Start with complete-ramble, turn-based interaction. Fully live interruptible voice is deferred.
- Validate all structured model output with Pydantic before persistence.
- Preserve provider/model, latency, cost, and confidence metadata for each AI operation.
- Use sensitivity gating before sending selected content to external providers.
- Keep the conversational clarification engine separate from domain persistence and external actions.

### Canonical Domain Model

- Area: ongoing responsibility with no completion condition.
- Goal: desired outcome with an observable condition and review horizon.
- Project: finite effort, optionally linked to an Area and/or Goal.
- Task: actionable work with exactly one primary owner.
- Subtask: child work under a Task or Project; only executable leaf items receive time tracking and scheduling.
- Capture: original unprocessed voice or text input.
- Routine: recurring behavior, metric, or review cycle.
- Routine instance: one occurrence of a Routine.
- Event: time-bound commitment.
- Focus block: overall calendar/Toggl period containing work and Pomodoro breaks.
- Focus interval: internal work or break segment inside a Focus block.
- Resource: reference material or reusable knowledge.
- Projection: representation of canonical data in an external tool.
- Sync operation: durable outbound or inbound integration action with status and retry metadata.

### Lifecycle Model

- Captures may be Captured, Clarifying, Proposed, Confirmed, or Archived.
- Tasks may be Confirmed, Planned, In Progress, Blocked, Waiting, Completed, Superseded, or Archived.
- Projects may be Proposed, Active, Paused, Completed, Superseded, or Archived.
- Goals may be Active, Achieved, Paused, Abandoned, Replaced, or Archived.
- Routines may produce Completed, Partial, Skipped, or Deferred instances.
- Detailed states remain internal; user-facing views group them into Needs attention, Planned, In progress, Blocked/Waiting, Completed, and Archived.
- Archival hides records from normal views without permanent deletion. Raw audio is the explicit exception because it is transient processing data.

### Clarification and Action Rules

- Every capture is preserved verbatim.
- The assistant provides concise classification reasoning.
- Ask one question at a time, prioritizing information that materially changes direction.
- Important missing information must be requested when proceeding could waste significant effort or create an unwanted commitment.
- If the user explicitly reports depletion or avoidance, the assistant may propose a safe provisional action while preserving unresolved questions.
- Provisional actions are reversible, marked provisional, limited to one focus session, and reviewed afterward.
- Decomposition stops when a task fits one 25/5 or 50/10 session, has one observable outcome, and has no unresolved blocking dependency.
- Do not create meaningless micro-tasks.
- Decompose further only after the user requests it or provides new execution evidence. The assistant may suggest deeper decomposition but may not silently create it.

### Scheduling, Focus, and Review

- Evening or previous-day planning creates a draft; morning planning confirms reality.
- Daily planning uses calendar constraints, capacity, energy, dependencies, estimates, deadlines, meals, commute, routines, and recovery time.
- Reserve approximately 30-40% of realistic capacity as slack.
- Google Calendar owns final event timing and rescheduling.
- Calendar displays one overall Focus block, not separate Pomodoro breaks.
- Toggl displays one overall Focus block including planned breaks. The app privately stores detailed work/break intervals and calculates net work.
- The app owns the focus timer and supports 25/5 and 50/10 configurations.
- Hans Zimmer OST is the default Focus profile. Other non-lyrical profiles may be suggested based on stated mood/context but require user approval.
- The app owns planning, routine, focus, and recovery reminders. Google Calendar owns actual event notifications.
- Reminder actions are Done, Snooze, Reschedule, Skip, and Not relevant. Dismissal is unresolved and triggers limited follow-up.
- Sleep/wake tracking starts with one-tap manual bedtime and wake logging. Health Connect may be added later if a data source becomes available.

### Integration Authority

- Supabase is canonical for meaning, history, lifecycle, relationships, and versions.
- Superlist is an execution projection for confirmed tasks, routine instances, and active project containers where useful.
- Superlist may use only the existing 52 lists. The integration must never create, delete, rename, or automatically reassign lists.
- Project-to-list mappings require explicit confirmation.
- Superlist owns simple execution state and syncs it back.
- Google Calendar is authoritative for event time, duration, conflicts, cancellation, and rescheduling.
- Toggl represents overall Focus block attendance, not net productive minutes.
- Notion receives a controlled one-way projection initially.
- YouTube Music is represented by stored playlist links and open actions only.
- Confirmed outbound changes synchronize automatically. Destructive changes require separate confirmation.
- Sync operations are durable, retryable, idempotent, and conflict-aware. Conflicts preserve both versions and require user resolution.

### Security and Deployment

- Use Supabase Auth with Google sign-in and passkey support where available.
- Restrict access to the single user's account.
- Apply RLS to all personal records and keep privileged keys server-side.
- Use HTTPS, managed secrets, and least-privilege integration credentials.
- Deploy the web client to Vercel and the FastAPI backend to Google Cloud Run. Supabase remains managed infrastructure.
- Operate online-only initially. Offline capture is explicitly deferred.

## Testing Decisions

Good tests should verify externally observable behavior at the highest practical seam. They should not assert internal implementation details, exact prompts, or framework-specific structure unless those are contractual boundaries.

### Primary Product Seam

Test the end-to-end domain boundary:

> Given a capture and user clarification responses, the system produces a validated canonical proposal, persists the confirmed result and version history, and emits an idempotent projection command for the selected external system.

This seam proves the product's central value without making core tests depend on live third-party APIs.

### Core Test Areas

- Capture processing: original input is preserved, raw audio retention ends after confirmation, and failures remain visible.
- Clarification: important missing information produces questions, concise reasoning is returned, and confirmation is required before commitments.
- Domain classification: tasks, projects, areas, goals, routines, events, resources, and captures are classified according to the canonical model.
- Decomposition: leaf tasks satisfy the focused-session and definition-of-done rules without meaningless micro-tasks.
- Lifecycle: state transitions, archival, superseding, and version history preserve meaning.
- Planning: fixed events, capacity buffers, estimates, routines, and replanning produce realistic plans.
- Focus: one calendar/Toggl block contains internal work/break intervals; the focus timer supports configured cycles.
- Rescue mode: stuck/depleted input generates a safe time-boxed action while retaining unresolved questions.
- Sync orchestration: confirmed changes produce durable idempotent operations, retry after failures, and never silently disappear.
- Conflict resolution: both versions are preserved and no external change is silently overwritten.
- Superlist safety: existing lists are never created, deleted, renamed, or auto-reassigned.
- Authentication and authorization: only the authenticated user can access personal records.
- AI provider seam: provider/model configuration, typed output validation, failure handling, and operation metadata.
- Mobile behavior: widget launch, recording, notification actions, focus timer, and cross-device state synchronization.

### External Integration Tests

Use adapter contract tests with fakes for normal test runs and configuration-gated integration tests against development accounts for:

- Google Calendar.
- Toggl.
- Superlist.
- Notion.
- ASR and LLM providers.

No test should depend on deleting a Superlist list, creating a new list, or mutating the user's production data.

### Review and Behavioral Tests

- Test review summaries against recorded focus blocks, routines, interruptions, and plan changes.
- Test reminder state actions and follow-up limits.
- Test sleep baseline tracking and adaptive replanning.
- Test that progress metrics reward meaningful movement and recovery rather than raw task counts.

## Out of Scope

- Recreating Notion, Google Calendar, Toggl, Superlist, or YouTube Music.
- Fully live, interruptible voice conversation in the first version.
- Offline capture and synchronization in the first version.
- Self-hosted or local LLMs, ASR, or TTS.
- Fine-tuning models.
- Multi-user accounts, sharing, collaboration, or workspaces.
- Automatic Superlist list creation, deletion, renaming, or reassignment.
- Superlist projection of captures, resources, goals, or areas.
- Full bidirectional Notion editing in the first version.
- Direct YouTube Music playback control.
- Device-level website blocking. StayFree and Android controls remain responsible for enforcement.
- Perfect behavior change, addiction treatment, or clinical sleep intervention.
- Backups and portable export in the first working milestone.
- Premature semantic search, vector retrieval, or a custom vector database.
- Redis, Kafka, Kubernetes, microservices, or other infrastructure without a concrete need.

## Further Notes

- The product is intentionally iterative. The first action model may be refined after real attempts reveal missing information.
- Bias to action means reducing uncertainty through a safe attempt, not skipping important clarification.
- The user remains the final authority over commitments, sensitive AI disclosure, external destructive actions, and material plan changes.
- AI operation metadata should support cost and quality decisions, but the first optimization target is capability and a reliable workflow.
- The project should be developed as a learning-friendly system. Tickets should briefly explain the concept, decision, acceptance criteria, and verification method.
- Linear project: GlueKPS in the Karthik Arigela Personal Projects workspace. Linear publication and tracer-bullet ticket creation are subsequent steps.
