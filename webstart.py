
from microWebSrv import MicroWebSrv
from machine import Pin, ADC
import time


pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

webs = []


def _acceptWebSocketCallback(webSocket, httpClient) :
    global webs
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback     = _closedCallback
    webs.append(webSocket)

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
    print("WS CLOSED")

@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
 
        </body>
    </html>
    """ % pot.read()
    
    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )



routeHandlers = [
   ( "/test",  "GET",  _httpHandlerTestGet ),
]
srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded       = True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
print("Vor Start")
srv.Start(threaded=True)
print("srv Ende")


while not webs:
    pass

pot_value = pot.read()
while pot_value > 1:
    for i in webs:
        i.SendText("counter:%s" % pot_value)
        time.sleep(0.3)
        pot_value = pot.read()

print("Schluss")

# ----------------------------------------------------------------------------
