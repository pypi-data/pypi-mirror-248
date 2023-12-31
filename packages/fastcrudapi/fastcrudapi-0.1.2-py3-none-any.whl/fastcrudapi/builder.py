from typing import List

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select


class BaseCRUDRouteBuilder:
    def create(self, schema, read_schema, create_schema):
        def route(data: create_schema) -> read_schema:
            return read_schema(**data.dict())

        return route

    def list(self, schema, read_schema):
        def route() -> List[read_schema]:
            return []

        return route

    def retrieve(self, schema, read_schema):
        def route(id: int | str) -> read_schema:
            return {}

        return route

    def update(self, schema, read_schema, update_schema):
        def route(data: update_schema) -> read_schema:
            return schema(**data.dict())

        return route

    def delete(self, schema, read_schema):
        def route(id: int | str) -> read_schema:
            return {}

        return route


class InMemoryCRUDRouteBuilder(BaseCRUDRouteBuilder):
    pass


class SqlCRUDRouteBuilder(BaseCRUDRouteBuilder):
    def __init__(self, engine) -> None:
        super().__init__()
        self.engine = engine

    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def create(self, schema, read_schema, create_schema):
        def route(
            data: create_schema, session: Session = Depends(self.get_session)
        ) -> read_schema:
            db_data = schema.model_validate(data)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data

        return route

    def list(self, schema, read_schema):
        def route(
            session: Session = Depends(self.get_session),
            offset: int = 0,
            limit: int = Query(default=100, le=100),
        ) -> List[read_schema]:
            return session.exec(select(schema).offset(offset).limit(limit)).all()

        return route

    def retrieve(self, schema, read_schema):
        def route(
            id: int | str, session: Session = Depends(self.get_session)
        ) -> read_schema:
            record = session.get(schema, id)
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"{schema.__name__} not found"
                )
            return record

        return route

    def update(self, schema, read_schema, update_schema):
        def route(
            id: int, data: update_schema, session: Session = Depends(self.get_session)
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

    def delete(self, schema, read_schema):
        def route(
            id: int | str, session: Session = Depends(self.get_session)
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
