from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


engine = create_engine(
    "postgresql://postgres:vortex02@localhost:5432/my_dest_db",
    echo=True  #  This is what you’re asking about
)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()