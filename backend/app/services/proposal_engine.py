import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai_adapter import OpenAIResponsesAdapter, AIAdapter
from app.schemas import LLMProposalOutput, TaskNode
from app.services.ai_telemetry import record_ai_operation

PROPOSAL_SYSTEM_PROMPT = """
You are the GlueKPS Task Decomposition Engine. Your job is to transform clarified
human thoughts into a structured, executable project or task proposal.
Analyze the user's original raw capture and the complete clarification history.
Guidelines:
1. BUILD THE PROPOSAL:
    - Use root_project for a multi-step project.
    - Use standalone_tasks for a single task, with subtasks when the work genuinely
      requires multiple focused sessions.
    - Do not populate both root_project and standalone_tasks.
2. APPLY THE LEAF RULE:
    - Every leaf must fit one 25 or 50 minute focused session.
    - Every leaf must include task_instructions and an observable definition_of_done.
    - Do not invent dependencies, requirements, or facts not present in the context.
3. OUTPUT:
    - Return only the requested structured output.
    - Container nodes may omit leaf-specific fields because their subtasks represent
      the executable work.
"""

class ProposalEngine:
    def __init__(self, ai_adapter: AIAdapter | None = None):
        self.ai_adapter = ai_adapter or OpenAIResponsesAdapter()

    def validate_leaf_rule(self, node: TaskNode) -> list[str]:
        errors = []

        if node.subtasks:
            for sub in node.subtasks:
                errors.extend(self.validate_leaf_rule(sub))
            return errors

        if node.session_estimate_minutes is None or node.session_estimate_minutes > 50:
            errors.append(f"Leaf '{node.title}': session estimate must be <= 50 min")
        if not node.task_instructions:
            errors.append(f"Leaf '{node.title}': task_instructions required")
        if not node.definition_of_done:
            errors.append(f"Leaf '{node.title}': definition_of_done required")
        return errors

    def validate_proposal_shape(self, proposal: LLMProposalOutput) -> list[str]:
        errors = []
        has_project = proposal.root_project is not None
        has_standalone_tasks = bool(proposal.standalone_tasks)

        if has_project and has_standalone_tasks:
            errors.append("Proposal cannot contain both root_project and standalone_tasks")
        if not has_project and not has_standalone_tasks:
            errors.append("Proposal must contain root_project or standalone_tasks")

        return errors

    async def generate_tree_proposal(
        self,
        session: AsyncSession,
        capture_id,
        raw_text: str,
        clarification_history: list[dict],
    ) -> LLMProposalOutput:
        prompt = json.dumps({
                "raw_capture": raw_text,
                "clarification_history": clarification_history,
        })
        proposal, latency_ms, raw_response = await self.ai_adapter.generate_structured(
            prompt=prompt,
            system_prompt=PROPOSAL_SYSTEM_PROMPT,
            response_model=LLMProposalOutput,
        )

        await record_ai_operation(
            session=session,
            capture_id=capture_id,
            provider=self.ai_adapter.provider_name,
            model=self.ai_adapter.model,
            prompt=prompt,
            response=raw_response,
            latency_ms=latency_ms,
        )

        errors = self.validate_proposal_shape(proposal)
        roots = []
        if proposal.root_project:
            roots.append(proposal.root_project)
        roots.extend(proposal.standalone_tasks)

        for root in roots:
            errors.extend(self.validate_leaf_rule(root))

        if errors:
            raise ValueError("Invalid task proposal: " + "; ".join(errors))

        return proposal
