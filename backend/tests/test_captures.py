import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_and_get_capture(async_client: AsyncClient):
    payload = {
        "raw_text": "I want to build a voice AI assistant for recipe notes",
        "kind": "text"
    }

    create_res = await async_client.post("/captures/", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert "capture_id" in created_data
    assert created_data["state"] in ["clarifying", "ready_for_proposal"]
    assert "messages" in created_data

    capture_id = created_data["capture_id"]

    get_res = await async_client.get(f"/captures/{capture_id}")
    assert get_res.status_code == 200
    single_data = get_res.json()
    assert single_data["id"] == capture_id
    assert single_data["raw_text"] == payload["raw_text"]

    list_res = await async_client.get("/captures/")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert isinstance(list_data, list)
    assert len(list_data) >= 1