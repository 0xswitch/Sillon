#!/usr/bin/python
#encoding:utf-8

import argparse

from core.Scrapper import *
from core.const import KEY
from utils.display import banner, nice_display
from utils.request import requester

# todo https or not
# todo remonter repertoire
# todo href in action formulaire
# todo [] in parameters
# todo dump output
# todo multithread .....


class Sillon():
    """
    https://github.com/0xswitch/Sillon
    https://0xswitch.fr

    2018
    """

    def __init__(self, args):
        req = requester(args)
        nice_display(*Scrapper(args, req)())


if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help="site to be scanned")
    parser.add_argument("--default_page", help="by default : index.php")
    parser.add_argument("--fields", "--f","-f", help=",".join(KEY))
    parser.add_argument("--verbose", "--v", "--v", action="store_true", help="blablalbla")
    parser.add_argument("--debug", "--d", "--d", action="store_true", help="Display errors")
    parser.add_argument("--remove", help=",".join(KEY))
    parser.add_argument("--excluded", help="List of word excluded from url comma separated")
    parser.add_argument("--timeout", type=float, help="Set request timeout")
    parser.add_argument("--max_retries", type=int, help="Set max retries")
    parser.add_argument("--recursive", "-r", "--r", type=int, help="max recursivity allowed")
    args = parser.parse_args()

    Sillon(args)
