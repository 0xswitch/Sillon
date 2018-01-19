#encoding: utf-8
from utils.colors import *
from utils.console_size import get_terminal_size
from core.const import KEY


def banner():
    print u"""     o
    -+-
     |              Happy Fuzzzzing
     |
  ^  |  ^
   \_|_/                      switch
"""

def maximum(liste):
    max_url  = 0
    max_length = 0
    max_ligne = 0
    for dico in liste:
        if len(dico["url"]) > max_url:
            max_url = len(dico["url"])

        if len(str(dico["length"])) > max_length:
            max_length = len(str(dico["length"]))

        if len(str(dico["ligne"])) > max_ligne:
            max_ligne = len(str(dico["ligne"]))

    return max_url, max_length, max_ligne

def mep(field, value):
    """
    MEP : Mise en page
    :param field:
    :param value:
    :return:
    """
    if field == "url":
        return "URL : %s" % value
    elif field == "after_host":
        return "After host : %s" % value
    elif field == "uri":
        return "URI : %s" % value
    elif field == "page_name":
        return "Page name : %s" % value
    elif field == "server":
        return "Server : %s " % value
    elif field == "parameters":
        return  "Parameters :\n" + "\n".join(["    "+ "=".join(param) for param in value])  if len(value) > 0 else "Parameters : None"
    elif field == "length":
        return "Char in page : %i" % value
    elif field == "ligne":
        return "Return in page : %i " % value
    elif field == "status":
       return "Status : %s" %  OKGREEN + str(value) + ENDC if value == 200 else "Status : %s" % FAIL + str(value) + ENDC
    elif field == "forms":
        if len(value) > 0:
            tmp = "Forms :\n"
            for form in value:
                ftmp = ""
                ftmp += "    Form ID : "
                ftmp += form["id"] if form["id"] != "" else "None"
                ftmp += "\n"
                ftmp += "    Action  : " + form["action"]
                ftmp += "\n"
                for inputs in form["inputs"]:
                    ftmp += "    Inputs  : " + " ".join(["=".join(attribut) for attribut in inputs])
                    ftmp += "\n"
                tmp += ftmp + "\n"
            tmp = tmp[:-1]
        else:
            tmp = "Forms : None"
        return  tmp
    elif field == "php_errors":
        if len(value) > 0:
            tmp = ""
            tmp += "PHP errors : \n"
            tmp += "\n".join(["    " + " : ".join(error) for error in value])
        else:
            tmp = "PHP errors : None"
        return tmp
    elif field == "cookies":
        if len(value) > 0:
            tmp = "Cookies : \n"
            tmp += "\n".join(["    " + "=".join(cookies) for cookies in value])
        else:
            tmp = "Cookies : None"
        return tmp



def nice_display(found_url, fields, remove):
    valid_fields =  parse_fields(fields, remove)
    i = 1
    if valid_fields is not None:
        for item in found_url:
            head = "=[ "+ OKGREEN + str(i) + ENDC +" ]" if i % 2 == 0 else "=[ "+ FAIL + str(i) + ENDC +" ]"
            print head  + "=" * (get_terminal_size()[0] - len(head) + 5)
            print
            for field in valid_fields:
                print "["+ OKGREEN + "+" + ENDC +"] " + mep(field, item[field]) if i % 2 == 0 else "["+ FAIL + "+" + ENDC +"] " + mep(field, item[field])
            print
            i += 1


def parse_fields(fields, remove):
    """
    Choose which fields must be display according to user parameters --field
    :param fields:
    :param remove:
    :return:
    """
    allowed = []

    if remove is not None:
        remove = remove.split(",")
    else:
        remove = []

    for field in KEY:
        if field not in remove:
            allowed.append(field)

    if fields is not None:
        selected_fields = fields.split(",")
        return [field for field in selected_fields if field in allowed]
    else:
        return [field for field in KEY if field in allowed]

def screen_size():
    return get_terminal_size()


# def old_display():
# url, length, ligne = maximum(found_url)
#
# header_two =  "[CODE]==[ U ]" + "=" * (url - 4 ) + "=[ C ]=" + "=" * (length - 7) + "=[ L ]=" + "=" * (ligne - 3) + "=[ F ]=" + "=[ E ]="
# header_one =  "=[ " + base_url + " ]="
# header_one += "=" * (len(header_two) - len(header_one))
# print header_one
# print "Uniq url found : %i" % len(found_url)
# print
# # print header_two
# print "=" * len(header_two)
# for item in found_url:
#     line =""
#     line += " " + OKGREEN + str(item["status"]) + ENDC if item["status"] == 200 else " " + FAIL + str(item["status"]) + ENDC
#     line += "\t" + item["url"]
#     line += " " * (url - len(item["url"]) + 3) + str(item["length"])
#     line += " "  * ( length - len(str(item["length"])) + 4) + str(item["ligne"])
#     line += " " * (ligne - len(str(item["ligne"])) + 5)
#     line += OKGREEN + str(len(item["forms"])) + ENDC if len(item["forms"]) >=1 else FAIL + str(len(item["forms"])) + ENDC
#     line += "\t"
#     line += OKGREEN + str(len(item["php_errors"])) + ENDC if len(item["php_errors"]) >= 1 else FAIL + str(len(item["php_errors"])) + ENDC
#     line += "\t"
#     line += OKGREEN + str(len(item["cookies"])) + ENDC if len(item["cookies"]) >= 1 else FAIL + str(len(item["cookies"])) + ENDC
#
#     print line