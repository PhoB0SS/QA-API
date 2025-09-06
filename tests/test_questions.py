"""Question tests"""

import uuid

import pytest


@pytest.mark.asyncio
async def test_get_question_with_answers(client):
    """Get question with answers test"""

    question_create_response = await client.post("/questions/", json={"text": "Test question for answer"})
    assert question_create_response.status_code == 201

    question_get_response = await client.get("/questions/")
    question_id = question_get_response.json()[-1]["id"]

    answer_create_response = await client.post(f"/questions/{question_id}/answers/", json={
        "question_id": question_id,
        "text": "Test answer",
        "user_id": str(uuid.uuid4()),
    })
    assert answer_create_response.status_code == 201

    response = await client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    answer = response.json()[1][0]["text"]
    assert answer == "Test answer"


@pytest.mark.asyncio
async def test_delete_question(client):
    """Delete question test"""

    post_resp = await client.post("/questions/", json={"text": "Question to delete"})
    assert post_resp.status_code == 201

    get_resp = await client.get("/questions/")
    assert get_resp.status_code == 200
    questions = get_resp.json()

    assert any(item["text"] == "Question to delete" for item in questions)

    question_id = questions[-1]["id"]

    del_resp = await client.delete(f"/questions/{question_id}")
    assert del_resp.status_code == 200
