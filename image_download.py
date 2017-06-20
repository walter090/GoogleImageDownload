from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686)'
                         ' AppleWebKit/537.17 (KHTML, like Gecko)'
                         ' Chrome/24.0.1312.27 Safari/537.17'}


def search(search_term, number=1, size=None):
    """Search for images from Google Images

    Args:
        search_term(str): Image search term
        number(int): Number of images to download
        size(str): Size of images to download, available options are
                   large, medium, icon

    Returns:
        bool, successful download
    """
    size_desig = {'large': 'l', 'medium': 'm', 'icon': 'i'}

    param = 'tbm=isch&q='
    root = 'https://www.google.com/search?'

    joined_search_term = '+'.join(search_term.split(' '))
    url = root + param + joined_search_term

    if size is not None:
        url = root + '&tbs=isz:' + size_desig[size] + '&tbm=isch&q=' + joined_search_term

    req = Request(url, headers=headers)
    source = urlopen(req).read()
    soup = BeautifulSoup(source, 'html5lib')
    body = soup.body
    results = body.find_all('div', class_='rg_meta notranslate')

    links = []

    for result in results:
        content = result.get_text()
        content_dict = json.loads(content)
        links.append(content_dict['ou'])
        if len(links) == number:
            break

    return links


def download(links, destination='images'):
    """Download images given links

    Args:
        links(list): list of links
        destination(str): destination to store the downloaded images

    Returns:
        None
    """
    if not os.path.isdir(destination):
        os.mkdir(destination)

    for img_link in links:
        req = requests.get(img_link, stream=True, headers=headers)
        with open(os.path.join(destination, img_link.split('/')[-1]), 'wb') as f:
            f.write(req.content)
