from collections import defaultdict, namedtuple
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
from engine import engine
from parts import CPU, Base, Component, Price
from parts.vga import VGA

@dataclass
class ComponentPrices:
    component: Component
    prices: list[Price]

def get_all_prices(cls):
    if cls not in Component.registry._class_registry.values():
        raise ValueError(f"{cls} is not a valid model")

    with Session(engine) as session:
        components = session.scalars(select(cls)).all()
        prices = session.scalars(
            select(Price).join(cls).where(cls.id == Price.component_id)
        ).all()
    components_prices: list[ComponentPrices] = []
    d = defaultdict(list)

    for price in prices:
        d[price.component_id].append(price)

    for component in components:
        components_prices.append(ComponentPrices(component, d[component.id]))

    return components_prices
