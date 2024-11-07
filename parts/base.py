from __future__ import annotations
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    price: Mapped[int]
    source: Mapped[str]
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"))
    component: Mapped[Component] = relationship(back_populates="prices")
