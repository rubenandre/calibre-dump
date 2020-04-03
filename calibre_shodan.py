import shodan


class CalibreShodan:
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
