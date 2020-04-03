import requests
import shodan

SHODAN_API_KEY = 'SHODAN_KEY_HERE'

class CalibreDump:
    def __init__(self, shodan_key):
        self.api = shodan.Shodan(shodan_key)
        self.hosts = set()
        self.dorks = ['/interface-data/init', '/browse/categories/allbooks']

    @staticmethod
    def check_open(self, ip_port):
        for dork in self.dorks:
            request = requests.get(f'http://{ip_port}{dork}')
            if request.status_code == 200:
                return True
        return False

    def find_calibre_hosts(self):
        try:
            results = self.api.search('calibre')

            for result in results['matches']:
                self.hosts.add(f"{result['ip_str']}:{result['port']}")

        except shodan.APIError as e:
            print(f'Error {e}')


if __name__ == '__main__':
    api = shodan.Shodan(SHODAN_API_KEY)
    hosts = []

