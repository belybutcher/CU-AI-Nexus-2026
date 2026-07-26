"""Tests for the prediction (classification) endpoints."""
import io

from PIL import Image


def _sample_png_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), color=(100, 150, 200)).save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def _upload_sample_image(client, auth_headers) -> str:
    files = {"file": ("scan.png", _sample_png_bytes(), "image/png")}
    response = client.post(
        "/api/v1/upload", files=files, data={"disease": "breast", "modality": "ultrasound"}, headers=auth_headers
    )
    return response.json()["image_id"]


def test_predict_breast_classification(client, auth_headers):
    image_id = _upload_sample_image(client, auth_headers)
    response = client.post(
        "/api/v1/predict",
        json={"image_id": image_id, "disease": "breast", "generate_heatmap": True},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["predicted_label"] in ("normal", "benign", "malignant")
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["heatmap_path"] is not None


def test_predict_unknown_disease_returns_503(client, auth_headers):
    image_id = _upload_sample_image(client, auth_headers)
    response = client.post(
        "/api/v1/predict",
        json={"image_id": image_id, "disease": "unknown_disease"},
        headers=auth_headers,
    )
    assert response.status_code == 503


def test_get_prediction_by_id(client, auth_headers):
    image_id = _upload_sample_image(client, auth_headers)
    predict_response = client.post(
        "/api/v1/predict", json={"image_id": image_id, "disease": "breast"}, headers=auth_headers
    )
    prediction_id = predict_response.json()["id"]

    get_response = client.get(f"/api/v1/prediction/{prediction_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == prediction_id
