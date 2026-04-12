from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):
    def __init__(self, message: str = "Database error"):
        self.message = message
        super().__init__(message)


class IntegrityDatabaseError(DatabaseError):
    def __init__(self, message: str = "Integrity constraint violated"):
        super().__init__(message)


class NotFoundError(DatabaseError):
    def __init__(self, entity: str, entity_id: int):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id={entity_id} not found")