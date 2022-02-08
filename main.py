from bs4 import BeautifulSoup
import json
import requests


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36"
}


for i in range(1,11):
    url = f"https://quotes.toscrape.com/page/{i}/"
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    quotes = soup.find_all(class_="quote")

    quotes_list = []
    tags_dict = {}

    for item in quotes:
        text = item.find(class_="text").text
        author = item.find(class_="author").text
        author_link = "https://quotes.toscrape.com" + item.find("a").get("href")
        # tags = item.find(class_="keywords").get("content")
        tags = item.find_all(class_="tags")

        for t in tags:
            tag = t.find_all(class_="tag")
            for j in tag:
                tagtext = j.text
                taglink = "https://quotes.toscrape.com" + j.get("href")
                tags_dict[tagtext] = taglink

        quotes_list.append(
            {
                "Text": text,
                "Author": author,
                "About author": author_link,
                "Tags": tags_dict
            }
        )

    with open(f"list_{i}.json", "a", encoding="utf-8") as file:
        json.dump(quotes_list, file, indent=4, ensure_ascii=False)
