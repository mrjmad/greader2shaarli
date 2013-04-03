# -*- coding: utf-8 -*-


import requests
import json


from HTMLParser import HTMLParser


IMPORT_TAG = ""
LOGIN_SHAARLI = ""
PASSWORD_SHAARLI = ""
URL_SHAARLI = ""
GREADER_STARRED_FILE = ""


try:
    from local_settings import *
except ImportError:
    pass


class ShaarliHTMLParser(HTMLParser):

    def __find_attr_value_in_list(self, attr_name, attrs):
        for key, value in attrs:
            if key == attr_name:
                return value
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'input':

            name = self.__find_attr_value_in_list('name', attrs)
            value = self.__find_attr_value_in_list('value', attrs)

            if name:
                self.__dict__[name] = value


def main():
    with requests.session() as c:
        login_page = c.get(URL_SHAARLI, params={'do': 'login'})
        page_str = login_page.text
        sparser = ShaarliHTMLParser()
        sparser.feed(page_str)
        login_params = {'login': LOGIN_SHAARLI, 'password': PASSWORD_SHAARLI, 'token': sparser.token}

        post_login = c.post(URL_SHAARLI, data=login_params)

        json_file = open(GREADER_STARRED_FILE)
        data = json.load(json_file)

        links = data['items']

        for link in links:
            title = link['title']
            url = link['alternate'][0]['href']
            get_add_link = c.get(URL_SHAARLI, params={'post': url})
            sparser.feed(get_add_link.text)
            add_params = {'lf_url': url, 'lf_title': title, 'lf_tags': IMPORT_TAG,
                          'save_edit': sparser.save_edit, 'lf_linkdate': sparser.lf_linkdate, 'token': sparser.token}
            post_add = c.post(URL_SHAARLI, data=add_params)

if __name__ == "__main__":
    main()
