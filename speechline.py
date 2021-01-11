from gtts import gTTS
import os 
import sys
import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
#import vlc
import textwrap


class Outline:
    def __init__(self):
        self.__api_base = 'https://api.outline.com/'
        self.__get_article_endoint = 'get_article_cdn?id='
        self.__parse_endpoint = 'parse_article?source_url='
        self.__parse_headers = {'authority': 'api.outline.com',
                                'accept': '*/*',
                                'origin': 'https://outline.com',
                                'sec-fetch-site': 'same-site',
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-dest': 'empty',
                                'referer': 'https://outline.com/',
                                'accept-language': 'en-US,en;q=0.9,pt;q=0.8'
                                }

    def parse_article(self, url: str = None):
        if not url:
            raise ValueError
        response = requests.get(self.__api_base+'v3/'+self.__parse_endpoint + url, headers=self.__parse_headers)
        return response.json()

    def get_article_cdn(self, id: str = None):
        if not id:
            raise ValueError
        response = requests.get(self.__api_base + self.__get_article_endoint + id, headers=self.__parse_headers)
        return response.json()


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError as e:
        sys.exit('Invalid usage.')

    outline = Outline()
    resp = outline.parse_article(url)
    soup = BeautifulSoup(resp.get('data').get('html'), 'html.parser')
    text_speech = gTTS(text=soup.text.replace('\n', ' '), lang='pt', slow=False, tld="com.br")
    file_name = '%s.mp3' % resp.get('data', {}).get('short_code')
    (Thread(target=text_speech.save, args=(file_name,))).start()
    time.sleep(3)

    print("\n".join(textwrap.wrap(soup.text, width=100)))
    os.system("cvlc --rate 2 %s vlc://quit" % file_name)
    # player = vlc.MediaPlayer(file_name)
    # player.play()
