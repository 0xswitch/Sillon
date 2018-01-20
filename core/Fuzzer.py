from core.const import KEY
from core.Scrapper import grep_char, grep_ligne, PHP_errors
from utils.display import p_i, display_sql

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
        ##
        self.receptive_url = {}


    def parse_args(self):
        if self.args.verbose :
            self.verbose = True

        if self.args.stop:
            self.stop = True

    def __call__(self, *args, **kwargs):
        """
        Main method return list of urls which were sensible to fuzzing
        """
        self.mapp(self.informations)
        self.parse_args()

        if len(self.parameters) > 0:

            self.receptive_url["url_array"] = self.array_in_url()
            self.receptive_url["sql_injection"] = self.sql_injection()

        if len(self.receptive_url) > 0:
            return self.receptive_url


    def __str__(self):
        for attr in dir(self):
            if attr in KEY:
                print attr + " : " + str(getattr(self, attr))
        return ""

    def mapp(self, informations):
        for item, value in zip(informations.keys(), informations.values()):
            setattr(self, item, value)


    def sql_injection(self):
        """
        Try to find injection SQL
        :return:
        """

        #todo formulaires

        url = []
        receptive_url = []
        length_changement = []
        ligne_changement = []

        for injec in self.payloads["sql_injection"].split("\n")[:-1]:

            for i in range(0, len(self.parameters)):
                payload = self.host + self.uri[1:] + "/" + self.page_name + "?"
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

                length_changement.append(difference_length)
                ligne_changement.append(difference_ligne)

                url.append({

                    "url": payload,
                    "length": difference_length,
                    "ligne": difference_ligne,
                    "page": query.text,
                    "parameters": fuzz

                })

        mini_len = self.minimum([ self.pourcentage(length_changement, url, test["length"]) for test in url])
        mini_ligne = self.minimum([ self.pourcentage(ligne_changement, url, test["ligne"]) for test in url])

        for test in url:
            score = 0
            pourcent_len = self.pourcentage(length_changement, url, test["length"])
            pourcent_ligne = self.pourcentage(ligne_changement, url, test["ligne"])

            if mini_len == pourcent_len and mini_len != 1.0:

                if len([ item for item in length_changement if self.pourcentage(length_changement, url, item) == pourcent_len]) != len(length_changement):
                    score += 1

            if mini_ligne == pourcent_ligne and mini_ligne != 1.0:
                score += 1

            php_errors = PHP_errors(test["page"])
            if len(php_errors) > 0:
                score += 1

            if score != 0:
                receptive_url.append((test["url"], test["parameters"], php_errors))

                if self.stop:
                    p_i("One potentially SQL injection found, continue ? [Y/n]")
                    display_sql(receptive_url[-1])

                    if raw_input("> ") == "n":
                        break

        return receptive_url


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

    def array_in_url(self):
        """
        Definie le type de variable comme un tableau, peut generer des erreurs
        :return:
        """
        receptive_url = []

        for i in range(0, len(self.parameters)):
            payload = self.host + self.uri[1:] + "/" + self.page_name  + "?"
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

            if difference_length != 0 or difference_ligne != 0:
                php_errors = PHP_errors(query.text)
                receptive_url.append((payload, fuzz, php_errors))

        return receptive_url
