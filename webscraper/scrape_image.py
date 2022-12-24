import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import time
import xlsxwriter
import random


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


class DataSetBuilder(object):
    def __init__(self, directory):
        self.directory = directory
        self.row = 2
        # genere a random number for the file name
        randomID = random.randint(1, 10000000)
        self.workbook = xlsxwriter.Workbook(
            f"./database/result{randomID}.xlsx")
        self.worksheet = self.workbook.add_worksheet('result1')
        self.COLUMNS = ['A', 'B']
        self.worksheet.write(self.COLUMNS[0]+'1', 'Filename')
        self.worksheet.write(self.COLUMNS[1]+'1', 'Choice')

    def on_key_press(self, event):
        print(event.key)
        if event.key == '1':
            self.worksheet.write(self.COLUMNS[1]+str(self.row), 1)
        elif event.key == '0':
            self.worksheet.write(self.COLUMNS[1]+str(self.row), 0)
        else:
            self.worksheet.write(self.COLUMNS[1]+str(self.row), 0)
        plt.close()
        return event.key

    def lookup_images(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.jpg' or '.png' or '.jpeg'):
                f = os.path.join(self.directory, filename)
                img = mpim.imread(f)
                fig = plt.gcf()
                fig.canvas.set_window_title('1: good , 0: Bad')
                fig.canvas.mpl_connect('key_press_event', self.on_key_press)

                plt.imshow(img)
                plt.show()
                self.worksheet.write(self.COLUMNS[0]+str(self.row), filename)
                self.row += 1
        self.workbook.close()


def main(url, path):
    # imgs = get_all_images(url)
    # for img in imgs:
    #     download(img, path)
    # time.sleep(10)
    dataset = DataSetBuilder(path)
    dataset.lookup_images()


if __name__ == "__main__":
    print(
        "Which website would you like to see some pieces of clothing that fits your style?"
    )
    url = input("Enter the url : ")
    main(url, './images/')
