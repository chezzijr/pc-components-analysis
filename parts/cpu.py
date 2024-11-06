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

    # we need to flatten our dataclass in a manner that’s convenient to plug it into Chroma
    def __repr__(self):
        return (
            f"The {self.name} Central Processing Unit (CPU) "
            f"features {self.core_count} cores running at a base clock of {self.core_clock} GHz "
            f"{f'with a boost clock up to {self.boost_clock} GHz' if self.boost_clock else ''}, "
            f"a thermal design power (TDP) of {self.tdp} W, "
            f"{f'{self.graphics} as' if self.graphics else "with no"} integrated graphics "
            f"and {'supports' if self.smt else 'does not support'} simultaneous multithreading "
        )
