#encoding: utf-8
import argparse
from core.Scrapper import *
from core.const import KEY

# todo https or not
# todo remonter repertoire
# todo href in action formulaire
# todo [] in parameters
# todo dump output
# todo multithread .....

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="site to be scanned")
    parser.add_argument("--default_page", help="by default : index.php")
    parser.add_argument("--fields", "--f","-f", help=",".join(KEY))
    parser.add_argument("--verbose", "--v", "--v", action="store_true", help="blablalbla")
    parser.add_argument("--remove", help=",".join(KEY))
    parser.add_argument("--excluded", help="List of word excluded from url comma separated")
    parser.add_argument("--recursive", "-r", "--r", type=int, help="max recursivity allowed")
    args = parser.parse_args()

    display.banner()
    display.nice_display(*Scrapper(args)())