import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import time
import xlsxwriter
from pynput.keyboard import Listener


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):

    soup = bs(requests.get(url).content, 'html.parser')
    urls = []
    i = 0
    for img in tqdm(soup.find_all('img'), 'Extracting images'):
        if i == 50:
            break
        img_url = img.attrs.get('src')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
        i += 1
    return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    filename += '.jpg'
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(
        1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main(url, path):
    # imgs = get_all_images(url)
    # for img in imgs:
    #     download(img, path)
    # time.sleep(10)
    lookup_images(path)


def on_release(key):
    if key == '1':
        return key
    elif key == '0':
        return key
    else:
        return 'null'


def lookup_images(directory):
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet('result1')
    row = 2
    COLUMNS = ['A', 'B']
    worksheet.write(COLUMNS[0]+'1', 'Filename')
    worksheet.write(COLUMNS[1]+'2', 'Choice')
    # with Listener(on_release=on_release) as listener:
    #     listener.join()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        img = mpim.imread(f)
        plt.imshow(img)
        plt.show()
        print(filename)
        worksheet.write(COLUMNS[0]+str(row), filename)
        choice = input("1: good , 0: Bad")
        if choice != '1' or choice != '0':
            choice = '0'
        worksheet.write(COLUMNS[1]+str(row), choice)
        plt.close()
        row += 1
    workbook.close()


if __name__ == "__main__":
    print(
        "Which website would you like to see some pieces of clothing that fits your style?"
    )
    url = input("Enter the url : ")
    main(url, './images/')
