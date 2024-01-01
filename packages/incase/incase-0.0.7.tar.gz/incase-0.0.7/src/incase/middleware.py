import json
import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from incase import Case, Caseless

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class MaybeJsonAsyncIterator:
    """This is used to wrap the iterable body of the streaming response
    so that the json keys can be handled when the iterable is called.
    """

    def __init__(self):
        self._iterable = []
        self.length = 0

    async def ingest_body_iterable(self, base_iterable):
        async for part in base_iterable:
            try:
                json_content = json.loads(part)
                new_part = json.dumps(
                    {
                        Caseless(key)[Case.CAMEL]: value
                        for key, value in json_content.items()
                    }
                ).encode(encoding="utf-8")
                self.length += len(new_part)
                self._iterable.append(new_part)
            except json.JSONDecodeError:
                self.length += len(part)
                self._iterable.append(part)

    def __aiter__(self):
        return self

    async def __anext__(self):
        for item in self._iterable:
            return item
        raise StopAsyncIteration


class JSONCaseTranslatorMiddleware(BaseHTTPMiddleware):
    """This middleware translates the case of json keys recieved and sent by the
    asgi app. It is helpful for allowing a python back-end to use snake_case
    while allowing a javascript front end to use camelCase."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            data = await request.body()
            request._body = json.dumps(
                {
                    Caseless(key)[Case.SNAKE]: value
                    for key, value in json.loads(data).items()
                }
            ).encode(encoding="utf-8")
            request.content_length = len(request._body)
        except json.JSONDecodeError:
            pass  # guess it wasn't json
        response = await call_next(request)
        if response.headers.get("content-type") == "application/json":
            new_body = MaybeJsonAsyncIterator()
            await new_body.ingest_body_iterable(response.body_iterator)
            response.body_iterator = new_body
        return response