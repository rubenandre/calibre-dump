import shodan
from messages import *


class CalibreShodan:
    def __init__(self, shodan_key):
        self.api = shodan.Shodan(shodan_key)

    def find_calibre_hosts(self):
        hosts = []
        try:
            results = self.api.search('calibre')

            for result in results['matches']:
                hosts.append(f"{result['ip_str']}:{result['port']}")

        except shodan.APIError as e:
            print_error('Invalid api key')

        return hosts
