"""Task, Project, and Comment SQLAlchemy models."""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime,
    ForeignKey, Enum, Index
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, ARRAY
from sqlalchemy.orm import relationship, DeclarativeBase
import uuid
import enum


class Base(DeclarativeBase):
    pass


class Priority(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    columns = relationship("BoardColumn", back_populates="project", order_by="BoardColumn.order")
    tasks = relationship("Task", back_populates="project")


class BoardColumn(Base):
    __tablename__ = "board_columns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    order = Column(Integer, default=0)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column", order_by="Task.position")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    column_id = Column(UUID(as_uuid=True), ForeignKey("board_columns.id"), nullable=False)
    position = Column(Integer, default=0)  # Order within column
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    assignee_id = Column(UUID(as_uuid=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    labels = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    # Full-text search vector (auto-updated via PostgreSQL trigger)
    search_vector = Column(TSVECTOR)

    project = relationship("Project", back_populates="tasks")
    column = relationship("BoardColumn", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", order_by="Comment.created_at")

    __table_args__ = (
        Index("idx_task_search", "search_vector", postgresql_using="gin"),
        Index("idx_task_project", "project_id"),
        Index("idx_task_assignee", "assignee_id"),
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    mentions = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="comments")
