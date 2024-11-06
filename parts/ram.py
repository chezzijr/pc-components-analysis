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
    first_word_latency: Mapped[float] # in nanoseconds
    cas_latency: Mapped[int] # in clock cycles

    def __repr__(self):
        return (
            f"The {self.name} Random Access Memory (RAM) module "
            f"has a memory size of {self.memory_size} GB, "
            f"features {self.memory_type} memory type, "
            f"with a bus speed of {self.bus_speed} MHz, "
            f"a first word latency of {self.first_word_latency} ns "
            f"and a CAS latency of {self.cas_latency} clock cycles"
        )
