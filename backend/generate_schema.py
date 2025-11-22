import sys
import os
import json
from fastapi.openapi.utils import get_openapi

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.main import app

def generate_schema():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    with open('backend/openapi.json', 'w') as f:
        json.dump(openapi_schema, f, indent=2)
    print("OpenAPI schema generated at backend/openapi.json")

if __name__ == "__main__":
    generate_schema()
