#!/usr/bin/python
#encoding:utf-8

import argparse

from core.Scrapper import Scrapp
from core.Fuzzer import  Fuzz
from core.const import KEY
from core.Loader import Load

from utils.display import banner, nice_display, display_parameters, display_header, fuzzer_mep
from utils.request import requester

# todo https or not
# todo remonter repertoire
# todo href in action formulaire
# todo [] in parameters
# todo dump output
# todo multithread .....
# todo ajouter / supprimer ext
# todo online payload
# todo random payload
# todo differencier sql / php errors
# todo ask utilisateurs si prompt quand injec detectée
# todo juste afficher comparatif sans score
# todo redirect 301

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
        payload = Load(__file__)()

        resultat = Scrapp(args, req)()

        if args.hide:
            nice_display(*resultat)

        if args.stop:
            display_header("Fuzzer output")



if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help="site to be scanned")
    parser.add_argument("--default_page", help="by default : index.php")
    parser.add_argument("--fields", "--f","-f", help=",".join(KEY))
    parser.add_argument("--alias", "--a","-a", help="Allow alias")
    parser.add_argument("--verbose", "--v", "-v", action="store_true", help="blablalbla")
    parser.add_argument("--stop", action="store_true", help="Ask if the script must continue even if an attack vector is found")
    parser.add_argument("--debug", "--d", "-d", action="store_true", help="Display errors")
    parser.add_argument("-p", action="store_true", help="Display parameters")
    parser.add_argument("--hide", "--h", action="store_false", help="Display output")
    parser.add_argument("--remove", help=",".join(KEY))
    parser.add_argument("--excluded", help="List of word excluded from url comma separated")
    parser.add_argument("--timeout", type=float, help="Set request timeout")
    parser.add_argument("--max_retries", type=int, help="Set max retries")
    parser.add_argument("--recursive", "-r", "--r", type=int, help="max recursivity allowed")
    args = parser.parse_args()

    Sillon(args)
