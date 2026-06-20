from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vacancy import (
    SortField,
    SortOrder,
    VacancyCreate,
    VacancyList,
    VacancyRead,
    VacancyUpdate,
)
from app.services import vacancies as vacancy_service

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
def create_vacancy(payload: VacancyCreate, db: DatabaseSession) -> VacancyRead:
    vacancy = vacancy_service.create(db, payload)
    return VacancyRead.model_validate(vacancy)


@router.get("", response_model=VacancyList)
def list_vacancies(
    db: DatabaseSession,
    sort: SortField = SortField.CREATED_AT,
    order: SortOrder = SortOrder.DESC,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> VacancyList:
    items, total = vacancy_service.list_all(db, sort, order, limit, offset)
    response_items = [VacancyRead.model_validate(item) for item in items]
    return VacancyList(items=response_items, total=total, limit=limit, offset=offset)


@router.get("/{vacancy_id}", response_model=VacancyRead)
def get_vacancy(vacancy_id: UUID, db: DatabaseSession) -> VacancyRead:
    vacancy = vacancy_service.get(db, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    return VacancyRead.model_validate(vacancy)


@router.patch("/{vacancy_id}", response_model=VacancyRead)
def update_vacancy(vacancy_id: UUID, payload: VacancyUpdate, db: DatabaseSession) -> VacancyRead:
    vacancy = vacancy_service.get(db, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    updated = vacancy_service.update(db, vacancy, payload)
    return VacancyRead.model_validate(updated)


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacancy(vacancy_id: UUID, db: DatabaseSession) -> Response:
    vacancy = vacancy_service.get(db, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    vacancy_service.delete(db, vacancy)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
