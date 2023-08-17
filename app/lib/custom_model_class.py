from flask_sqlalchemy.model import Model
import sqlalchemy as sa 
import sqlalchemy.orm 

class IdModel(Model):
    @sa.orm.declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base,"__table__", None) is not None:
                type = sa.ForeignKey(base.id)
                break
            else:
                type = sa.Integer
            
            return sa.Column(type, primary_key=True)