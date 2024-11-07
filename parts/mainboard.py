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
    name: Mapped[str]
    socket: Mapped[str]
    form_factor: Mapped[str]
    max_memory: Mapped[int]
    memory_slots: Mapped[int]

    def to_query(self) -> str:
        return f"{self.name}"

    # we need to flatten our dataclass in a manner that’s convenient to plug it into Chroma
    def __repr__(self):
        return (
            f"The {self.name} Mainboard or Motherboard is the central printed circuit board (PCB) "
            f"that holds and allows communication between crucial electronic components of a computer system. "
            f"It features {self.memory_type} memory type, "
            f"with a bus speed of {self.bus_speed} MHz, "
            f"and supports {self.memory_size} GB of RAM"
        )
