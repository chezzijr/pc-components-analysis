from parts import CPU, VGA, RAM, HDD, SSD, Mainboard
from repo import get_all_prices
from jinja2 import Template

PATH_TEMPLATE = "./templates/{}.txt"
PATH_DOCUMENT = "./documents/{}.txt"

def create_documents():
    models = [CPU, VGA, RAM, HDD, SSD, Mainboard]
    for model in models:
        cprices = get_all_prices(model)
        li = []
        for cprice in cprices:
            c, ps = cprice.component, cprice.prices
            d = c.__dict__
            d["prices"] = [p.__dict__ for p in ps]
            li.append(d)
        with open(PATH_TEMPLATE.format(model.__name__.lower()), "r") as f:
            template = Template(f.read())
        content = template.render({model.__tablename__: li})
        with open(PATH_DOCUMENT.format(model.__name__.lower()), "w") as f:
            f.write(content)

if __name__ == "__main__":
    create_documents()
