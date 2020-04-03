import requests
import shodan

SHODAN_API_KEY = 'SHODAN_KEY_HERE'

class CalibreDump:
    def __init__(self, shodan_key):
        self.api = shodan.Shodan(shodan_key)
        self.hosts = []

    @staticmethod
    def check_open(ip_port):
        dorks = ['/interface-data/init', '/browse/categories/allbooks']
        for dork in dorks:
            request = requests.get(f'http://{ip_port}{dork}')
            if request.status_code == 200:
                return True
        return False

    def find_calibre_hosts(self):
        try:
            results = self.api.search('calibre')

            for result in results['matches']:
                self.hosts.append(f"{result['ip_str']}:{result['port']}")

        except shodan.APIError as e:
            print(f'Error {e}')


if __name__ == '__main__':
    calibre = CalibreDump(SHODAN_API_KEY)

