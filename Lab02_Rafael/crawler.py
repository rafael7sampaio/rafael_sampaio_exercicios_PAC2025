import json
import os
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


USER_AGENT = "RafaelCrawler/1.0 (PAC2025; educational use only)"
REQUEST_DELAY = 1
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def get_robots_parser(base_url: str) -> RobotFileParser:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        pass
    return rp


def is_allowed(rp: RobotFileParser, url: str) -> bool:
    try:
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def fetch_page(url: str, session: requests.Session) -> BeautifulSoup | None:
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as error:
        print(f"  [ERRO] Não foi possível aceder a {url}: {error}")
        return None


def extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.scheme in ("http", "https"):
            links.append(full_url)
    return links


def extract_headings(soup: BeautifulSoup) -> list[str]:
    headings = []
    for tag in soup.find_all(["h1", "h2"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append(text)
    return headings


def extract_paragraphs(soup: BeautifulSoup) -> list[str]:
    paragraphs = []
    for tag in soup.find_all("p"):
        text = tag.get_text(strip=True)
        if text:
            paragraphs.append(text)
    return paragraphs


def same_domain(url: str, base_domain: str) -> bool:
    return urlparse(url).netloc == base_domain


def crawler(url_inicial: str, max_paginas: int, apenas_mesmo_dominio: bool = True) -> list[dict]:
    base_domain = urlparse(url_inicial).netloc
    rp = get_robots_parser(url_inicial)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    visited: set[str] = set()
    queue: list[str] = [url_inicial]
    results: list[dict] = []
    navigation_graph: dict[str, list[str]] = {}

    print(f"A iniciar o crawler em: {url_inicial}")
    print(f"Máximo de páginas: {max_paginas}")
    print(f"Filtro de domínio: {'Sim (' + base_domain + ')' if apenas_mesmo_dominio else 'Não'}\n")

    while queue and len(visited) < max_paginas:
        url = queue.pop(0)

        if url in visited:
            continue

        if not is_allowed(rp, url):
            print(f"  [BLOQUEADO pelo robots.txt] {url}")
            visited.add(url)
            continue

        print(f"[{len(visited) + 1}/{max_paginas}] A visitar: {url}")

        soup = fetch_page(url, session)
        if soup is None:
            visited.add(url)
            continue

        titulo = soup.title.get_text(strip=True) if soup.title else ""
        links = extract_links(soup, url)
        headings = extract_headings(soup)
        paragraphs = extract_paragraphs(soup)

        if apenas_mesmo_dominio:
            links = [l for l in links if same_domain(l, base_domain)]

        page_data = {
            "url": url,
            "titulo": titulo,
            "links": links,
            "headings": headings,
            "paragraphs": paragraphs,
        }

        results.append(page_data)
        navigation_graph[url] = links
        visited.add(url)

        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)

        time.sleep(REQUEST_DELAY)

    output_path = os.path.join(RESULTS_DIR, "resultados.json")
    graph_path = os.path.join(RESULTS_DIR, "grafo_navegacao.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(navigation_graph, f, ensure_ascii=False, indent=2)

    print(f"\nCrawling concluído. {len(results)} páginas visitadas.")
    print(f"Resultados guardados em: {output_path}")
    print(f"Grafo de navegação guardado em: {graph_path}")

    return results


if __name__ == "__main__":
    url_inicial = "https://example.com"
    max_paginas = 5

    dados = crawler(url_inicial, max_paginas, apenas_mesmo_dominio=False)

    print("\n--- Resumo ---")
    for pagina in dados:
        print(f"\nURL: {pagina['url']}")
        print(f"  Título: {pagina['titulo']}")
        print(f"  Links encontrados: {len(pagina['links'])}")
        print(f"  Cabeçalhos: {pagina['headings']}")
