from copy import deepcopy
from typing import Any, Callable, List, Optional, Type

from fastapi import APIRouter
from typing_extensions import Annotated, Doc

from .builder import BaseCRUDRouteBuilder, InMemoryCRUDRouteBuilder


class CrudApiRouter(APIRouter):
    def __init__(
        self,
        schema: Type,
        prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
        create_schema: Optional[Type] = None,
        read_schema: Optional[Type] = None,
        update_schema: Optional[Type] = None,
        actions: set = {"create", "list", "retrieve", "update", "delete"},
        api_handler_builder: BaseCRUDRouteBuilder = InMemoryCRUDRouteBuilder(),
        pagination=None,
        *args,
        **kwargs,
    ):
        self.actions = actions
        self.schema = schema
        self.create_schema = create_schema or schema
        self.read_schema = read_schema or schema
        self.update_schema = update_schema or schema
        self.api_handler_builder = api_handler_builder
        super().__init__(prefix=prefix, *args, **kwargs)
        self._refresh_api_routes()

    def _refresh_api_routes(self):
        self.routes = []
        if "create" in self.actions:
            self._add_api_action_route(
                endpoint=self.api_handler_builder.create(
                    self.schema, self.read_schema, self.create_schema
                ),
                path="",
                name=f"Create new {self.schema.__name__.lower()}",
                methods=["POST"],
                status_code=201,
                response_model=self.schema,
            )

        if "list" in self.actions:
            self._add_api_action_route(
                endpoint=self.api_handler_builder.list(self.schema, self.read_schema),
                path="",
                name=f"List all {self.schema.__name__.lower()}",
                methods=["GET"],
                status_code=200,
                response_model=List[self.schema],
            )
        if "retrieve" in self.actions:
            self._add_api_action_route(
                endpoint=self.api_handler_builder.retrieve(
                    self.schema, self.read_schema
                ),
                path="/:id",
                name=f"Retrieve {self.schema.__name__.lower()} by id",
                methods=["GET"],
                status_code=200,
                response_model=self.schema,
            )
        if "update" in self.actions:
            self._add_api_action_route(
                endpoint=self.api_handler_builder.update(
                    self.schema, self.read_schema, self.update_schema
                ),
                path="/:id",
                name=f"Update {self.schema.__name__.lower()} by id",
                methods=["PUT"],
                status_code=200,
                response_model=self.schema,
            )
        if "delete" in self.actions:
            self._add_api_action_route(
                endpoint=self.api_handler_builder.delete(self.schema, self.read_schema),
                path="/:id",
                name=f"Update {self.schema.__name__.lower()} by id",
                methods=["DELETE"],
                status_code=200,
                response_model=self.schema,
            )

    def _add_api_action_route(
        self,
        endpoint: Callable,
        path: str,
        name: str,
        methods: List[str],
        status_code: int,
        response_model: Type,
    ):
        self.add_api_route(
            path=path,
            name=name,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            methods=methods,
        )

    def update_api_handler_builder(self, api_handler_builder):
        self.api_handler_builder = api_handler_builder
        self._refresh_api_routes()
        return self

    def get(
        self,
        path: str,
        *args,
        **kargs,
    ):
        self._remove_related_routes(path=self.prefix + path, methods=set(["GET"]))
        return super().get(
            path=path,
            *args,
            **kargs,
        )

    def _remove_related_routes(self, path: str, methods: set[str]):
        related_routes = filter(
            lambda route: route.path == path and (route.methods & methods != set()),
            self.routes,
        )
        for related_route in list(related_routes):
            cloned_route = deepcopy(related_route)
            cloned_route.methods -= methods
            self.routes.remove(related_route)
            if len(cloned_route.methods) > 0:
                self.routes.append(cloned_route)

    @property
    def create_route(self):
        return self.api_handler_builder.create(
            schema=self.schema, create_schema=self.create_schema
        )

    @property
    def list_route(self):
        return self.api_handler_builder.list(
            schema=self.schema, read_schema=self.read_schema
        )

    @property
    def retrieve_route(self):
        return self.api_handler_builder.retrieve(
            schema=self.schema, read_schema=self.read_schema
        )

    @property
    def update_route(self):
        return self.api_handler_builder.retrieve(
            schema=self.schema, read_schema=self.read_schema
        )

    @property
    def delete_route(self):
        return self.api_handler_builder.retrieve(
            schema=self.schema, read_schema=self.read_schema
        )
