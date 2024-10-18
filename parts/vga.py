from dataclasses import dataclass


@dataclass
class VGA:
    name: str
    chipset: str
    memory: float  # in GB
    core_clock: float | None  # in MHz
    boost_clock: float | None  # in MHz
    color: str | None # ignore
    length: int | None

    def __str__(self):
        return (
            f"The {self.name} Video Graphics Array (VGA) or Graphics Processing Unit (GPU) or Graphics Card "
            f"is powered by the {self.chipset} chipset, "
            f"features {self.memory} GB of memory, "
            f"{f'with a core clock of {self.core_clock} MHz ' if self.core_clock else ''}"
            f"{f'and a boost clock of {self.boost_clock} MHz ' if self.boost_clock else ''}"
            f"{f'and a length of {self.length} mm ' if self.length else ''}"
        )
