import asyncio
import json
import logging
import os
import sys
import ssl

from aiohttp_sse import sse_response
from ssl import SSLContext
from json.decoder import JSONDecodeError
from collections import defaultdict

from aiohttp import web

logging.basicConfig(format='%(asctime)s %(message)s', filename='logs/log.txt', filemode='a', level=logging.DEBUG)

# Print to console
logging.getLogger().addHandler(logging.StreamHandler())



###############################################################################################################################
#
# Processinng the observations from the mouth
#
###############################################################################################################################

async def observations(request):
    
    # If request's body is empty
    if not request.can_read_body:
        logging.info("RequestBodyEmtpy")
        return web.Response(status=400, body="RequestBodyEmpty")

    # Try to parse request body as json
    try:
        observation = await request.json()
    except JSONDecodeError:
        logging.info("JsonDecodeError: {}".format(await request.text()))
        return web.Response(status=400, body="JsonDecodeError")

    #
    # 
    # DO SOMETHING WITH observation in JSON FORMAT
    # Note: to see the format of the incoming observations, subscribe to recieve SSE
    #
    #

    # Send an SSE to a subscriber
    app = request.app
    for queue in app['channels']:
        payload = json.dumps(dict(observation))
        await queue.put(payload)

    # return a simple responce
    return web.Response(status=200, body="OK")



###############################################################################################################################
#
# Subscribe a client to SSE
#
###############################################################################################################################

async def subscribe(request):
    async with sse_response(request) as response:
        app = request.app
        queue = asyncio.Queue()
        
        logging.info('Someone joined.')
        app['channels'].add(queue)

        try:
            while not response.task.done():
                payload = await queue.get()
                await response.send(payload)
                queue.task_done()
        finally:
            app['channels'].remove(queue)
            logging.info('Someone left.')
    
    return response



###############################################################################################################################
#
# Main
#
###############################################################################################################################

sslEnabled = False
sslContext = None

# If both public and private keys were defined, use HTTPS 
if os.path.isfile("cert/server.crt") and os.path.isfile("cert/server.key"):
    sslEnabled = True
    sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslContext.load_cert_chain("cert/server.crt", "cert/server.key")

logging.info("HTTPS: " + str(sslEnabled))

# If port was specified, use that port. 
if "ENDPOINT_PORT" in os.environ:
    port = int(os.environ.get('ENDPOINT_PORT'))
else:
    # Otherwise, use default HTTP(S) ports
    port = 443 if sslEnabled else 80

logging.info("PORT: " + str(port))


# Initialise aiohttp web
app = web.Application()

# Open channels to enable SSE (optional)
app['channels'] = set()


app.router.add_post('/observations', observations)
app.router.add_get('/subscribe', subscribe)

web.run_app(app, host = "0.0.0.0", port=port, ssl_context=sslContext)

    