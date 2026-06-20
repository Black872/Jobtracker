from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.vacancy import Vacancy  # noqa: E402, F401
