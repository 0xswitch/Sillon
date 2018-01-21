#!/usr/bin/python
#encoding:utf-8

import argparse

from core.Scrapper import Scrapp
from core.Fuzzer import  Fuzz
from core.const import KEY
from core.Loader import Load

from utils.display import banner, nice_display, display_parameters, display_header
from utils.request import requester

# todo remonter repertoire
# todo href in action formulaire
# todo [] in parameters
# todo dump output
# todo multithread .....
# todo ajouter / supprimer ext
# todo random payload
# todo differencier sql / php errors
# todo redirect 301
# todo port in url :8080

class Sillon():
    """
    https://github.com/0xswitch/Sillon
    https://0xswitch.fr

    2018
    """

    def __init__(self, args):

        if args.p:
            display_parameters(args)

        req = requester(args)
        payload = Load(__file__, args)()
        resultat = Scrapp(args, req)()

        if args.hide:
            nice_display(*resultat)

        if not args.nofuzz:
            display_header("Fuzzer output")
            [Fuzz(url, req, payload, args)() for url in resultat[0]]



if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help="site to be scanned")
    parser.add_argument("--default_page", help="by default : index.php")
    parser.add_argument("--fields", "--f","-f", help=",".join(KEY))
    parser.add_argument("--alias", "--a","-a", help="Allow alias")
    parser.add_argument("--verbose", "--v", "-v", action="store_true", help="blablalbla")
    parser.add_argument("--nofuzz", "--nf", "-nf", action="store_true", help="Don't fuzz")
    parser.add_argument("--stop", action="store_true", help="Ask if the script must continue even if an attack vector is found")
    parser.add_argument("--debug", "--d", "-d", action="store_true", help="Display errors")
    parser.add_argument("-p", action="store_true", help="Display parameters")
    parser.add_argument("--hide", "--h", action="store_false", help="Display output")
    parser.add_argument("--remove", help=",".join(KEY))
    parser.add_argument("--excluded", help="List of word excluded from url comma separated")
    parser.add_argument("--sqli_file", help="List of url where to fetch SQL payload")
    parser.add_argument("--name", help="Name for the file to be saved")
    parser.add_argument("--timeout", type=float, help="Set request timeout")
    parser.add_argument("--max_retries", type=int, help="Set max retries")
    parser.add_argument("--recursive", "-r", "--r", type=int, help="max recursivity allowed")
    args = parser.parse_args()

    Sillon(args)
