class UseCaseError(Exception):
    pass


class EntityNotFoundError(UseCaseError):
    def __init__(self, entity: str, entity_id: int):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id={entity_id} not found")


class EntityAlreadyExistsError(UseCaseError):
    def __init__(self, entity: str, field: str | None = None):
        self.entity = entity
        self.field = field
        msg = f"{entity} already exists"
        if field:
            msg += f" (field: {field})"
        super().__init__(msg)