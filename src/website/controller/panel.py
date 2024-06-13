from . import *



async def admin(request: Request):
	return response.html(Render.content(Path("index.html")))

async def client(request: Request):
	return response.html(Render.content(Path("index.html")))
