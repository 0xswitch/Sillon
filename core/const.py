"""
Constants which are compulsory for the whole program
"""
KEY = [
    "host",
    "url",
    "after_host",
    "uri",
    "page_name",
    "server",
    "parameters",
    "length",
    "ligne",
    "status",
    "forms",
    "php_errors",
    "cookies",
]
EXCLUDED_EXT = "xml"
ALLOW_EXT = "php"
HOST_REGEX = r"(https?://([a-zzZ-a0-9\.-]+)/?)"
URI_REGEX = r"([\w\/\-\s]+\/+)?(\w+(\.\w+)?\??)?(.*)"
PARAMETERS_REGEX = r"(\w+)=?([^&\s]*)?"
AHREF_REGEX = r"\s*(?i)href\s*=\s*(\"([^\"]*\")|'[^']*'|([^'\">\\s]+))"
PHP_ERRORS_R = r"(Warning|Notice|Fatal Error):(.*?)(on line (<i>)?\d+)"
FIELD_REGEX = r"(\s(id|type|name|value)=\"(.*?)\")"
INPUT_REGEX = r"<input(.*?)>"
ACTION_REGEX = r"action=[\"'](.*)[\"']"
METHOD_REGEX = r"method=[\"']post[\"']"
FORM_REGEX = r"<form (.*?)<\/form>"
ID_R = r"id=\"(.*?)\""
ALONE_FILE = r"^(?!https?://)(\.\/|\/)?([a-zA-Z0-9\_\/]+)(\.(php|html))?(\?(\w+=\w+))?"
ALONE_FILE_WITH_DOT = r"^(?!https?://)(\.\/)([a-zA-Z0-9\_\/]+)(\.(php|html))?(\?(\w+=\w+))?"
ALONE_FILE_WITH_SLASH = r"^(?!https?://)(\/)([a-zA-Z0-9\_\/]+)(\.(php|html))?(\?(\w+=\w+))?"