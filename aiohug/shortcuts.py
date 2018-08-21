from aiohttp import web

RESPONSE_STATUS = 0
RESPONSE_BODY = 1


def process_response(resp):
    # plain text
    if type(resp) is str:
        resp = web.Response(text=resp)

    # json
    elif type(resp) is dict or type(resp) is list:
        resp = web.json_response(data=resp)

    # status and body
    elif (
        type(resp) is tuple
        and type(resp[RESPONSE_STATUS]) is int
        and (type(resp[RESPONSE_BODY]) is dict or type(resp[RESPONSE_BODY]) is list)
    ):
        resp = web.json_response(status=resp[RESPONSE_STATUS], data=resp[RESPONSE_BODY])

    return resp
