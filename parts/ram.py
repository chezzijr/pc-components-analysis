from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Component


class RAM(Component):
    __tablename__ = "rams"
    __mapper_args__ = {
        "polymorphic_identity": "ram",
    }
    id: Mapped[int] = mapped_column(ForeignKey("components.id"), primary_key=True)
    memory_size: Mapped[int]
    memory_type: Mapped[str]
    bus_speed: Mapped[int]
    module_sticks: Mapped[int]
    module_capacity: Mapped[int]
    first_word_latency: Mapped[float] # in nanoseconds
    cas_latency: Mapped[float] # in clock cycles

    def to_query(self) -> str:
        return f"{self.name} {self.memory_size}GB"
