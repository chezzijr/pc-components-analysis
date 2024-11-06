import asyncio
import re
import aiohttp
from urllib.parse import quote
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int
    currency: str
    source: str


def clean_name(name: str):
    return re.sub(r"<.*?>", "", name)


def match_name(product_name: str, query: str):
    """
    Check if the query matches the product name
    """
    tokens = query.lower().split()
    punctuation = "()"
    for p in punctuation:
        product_name = product_name.replace(p, "")
    target = product_name.lower().split()
    for token in tokens:
        if token not in target:
            return False
    return True


async def bs4_page_content(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status not in (200, 201):
                return None
            content = await response.text()
    soup = BeautifulSoup(content, "html.parser")
    return soup


async def ttg(query: str) -> list[Product]:
    base_url = "https://ttgshop.vn"
    query_url = "https://ttgshop.vn/search?type=product&q={query}"

    url = query_url.format(query=quote(query))
    soup = await bs4_page_content(url)
    if soup is None:
        return []
    product_containers = soup.find_all("div", class_="proloop-detail")
    products = []
    for container in product_containers:
        name = container.select_one("h3 a.quickview-product").text
        price = container.select_one("span.price").text
        price = int("".join(filter(str.isdigit, price)))
        products.append(
            Product(
                name=name,
                price=price,
                currency="VND",
                source=base_url,
            )
        )
    return products


async def gearvn(query: str) -> list[Product]:
    base_url = "https://gearvn.com"
    products_search_url = "https://gearvn.com/apps/gvn_search/search_products"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            products_search_url,
            json={
                "filters": [],
                "gearvn_store": "",
                "pageIndex": 1,
                "pageSize": 20,
                "search": query,
            },
        ) as response:
            if response.status not in (200, 201):
                return []
            body = await response.json()
            products = body["data"]
            products = [
                Product(
                    name=product["title"],
                    price=product["price"],
                    currency="VND",
                    source=base_url,
                )
                for product in products
            ]
            return products


async def tinhocngoisao(query: str) -> list[Product]:
    base_url = "https://tinhocngoisao.com"
    search_url = "https://tinhocngoisao.com/search?q=filter=(title%3Aproduct**%20{query})%7C%7C(sku%3Aproduct**%20{query})"
    url = search_url.format(query=quote(query))
    soup = await bs4_page_content(url)
    if soup is None:
        return []
    product_containers = soup.find_all("div", class_="product-item")
    products = []
    for container in product_containers:
        name = container.select_one("a.productName").text
        price = container.select_one("p.pdPrice span").text
        price = int("".join(filter(str.isdigit, price)))
        products.append(
            Product(
                name=name,
                price=price,
                currency="VND",
                source=base_url,
            )
        )
    return products


async def memoryzone(query: str) -> list[Product]:
    search_url = "https://memoryzone.aecomapp.com/api/store/query?query={query}&page=1"
    url = search_url.format(query=quote(query))
    async with aiohttp.ClientSession() as session:
        headers = {
            "Ae-Api-Key": "2",
        } 
        async with session.get(url, headers=headers) as response:
            if response.status not in (200, 201):
                return []
            body = await response.json()
            products = body["data"]
            products = [
                Product(
                    name=clean_name(product["name"]),
                    price=product["price"],
                    currency="VND",
                    source="https://memoryzone.com.vn",
                )
                for product in products
            ]
            return products


async def query_all_shops(query: str):
    crawlers = [ttg, gearvn, tinhocngoisao, memoryzone]
    products = await asyncio.gather(*(crawl(query) for crawl in crawlers))
    products = [product for sublist in products for product in sublist]
    products = [product for product in products if match_name(product.name, query)]
    print(products)
    return products


# asyncio.run(query_all_shops("Corsair Vengeance RGB 32GB"))
