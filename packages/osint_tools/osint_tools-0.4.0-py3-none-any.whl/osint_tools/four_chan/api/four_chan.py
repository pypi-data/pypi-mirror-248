from ..schemas import *
# import json
# import httpx
import requests
# import urllib.parse
import urllib.request
# import asyncio
# import random
from time import sleep
import os.path

def get_catalog(board: Board, as_dict: bool = False) -> list[CatalogThread]:
    url = f'https://a.4cdn.org/{Board[board]}/catalog.json'
    data = requests.get(url).json()

    all_posts: list[CatalogThread] = []
    for page in data:
        for thread in page['threads']:
            '''attach board to thread'''
            assert not isinstance(board, list), 'board should not be list'
            thread['board'] = board
            all_posts.append(CatalogThread(**thread))
    return all_posts

def catalog_image_generator(board: Board):
    # https://github.com/4chan/4chan-API/blob/master/pages/User_images_and_static_content.md
    url = f'https://a.4cdn.org/{Board[board]}/catalog.json'
    r = requests.get(url).json()
    lst = []
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            if 'last_replies' in thread:
                for comment in thread['last_replies']:
                    if 'ext' in comment and 'tim' in comment:
                        url = 'http://i.4cdn.org/{0}/{1}{2}'.format(
                            board, 
                            str(comment['tim']), 
                            str(comment['ext'])
                        )
                        lst.append(url)
    print(lst)
    print(len(lst))
    for i in lst:
        yield i

def iter_img_lst(board, save_dir: str):
    '''
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Modified-Since
    If-Modified-Since: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
    e.g.:  Thu, 15 Dec 2022 03:51:47 GMT
    '''
    path = f'{save_dir}/'
    counter = 0
    for img in catalog_image_generator(board):
        file_name = img.split('/')[-1]
        if not os.path.isfile(path + file_name):# if file does not exist; download image.
            sleep(5)
            try:
                filename, headers = urllib.request.urlretrieve(img, path + file_name)
            except Exception as e:
                print(e)
            else:
                counter += 1
                print(f'{counter}: {filename} {headers}')
        else:
            print(f'file exists: {file_name}')
            continue

# req = urllib.request.Request('http://www.example.com/')
# req.add_header('Referer', 'http://www.python.org/')
# # Customize the default User-Agent header value:
# req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
# r = urllib.request.urlopen(req)
