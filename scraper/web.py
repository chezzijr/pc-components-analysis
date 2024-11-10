import asyncio
import re
import aiohttp
import logging
from urllib.parse import quote
from bs4 import BeautifulSoup
from dataclasses import dataclass
from parts import Price

logger = logging.getLogger(__name__)

@dataclass
class Product:
    name: str
    price: int
    currency: str
    source: str

    def to_price(self, cid: int) -> Price:
        return Price(
            component_id=cid,
            price=self.price,
            source=self.source,
        )


def clean_name(name: str):
    return re.sub(r"<.*?>", "", name)

def match_by_tokens(product_name: str, query: str):
    tokens = query.split()
    prod_tokens = product_name.split()
    for token in tokens:
        if token not in prod_tokens:
            return False
    return True

def match_by_lcs(product_name: str, query: str):
    n, m = len(query), len(product_name)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if query[i - 1] == product_name[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m] >= n
    

def match_name(product_name: str, query: str):
    """
    Check if the query matches the product name
    There some edge case such as WIFI but the product name is Wi-Fi
    Remove those hyphen will lead to incorrect name like the model name
    So use Longest Common Subsequence to check if the query is a substring of the product name
    """
    substring = query.lower()
    punctuation = "()"
    for p in punctuation:
        product_name = product_name.replace(p, "")
    target = product_name.lower()
    return match_by_tokens(target, substring) or match_by_lcs(target, substring)


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
    results = await asyncio.gather(*(crawl(query) for crawl in crawlers), return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, BaseException):
            logger.error(f"Error in crawling {crawlers[i].__name__} with query {query}: {result}")
    products = [product for sublist in results if isinstance(sublist, list) for product in sublist]
    products = [product for product in products if match_name(product.name, query)]
    logger.info(f"Found {len(products)} products for query {query}")
    return products
