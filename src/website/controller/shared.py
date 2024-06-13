from . import *



async def shared(request: Request, ID:str):
	# if request.method == "POST":
	# 	return response.text("post")
	# else:
	# 	return response.text("get")

	html, data = "", {}
	for val in dir(request):
		if val not in ["scope", "stream_id", "json"] and hasattr(request, val):
			html+=f"{val}: {{{{ ctx['data']['{val}'] }}}}<br><hr>\n"
			data[val] = getattr(request, val) if not "json" in val else ""
	return response.html(Render.content(html, {"data": data}))
