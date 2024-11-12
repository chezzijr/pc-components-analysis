import asyncio
import argparse as ap
import logging
from chat import chat
from populate import insert_data, insert_prices

# stdout as the default logging handler
logfile = "log.txt"
logging.basicConfig(
    filename=logfile,
    filemode="a",
    format="%(asctime)s - %(name)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

parser = ap.ArgumentParser()
parser.add_argument(
    "task",
    help="The task to be performed",
    choices=["insert_data", "query_prices", "chat"],
)
args = parser.parse_args()

match args.task:
    case "insert_data":
        insert_data()
        print("Data inserted")
    case "query_prices":
        asyncio.run(insert_prices())
        print("Prices inserted")
    case "chat":
        chat()
    case _:
        print("Invalid task")
