import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://tabdeal.org/help/"


def get_article_links():
    response = requests.get(BASE_URL, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(BASE_URL, href)

        if "/help/" in full_url:
            links.add(full_url)

    return list(links)


def extract_page(url):
    response = requests.get(url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text("\n", strip=True)

    return {
        "url": url,
        "content": text,
    }


urls = get_article_links()
print(f"Found {len(urls)} URLs")
pages = []
for url in urls:
    try:
        pages.append(extract_page(url))
        print("SUCCESSFUL", url)
    except Exception as e:
        print("FAILED", url, e)

with open("data/tabdeal_help.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

print(f"Saved {len(pages)} pages")