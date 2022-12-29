import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
    """
    Returns all image URLs on a single `url`
    """
    request = requests.get(url)
    print(request)
    if(request.status_code != 200):
        print("Error: ", request.status_code)
        return
    soup = bs(request.content, 'html.parser')
    # print(soup)
    urls = []
    i = 0
    for img in tqdm(soup.find_all('img'), 'Extracting images'):
        print(img)
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


def get_all_images_selenium(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    for i in range(5):
        driver.execute_script(
            f"window.scrollTo(0,{i}*1000)")
        time.sleep(2)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    images = soup.find_all('img')
    urls = []
    for image in images:
        print(image.get('srcset'))
        if image.get('srcset'):
            image_url = image['srcset']
        else:
            image_url = image['src']
        # if image_url.endswith('.jpg') or image_url.endswith('.png'):
        if not image_url.startswith('http'):
            image_url = 'http:' + image_url
        print('----- getit -----')
        urls.append(image_url)
        print(image_url)

    driver.quit()
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
    # generate a random number to avoid duplicate file names
    random_number = random.randint(1, 100000)
    filename = os.path.join(pathname, url.split("/")[-1]+str(random_number))
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
    imgs = get_all_images_selenium(url)
    if(imgs == None):
        print("Error: Images cannot be downloaded from this website.")
        return
    print(f'Downloading {len(imgs)} images')
    for img in imgs:
        try:
            download(img, path)
        except:
            print("Error: ", img)


if __name__ == "__main__":
    print(
        "Which website would you like to see some pieces of clothing that fits your style?"
    )
    website_name = input("Enter the website name : ")
    url = input("Enter the url : ")
    main(url, '..\images\\' + website_name)
    print("All images have been downloaded! You can now start to classify them, by running the dataset_builder.py file.")
