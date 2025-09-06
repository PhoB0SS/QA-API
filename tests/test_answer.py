"""Answer test"""

import uuid

import pytest


@pytest.mark.asyncio
async def test_create_answer(client):
    """Create an answer test"""

    await client.post("/questions/", json={"text": "Test question"})

    response = await client.post("/questions/1/answers/", json={
        "question_id": 1,
        "user_id": str(uuid.uuid4()),
        "text": "Test answer"
    })
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_answer(client):
    """Get an answer test"""

    response = await client.get("/answers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["text"].startswith("Test answer")


@pytest.mark.asyncio
async def test_delete_answer(client):
    """Delete an answer test"""

    response = await client.delete("/answers/1")
    assert response.status_code == 200
