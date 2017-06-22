from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json
import os
import argparse
import sys

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686)'
                         ' AppleWebKit/537.17 (KHTML)'
                         ' Chrome/24.0.1312.27 Safari/537.17'}


def search(search_terms, number=15, size=None):
    """Search for images from Google Images.

    Args:
        search_terms(list): A list of image search terms.
        number(int): Number of images to download.
        size(str): Size of images to download, available options are
                   large, medium, icon.

    Returns:
        dict, a dictionary of links.
    """
    size_desig = {'large': 'l', 'medium': 'm', 'icon': 'i'}

    param = 'tbm=isch&q='
    file_format = '&tbs=ift:jpg'
    root = 'https://www.google.com/search?'

    _links = {}

    for search_term in search_terms:
        _links[search_term] = []

        joined_search_term = '+'.join(search_term.split(' '))
        url = root + param + joined_search_term + file_format

        if size is not None:
            url = root + '&tbs=isz:' + size_desig[size] + '&tbm=isch&q=' + joined_search_term

        req = Request(url, headers=headers)
        # noinspection PyBroadException
        try:
            source = urlopen(req).read()
        except Exception:
            continue

        soup = BeautifulSoup(source, 'html5lib')
        body = soup.body
        results = body.find_all('div', class_='rg_meta notranslate')

        for result in results:
            content = result.get_text()
            content_dict = json.loads(content)
            _links[search_term].append(content_dict['ou'])
            if len(_links[search_term]) == number:
                break
        print('Found {0} links for {1}'.format(len(_links[search_term]), search_term))

    return _links


def download(links, destination='images', categorize=True, to_home=True):
    """Download images given links

    Args:
        links(dict): Dictionary of links.
        destination(str): Destination to store the downloaded images.
        categorize(bool): Set to True to place downloaded contents in
            different folders, categorized by search terms.
        to_home(bool): Set to True to save images to the user's home
            directory instead of locally where the script is run.

    Returns:
        None
    """
    download_count = 0

    if to_home:
        destination = os.path.join(os.path.expanduser('~'), destination)

    if not os.path.isdir(destination):
        os.mkdir(destination)

    for category in links.keys():
        folder = destination
        if categorize:
            folder = os.path.join(destination, '_'.join(category.split(' ')))
            if not os.path.isdir(folder):
                os.mkdir(folder)

        for img_link in links[category]:
            img_name = img_link.split('/')[-1]
            # noinspection PyBroadException
            try:
                req = requests.get(img_link, stream=True, headers=headers)
            except Exception:
                continue
            try:
                with open(os.path.join(folder, img_name), 'wb') as f:
                    f.write(req.content)
            except IOError:
                pass
            download_count += 1
            print('Downloaded image {}'.format(img_name))

    print('Download complete, total images downloaded: {}'.format(download_count))


if __name__ == '__main__':

    if sys.version_info[0] < 3:
        raise Exception('Python 3.x required')

    parser = argparse.ArgumentParser()
    parser.add_argument('--search-for', dest='search', type=str,
                        help='Search term for google image search')
    parser.add_argument('--number', dest='number', type=int, default=15,
                        help='Number of search results to return')
    parser.add_argument('--size', dest='size', type=str, default=None,
                        help='Size of image results')
    parser.add_argument('--destination', dest='destination', type=str, default='images',
                        help='Destination to store the searched results')
    parser.add_argument('--no-categorize', dest='categorize', action='store_false',
                        help='Use this flag to skip sorting results from different search'
                             ' terms into folders and save them under the same directory')
    parser.add_argument('--local', dest='to_home', action='store_false',
                        help='Use this flag if you want your images stored in a folder in '
                             'the same directory this script is run, other wise they will'
                             'be downloaded to your home directory')

    args = parser.parse_args()

    search_list = args.search.split(',')

    links = search(search_terms=search_list, number=args.number, size=args.size)
    download(links, destination=args.destination, categorize=args.categorize, to_home=args.to_home)
