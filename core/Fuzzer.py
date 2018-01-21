from core.const import KEY
from core.Scrapper import grep_char, grep_ligne, PHP_errors
from utils.display import p_i, display_sql, display_array_url

class Fuzz():
    """"
    Class who fuzz the page found via Scrapper
    """

    def __init__(self, informations, requester, payloads, args):
        self.args = args
        self.payloads = payloads
        self.informations = informations
        self.requester = requester
        self.stop = False
        self.suitable = True
        #
        self.host = None
        self.after_host = None
        self.cookies = None
        self.forms = None
        self.length = None
        self.ligne = None
        self.page_name = None
        self.parameters = None
        self.php_errors = None
        self.server = None
        self.status = None
        self.uri = None
        self.url = None



    def parse_args(self):
        if self.args.verbose :
            self.verbose = True

        if self.args.stop:
            self.stop = True

    def suitable_for_fuzzing(self):

        if self.page_name != "":
            if len(self.page_name.split(".")) > 1 :
                if self.page_name.split(".")[1] != "php":
                    self.suitable = False

    def __call__(self, *args, **kwargs):
        """
        Main method return list of urls which were sensible to fuzzing
        """
        self.mapp(self.informations)
        self.suitable_for_fuzzing()
        if self.suitable:
            self.parse_args()

            if len(self.parameters) > 0:
                display_array_url(self.array_in_url())
                display_sql(self.sql_injection())


    def __str__(self):
        for attr in dir(self):
            if attr in KEY:
                print attr + " : " + str(getattr(self, attr))
        return ""

    def mapp(self, informations):
        for item, value in zip(informations.keys(), informations.values()):
            setattr(self, item, value)

    def pourcentage(self, changement, liste, item):
        """
        Pourcentage de cette item dans la liste changement, permet de detecter un element different
        """
        return float(changement.count(item)) / len(liste)

    def minimum(self, listing):
        mini = 1
        for a in listing:
            if a < mini:
                mini = a
        return mini


    ################################
    #            TESTS             #
    ################################


    def sql_injection(self):
        """
        Try to find injection SQL
        :return:
        """

        #todo formulaires

        url = []

        for injec in self.payloads["sql_injection"].split("\n"):

            for i in range(0, len(self.parameters)):
                payload = self.host + self.uri[1:] + self.page_name + "?"
                for (key, value), x in zip(self.parameters, range(0, len(self.parameters))):
                    if i == x:
                        fuzz = key + "=" + value + injec
                        payload += key + "=" + value + injec + "&"
                    else:
                        payload += key + "=" + value + "&"

                payload = payload[:-1]

                query = self.requester.get(payload)
                difference_length = self.length - grep_char(query.text)
                difference_ligne = self.ligne - grep_ligne(query.text)


                url.append([
                        payload,
                        difference_length,
                        difference_ligne,
                        fuzz,
                        PHP_errors(query.text),
                        query.status_code
                    ])

        return url


    def array_in_url(self):
        """
        Definie le type de variable comme un tableau, peut generer des erreurs
        """

        tested_urls = []

        for i in range(0, len(self.parameters)):
            payload = self.host + self.uri[1:]  + self.page_name  + "?"
            for (key, value), x in zip(self.parameters, range(0, len(self.parameters))):
                if i == x:
                    fuzz = key + "[]=" + value
                    payload += key + "[]=" + value + "&"
                else:
                    payload += key + "=" + value + "&"

            payload = payload[:-1]
            query = self.requester.get(payload[:-1])

            difference_length = self.length - grep_char(query.text)
            difference_ligne = self.ligne - grep_ligne(query.text)

            php_errors = PHP_errors(query.text)

            tested_urls.append([payload, difference_length, difference_ligne, php_errors, query.status_code])

        return tested_urls


