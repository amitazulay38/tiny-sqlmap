import requests
from Enums import HTTP_Types
from HTTPRequest import HTTPRequest

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

def send_sql_request(request, parameter, query):
    """
    sends sql query request
    :param request: the HTTPRequest object we will modify
    :param parameter: the exploitable parameter
    :param query: the query we want to send in the exploitable parameter
    :return: the reponse object
    """
    request.set_parameter(parameter, query)
    return send_request(request)