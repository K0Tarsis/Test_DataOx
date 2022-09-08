from peewee import *


user = 'root'
password = 'root'
db_name = 'apart_db'

dbhandle = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Apartment(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField()
    pict_url = CharField()
    city = CharField()
    beds = IntegerField()
    description = TextField()
    price = DecimalField()
    currency = CharField()
    date = DateField(formats=['%d-%m-%Y'])

    class Meta:
        db_table = "apartments"
        order_by = ('id',)