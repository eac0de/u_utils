from jinja2 import Environment, FileSystemLoader, select_autoescape

_DEFAULT_TEMPLATES_PATH = "templates"
"""
str: Путь по умолчанию к директории с шаблонами.
"""
_env = Environment(
    loader=FileSystemLoader(_DEFAULT_TEMPLATES_PATH),
    autoescape=select_autoescape(["html", "xml"]),
    enable_async=True,
)
"""
Environment: Глобальное окружение Jinja2 для рендера шаблонов. 
Изначально настроено на использование директории `_DEFAULT_TEMPLATES_PATH`.
"""


class TemplateRenderer:
    """
    Класс для асинхронного рендера шаблонов с использованием Jinja2.

    Methods:
        render_template(template_name: str, context: dict) -> str:
            Асинхронно рендерит указанный шаблон с заданным контекстом.
    """

    @staticmethod
    async def render(template_name: str, context: dict) -> str:
        """
        Асинхронно рендерит шаблон с указанным контекстом.

        Args:
            template_name (str): Имя файла шаблона, который нужно отрендерить.
            context (dict): Словарь с данными, которые будут использоваться в шаблоне.

        Returns:
            str: Рендеренный HTML-код.

        Raises:
            TemplateNotFound: Если указанный шаблон не найден.
            TemplateError: Если произошла ошибка во время рендера шаблона.
        """
        template = _env.get_template(template_name)
        return await template.render_async(context)


async def config_template_renderer(templates_path: str | None = None):
    """
    Настраивает глобальное окружение Jinja2 с использованием указанного пути к шаблонам.

    Функция должна быть вызвана один раз при старте приложения, если требуется использовать
    директорию шаблонов, отличную от значения по умолчанию (`_DEFAULT_TEMPLATES_PATH`).

    Args:
        templates_path (str | None): Путь к директории с шаблонами.
                                     Если не указан, используется `_DEFAULT_TEMPLATES_PATH`.

    Raises:
        OSError: Если директория с шаблонами недоступна или недействительна.
    """
    if not templates_path:
        templates_path = _DEFAULT_TEMPLATES_PATH
    global _env
    _env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=True,
    )
