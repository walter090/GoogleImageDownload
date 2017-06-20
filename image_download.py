from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json


def search_and_download(search_term, number=15, save_to=None):
    """Search for and download images from Google Images

    Args:
        search_term(str): image search term
        number(int): number of images to download

    Returns:
        bool, successful download
    """
    url = 'https://www.google.com/search?tbm=isch&q='
    joined_search_term = '+'.join(search_term.split(' '))
    req = Request(url + joined_search_term,
                  headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686)'
                                         ' AppleWebKit/537.17 (KHTML, like Gecko)'
                                         ' Chrome/24.0.1312.27 Safari/537.17'})
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
