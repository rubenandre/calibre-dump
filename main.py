import argparse
import re

from calibre_shodan import CalibreShodan
from calibre_tools import CalibreTools
from messages import *


def validate_args(parser, args):
    if args.ip_port is None and args.api_key is None:
        print_error('Only one parameter can be set')
        parser.print_help()
        exit(0)
    if args.ip_port is not None and args.api_key is not None:
        print_error('Only one parameter can be set')
        parser.print_help()
        exit(0)
    if args.ip_port is not None and not re.match('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}:\\d+$', args.ip_port):
        print_error('Invalid ip')
        parser.print_help()
        exit(0)


def shodan_implementation(api_key):
    calibre = CalibreShodan(api_key)
    print_step(f'Finding hosts with shodan')
    hosts = calibre.find_calibre_hosts()

    if len(hosts) == 0:
        print_error('Not host found')
        exit(0)

    print_success(f'Found {len(hosts)} hosts')
    print_step(f'Writing to file')
    with open('found-hosts.txt', 'w') as file:
        for host in hosts:
            file.write(f'{host}\n')

    print_finish('Download all books available')


def single_calibre_implementation(ip_port):
    print_step('Checking if this calibre are open')
    if not CalibreTools.check_open(ip_port):
        print_error('Calibre with authentication')
        exit(0)
    print_success('Calibre without authentication')

    print_step('Getting libraries of calibre')
    libraries = CalibreTools.get_libraries(ip_port)
    if len(libraries) == 0:
        print_error('Not found any library')
        exit(0)
    print_success(f'Found {len(libraries)} libraries')

    for library in libraries:
        print_step(f'Downloading Books from library: {library} (can take a while)')
        CalibreTools.download_books(ip_port, library)

    print_finish('Download all books available')
    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Calibre Dumper")
    parser.add_argument('-s', '--use-shodan', type=str, dest='api_key', action='store',
                        help='To use shodan provide your api key')
    parser.add_argument('-c', '--calibre-host', type=str, dest='ip_port', action='store',
                        help='Provide ip and port of calibre server. Format ip:port')
    parser.usage = ''' CALIBRE DUMPER
    1. Tool to extract unprotected calibre servers using shodan using --use-shodan <API-KEY> or -s <API-KEY>
    2. Download all books from all libraries of calibre server using --calibre-host <API-KEY> or -c <IP:PORT>

    python3 main.py -s <API-KEY>
               or
    python3 main.py -c <IP:PORT>
    '''

    args = parser.parse_args()
    validate_args(parser, args)

    if args.ip_port is not None:
        single_calibre_implementation(args.ip_port)

    if args.api_key is not None:
        shodan_implementation(args.api_key)