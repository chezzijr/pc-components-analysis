from __future__ import annotations
from datetime import datetime
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Component(Base):
    __tablename__ = "components"
    __mapper_args__ = {"polymorphic_identity": "component"}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    prices: Mapped[List[Price]] = relationship(back_populates="component")

class Price(Base):
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(BigInteger)
    source: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"))
    component: Mapped[Component] = relationship(back_populates="prices")
