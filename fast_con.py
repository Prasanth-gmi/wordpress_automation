from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WordPress Automation",
        version="1.0.0",
        description="The project is designed for automating various tasks in WordPress using the REST API with JWT token authentication. It handles the creation, editing, and deletion of both posts and pages, ensuring efficient content management. Additionally, the project includes functionality for creating custom WordPress themes, streamlining the process for developers. This automation enhances productivity and consistency in managing WordPress sites.",
        routes=app.routes,
    )
    # Remove the `components` section that includes schemas
    openapi_schema.pop("components", None)
    app.openapi_schema = openapi_schema
    return app.openapi_schema