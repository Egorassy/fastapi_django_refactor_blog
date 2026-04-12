from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):
    pass


class IntegrityDatabaseError(DatabaseError):
    pass


class NotFoundError(DatabaseError):
    pass