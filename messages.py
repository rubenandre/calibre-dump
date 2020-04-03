from colorama import Style, Fore


def print_error(message):
    print(f'{Fore.RED}[Error *] - {message}{Style.RESET_ALL}')


def print_success(message):
    print(f'{Fore.GREEN}[Sucess *] - {message}{Style.RESET_ALL}')


def print_warning(message):
    print(f'{Fore.YELLOW}[Warning *] - {message}{Style.RESET_ALL}')


def print_step(message):
    print(f'{Fore.BLUE}[*] - {message}{Style.RESET_ALL}')

def print_finish(message):
    print(f'{Fore.GREEN}[Finish *] - {message}{Style.RESET_ALL}')