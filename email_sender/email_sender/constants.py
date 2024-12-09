from enum import Enum


class MailBodyType(str, Enum):
    """
    Перечисление для определения типа тела письма.

    Attributes:
        PLAIN: Обычный текст.
        HTML: HTML формат.
    """

    PLAIN = "plain"
    HTML = "html"
