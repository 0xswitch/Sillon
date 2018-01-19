import requests
from requests.exceptions import *

from utils.display import p_e
from utils.colors import ENDC


class requester():

    def __init__(self, args):
        self.timeout = 2.0
        self.max_retries = 5
        self.debug = False
        self.parse_args(args)
        ###
        self.sess = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self.sess.mount("http://", adapter)

    def parse_args(self, args):
        if args.timeout is not None:
            self.timeout = args.timeout
        if args.max_retries is not None:
            self.max_retries = args.max_retries
        if args.debug:
            self.debug = True

    def get(self,*args, **kwargs):
        """
        Override requets.get method
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return self.sess.get(*args, timeout=self.timeout, **kwargs)

        except ConnectTimeout as e:
           return self.trace(e, "Could not join %s timeout reached" % args[0], None)

        except ConnectionError as e:
            return self.trace(e, "Error while receiving data for : %s%s " % (ENDC, args[0]), None)


    def trace(self, e, msg, ret):
        p_e(msg)
        if self.debug:
            print e
        return None