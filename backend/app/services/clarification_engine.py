import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Capture
from app.schemas import LLMClarificationOutput, ClarificationResponse
from app.services.ai_adapter import OpenAIResponsesAdapter, AIAdapter
from app.services.ai_telemetry import record_ai_operation

CLARIFICATION_SYSTEM_PROMPT = """
You are the GlueKPS Clarification Co-Pilot. Your job is to transform raw human thoughts into clear, structured, actionable projects or tasks.
Analyze the user's initial raw capture and any subsequent conversation Q&A history.
Guidelines:
1. CLASSIFY the intention:
   - 'project': Multi-step initiative requiring multiple sessions, contexts, or distinct sub-tasks.
   - 'task': A single, clear execution unit (usually doable in one focused session).
   - 'not_actionable': A random thought, greeting, quote, or note that requires no execution.
2. EVALUATE STATUS:
   - If 'not_actionable', set status='terminal' and question=null.
   - If you have enough clear details (Outcome, Scope, Key Requirements/Constraints) to build a detailed project/task tree proposal, set status='ready_for_proposal' and question=null.
   - Otherwise, set status='question' and provide ONE focused clarifying question.
3. QUESTION RULES:
   - Ask strictly ONE question at a time.
   - Focus on missing critical details: Why/Outcome, Scope, Dependencies, Constraints, or Definition of Done.
   - Be concise, direct, and conversational.
"""

class ClarificationEngine:
    def __init__(self, ai_adapter: AIAdapter | None = None):
        self.ai_adapter = ai_adapter or OpenAIResponsesAdapter()
     
    async def process_clarification(self, session: AsyncSession, capture: Capture, user_answer: str | None = None) -> ClarificationResponse:
        """Processes a clarification turn: initial start, thread resume, or user answer turn."""
        history = list(capture.clarification_history) if capture.clarification_history else []

        # Case A: Resume/Reload active Conversation (No new User Answer & History already exists)
        if user_answer is None and history:
            return self._build_response(capture, last_output=None)

        # Case B: Initial Clarification Conversation (No history yet)
        if user_answer is None and not history:
            history.append({"role": "user", "content": f"Raw Capture Intention: {capture.raw_text}"})

        # Case C: User Answers the Clarification Questions
        elif user_answer is not None:
            history.append({"role": "user", "content": user_answer})

        prompt = json.dumps(history)
        llm_output, latency_ms, raw_text = await self.ai_adapter.generate_structured(
            prompt=prompt,
            system_prompt=CLARIFICATION_SYSTEM_PROMPT,
            response_model=LLMClarificationOutput
        )

        await record_ai_operation(
            session=session,
            capture_id=capture.id,
            provider=self.ai_adapter.provider_name,
            model=self.ai_adapter.model,
            prompt=prompt,
            response=raw_text,
            latency_ms=latency_ms,
        )

        if llm_output.question:
            history.append({"role": "assistant", "content": llm_output.question})
        elif llm_output.status == "ready_for_proposal":
            history.append({"role": "assistant", "content": "I have enough details to generate your project proposal!"})
        
        capture.clarification_history = history
        
        if llm_output.outcome:
            capture.outcome = llm_output.outcome
        if llm_output.status == "ready_for_proposal":
            capture.state = "ready_for_proposal"
        elif llm_output.status == "terminal":
            capture.state = "not_actionable"
        else:
            capture.state = "clarifying"
        
        capture.updated_at = datetime.utcnow()
        session.add(capture)
        await session.commit()
        await session.refresh(capture)
        return self._build_response(capture, llm_output)
    
    def _build_response(self, capture: Capture, last_output: LLMClarificationOutput | None) -> ClarificationResponse:
        return ClarificationResponse(
            capture_id=capture.id,
            state=capture.state,
            classification=last_output.classification if last_output else "project",
            status=last_output.status if last_output else ("ready_for_proposal" if capture.state == "ready_for_proposal" else "question"),
            question=last_output.question if last_output else None,
            reasoning=last_output.reasoning if last_output else "Resumed existing conversation state.",
            summary_so_far=last_output.summary_so_far if last_output else None,
            messages=capture.clarification_history,
        )