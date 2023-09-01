from flask import abort
from flask_sqlalchemy.model import Model
from app.extensions import db
import typing as t

_O = t.TypeVar("_O", bound=object)


class DBStatement:
    def __init__(self, *, model_class: type[Model] = None) -> None:
        self.model = model_class
        self.session = db.session

    def get_first_or_404(
        self, statement: db.sql.Select[t.Any], *, description: str | None = None
    ) -> t.Any:
        """Like :meth:`Result.scalar() <sqlalchemy.engine.Result.scalar>`, but aborts
        with a ``404 Not Found`` error instead of returning ``None``.

        :param statement: The ``select`` statement to execute.
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

    def delete_data(self, statement: type[_O]) -> _O:
        self.session.delete(statement)
        return self.session.commit()

    def update_data(self) -> _O:
        return self.session.commit()

    def dbs_abort(self, status_code: int, description: str | None = None) -> t.Any:
        abort(status_code, description=description)
