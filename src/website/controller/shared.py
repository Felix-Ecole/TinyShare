from . import *



async def shared(request: Request, ID:str):
	if request.method == "POST":
		...
	else:
		html, data = "", {}
		for val in dir(request):
			if val not in ["scope", "stream_id"] and hasattr(request, val):
				html+=f"{val}: {{{{ context['data']['{val}'] }}}}<br><hr>\n"
				data[val] = getattr(request, val)
		return response.html(Render.text(html, {"data": data}))
