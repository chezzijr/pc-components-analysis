import asyncio
import logging
from chat import chat
from populate import insert_components, insert_prices
from settings import settings

# stdout as the default logging handler
logfile = "log.txt"
logging.basicConfig(
    filename=logfile,
    filemode="a",
    format="%(asctime)s - %(name)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

if not settings.ignore_insert_components:
    insert_components()
if not settings.ignore_insert_prices:
    asyncio.run(insert_prices())
chat()
