from tortoise import Model, fields as fs


class Shared_ID(Model):
	id = fs.IntField(primary_key=True)
	data = fs.CharField(6)
