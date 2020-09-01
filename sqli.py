import requests
import sys
import os
import copy

from DB import DB
from Table import Table
from HTTPRequest import HTTPRequest
from Enums import HTTP_Types

# communication with user
SQLI_DETECTED_MSG = "SQLi may have been detected!\n"
SQLI_NOT_DETECTED_MSG = "SQLi not detected. \n"

# chars and seperators
HEADER_SEP = ": "
AMPERSAND = "&"
EQUAL_SIGN = "="

# flags
SQLI_NOT_DETECTED = "no"

# flags for operating the program
READ_REQUEST_FILE_FLAG = '-r'
PARAMETER_FLAG = "-p"

# lists of Strings
SQL_ERRORS = ["you have an error in your sql syntax"]
SQLI_CHARS = ["\'", "\0", "\\", "-", "%", "#"]

def parse_request_file(request_filepath):
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
    new_request = copy.deepcopy(request)
    new_parameters = copy.deepcopy(request.get_parameters())
    new_headers = copy.deepcopy(request.get_headers())
    new_request.set_parameters(new_parameters)
    new_request.set_headers(new_headers)
    return new_request


def send_post_request(request):
    return requests.post(request.get_url(), data=request.get_parameters(), headers=request.get_headers())


def send_request(request):
    if request.get_method() == HTTP_Types.POST:
        return send_post_request(request)


def find_sqli(request, parameter):
    for char in SQLI_CHARS:
        request.set_parameter(parameter, char)
        response = send_request(request)
        for error_msg in SQL_ERRORS:
            if error_msg in response.text.lower():
                print(SQLI_DETECTED_MSG)
                return char
    print(SQLI_NOT_DETECTED_MSG)
    return SQLI_NOT_DETECTED



if __name__ == '__main__':
    origin_request = parse_request_file("C:\\Users\\Amit\\Downloads\\request.txt")
    parameter = "username"
    request = get_request_copy(origin_request)
    is_there_sqli = find_sqli(request, parameter)
    if is_there_sqli == SQLI_NOT_DETECTED:
        exit(0)
    
