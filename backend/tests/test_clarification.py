import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_clarification_multi_turn_flow(async_client: AsyncClient):
    payload = {
        "raw_text": "I want to apply for my sister's passport in Hyderabad",
        "kind": "text"
    }
    create_res = await async_client.post("/captures/", json=payload)
    assert create_res.status_code == 201
    data_turn1 = create_res.json()
    capture_id = data_turn1["capture_id"]
    
    assert data_turn1["state"] == "clarifying"
    assert data_turn1["status"] in ["question", "ready_for_proposal"]
    assert len(data_turn1["messages"]) >= 2  # Raw capture + Assistant question

    answer_payload = {
        "answer": "No strict deadline, before October for holiday travel."
    }
    clarify_res = await async_client.post(f"/captures/{capture_id}/clarify", json=answer_payload)
    assert clarify_res.status_code == 200
    data_turn2 = clarify_res.json()
    
    assert data_turn2["capture_id"] == capture_id
    assert len(data_turn2["messages"]) >= 4
