import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import json

gpu_url = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/gpu_specs.json"
cpu_url = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/cpu_specs.json"

class gpu:
    def __init__(self):
        self.ProductName = ""
        self.GPUChip = ""
        self.Released = ""
        self.Bus = ""
        self.Memory = ""
        self.MemorySize = ""
        self.MemoryType = ""
        self.MemoryBandwidth = ""
        self.GPUClock = "" # Mhz
        self.MemoryClock = "" # Mhz
    def get_from_row(self, row):
        self.ProductName = row['Product Name']
        self.GPUChip = row['GPU Chip']
        self.Released = row['Released']
        self.Bus = row['Bus']
        self.Memory = row['Memory']
        if self.Memory == "System Shared":
            self.MemorySize = "N/A"
            self.MemoryType = "N/A"
            self.MemoryBandwidth = "N/A"
        else:
            self.MemorySize = row['Memory'].split(', ')[0] 
            if "GB" in self.MemorySize:
                current_size = self.MemorySize.split('GB')[0]
                current_size = str(float(current_size) * 1024) + "MB"
                self.MemorySize = current_size
            self.MemoryType = row['Memory'].split(', ')[1]
            self.MemoryBandwidth = row['Memory'].split(', ')[2]
        self.GPUClock = row['GPU clock']
        self.MemoryClock = row['Memory clock']
        return self
        
class cpu:
    def __init__(self) :
        self.Name = ""
        self.Cores = ""
        self.Threads = ""
        self.Socket = ""
        self.Clock = "" # Ghz
        self.ClockMaxSpeed = "" # Ghz
        self.Process = ""
        # self.Cache = ""
        # self.CacheType = ""
        self.TDP = ""
        self.release = ""
    def get_from_row(self, row):
        self.Name = row['Name']
        self.Cores = row['Cores'] if "/" not in row['Cores'] else row['Cores'].split("/")[0]
        self.Socket = row['Socket']
        self.Clock = row['Clock'].split(" ")[0] if "to" not in row['Clock'] else row['Clock'].split(" ")[0]
        self.ClockMaxSpeed = row['Clock'].split(" ")[0] if "to" not in row['Clock'] else row['Clock'].split(" ")[2]
        self.Process = row['Process']
        self.TDP = row['TDP']
        self.release = row['Released']
        return self
    


async def get_gpu_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(gpu_url) as response:
            gpu_data = await response.text()
            return pd.DataFrame(json.loads(gpu_data))
        

async def get_cpu_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(cpu_url) as response:
            cpu_data = await response.text()
            return pd.DataFrame(json.loads(cpu_data))
        
async def main():
    gpu_df = await get_gpu_data()
    cpu_df = await get_cpu_data()
    
    gpu_list = []
    cpu_list = []
    
    for index, row in gpu_df.iterrows():
        gpu_list.append(gpu().get_from_row(row))
    for index, row in cpu_df.iterrows():
        cpu_list.append(cpu().get_from_row(row))


if __name__ == "__main__":
    asyncio.run(main())
