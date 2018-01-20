#encoding: utf-8
import re
import sys

from const import *
from const import KEY
from utils.display import p_e, display_header


class Scrapp(object):
    """
    Main class which handle all found url
    """

    def __init__(self, arguments, requester):
        self.requester = requester
        self.args = arguments
        self.url = None
        self.base_url =  None
        self.found_url = []
        self.waiting_link = []
        self.default_page = None
        self.verbose = False
        self.recursion = -1
        self.remove = None
        self.alias = ""
        self.debug = False


    def __call__(self, *args, **kwargs):
        """
        Return processed data
        :param args:
        :param kwargs:
        :return: (dic:url, str:asked_fields: str:excluded_fields)
        """
        self.parse_arguments(self.args)

        if self.verbose:
            display_header("Verbose")
            self.get_url_parameters(self.url, base_url=self.base_url)
            print
        else:
            self.get_url_parameters(self.url,base_url=self.base_url)

        return (self.found_url, self.args.fields, self.args.excluded)

    def parse_arguments(self, arguments):
        """
        Parse user arguments
        :param arguments:
        :return:
        """
        if not re.match(HOST_REGEX, arguments.url):
            p_e("The provided url does not match the url format")
            sys.exit(-1)
        else:
            if re.search("\."+ALLOW_EXT+"$", arguments.url) is None and re.search("\w+=\w+$", arguments.url) is None:
                self.url = arguments.url + "/" if arguments.url[-1] != "/" else arguments.url
            else:
                self.url = arguments.url

        self.base_url = self.get_base_url()
        if arguments.default_page is None:
            self.default_page = "index.php"
        else:
            self.default_page = arguments.default_page
        if arguments.verbose :
            self.verbose = True
        else:
            self.verbose = False

        if  arguments.recursive is not None:
            self.recursion = arguments.recursive

        if arguments.remove is not None:
            if "," in arguments.remove:
                self.remove = r"" + arguments.remove.replace(",","|")
            else:
                self.remove = r"" + arguments.remove

        if arguments.alias is not None:
            self.alias = arguments.alias

        if arguments.debug:
            self.debug = True

    def create_dictionnary(self, args):
        """
        Create a dictionnary for each page of the website containing each informations gathered
        :param args:
        :return:
        """
        dic = {}
        for key, value in zip(KEY, args):
            dic[key] = value

        return dic

    def get_url_parameters(self, url, base_url=None, referer=None, recursion=0 ):
        """
        Main function gather informations through website
        :param url:
        :param referer:
        :return:
        """
        after_host = url.replace(base_url, "")

        if self.verbose:
            print "Analyzing : %s" % url

        try:
            uri, page_name, parameters = re.findall(URI_REGEX, after_host)[0] # URI / page.php / parameters
        except IndexError:
            uri = ""
            page_name = self.default_page
            parameters = ""

        if page_name == "":
            page_name = self.default_page
            if not parameters:
                url += self.default_page
            else:
                try:
                    before, after = url.split("?")
                    url = before + self.default_page + "?" + after
                except ValueError:
                    before, after = url.split("#")
                    url = before + self.default_page + "#" + after


        parameters = re.findall(PARAMETERS_REGEX, parameters)

        # informations gathered
        try:
            ligne, length, status, page, headers, cookies = self.page_info(url)
        except TypeError:
            pass
        else:
            forms = HTMLforms(page, referer=url)
            php_errors = PHP_errors(page)

            dic = self.create_dictionnary([
                base_url,
                url,
                "/" + after_host,
                "/" + uri,
                page_name.replace("?", ""),
                headers["Server"],
                parameters,
                length,
                ligne,
                status,
                forms,
                php_errors,
                cookies.items()
            ])

            self.found_url.append(dic)

            try: self.waiting_link.remove(url)
            except ValueError: pass
            # Looking for new link in newly found url
            self.grep_link(page, status, url, recursion)

            # test the url without parameters
            if parameters and url.split("?")[0] not in self.waiting_link and url.split("?")[0] not in [item["url"] for item in self.found_url]:
                self.get_url_parameters(url.split("?")[0], base_url=base_url, referer=referer, recursion=recursion)


    def get_base_url(self, force=None):
        """
        Return base url : http(s)://host/
        :return:
        """
        url = force if force is not None else self.url

        try:
            base = re.findall(HOST_REGEX, url)[0][0]
            return base
        except IndexError: # pas de parametres
            return url


    def grep_link(self, page, status_code, referer, recursion):
        """
        Look for new links in page
        :param page:
        :param status_code:
        :param referer:
        :return:
        """

        recursion += 1

        if recursion < self.recursion or self.recursion == -1:
            already_know_link = [item["url"] for item in self.found_url]
            new_link = []

            if status_code == 200:
                for lien in re.findall(AHREF_REGEX, page):
                    lien = lien[1][:-1]

                    if re.match(r"^\.\/?\?(.*)", lien) and lien not in referer:
                        if re.match(r"^\.\/\?(.*)", lien):
                            lien = lien[2:]
                        referer = referer.split("?")[0]
                        lien = referer + lien

                    if ((re.search(r"https?://", lien) and  (re.match(r"" + self.base_url, lien) or (re.match(r"http://(" + self.alias.replace(",", "|") + ")/", lien) and self.alias != "" ) ) ) or (re.match(r"^\.\/?\?(.*)", lien) and lien not in referer )) \
                            and lien not in new_link and lien not in already_know_link  and lien not in self.waiting_link:

                        ok = False
                        if self.remove != None:
                            if not re.search(self.remove, lien):
                                ok = True
                        else:
                            ok = True

                        if ok:
                            new_link.append([lien, referer,recursion])
                            self.waiting_link.append(lien)
                            if self.verbose:
                                print "\tNew link found : %s" % lien
                    elif self.debug:
                        print "Nope %s" % lien

            for lien, referer, recursion in new_link:
                self.get_url_parameters(lien, base_url=self.get_base_url(lien), referer=referer, recursion=recursion)


    def page_info(self, url,):
        """
        Get some page informations
        :param url:
        :return:
        """
        query = self.requester.get(url)
        if query is not None:
            ligne = grep_ligne(query.text)
            char = grep_char(query.text)
            return ligne, char, query.status_code, query.text, query.headers, query.cookies
        else:
            return None


