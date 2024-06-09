"""
## WebSocket Sanic Demo/Test
Add this in the router:
```
from .controller import websocket_demo as WSD
_ = URL.add_route(WSD.demo, "/WSD_demo")
_ = URL.add_websocket_route(WSD.ws_demo, "/ws_demo")
```
"""

HTML = """
<!DOCTYPE html>
<html lang="fr">
    <head>
        <title>WebSocket Client Demo</title>
        <meta charset="UTF-8">

        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <script>
            const socket = new WebSocket('ws://localhost:5000/ws_demo');

            socket.onopen = async () => {
                let res; socket.onmessage = async (event) => {res = event.data}
                alert("The Websocket connection is opened! Connection timeout is 10 secondes.")

                while (true) {
                    await socket.send(prompt(res || "Say Hello"))
                    if (socket.readyState == 3) break

                    await new Promise(resolve => setTimeout(resolve, 100))
                }
                
                if (confirm("Websocket connection closed. Reload?")) location.reload()
            }

            socket.onerror = async (error) => {console.error('WebSocket error:', error)}
        </script>
    </body>
</html>
"""


from sanic import Request, Websocket, response

# ----------------------------------------------------------------------------------------------------
async def demo(request: Request):
	return response.html(HTML)


async def ws_demo(request: Request, ws: Websocket):
	while True:
		msg = await ws.recv(10) # 10 secondes
		if not msg: break; print(f"Received messages: {msg}")

		res = f"Roger! You say me: {msg}"
		await ws.send(res)
		print(f"I replied: {res}")

	print("connection close")
# ----------------------------------------------------------------------------------------------------
