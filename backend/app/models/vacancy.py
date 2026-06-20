import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, Numeric, String, Text, func
from sqlalchemy import Uuid as SQLAlchemyUuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VacancyStatus(StrEnum):
    WISHLIST = "wishlist"
    APPLIED = "applied"
    RESPONSE_RECEIVED = "response_received"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    TECHNICAL_INTERVIEW = "technical_interview"
    FINAL_INTERVIEW = "final_interview"
    OFFER = "offer"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


def vacancy_status_values(enum_class: type[VacancyStatus]) -> list[str]:
    return [member.value for member in enum_class]


class Vacancy(Base):
    __tablename__ = "vacancies"
    __table_args__ = (
        CheckConstraint("salary_min IS NULL OR salary_min >= 0", name="ck_salary_min_positive"),
        CheckConstraint("salary_max IS NULL OR salary_max >= 0", name="ck_salary_max_positive"),
        CheckConstraint(
            "salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max",
            name="ck_salary_range",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    position_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_url: Mapped[str | None] = mapped_column(String(2048))
    location: Mapped[str | None] = mapped_column(String(255))
    employment_type: Mapped[str | None] = mapped_column(String(100))
    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    application_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[VacancyStatus] = mapped_column(
        Enum(
            VacancyStatus,
            name="vacancy_status",
            native_enum=False,
            create_constraint=True,
            values_callable=vacancy_status_values,
        ),
        nullable=False,
        default=VacancyStatus.WISHLIST,
    )
    contact_person: Mapped[str | None] = mapped_column(String(255))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    contact_phone: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
    status_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
