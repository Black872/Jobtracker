from datetime import UTC, date, datetime, timedelta

from app.models.vacancy import Vacancy, VacancyStatus
from app.schemas.vacancy import VacancyRead


def test_calculated_days_are_derived() -> None:
    now = datetime.now(UTC)
    vacancy = Vacancy(
        company_name="Acme",
        position_title="Engineer",
        application_date=date.today() - timedelta(days=5),
        status=VacancyStatus.APPLIED,
        status_changed_at=now - timedelta(days=2),
        created_at=now,
        updated_at=now,
    )
    vacancy.id = __import__("uuid").uuid4()

    result = VacancyRead.model_validate(vacancy)
    assert result.days_since_application == 5
    assert result.days_in_current_status == 2
