from __future__ import annotations
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Component

class VGA(Component):
    __tablename__ = "vgas"
    __mapper_args__ = {
        "polymorphic_identity": "vga",
    }

    id: Mapped[int] = mapped_column(ForeignKey("components.id"), primary_key=True)
    chipset: Mapped[str]
    memory: Mapped[float]  # in GB
    core_clock: Mapped[Optional[float]]  # in MHz
    boost_clock: Mapped[Optional[float]]  # in MHz
    length: Mapped[Optional[int]]

    def to_query(self) -> str:
        return f"{self.name} {self.chipset}GB"

    def __repr__(self):
        return (
            f"The {self.name} Video Graphics Array (VGA) or Graphics Processing Unit (GPU) or Graphics Card "
            f"is powered by the {self.chipset} chipset, "
            f"features {self.memory} GB of memory, "
            f"{f'with a core clock of {self.core_clock} MHz ' if self.core_clock else ''}"
            f"{f'and a boost clock of {self.boost_clock} MHz ' if self.boost_clock else ''}"
            f"{f'and a length of {self.length} mm ' if self.length else ''}"
        )
