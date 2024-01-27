import typing

from starlette import status
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


class JSONResponse404(JSONResponse):
    def __init__(self,
                 content: typing.Any,
                 headers: typing.Optional[typing.Mapping[str, str]] = None,
                 media_type: typing.Optional[str] = None,
                 background: typing.Optional[BackgroundTask] = None
                 ) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(content, status_code, headers, media_type, background)
