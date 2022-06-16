import requests
import shutil
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpim


def main(url: str):
    web_site_html = getData(url)
    soup = BeautifulSoup(web_site_html, "html.parser")
    i = 0
    for item in soup.find_all("img"):
        img_ext = item["src"]
        print(img_ext)
        # full_url = url + img_ext
        # r = requests.get(full_url, stream=True)
        # if r.status_code == 200:
        #     with open(f"images/{i}.jpg", "wb") as f:
        #         r.raw.decode_content = True
        #         shutil.copyfileobj(r.raw, f)
        #     img = mpim.imread(f"images/{i}.jpg")
        #     imgplot = plt.imshow(img)
        #     plt.show()
        print(item["src"])


def getData(url: str):
    r = requests.get(url)
    return r.text


if __name__ == "__main__":
    print(
        "Which website would you like to see some pieces of clothing that fits your style?"
    )
    url = input("Enter the url : ")
    main(url)
