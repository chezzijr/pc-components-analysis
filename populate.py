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
    tables = [CPU, VGA, RAM, Mainboard, SSD, HDD]
    table_names = [table.__name__.lower() for table in tables]
    if all(exists(join("./obj", f"{table_name}.pkl")) for table_name in table_names):
        logger.info("Loading from cache...")
        for table in tables:
            with open(f"./obj/{table.__name__.lower()}.pkl", "rb") as f:
                rows = pickle.load(f)
            with Session(engine) as session:
                session.add_all(rows)
                session.commit()
    else:
        with Session(engine) as session:
            for csv, constructor in csv_to_constructor_map.items():
                data = pd.read_csv(f"./datasets/refined/{csv}")
                data = data.replace({np.nan: None})
                for _, row in data.iterrows():
                    component = constructor(**row.to_dict())
                    session.add(component)
            session.commit()

async def insert_prices():
    table = Price
    table_name = table.__name__.lower()
    if exists(join("./obj", f"{table_name}.pkl")):
        logger.info("Loading from cache...")
        with open(f"./obj/{table_name}.pkl", "rb") as f:
            rows = pickle.load(f)
        with Session(engine) as session:
            session.add_all(rows)
            session.commit()
    else:
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

def save_cache():
    # save all database into pickle
    tables = [CPU, VGA, RAM, Mainboard, SSD, HDD, Price]
    for table in tables:
        with Session(engine) as session:
            rows = session.execute(select(table)).scalars().all()
            with open(f"./obj/{table.__name__.lower()}.pkl", "wb") as f:
                pickle.dump(rows, f)
