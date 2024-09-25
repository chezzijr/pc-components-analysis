import asyncio
import aiohttp
import pandas as pd
import json
from dataclasses import dataclass
from datetime import date
from dateparser import parse

GPU_URL = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/gpu_specs.json"
CPU_URL = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/cpu_specs.json"

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

    def getAttributeFromDfRow(self, row):
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


@dataclass
class Cpu():
    name : str
    code_name : str
    cores : int
    clock : int # in GHz
    max_clock : int # in GHz
    socket : str
    process : int # in nm
    tdp : int
    release : date

    def getAttributeFromDfRow(self, row):
        """Get attributes from a row of a dataframe
            Sample :
                "Name": "Core Ultra 7 265",
                "Codename": "Arrow Lake-S",
                "Cores": "20 ",
                "Clock": "2.4 to 5.3 GHz",
                "Socket": "Socket 1851",
                "Process": "7 nm",
                "L3 Cache": "33 MB",
                "TDP": "65 W",
                "Released": "Oct 2024"
            """
        
        self.name = row['name']
        self.code_name = row['code_name']
        self.cores = int(row['cores'])
        self.clock = float(row['clock'].split(" ")[0])
        self.max_clock = float(row['clock'].split(" ")[2])
        self.socket = row['socket']
        self.process = int(row['process'].split(" ")[0])
        self.tdp = int(row['tdp'].split(" ")[0])
        self.release = date(parse(row['release']))

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def main():
    tasks = [fetch(GPU_URL), fetch(CPU_URL)]
    gpu_data, cpu_data = await asyncio.gather(*tasks)
    gpu_df = pd.DataFrame(json.loads(gpu_data))
    cpu_df = pd.DataFrame(json.loads(cpu_data))

    gpu_list = []
    cpu_list = []

    for index, row in gpu_df.iterrows():
        gpu = Gpu()
        gpu.getAttributeFromDfRow(row)
        gpu_list.append(gpu)

    for index, row in cpu_df.iterrows():
        cpu = Cpu()
        cpu.getAttributeFromDfRow(row)
        cpu_list.append(cpu)
    

if __name__ == "__main__":
    asyncio.run(main())
