from . import *



async def god(request: Request):
	return response.text("god")

async def admin(request: Request):
	return response.text("admin")

async def client(request: Request):
	return response.text("client")
