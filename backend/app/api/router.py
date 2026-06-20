from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.vacancies import router as vacancies_router
from app.db.session import get_db

router = APIRouter()
router.include_router(vacancies_router, prefix="/api/v1/vacancies", tags=["vacancies"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/health", tags=["health"])
def health(db: DatabaseSession) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


api_router = router
