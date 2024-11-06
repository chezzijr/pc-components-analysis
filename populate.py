from collections import namedtuple
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from parts import CPU, VGA, RAM, Component
from engine import engine
import pandas as pd
import numpy as np

Tables = namedtuple("Tables", ["constructor", "ignore_columns"])

csv_to_constructor_map = {
    "cpu.csv": Tables(CPU, ["price"]),
    "video-card.csv": Tables(VGA, ["price"]),
}

def populate(engine: Engine):
    parts = (
        pd.read_csv(f"./datasets/csv/cpu.csv")
        .drop("price", axis=1)
        .replace(np.nan, None)
    )

print(populate(engine))
