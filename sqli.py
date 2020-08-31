import requests
import sys
import os

from DB import DB
from Table import Table
from HTTPRequest import HTTPRequest
from Enums import HTTP_Types

# chars and seperators
HEADER_SEP = ": "
AMPERSAND = "&"
EQUAL_SIGN="="

# flags for operating the program
READ_REQUEST_FILE_FLAG = '-r'


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
                request.append_header(header_name, lines[i].split(header_name)[-1])
            else:  # assuming only parameters and no data
                for parameter in lines[i].split(AMPERSAND):
                    name = parameter.split(EQUAL_SIGN)[0]
                    value = parameter.split(name+EQUAL_SIGN)[1]
                    request.append_parameter(name, value)
    return request

if __name__ == '__main__':
    request = parse_request_file("C:\\Users\\Amit\\Downloads\\request.txt")
    print(request)
