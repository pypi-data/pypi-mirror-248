from copy import deepcopy
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, params
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from fastapi.types import DecoratedCallable, IncEx
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Lifespan

from .builder import BaseCRUDRouteBuilder, InMemoryCRUDRouteBuilder

ACTION_SETS: set = {"create", "list", "retrieve", "update", "delete"}


class CrudApiRouter(APIRouter):
    """
    `CrudApiRouter` class, used to create CRUD operations more faster and works
    as an `APIRouter` in `FastAPI` app.


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
    )

    app.include_router(router)
    ```
    """

    def __init__(
        self,
        schema: Type,
        prefix: str = "",
        create_schema: Optional[Type] = None,
        read_schema: Optional[Type] = None,
        update_schema: Optional[Type] = None,
        actions: set = ACTION_SETS,
        api_handler_builder: BaseCRUDRouteBuilder = InMemoryCRUDRouteBuilder(),
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        lifespan: Optional[Lifespan[Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ):
        self.actions = actions
        self.schema = schema
        self.create_schema = create_schema or schema
        self.read_schema = read_schema or schema
        self.update_schema = update_schema or schema
        self.api_handler_builder = api_handler_builder
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )
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
                endpoint=self.api_handler_builder.list(
                    self.schema,
                    self.read_schema,
                ),
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
                endpoint=self.api_handler_builder.delete(
                    self.schema,
                    self.read_schema,
                ),
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
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_related_routes(path=self.prefix + path, methods=set("GET"))
        return super().get(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def post(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_related_routes(path=self.prefix + path, methods=set("POST"))
        return super().post(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def patch(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_related_routes(path=self.prefix + path, methods=set("PATCH"))
        return super().patch(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def put(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_related_routes(path=self.prefix + path, methods=set("PUT"))
        return super().put(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def delete(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_related_routes(path=self.prefix + path, methods=set("DELETE"))
        return super().delete(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
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
