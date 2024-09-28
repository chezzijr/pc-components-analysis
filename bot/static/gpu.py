from dataclasses import dataclass
from datetime import date
from dateparser import parse
import pandas


@dataclass
class Gpu():
    product_name: str
    gpu_chip: str
    release : date 
    bus : str
    memory_size : int # in MB
    memory_type : str
    memory_width : int # in bits
    clock_speed : int # in MHz
    memory_clock : int # in MHz

    def getAttributeFromDfRow(self, row : pandas.core.series.Series):
        """Get attributes from a row of a dataframe
            Sample : 
            "Product Name": "3D Rage",
            "GPU Chip": "Mach64 GT",
            "Released": "Apr 1st, 1996",
            "Bus": "PCI",
            "Memory": "2 MB, EDO, 64 bit",
            "GPU clock": "44 MHz",
            "Memory clock": "66 MHz",
        """
        self.product_name = row['product_name']
        self.gpu_chip = row['gpu_chip']
        self.release = date(parse(row['release']))
        self.bus = row['bus']
        memory = row['memory'].split(", ")
        if "GB" in memory[0]:
            self.memory_size = int(memory[0].split(" ")[0]) * 1024
        self.memory_type = memory[1]
        self.memory_width = int(memory[2].split(" ")[0])
        self.clock_speed = int(row['clock_speed'].split(" ")[0])
        self.memory_clock = int(row['memory_clock'].split(" ")[0])

    def exportToDict(self) -> dict  :
        return {
            "product_name": self.product_name,
            "gpu_chip": self.gpu_chip,
            "release": self.release.strftime("%m/%d/%Y"),
            "bus": self.bus,
            "memory_size": self.memory_size,
            "memory_type": self.memory_type,
            "memory_width": self.memory_width,
            "clock_speed": self.clock_speed,
            "memory_clock": self.memory_clock
        }
