from __future__ import annotations
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Component


class SSD(Component):
    __tablename__ = "ssds"
    __mapper_args__ = {
        "polymorphic_identity": "ssd",
    }
    id: Mapped[int] = mapped_column(ForeignKey("components.id"), primary_key=True)
    capacity: Mapped[int]
    cache: Mapped[Optional[int]]
    form_factor: Mapped[str]
    interface: Mapped[str]
    
    def to_query(self) -> str:
        size = f"{self.capacity}GB" if self.capacity < 1000 else f"{self.capacity // 1000}TB"
        return f"{self.name} {size}"
