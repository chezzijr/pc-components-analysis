from dataclasses import dataclass


@dataclass
class CPU:
    name: str
    core_count: int
    core_clock: float
    boost_clock: float | None
    tdp: int
    graphics: str | None  # integrated graphics
    smt: bool  # simultaneous multithreading

    # we need to flatten our dataclass in a manner that’s convenient to plug it into Chroma
    def __str__(self):
        return (
            f"The {self.name} Central Processing Unit (CPU) "
            f"features {self.core_count} cores running at a base clock of {self.core_clock} GHz "
            f"{f'with a boost clock up to {self.boost_clock} GHz' if self.boost_clock else ''}, "
            f"a thermal design power (TDP) of {self.tdp} W, "
            f"{f'{self.graphics} as' if self.graphics else "with no"} integrated graphics "
            f"and {'supports' if self.smt else 'does not support'} simultaneous multithreading "
        )
