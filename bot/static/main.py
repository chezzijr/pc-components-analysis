import asyncio
import aiohttp
import pandas as pd
import json
from gpu import Gpu
from cpu import Cpu


GPU_URL = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/gpu_specs.json"
CPU_URL = "https://raw.githubusercontent.com/jnswkz/gpu-cpu-crawl/main/cpu_specs.json"


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
