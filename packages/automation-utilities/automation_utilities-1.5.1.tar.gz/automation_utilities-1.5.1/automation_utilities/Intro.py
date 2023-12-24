from uuid import getnode
from art import text2art
from colorama import Fore


def intro(name: str):
    print(f'{Fore.LIGHTYELLOW_EX}{text2art("Hazem3010", "alligator")}')
    indent = '\t'*15
    print(f'{Fore.GREEN}{indent}{name}\t{Fore.LIGHTMAGENTA_EX}::\t{Fore.CYAN}Your ID: {getnode()}')


intro("Test")
