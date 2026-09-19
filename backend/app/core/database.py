from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

MODELS_MODULES = ["app.models"]

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        }
    },
}


def init_db(app) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
