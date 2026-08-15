# GlueKPS - Domain Context

## Product

**GlueKPS**
A private, single-user personal knowledge and productivity system that glues together existing tools. It turns vague captures into clarified, executable commitments and keeps the resulting plans aligned with real execution.

**Canonical source of truth**
Supabase PostgreSQL. It stores meaning, relationships, versions, lifecycle state, confirmations, plan history, and synchronization metadata. External applications are projections or operational authorities according to explicit rules.

**Projection**
A controlled representation of canonical data in an external application. A projection is not automatically the complete domain model.

**Capture**
An original, unprocessed voice or text input. The raw capture is preserved verbatim. Audio is temporary processing data and is deleted after transcription and interpretation are confirmed.

## Domain Model

**Area**
An ongoing responsibility with no completion condition, such as Health, Finance, Learning, or Personal Operations.

**Goal**
A desired outcome with an observable success condition and a review horizon. A goal may be exploratory initially and may be refined as information improves.

**Project**
A finite effort that produces an outcome. A project may belong to an Area, support a Goal, belong to both, or stand alone. The system must not invent a relationship merely to fill a field.

**Task**
Actionable work with exactly one primary owner. A task has a clear next action and definition of done when it is executable.

**Subtask**
A child item under a task or project. The hierarchy may be deep when genuinely needed, but the assistant stops decomposing when the item fits one focused session and has a clear outcome.

**Leaf task**
The executable task at the bottom of the current hierarchy. Calendar scheduling, focus sessions, and Toggl tracking attach to leaf tasks rather than containers.

**Resource**
Reference material, notes, or reusable knowledge. Resources remain in Supabase or are projected to Notion when appropriate; they are not sent to Superlist as execution tasks.

**Routine**
A recurring behavior, metric, or review cycle. A routine has a full version and may have a minimum viable version.

**Routine instance**
One occurrence of a routine. It can be Completed, Partial, Skipped, or Deferred.

**Event**
A time-bound commitment. Google Calendar owns the final event time, duration, conflict, cancellation, and rescheduling.

**Capture-to-action loop**
The primary product loop: capture, transcribe, interpret, clarify, propose, confirm, persist, project, execute, review, and replan.

## Execution Vocabulary

**Focus block**
The overall planned and tracked period for focused work. Calendar and Toggl each show one focus block including planned Pomodoro breaks.

**Focus interval**
An internal work or break segment within a focus block. GlueKPS stores these details; Toggl does not receive each interval by default.

**Focus profile**
A mood/context-aware focus configuration containing session settings and an optional YouTube Music playlist URL.

**Rescue mode**
A supportive flow activated by "I am stuck" or "Move me forward." It identifies the blocker, shrinks the next action, offers a safe time-boxed action, and preserves unresolved questions.

**Provisional action**
A reversible action taken when the user is depleted or avoiding clarification. It is limited to one focus session and must be reviewed afterward.

**Definition of done**
An observable condition that tells the user when a task is complete.

**Exploration task**
A task for uncertain research or discovery. It has a question, scope, stopping rule, and expected output instead of pretending that the final outcome is already known.

**Capacity buffer**
The intentional 30-40% of realistic daily capacity left unscheduled for transitions, ordinary life, overruns, recovery, and new information.

## Lifecycle

**Capture states**
Captured, Clarifying, Proposed, Confirmed, Archived.

**Task states**
Confirmed, Planned, In Progress, Blocked, Waiting, Completed, Superseded, Archived.

**Project states**
Proposed, Active, Paused, Completed, Superseded, Archived.

**Goal states**
Active, Achieved, Paused, Abandoned, Replaced, Archived.

**Archive**
A non-destructive state hidden from normal views. Archived structured records remain restorable and retain history. Raw audio is deleted after its processing purpose is complete.

**Superseded**
Replaced by a better-informed interpretation or plan. The previous version remains available for history.

## AI and Voice

**Turn-based voice**
The user records a complete ramble, ends the recording, and then receives transcription and clarification. The assistant does not interrupt the initial thought.

**ASR/STT**
Automatic Speech Recognition or Speech-to-Text: conversion of the English voice capture into text.

**Provider adapter**
A replaceable interface around a hosted ASR or LLM provider. OpenRouter and other OpenAI-compatible APIs can be changed through configuration rather than domain code.

**AI operation metadata**
Provider, model, latency, cost, and confidence recorded for each transcription or interpretation operation.

**Sensitivity gating**
Classification before external AI processing: Normal, Sensitive, or Highly private. Sensitive content requires confirmation; Highly private content requires explicit per-use approval.

## External Systems

**Superlist execution projection**
Confirmed actionable tasks, routine instances, and useful active project containers may be sent to Superlist. Only the user's existing 52 lists may be used. The integration must never create, delete, rename, or automatically reassign lists.

**Superlist list mapping**
An explicitly confirmed mapping from a canonical project to one existing Superlist list. If no mapping exists, the item remains in Supabase until a destination is chosen.

**Google Calendar authority**
Calendar is authoritative for the final timing, duration, conflict, cancellation, and rescheduling of events.

**Toggl focus-block authority**
Toggl records overall focus-block attendance, including planned breaks. GlueKPS owns detailed work/break intervals and net-work analysis.

**Notion projection**
A controlled one-way projection initially. Notion is a readable second-brain surface, not the canonical source of truth.

**YouTube Music focus profile**
A stored playlist URL and open action. Playback control and YouTube Music API dependence are out of scope.

## Planning and Review

**Evening plan draft**
A lightweight proposal for the next day.

**Morning confirmation**
The final plan recalculated using actual wake time, energy, calendar commitments, available capacity, and changed constraints.

**Daily review**
End-of-day reconciliation of focus blocks, unfinished work, distractions, and changed assumptions.

**Weekly review**
Inspection of project progress, escape patterns, reminder failures, estimate accuracy, and plan adjustments.

**Quarterly review**
Review of goals, areas, and quarterly quests.

**Meaningful progress**
Movement toward outcomes and project completion, not merely the number of checked tasks.
