from typing import Collection
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import JSON
from src.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(
        String(255),
        primary_key=True,
        comment="기본키",
    )
    project_name = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="프로젝트명"
    )
    description = Column(
        Text,
        nullable=True,
        comment="설명",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )

class Model(Base):
    __tablename__ = "models"

    model_id = Column(
        String(255),
        primary_key=True,
        comment="기본키",
    )
    project_id = Column(
        String(255),
        ForeignKey("projects.project_id"),
        nullable=False,
        comment="외부키",
    )
    model_name = Column(
        String(255),
        nullable=False,
        comment="모델명",
    )
    description = Column(
        Text,
        nullable=True,
        comment="설명",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )

class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(
        String(255),
        primary_key=True,
        comment="기본키",
    )
    model_id = Column(
        String(255),
        ForeignKey("models.model_id"),
        nullable=False,
        comment="외부키",
    )
    model_version_id = Column(
        String(255),
        nullable=False,
        comment="모델 실험 버전 ID",
    )
    parameters = Column(
        JSON,
        nullable=True,
        comment="학습 파라미터",
    )
    training_dataset = Column(
        Text,
        nullable=True,
        comment="학습 데이터",
    )
    validation_dataset = Column(
        Text,
        nullable=True,
        comment="평가 데이터",
    )
    test_dataset = Column(
        Text,
        nullable=True,
        comment="테스트 데이터",
    )
    evaluations = Column(
        JSON,
        nullable=True,
        comment="평가결과",
    )
    artifact_file_paths = Column(
        JSON,
        nullable=True,
        comment="모델 파일 경로",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )