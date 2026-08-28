import uuid

import pytest

from app.schemas import LLMProposalOutput, TaskNode
from app.services import proposal_engine as proposal_engine_module
from app.services.proposal_engine import ProposalEngine
from httpx import AsyncClient


class FakeProposalAdapter:
    provider_name = "fake-provider"
    model = "fake-model"

    def __init__(self, proposal: LLMProposalOutput):
        self.proposal = proposal
        self.calls = []

    async def generate_structured(self, prompt, system_prompt, response_model):
        self.calls.append((prompt, system_prompt, response_model))
        return self.proposal, 12.5, '{"fake": true}'


def valid_leaf(title="Complete focused task"):
    return TaskNode(
        title=title,
        task_type="task",
        task_instructions="Perform the first concrete step",
        definition_of_done="The expected result is recorded",
        session_estimate_minutes=25,
    )


def valid_project():
    return TaskNode(
        title="Complete project",
        task_type="project",
        subtasks=[valid_leaf("First task")],
    )


@pytest.fixture
def engine():
    return ProposalEngine(ai_adapter=FakeProposalAdapter(LLMProposalOutput(root_project=valid_project())))


def test_valid_project_tree_passes(engine):
    assert engine.validate_proposal_shape(
        LLMProposalOutput(root_project=valid_project())
    ) == []
    assert engine.validate_leaf_rule(valid_project()) == []


def test_valid_standalone_leaf_passes(engine):
    assert engine.validate_proposal_shape(
        LLMProposalOutput(standalone_tasks=[valid_leaf()])
    ) == []


def test_valid_standalone_task_with_subtasks_passes(engine):
    standalone_task = TaskNode(
        title="Renew driving licence",
        task_type="task",
        subtasks=[valid_leaf("Collect required documents")],
    )
    assert engine.validate_proposal_shape(
        LLMProposalOutput(standalone_tasks=[standalone_task])
    ) == []
    assert engine.validate_leaf_rule(standalone_task) == []


@pytest.mark.parametrize(
    "overrides, expected_message",
    [
        ({"task_instructions": None}, "task_instructions required"),
        ({"definition_of_done": None}, "definition_of_done required"),
        ({"session_estimate_minutes": 51}, "session estimate must be <= 50 min"),
    ],
)
def test_invalid_leaf_fails_validation(engine, overrides, expected_message):
    leaf = valid_leaf()
    invalid_leaf = leaf.model_copy(update=overrides)

    errors = engine.validate_leaf_rule(invalid_leaf)

    assert expected_message in errors[0]


def test_invalid_proposal_shape_is_rejected(engine):
    mixed = LLMProposalOutput(
        root_project=valid_project(),
        standalone_tasks=[valid_leaf()],
    )
    empty = LLMProposalOutput()

    assert engine.validate_proposal_shape(mixed)
    assert engine.validate_proposal_shape(empty)


@pytest.mark.anyio
async def test_generation_records_ai_telemetry(monkeypatch):
    recorded = {}

    async def fake_record_ai_operation(**kwargs):
        recorded.update(kwargs)

    monkeypatch.setattr(
        proposal_engine_module,
        "record_ai_operation",
        fake_record_ai_operation,
    )

    adapter = FakeProposalAdapter(
        LLMProposalOutput(standalone_tasks=[valid_leaf()])
    )
    engine = ProposalEngine(ai_adapter=adapter)

    proposal = await engine.generate_tree_proposal(
        session=object(),
        capture_id=uuid.uuid4(),
        raw_text="I need to complete a focused task",
        clarification_history=[{"role": "user", "content": "Make it actionable"}],
    )

    assert proposal.standalone_tasks
    assert recorded["provider"] == "fake-provider"
    assert recorded["model"] == "fake-model"
    assert recorded["latency_ms"] == 12.5
    assert recorded["capture_id"] is not None
    assert adapter.calls[0][2] is LLMProposalOutput


@pytest.mark.anyio
async def test_proposal_endpoint_returns_404_for_unknown_capture(async_client: AsyncClient):
    response = await async_client.post(f"/captures/{uuid.uuid4()}/proposal")

    assert response.status_code == 404
    assert response.json()["detail"] == "Capture not found"
