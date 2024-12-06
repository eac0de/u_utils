from collections.abc import Iterable
from enum import Enum
from typing import Any

from starlette import status
from starlette.datastructures import QueryParams
from starlette.exceptions import HTTPException

from qp_translator.schemes import Filter, ParseResult


class QPTranslatorMetaclass(type):

    def __new__(
        cls,
        name: str,
        bases: tuple,
        namespace: dict[str, Any],
    ):
        filters: dict[str, Filter] = {}
        required_filter_set: set[str] = set()
        for base in bases:
            if hasattr(base, "__filters__"):
                filters.update(getattr(base, "__filters__", {}).copy())
        filters.update(namespace.get("__filters__", {}))
        required_filter_set.update(
            [n for n, f in namespace.get("__filters__", {}).items() if f.is_required]
        )
        namespace["__filters__"] = filters
        namespace["__required_filter_set__"] = required_filter_set
        namespace["__docs__"] = ""
        if namespace["__filters__"]:

            def filter_info(f: Filter):
                """Функция для извлечения информации о фильтре."""
                type_info = f.__pydantic_generic_metadata__["args"][0]  # type: ignore
                if issubclass(type_info, Enum):  # Проверяем, является ли тип Enum
                    enum_values = ", ".join(
                        [e.value for e in type_info]
                    )  # Получаем имена всех значений Enum
                    type_info = f"{type_info.__bases__[0].__name__ }({enum_values})"
                else:
                    type_info = type_info.__name__
                return f"{f.description + '<br><br>' if f.description else ''}**ValueType:** {type_info}<br>**Many:** {f.many}<br>**Is Required:** {f.is_required}{'<br>**Exclusions:** ' + ', '.join(f.exclusions) if f.exclusions else ''}"

            namespace["__docs__"] = "<h2>Filters:</h2>" + "<br>".join(
                f"<br><h3>{n}</h3>{filter_info(f)}"
                for n, f in namespace["__filters__"].items()
            )
        return super().__new__(cls, name, bases, namespace)


class QPTranslator(metaclass=QPTranslatorMetaclass):

    __filters__: dict[str, Filter[Any]] = {}
    __required_filter_set__: set[str] = set()
    __docs__: str = ""

    @classmethod
    async def parse(cls, qps: QueryParams) -> ParseResult:

        limit = qps.get("limit")
        offset = qps.get("offset")
        filter_params = ParseResult(
            limit=int(limit) if limit and limit.isdigit() else None,
            offset=int(offset) if offset and offset.isdigit() else None,
            sort=qps.getlist("sort_by"),
        )
        query: dict[str, dict[str, Any]] = {}
        qp_keys = qps.keys()
        invalid_qps = set()
        for param in qp_keys:
            if param in ["limit", "offset", "sort_by"] or param in query:
                continue
            f = cls.__filters__.get(param)
            if not f:
                invalid_qps.add(param)
                continue
            for exclusion in f.exclusions:
                if exclusion in qp_keys:
                    query[param] = {}
                    break
            else:
                try:
                    if f.many:
                        value = [f.t_parser(p) for p in qps.getlist(param)]
                    else:
                        value = f.t_parser(qps.get(param))  # type: ignore
                except ValueError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=str(e),
                    ) from e
                except Exception as e:
                    raise Warning("t_parser can only raise a ValueError") from e
                query[param] = f.q_func(value)
        if invalid_qps:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Invalid query params: {", ".join(invalid_qps)}',
            )
        await cls._check_required_filters(query.keys())
        filter_params.query_list = list(query.values())
        return filter_params

    @classmethod
    async def _check_required_filters(cls, existing_filters: Iterable[str]):
        if not cls.__required_filter_set__:
            return
        if undefined_required_filters := cls.__required_filter_set__ - set(
            existing_filters
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required query params: {', '.join(undefined_required_filters)}",
            )

    @classmethod
    def get_docs(cls) -> str:
        return cls.__docs__
