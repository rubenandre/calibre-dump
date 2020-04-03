import os
import re

import requests
import wget
from bs4 import BeautifulSoup


class CalibreTools:
    @staticmethod
    def check_open(ip_port):
        dorks = ['/interface-data/init', '/browse/categories/allbooks']
        for dork in dorks:
            request = requests.get(f'http://{ip_port}{dork}')
            if request.status_code == 200:
                return True
        return False

    @staticmethod
    def get_libraries(ip_port):
        libraries = []

        request = requests.get(f'http://{ip_port}/mobile')
        soap = BeautifulSoup(request.text, features='html.parser')

        library_div = soap.find('div', attrs={'id': 'choose_library'})
        try:
            results = library_div.find_all_next('option')

            for result in results:
                library = str(result.text).replace(' ', '_')
                libraries.append(library)
        except AttributeError:
            # will work because calibre accepts any string and redirects to the library that exists
            libraries.append("random")

        return libraries

    @staticmethod
    def get_total_books(ip_port, library_name):
        request = requests.get(f'http://{ip_port}/mobile?library_id={library_name}')
        soap = BeautifulSoup(request.text, features='html.parser')

        span_tags = soap.findAll('span')

        for span in span_tags:
            if re.search('Books \\d+ to \\d+ of \\d+', span.text):
                return str(span.text).split('of')[1].strip()

    @staticmethod
    def download_books(ip_port, library_name, max=None):
        download_links = CalibreTools.get_books_link(ip_port, library_name, 25, max)

        directory_ip = str(ip_port).split(':')[0]
        directory_name = f'{directory_ip}-{library_name}'

        try:
            os.mkdir(f'./{directory_name}')
        except FileExistsError:
            print()

        for link in download_links:
            try:
                wget.download(link, directory_name)
            except:
                continue

    @staticmethod
    def get_books_link(ip_port, library_name, multiple, max=None):
        n_books = int(CalibreTools.get_total_books(ip_port, library_name))

        if max is not None:
            n_books = max

        difference_next_multiple = multiple - (n_books % multiple)
        if difference_next_multiple == multiple:
            difference_next_multiple = 0
        major_number_it = (n_books + difference_next_multiple) // 25

        books_links = []

        for i in range(major_number_it):
            start = multiple * i + 1
            request = requests.get(
                f'http://{ip_port}/mobile?sort=timestamp&library_id={library_name}&num={n_books}&order=descending&start={start}')
            soap = BeautifulSoup(request.text, features='html.parser')

            links_soap = soap.findAll('a', attrs={'href': re.compile('\\.epub|\\.pdf|\\.mobi')})

            for link in links_soap:
                download_link = f'http://{ip_port}{link.get("href")}'
                books_links.append(download_link)

        return books_links