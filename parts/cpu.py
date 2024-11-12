from __future__ import annotations
from .base import Component
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class CPU(Component):
    __tablename__ = "cpus"
    __mapper_args__ = {
        "polymorphic_identity": "cpu",
    }
    id: Mapped[int] = mapped_column(ForeignKey("components.id"), primary_key=True)
    core_count: Mapped[int]
    core_clock: Mapped[float]
    boost_clock: Mapped[Optional[float]]
    tdp: Mapped[int]
    graphics: Mapped[Optional[str]]  # integrated graphics
    smt: Mapped[bool]  # simultaneous multithreading

    def to_query(self) -> str:
        return f"{self.name}"
