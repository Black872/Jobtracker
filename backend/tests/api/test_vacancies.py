from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.vacancy import Vacancy


def vacancy_payload(company: str) -> dict[str, object]:
    return {
        "company_name": company,
        "position_title": "Backend Engineer",
        "status": "applied",
        "application_date": "2026-06-01",
        "salary_min": "70000.00",
        "salary_max": "90000.00",
    }


def test_vacancy_crud(client: TestClient) -> None:
    create_response = client.post("/api/v1/vacancies", json=vacancy_payload("Acme"))
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["company_name"] == "Acme"
    assert created["days_since_application"] >= 0

    vacancy_id = created["id"]
    get_response = client.get(f"/api/v1/vacancies/{vacancy_id}")
    assert get_response.status_code == 200

    update_response = client.patch(
        f"/api/v1/vacancies/{vacancy_id}", json={"status": "interview_scheduled"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "interview_scheduled"

    delete_response = client.delete(f"/api/v1/vacancies/{vacancy_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/api/v1/vacancies/{vacancy_id}").status_code == 404


def test_list_supports_pagination_and_sorting(client: TestClient, db_session: Session) -> None:
    first = client.post("/api/v1/vacancies", json=vacancy_payload("First")).json()
    second = client.post("/api/v1/vacancies", json=vacancy_payload("Second")).json()

    first_model = db_session.get(Vacancy, UUID(first["id"]))
    second_model = db_session.get(Vacancy, UUID(second["id"]))
    assert first_model is not None and second_model is not None
    first_model.created_at = datetime(2026, 1, 1, tzinfo=UTC)
    second_model.created_at = datetime(2026, 2, 1, tzinfo=UTC)
    db_session.commit()

    response = client.get("/api/v1/vacancies?sort=created_at&order=desc&limit=1&offset=0")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["limit"] == 1
    assert body["items"][0]["company_name"] == "Second"

    ascending = client.get("/api/v1/vacancies?sort=created_at&order=asc")
    assert ascending.json()["items"][0]["company_name"] == "First"


def test_list_rejects_unsupported_sort_field(client: TestClient) -> None:
    response = client.get("/api/v1/vacancies?sort=company_name&order=desc")
    assert response.status_code == 422


def test_validation_rejects_invalid_salary_range(client: TestClient) -> None:
    payload = vacancy_payload("Acme")
    payload["salary_min"] = "100000"
    payload["salary_max"] = "50000"
    response = client.post("/api/v1/vacancies", json=payload)
    assert response.status_code == 422


def test_health_checks_database(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
