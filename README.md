# GoogleImageDownload
Python script for downloading Google image search results.

## Introduction
Simple script to bulk download images from Google Images, it is written in Python 3 and requires requests library and BeautifulSoup.

To install [requests](http://docs.python-requests.org/en/master/user/install/#install) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) go to the links for instructions.

## Usage
To run the script in terminal, from the working directory.
For example:
```commandline
python image_download.py --search-for "mountain view california"
```
You can also customize the number of images to download from the result page by specifying the argument `number`, and change the default destination to store your downloaded images by modifying the argument `destination`.
