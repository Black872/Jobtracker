from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    computed_field,
    field_validator,
    model_validator,
)

from app.models.vacancy import VacancyStatus


class SortField(StrEnum):
    CREATED_AT = "created_at"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class VacancyFields(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    company_name: str = Field(min_length=1, max_length=255)
    position_title: str = Field(min_length=1, max_length=255)
    job_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=255)
    employment_type: str | None = Field(default=None, max_length=100)
    salary_min: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    salary_max: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    application_date: date | None = None
    status: VacancyStatus = VacancyStatus.WISHLIST
    contact_person: str | None = Field(default=None, max_length=255)
    contact_email: EmailStr | None = None
    contact_phone: str | None = Field(default=None, max_length=50)
    notes: str | None = None

    @field_validator(
        "location", "employment_type", "contact_person", "contact_phone", "notes", mode="after"
    )
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        return value or None

    @field_validator("application_date")
    @classmethod
    def application_date_is_not_future(cls, value: date | None) -> date | None:
        if value is not None and value > datetime.now(UTC).date():
            raise ValueError("application_date cannot be in the future")
        return value

    @model_validator(mode="after")
    def salary_range_is_valid(self) -> Self:
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min cannot exceed salary_max")
        return self


class VacancyCreate(VacancyFields):
    pass


class VacancyUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    company_name: str | None = Field(default=None, min_length=1, max_length=255)
    position_title: str | None = Field(default=None, min_length=1, max_length=255)
    job_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=255)
    employment_type: str | None = Field(default=None, max_length=100)
    salary_min: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    salary_max: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    application_date: date | None = None
    status: VacancyStatus | None = None
    contact_person: str | None = Field(default=None, max_length=255)
    contact_email: EmailStr | None = None
    contact_phone: str | None = Field(default=None, max_length=50)
    notes: str | None = None

    @field_validator("company_name", "position_title")
    @classmethod
    def required_strings_cannot_be_null(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("field cannot be null")
        return value

    @field_validator("status")
    @classmethod
    def status_cannot_be_null(cls, value: VacancyStatus | None) -> VacancyStatus | None:
        if value is None:
            raise ValueError("field cannot be null")
        return value

    @field_validator("application_date")
    @classmethod
    def application_date_is_not_future(cls, value: date | None) -> date | None:
        return VacancyFields.application_date_is_not_future(value)


class VacancyRead(VacancyFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status_changed_at: datetime
    created_at: datetime
    updated_at: datetime

    @computed_field  # type: ignore[prop-decorator]
    @property
    def days_since_application(self) -> int | None:
        if self.application_date is None:
            return None
        return max(0, (datetime.now(UTC).date() - self.application_date).days)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def days_in_current_status(self) -> int:
        changed_at = self.status_changed_at
        if changed_at.tzinfo is None:
            changed_at = changed_at.replace(tzinfo=UTC)
        return max(0, (datetime.now(UTC).date() - changed_at.astimezone(UTC).date()).days)


class VacancyList(BaseModel):
    items: list[VacancyRead]
    total: int
    limit: int
    offset: int
