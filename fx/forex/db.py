import peewee
import datetime

db = peewee.SqliteDatabase('test.db')

# orm class for transaction model
class Forex(peewee.Model):

    from_cur = peewee.CharField()
    to_cur = peewee.CharField()
    amount = peewee.FloatField()
    rate = peewee.FloatField()
    result = peewee.FloatField()
    transation_date = peewee.IntegerField()
    created = peewee.DateField(default=datetime.date.today)

    class Meta:

        database = db
        db_table = 'transaction'

# creading the table 
Forex.create_table()
