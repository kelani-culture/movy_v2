from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from schemas.settings import setting

settings = setting()


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constrain_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


DATABASE_URL = (
    f"mysql+pymysql://{settings.local_user}:"
    + f"{settings.local_db_password}@"
    + f"{settings.local_hostname}/{settings.local_db}"
)

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
