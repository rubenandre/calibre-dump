import requests
import shodan
from bs4 import BeautifulSoup

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
