#WebScrappingReptiles

import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {"User-Agent": "Mozilla/5.0"}


PAGES = {
    "Toads": "https://www.backwaterreptiles.com/toads-for-sale.html",
    "Salamanders": "https://www.backwaterreptiles.com/salamanders-for-sale.html",
    "Newts": "https://www.backwaterreptiles.com/newts-for-sale.html",
    "Lizards": "https://www.backwaterreptiles.com/lizards/lizards-for-sale.html",
    "Snakes": "https://www.backwaterreptiles.com/snakes/snakes-for-sale.html",
    "Turtles": "https://www.backwaterreptiles.com/turtles-for-sale.html",
    "Tortoises": "https://www.backwaterreptiles.com/tortoises-for-sale.html",
    # etc: adicione quantas abas desejar
}

def scrape_category(category_name, url):
    print(f"🔍 Coletando {category_name}...")
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Aqui você precisa inspecionar a página para decidir a “query selector” correta.
    # No caso das páginas que já fizemos (toads, frogs, newts), usamos:
    blocks = soup.select("div.stacks_div.stacks_middle")

    items = []
    for block in blocks:
        name_tag = block.find("a")
        # preço geralmente é o último <span>
        price_tag = block.find_all("span")[-1]

        name = name_tag.text.strip() if name_tag else "N/A"
        link = ("https://www.backwaterreptiles.com/" + name_tag['href']) if (name_tag and name_tag.has_attr('href')) else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"

        print(f"  • {name} — {price}")

        items.append({
            "category": category_name,
            "name": name,
            "price": price,
            "link": link
        })

    return items

def main():
    all_items = []
    for cat, url in PAGES.items():
        try:
            cat_items = scrape_category(cat, url)
            all_items.extend(cat_items)
        except Exception as e:
            print(f"⚠️ Erro ao coletar {cat}: {e}")

    # Salvar tudo em CSV
    with open("all_animals.csv", "w", newline="", encoding="utf-8") as f:
        campos = ["category", "name", "price", "link"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(all_items)

    print(f"\n✅ Total de itens coletados: {len(all_items)}")
    print("Arquivo gerado: all_animals.csv")

if __name__ == "__main__":
    main()










