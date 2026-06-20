"""Create vacancies table.

Revision ID: 20260620_01
Revises:
Create Date: 2026-06-20
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260620_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

vacancy_status = sa.Enum(
    "wishlist",
    "applied",
    "response_received",
    "interview_scheduled",
    "technical_interview",
    "final_interview",
    "offer",
    "accepted",
    "rejected",
    "withdrawn",
    name="vacancy_status",
    native_enum=False,
    create_constraint=True,
)


def upgrade() -> None:
    op.create_table(
        "vacancies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("position_title", sa.String(length=255), nullable=False),
        sa.Column("job_url", sa.String(length=2048), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("employment_type", sa.String(length=100), nullable=True),
        sa.Column("salary_min", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("salary_max", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("application_date", sa.Date(), nullable=True),
        sa.Column("status", vacancy_status, nullable=False),
        sa.Column("contact_person", sa.String(length=255), nullable=True),
        sa.Column("contact_email", sa.String(length=320), nullable=True),
        sa.Column("contact_phone", sa.String(length=50), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "status_changed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("salary_min IS NULL OR salary_min >= 0", name="ck_salary_min_positive"),
        sa.CheckConstraint("salary_max IS NULL OR salary_max >= 0", name="ck_salary_max_positive"),
        sa.CheckConstraint(
            "salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max",
            name="ck_salary_range",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_vacancies_created_at", "vacancies", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_vacancies_created_at", table_name="vacancies")
    op.drop_table("vacancies")
