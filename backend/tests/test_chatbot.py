"""Tests for the AI medical assistant chatbot endpoint."""


def test_chat_returns_answer(client, auth_headers):
    response = client.post(
        "/api/v1/chat", json={"question": "What does a BI-RADS score mean?"}, headers=auth_headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What does a BI-RADS score mean?"
    assert len(body["answer"]) > 0
    assert isinstance(body["retrieved_context"], list)
