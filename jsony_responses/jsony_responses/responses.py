import json
import typing

import jsony
from starlette.responses import JSONResponse


class JSONYResponse(JSONResponse):
    """
    Расширение класса `JSONResponse` из библиотеки `Starlette`, которое использует кастомный сериализатор
    `JSONYEncoder` из библиотеки `jsony` для преобразования данных в JSON.

    Пример использования:
        ```python
        from fastapi import FastAPI
        from mymodule import JSONYResponse

        app = FastAPI()

        @app.get("/data", response_class=JSONYResponse)
        async def get_data():
            return {"message": "Hello, World!", "status": "success"}
        ```
    """

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=jsony.JSONYEncoder,
        ).encode("utf-8")
