from __future__ import annotations
from .base import Component
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Mainboard(Component):
    __tablename__ = "mainboards"
    __mapper_args__ = {
        "polymorphic_identity": "mainboard",
    }
    id: Mapped[int] = mapped_column(ForeignKey("components.id"), primary_key=True)
    socket: Mapped[str]
    form_factor: Mapped[str]
    max_memory: Mapped[int]
    memory_slots: Mapped[int]

    def to_query(self) -> str:
        return f"{self.name}"
