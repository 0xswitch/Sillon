import os
import sys
import requests
import re
from utils.display import p_e, p_i

class Load():
    """
    Load each payloads file for directory and charge it one time in RAM to prevent too much read action
    """

    def __init__(self, path, args):
        self.args = args
        self.path = os.path.dirname(os.path.realpath(path)) + "/payloads/"
        self.user_path = self.path + "user_payloads/"
        self.sqli_UF = False
        self.selected_files = {}

    def parse_args(self):


        if self.args.sqli_file is not None:

            if re.match("^[a-zA-Z0-9\_\-\.]+$", self.args.sqli_file):
                if os.path.isfile(self.user_path + self.args.sqli_file):
                    self.sqli_UF = self.args.sqli_file
                    p_i("Successfully loaded : %s" % self.user_path + self.sqli_UF)
                else:
                    p_e("File not found : %s" % (self.user_path + self.args.sqli_file))
                    sys.exit(0)

            else:

                if self.args.name is None:
                    p_e("--name required !")
                    sys.exit(0)
                elif not re.match("^[a-zA-Z0-9\_\-\.]+$", self.args.name):
                    p_e("name must respect ^[a-zA-Z0-9_\-\.]+$ ;)")
                    sys.exit(0)

                self.sqli_UF = self.args.name
                self.fetch_file(self.args.sqli_file, self.args.name)

    def __call__(self, *args, **kwargs):
        self.parse_args()
        self.select_file()
        return self.selected_files


    def select_file(self):


        for file in os.listdir(self.path):
            if os.path.isfile(self.path + file):
                self.selected_files[file] = open(self.path + file).read()

        if self.sqli_UF:
            self.selected_files["sql_injection"] = open(self.user_path + self.sqli_UF).read()



    def fetch_file(self, sqli_file, name):
        try:
             data = requests.get(sqli_file).text
             self.save_file(data, name)
        except requests.exceptions.MissingSchema:
            p_e("Bad url provided, unable to fetch sqli file at : %s" % sqli_file)


    def save_file(self, data, name):
        name = self.user_path + name
        open(name, "w").write(data.replace("\r",""))


