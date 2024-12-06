from collections.abc import Callable
from datetime import datetime
from typing import TypeVar

T = TypeVar("T")


def datetime_parser(v: str) -> datetime:
    """
    Парсер даты и времени.

    Args:
        v (str): Дата и время в ISO формате.

    Raises:
        ValueError: При неверном формате даты и времени.

    Returns:
        datetime: Результат парсинга.
    """
    try:
        return datetime.fromisoformat(v)
    except Exception as e:
        raise ValueError("Field with date must be in ISO format") from e


def bool_parser(v: str) -> bool:
    """
    Парсер булевых значений.

    Args:
        v (str): 'false' или 'true' в строковом формате.

    Raises:
        ValueError: При неверном формате булевого значения.

    Returns:
        bool: Результат парсинга.
    """
    if v not in ["false", "true"]:
        raise ValueError("Field with bool must be 'false' or 'true'")
    return v != "false"


def get_type_parser(_type: type[T]) -> Callable[[str], T]:
    """
    Метод для получения парсера для типовых значений.

    Args:
        _type (type[T]): Тип, для которого требуется парсер.

    Returns:
        Callable[[str], T]: Парсер, который преобразует строку в указанный тип.
    """

    def type_parser(v: str) -> T:
        try:
            return _type(v)  # type: ignore
        except Exception as e:
            raise ValueError(
                f"Value {v} is not correct for type {_type.__name__}"
            ) from e

    return type_parser


def get_enum_parser(enum: type[T]) -> Callable[[str], T]:
    """
    Метод для получения парсера для типовых значений Enum.

    Args:
        enum (Type[T]): Класс Enum, для которого требуется парсер.

    Returns:
        Callable[[str], T]: Парсер, который преобразует строку в элемент Enum.
    """

    def enum_parser(v: str) -> T:
        try:
            return enum(v)  # type: ignore
        except ValueError as e:
            enum_values = ", ".join([e.value for e in enum])  # type: ignore
            type_info = f"{enum.__bases__[0].__name__ }({enum_values})"
            raise ValueError(f"Value '{v}' is not a valid member of {type_info}") from e

    return enum_parser
