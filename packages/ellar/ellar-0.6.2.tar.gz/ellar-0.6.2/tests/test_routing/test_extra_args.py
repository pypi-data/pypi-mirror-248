from functools import wraps

from ellar.common import IExecutionContext, Inject, Query, extra_args, get
from ellar.common.params import ExtraEndpointArg
from ellar.common.serializer import serialize_object
from ellar.core.connection import Request
from ellar.openapi import OpenAPIDocumentBuilder
from ellar.testing import Test
from starlette.responses import Response

from .sample import Filter

tm = Test.create_test_module()
app = tm.create_application()


def add_additional_signature_to_endpoint(func):
    # EXTRA ARGS SETUP
    query1 = ExtraEndpointArg(name="query1", annotation=str, default_value=Query())
    query2 = ExtraEndpointArg(
        name="query2", annotation=str
    )  # will default to Query during computation

    extra_args(query1, query2)(func)

    @wraps(func)
    def _wrapper(*args, **kwargs):
        # RESOLVING EXTRA ARGS
        # All extra args must be resolved before calling route function
        # else extra argument will be pushed to the route function
        resolved_query1 = query1.resolve(kwargs)
        resolved_query2 = query2.resolve(kwargs)

        response = func(*args, **kwargs)
        response.update(query1=resolved_query1, query2=resolved_query2)
        return response

    return _wrapper


def add_extra_non_field_extra_args(func):
    # EXTRA ARGS SETUP
    context = ExtraEndpointArg(
        name="context", annotation=Inject[IExecutionContext], default_value=None
    )
    response = ExtraEndpointArg(
        name="response", annotation=Inject[Response], default_value=None
    )

    extra_args(response)(func)
    extra_args(context)(func)

    @wraps(func)
    def _wrapper(*args, **kwargs):
        # RESOLVING EXTRA ARGS
        resolved_context = context.resolve(kwargs)
        resolved_response = response.resolve(kwargs)
        assert isinstance(resolved_response, Response)
        assert isinstance(resolved_context, IExecutionContext)

        return func(*args, **kwargs)

    return _wrapper


@get("/test")
@add_extra_non_field_extra_args
@add_additional_signature_to_endpoint
def query_params_extra(
    request: Inject[Request],
    filters: Filter = Query(),
):
    return filters.dict()


app.router.append(query_params_extra)

openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "Ellar API Docs", "version": "1.0.0"},
    "paths": {
        "/test": {
            "get": {
                "operationId": "query_params_extra_test_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "type": "string",
                            "format": "date-time",
                            "title": "To",
                            "repr": True,
                        },
                        "name": "to",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {
                            "type": "string",
                            "format": "date-time",
                            "title": "From",
                            "repr": True,
                        },
                        "name": "from",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {
                            "allOf": [{"$ref": "#/components/schemas/Range"}],
                            "title": "Range",
                            "default": 20,
                            "repr": True,
                        },
                        "name": "range",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"type": "string", "title": "Query1"},
                        "name": "query1",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"type": "string", "title": "Query2"},
                        "name": "query2",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object", "title": "Response Model"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "type": "array",
                        "title": "Details",
                    }
                },
                "type": "object",
                "required": ["detail"],
                "title": "HTTPValidationError",
            },
            "Range": {"type": "integer", "enum": [20, 50, 200], "title": "Range"},
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"type": "string"},
                        "type": "array",
                        "title": "Location",
                    },
                    "msg": {"type": "string", "title": "Message"},
                    "type": {"type": "string", "title": "Error Type"},
                },
                "type": "object",
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
            },
        }
    },
    "tags": [],
}


def test_openapi_schema():
    document = serialize_object(OpenAPIDocumentBuilder().build_document(app))
    assert document == openapi_schema


def test_query_params_extra():
    client = tm.get_test_client()
    response = client.get(
        "/test?from=1&to=2&range=20&foo=1&range2=50&query1=somequery1&query2=somequery2"
    )
    assert response.json() == {
        "to_datetime": "1970-01-01T00:00:02Z",
        "from_datetime": "1970-01-01T00:00:01Z",
        "range": 20,
        "query1": "somequery1",
        "query2": "somequery2",
    }

    response = client.get("/test?from=1&to=2&range=20&foo=1&range2=50")
    assert response.status_code == 422
