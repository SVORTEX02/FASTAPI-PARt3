from sqlalchemy import Column, Integer, String, ARRAY, Date, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum
from sqlalchemy.sql import func
Base = declarative_base()

class DestinationDB(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    comments = Column(ARRAY(String), nullable=False)  


class UserDetail(Base):
    __tablename__="user"
    
    id=Column(Integer,primary_key=True,index=True,unique=True)
    name=Column(String,nullable=True)
    password=Column(String,nullable=True)
    hashed_password=Column(String,nullable=True)
    
class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    priority = Column(Integer, nullable=False)
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )
    due_date = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    attachment = Column(String, nullable=True) 