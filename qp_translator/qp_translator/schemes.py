from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Filter(BaseModel, Generic[T]):
    """
    Класс фильтра для параметров запроса.

    Этот класс позволяет создавать фильтры для параметров запроса в API. Он включает
    функции для парсинга значений, применения условий фильтрации и определения,
    является ли фильтр обязательным.

    Attrs:
        q_func (Callable[[T | list[T]], dict[str, Any]]): Функция для преобразования
            значений фильтра в словарь для запроса к базе данных.
        t_parser (Callable[[str], T | list[T]]): Функция для преобразования строки
            в нужный тип данных.
        many (bool): Если True, фильтр может принимать список значений.
        exclusions (list[str]): Список фильтров, которые исключают текущий фильтр.
        is_required (bool): Если True, фильтр обязателен.
        description (str | None): Описание фильтра.

    Example:
        class RequestFilter(DocumentFilter):
            __filters__ = {
                "provider_id": Filter[PydanticObjectId](
                    q_func=lambda x: {"provider_id": x},
                    t_parser=StandartParser.get_type_parser(PydanticObjectId),
                    many=True,
                    exclusions=["position_id"],
                ),
            }
    """

    q_func: Callable[[T | list[T]], dict[str, Any]] = Field(
        title="Функция, возвращающая словарь для запроса к базе данных",
    )
    t_parser: Callable[[str], T | list[T]] = Field(
        default=lambda x: x,
        title="Функция для преобразования строки в нужный тип данных",
    )
    many: bool = Field(
        default=False,
        title="Определяет, может ли фильтр принимать список значений",
    )
    exclusions: list[str] = Field(
        default_factory=list,
        title="Список ключей фильтров, которые исключают текущий фильтр",
    )
    is_required: bool = Field(
        default=False,
        title="Если фильтр обязателен",
    )
    description: str | None = Field(
        default=None,
        title="Описание фильтра",
    )


class ParseResult(BaseModel):
    """
    Модель результата парсинга параметров запроса.

    Этот класс используется для хранения информации о фильтрах, полученных
    из параметров запроса API. Он также включает информацию о сортировке,
    лимите и смещении (пагинации).

    Attrs:
        query_list (list[dict[str, Any]]): Список фильтров, полученных из параметров запроса.
        sort (list[str]): Список ключей сортировки, указанных в запросе.
        limit (int | None): Лимит на количество возвращаемых результатов.
        offset (int | None): Смещение для пагинации результатов.
    """

    query_list: list[dict[str, Any]] = Field(
        default_factory=list,
        title="Список фильтров, полученных из параметров запроса",
    )
    sort: list[str] = Field(
        default_factory=list,
        title="Ключи сортировки, указанные в запросе",
    )
    limit: int | None = Field(
        default=None,
        title="Лимит на количество возвращаемых результатов",
    )
    offset: int | None = Field(
        default=None,
        title="Смещение для пагинации результатов",
    )
