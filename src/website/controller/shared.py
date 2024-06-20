from . import *
from ..models import Shared


async def shared(request: Request, ID:str):
	print(request.method)
	if request.method == "POST":
		if "link_shared" in getattr(request, "route").name:
			if not request.form: return response.text("Null 'link' not valid")

			link_id = await Shared_ID.get(id=ID)
			if await Shared.get_or_none(id=link_id.data): return response.text("url_id is used")
			_ = await Shared.create(
				id=link_id.data, type="link", data=request.form["link"][0],
				cr_date=datetime.now()
			)

			await link_id.delete()
			return response.text(request.host + "/l/" + link_id.data)

			# TODO: Implémenté l'ID de session dans le token renvoyer à l'utilisateur !
			# request.ctx.token

		else:
			return response.text("post")
	else:
		if "link_shared" in getattr(request, "route").name:
			link = await Shared.get_or_none(id=ID)
			return response.redirect(link.data if link else "/")

		else:
			html, data = "", {}
			for val in dir(request):
				if val not in ["scope", "stream_id", "json"] and hasattr(request, val):
					html+=f"{val}: {{{{ ctx['data']['{val}'] }}}}<br><hr>\n"
					data[val] = getattr(request, val) if not "json" in val else ""
			return response.html(Render.content(html, {"data": data}))
