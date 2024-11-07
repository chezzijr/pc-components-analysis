from sqlalchemy import Engine
from sqlalchemy.orm import Session
from parts import CPU, VGA, RAM, Mainboard
from engine import engine
import pandas as pd
import numpy as np

csv_to_constructor_map = {
    "cpu.csv": CPU,
    "video-card.csv": VGA,
    "motherboard.csv": Mainboard,
    "memory.csv": RAM,
}

def populate(engine: Engine):
    with Session(engine) as session:
        for csv, constructor in csv_to_constructor_map.items():
            data = pd.read_csv(f"./datasets/refined/{csv}")
            data = data.replace({np.nan: None})
            for _, row in data.iterrows():
                component = constructor(**row.to_dict())
                session.add(component)
        session.commit()
    print("Data has been populated")

print(populate(engine))
