import asyncio
import pandas as pd
import numpy as np
import logging
import pickle
from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from parts import CPU, VGA, RAM, Mainboard, Price, SSD, HDD
from engine import engine
from scraper import query_all_shops
from os.path import exists, join
from os import listdir

logger = logging.getLogger(__name__)

csv_to_constructor_map = {
    "cpu.csv": CPU,
    "vga.csv": VGA,
    "mainboard.csv": Mainboard,
    "ram.csv": RAM,
    "ssd.csv": SSD,
    "hdd.csv": HDD
}

def chunking[T](seq: Sequence[T], size: int):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_components():
    with Session(engine) as session:
        for csv, constructor in csv_to_constructor_map.items():
            data = pd.read_csv(f"./datasets/refined/{csv}")
            data = data.replace({np.nan: None})
            for _, row in data.iterrows():
                component = constructor(**row.to_dict())
                session.add(component)
        session.commit()

async def insert_prices():
    obj_dir = "./obj"
    if not exists(obj_dir):
        with Session(engine) as session:
            tables = [CPU, VGA, RAM, Mainboard, SSD, HDD]
            prices = []
            for table in tables:
                logger.info(f"Querying {table.__tablename__}...")
                rows = session.execute(select(table)).scalars().all()
                logger.info(f"Queried {len(rows)} rows")

                chunk_size = 10
                # sleep to avoid getting rate limited
                sleep_time = 5.0
                for chunk_num, chunk in enumerate(chunking(rows, chunk_size)):
                    logger.info(f"Processing chunk {chunk_num + 1}/{len(rows)//chunk_size + 1}")
                    # query all shops already handle exception
                    results = await asyncio.gather(*[query_all_shops(row.to_query()) for row in chunk])   

                    for i, result in enumerate(results):
                        prices.extend(product.to_price(chunk[i].id) for product in result)

                    logger.info(f"Sleeping for {sleep_time} seconds...")
                    await asyncio.sleep(sleep_time)

                with open("./obj/{}_prices.pkl".format(table.__name__.lower()), "wb") as f:
                    pickle.dump(prices, f)
                logger.info(f"Inserting {len(prices)} prices...")
                session.add_all(prices)
                session.commit()
    else:
        files = listdir(obj_dir)
        file_paths = [join(obj_dir, file) for file in files]
        prices = []
        for file_path in file_paths:
            with open(file_path, "rb") as f:
                prices.extend(pickle.load(f))
        with Session(engine) as session:
            logger.info(f"Inserting {len(prices)} prices...")
            session.add_all(prices)
            session.commit()