def grep_char(page):
    return len(page)

def grep_ligne(page):
    return page.count("\n")

def HTMLforms(page, referer=None):
    """
    Find each HTML form present in web page
    :param page:
    :param referer:
    :return:
    """
    found_forms = []
    for form in (re.findall(FORM_REGEX, page, re.DOTALL)):
        if re.findall(METHOD_REGEX, form, re.IGNORECASE):

            try:
                id = re.findall(ID_R, form, re.IGNORECASE)[0]
            except IndexError:
                id = ""

            try:
                action = re.findall(ACTION_REGEX, form, re.IGNORECASE)[0]
            except IndexError:
                action = referer
            else:
                if referer.find("?") != -1:  # il y a des parametres dans l'url qui mene au formulaire
                    action = referer + action.replace("?", "&")
                else:
                    action = referer + action

            intput_list = []

            for input in re.findall(INPUT_REGEX, form):
                field_list = []
                for field in re.findall(FIELD_REGEX, input):
                    trash, key, value = field
                    field_list.append((str(key), str(value)))
                intput_list.append(field_list)

            found_forms.append({"id": id, "action": action, "inputs": intput_list})

    return found_forms


def PHP_errors(page):
    """
    Try to find php errors if present
    :param page:
    :return:
    """
    return [(str(warning[0]), str(warning[1]), str(warning[2]).replace("<i>", "")) for warning in re.findall(PHP_ERRORS_R, page, re.IGNORECASE)]