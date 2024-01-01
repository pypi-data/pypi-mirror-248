from typing import List, Type

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select


class BaseCRUDRouteBuilder:
    """
    `BaseCRUDRouteBuilder` class, used to wrap all logic of all CRUD operations
    which is used in CrudApiRouter as an input.
    """

    def create(self, schema: Type, read_schema: Type, create_schema: Type):
        def route(data: create_schema) -> read_schema:
            return read_schema(**data.dict())

        return route

    def list(self, schema: Type, read_schema: Type):
        def route() -> List[read_schema]:
            return []

        return route

    def retrieve(self, schema: Type, read_schema: Type):
        def route(id: int | str) -> read_schema:
            return {}

        return route

    def update(self, schema: Type, read_schema: Type, update_schema):
        def route(data: update_schema) -> read_schema:
            return schema(**data.dict())

        return route

    def delete(self, schema: Type, read_schema: Type):
        def route(id: int | str) -> read_schema:
            return {}

        return route


class InMemoryCRUDRouteBuilder(BaseCRUDRouteBuilder):
    """
    `BaseCRUDRouteBuilder` class, used to wrap all logic of all CRUD operations
    which is used in CrudApiRouter as an input.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastcrudapi import CrudApiRouter
    from pydantic import BaseModel

    app = FastAPI()

    class User(BaseModel):
        first_name: str
        last_name: str

    router = CrudApiRouter(
        prefix="/users",
        schema=User,
        api_handler_builder=InMemoryCRUDRouteBuilder()
    )

    app.include_router(router)
    ```
    """


class SqlCRUDRouteBuilder(BaseCRUDRouteBuilder):
    """
    `SqlCRUDRouteBuilder` class, used to wrap all logic of all CRUD operations
    which works with `sqlmodel` to interact with sql database.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastcrudapi import CrudApiRouter
    from sqlmodel import Field, SQLModel

    from db import engine

    app = FastAPI()

    class User(SQLModel, table=True):
        name: str = Field(default=None, primary_key=True)

    router = CrudApiRouter(
        prefix="/users",
        schema=User,
        api_handler_builder=SqlCRUDRouteBuilder(engine)
    )

    app.include_router(router)
    ```
    """

    def __init__(self, engine) -> None:
        super().__init__()
        self.engine = engine

    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def create(self, schema: Type, read_schema: Type, create_schema: Type):
        def route(
            data: create_schema,
            session: Session = Depends(self.get_session),
        ) -> read_schema:
            db_data = schema.model_validate(data)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data

        return route

    def list(self, schema: Type, read_schema: Type):
        def route(
            session: Session = Depends(self.get_session),
            offset: int = 0,
            limit: int = Query(default=100, le=100),
        ) -> List[read_schema]:
            return session.exec(select(schema).offset(offset).limit(limit)).all()

        return route

    def retrieve(self, schema: Type, read_schema: Type):
        def route(
            id: int | str,
            session: Session = Depends(self.get_session),
        ) -> read_schema:
            record = session.get(schema, id)
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"{schema.__name__} not found"
                )
            return record

        return route

    def update(self, schema: Type, read_schema: Type, update_schema):
        def route(
            id: int,
            data: update_schema,
            session: Session = Depends(self.get_session),
        ) -> read_schema:
            record = session.get(schema, id)
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"{schema.__name__} not found"
                )
            record_data = data.model_dump(exclude_unset=True)
            for key, value in record_data.items():
                setattr(record, key, value)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

        return route

    def delete(self, schema: Type, read_schema: Type):
        def route(
            id: int | str,
            session: Session = Depends(self.get_session),
        ) -> read_schema:
            record = session.get(schema, id)
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"{schema.__name__} not found"
                )
            session.delete(record)
            session.commit()
            return {"ok": True}

        return route
