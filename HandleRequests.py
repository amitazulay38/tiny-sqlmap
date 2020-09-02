import aiohttp
import asyncio
from aiohttp_requests import requests
from Enums import HTTP_Types
from HTTPRequest import HTTPRequest
import copy

async def send_post_request(request, session):
    """
    sends post request
    :param request: a HTTPRequest object containing all the data we want to send
    :return: the response
    """
    headers = request.get_headers()
    new_headers = {}
    for key in headers.keys():
        if key not in ['Content-Length']:
            new_headers[key] = copy.deepcopy(headers[key])
    response = await session.post(request.get_url(), data=request.get_parameters(), headers = new_headers)
    return response


async def send_request(request, session):
    """
    redirects the request to the relevant function, according to the HTTP method we want to use
    :param request: a HTTPRequest object containing all the data we want to send
    :return: the response
    """
    if request.get_method() == HTTP_Types.POST:

        return await send_post_request(request, session)

async def send_sql_request(request, parameter, query, session):
    """
    sends sql query request
    :param request: the HTTPRequest object we will modify
    :param parameter: the exploitable parameter
    :param query: the query we want to send in the exploitable parameter
    :return: the reponse object
    """
    request.set_parameter(parameter, query)
    return await send_request(request, session)