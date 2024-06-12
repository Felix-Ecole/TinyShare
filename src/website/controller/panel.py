from . import *



async def admin(request: Request):
	return response.html(Render.file("index.html"))

async def client(request: Request):
	return response.html(Render.file("index.html"))
