from piccolo.columns import Boolean, Varchar
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table

DB = SQLiteEngine("bd.sqlite")


class Order(Table, db=DB):
    uuid = Varchar(primary_key=True)
    name = Varchar()
    completed = Boolean(default=False)
    date = Varchar()
