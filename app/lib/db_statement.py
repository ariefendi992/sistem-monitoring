from flask import abort
from flask_sqlalchemy.model import Model
from app.extensions import db
import typing as t

_O = t.TypeVar("_O", bound=object)


class DBStatement:
    def __init__(self, *, model_class: type[Model] = None) -> None:
        self.model = model_class
        self.session = db.session

    def add_data(self, data: t.Any) -> t.Any:
        """AI is creating summary for add_data table"""
        if type(data) == t.List:
            return self.session.add_all(data)
        return self.session.add(data)

    # def add_data(self, entity: type[_O], data: t.Any):
    #     if type(data) == t.List:
    #         model = entity(data)
    #         return self.session.add_all(model)

    #     else:
    #         model = entity(data)
    #         return self.session.add(data)

    def get_first_or_404(
        self, statement: db.sql.Select[t.Any], *, description: str | None = None
    ) -> t.Any:
        """Like :meth:`Result.scalar() <sqlalchemy.engine.Result.scalar>`, but aborts
        with a ``404 Not Found`` error instead of returning ``None``.

        :param statement: The ``select`` stateme nt to execute.
        :param description: A custom message to show on the error page.

        .. versionadded:: 3.0
        """
        value = self.session.execute(statement).scalar()

        if value is None:
            abort(404, description=description)

        return value

    def get_one(self, entity: type[_O], **ident: t.Any) -> _O:
        """Like : met: `Resuslt.first() <flask_sqlalchemy.SqlAlchemy>
        :param entity: The model class ot query
        :param ident: The filter Field to query
        """
        value = self.session.query(entity).filter_by(**ident).first()
        return value

    def get_all(self, entity: type[_O], *filter: t.Any, **filter_by: t.Any) -> _O:
        """AI is creating summary for get_all

        Args:
            entity (type[_O]): [DataBase Model]

        Returns:
            _O: [Get All Data Query]
        """
        if filter is not None and filter_by == None:
            value = self.session.query(entity).filter(*filter).all()
        elif filter_by is not None and filter == None:
            value = self.session.query(entity).filter_by(**filter_by).all()
        else:
            value = self.session.query(entity).all()

        return value

    def delete_data(self, statement: type[_O]) -> _O:
        self.session.delete(statement)
        return self.session.commit()

    def commit_data(self) -> _O:
        """AI is creating summary for commit_data

        Returns:
            _O: [Result commit database]
        """
        return self.session.commit()

    def dbs_abort(self, status_code: int, description: str | None = None) -> t.Any:
        """AI is creating summary for dbs_abort

        Args:
            status_code (int): [HTTP Status]
            description (str, optional): [description about connection status]. Defaults to None.

        Returns:
            t.Any: [description]
        """
        abort(status_code, description=description)
