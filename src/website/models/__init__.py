from tortoise import Model, fields as fs
from .shared_id import *


class Users(Model):
	id = fs.IntField(primary_key=True)
	pseudo = fs.CharField(64, unique=True, db_index=True)
	mail = fs.CharField(64, unique=True)
	passwd = fs.CharField(90)
	cr_date = fs.DatetimeField()

	connections: fs.ReverseRelation["Connections"]
	groups: fs.ManyToManyRelation["Groups"] = fs.ManyToManyField(
		"models.Groups", related_name="users"
	)


class Groups(Model):
	id = fs.SmallIntField(primary_key=True)
	name = fs.CharField(32)
	level = fs.SmallIntField()

	connections: fs.ReverseRelation["Connections"]
	users: fs.ManyToManyRelation["Users"]
	shares: fs.ReverseRelation["Shared"]


class Connections(Model):
	id = fs.IntField(primary_key=True)
	cnn_date = fs.DatetimeField()
	dcn_date = fs.DatetimeField(null=True)
	max_date = fs.DatetimeField()

	fk_user: fs.ForeignKeyRelation[Users]|None = fs.ForeignKeyField("models.Users", "connections")
	fk_group: fs.ForeignKeyNullableRelation[Groups]|None = fs.ForeignKeyField("models.Groups", "connections", null=True)


class Shared(Model):
	id = fs.CharField(6, primary_key=True)
	type = fs.CharField(16)
	data = fs.TextField()
	cr_date = fs.DatetimeField()

	fk_user = fs.ForeignKeyField("models.Users", "shares", null=True)
