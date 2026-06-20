from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.vacancy import Vacancy
from app.schemas.vacancy import SortField, SortOrder, VacancyCreate, VacancyUpdate


def _persistence_values(payload: VacancyCreate | VacancyUpdate) -> dict[str, Any]:
    values = payload.model_dump(exclude_unset=True)
    if "job_url" in values and values["job_url"] is not None:
        values["job_url"] = str(values["job_url"])
    if "contact_email" in values and values["contact_email"] is not None:
        values["contact_email"] = str(values["contact_email"])
    return values


def create(db: Session, payload: VacancyCreate) -> Vacancy:
    vacancy = Vacancy(**_persistence_values(payload))
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy


def get(db: Session, vacancy_id: UUID) -> Vacancy | None:
    return db.get(Vacancy, vacancy_id)


def list_all(
    db: Session,
    sort: SortField,
    order: SortOrder,
    limit: int,
    offset: int,
) -> tuple[list[Vacancy], int]:
    sort_columns = {SortField.CREATED_AT: Vacancy.created_at}
    sort_column = sort_columns[sort]
    ordering = sort_column.asc() if order is SortOrder.ASC else sort_column.desc()

    query = select(Vacancy).order_by(ordering, Vacancy.id.asc()).limit(limit).offset(offset)
    items = list(db.scalars(query).all())
    total = db.scalar(select(func.count()).select_from(Vacancy)) or 0
    return items, total


def update(db: Session, vacancy: Vacancy, payload: VacancyUpdate) -> Vacancy:
    values = _persistence_values(payload)
    salary_min = values.get("salary_min", vacancy.salary_min)
    salary_max = values.get("salary_max", vacancy.salary_max)
    if salary_min is not None and salary_max is not None and salary_min > salary_max:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="salary_min cannot exceed salary_max",
        )

    new_status = values.get("status")
    if new_status is not None and new_status != vacancy.status:
        vacancy.status_changed_at = datetime.now(UTC)

    for field, value in values.items():
        setattr(vacancy, field, value)

    db.commit()
    db.refresh(vacancy)
    return vacancy


def delete(db: Session, vacancy: Vacancy) -> None:
    db.delete(vacancy)
    db.commit()
