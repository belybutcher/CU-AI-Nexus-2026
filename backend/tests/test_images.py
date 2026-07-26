"""Tests for image upload and enhancement endpoints."""
import io

from PIL import Image


def _sample_png_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), color=(100, 150, 200)).save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def test_upload_image_requires_auth(client):
    files = {"file": ("scan.png", _sample_png_bytes(), "image/png")}
    response = client.post("/api/v1/upload", files=files, data={"disease": "breast"})
    assert response.status_code == 401


def test_upload_and_enhance_image(client, auth_headers):
    files = {"file": ("scan.png", _sample_png_bytes(), "image/png")}
    upload_response = client.post(
        "/api/v1/upload", files=files, data={"disease": "breast", "modality": "ultrasound"}, headers=auth_headers
    )
    assert upload_response.status_code == 201
    image_id = upload_response.json()["image_id"]

    enhance_response = client.post(
        "/api/v1/enhance", json={"image_id": image_id, "disease": "breast"}, headers=auth_headers
    )
    assert enhance_response.status_code == 200
    assert enhance_response.json()["image_id"] == image_id

    fetch_response = client.get(f"/api/v1/enhanced/{image_id}", headers=auth_headers)
    assert fetch_response.status_code == 200


def test_upload_rejects_unsupported_extension(client, auth_headers):
    files = {"file": ("scan.txt", b"not an image", "text/plain")}
    response = client.post("/api/v1/upload", files=files, data={"disease": "breast"}, headers=auth_headers)
    assert response.status_code == 422
