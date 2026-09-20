import asyncio

from tortoise import Tortoise

from app.core.database import TORTOISE_ORM
from app.seeds.admin_seed import seed_admin
from app.seeds.business_hours_seed import seed_business_hours
from app.seeds.service_seed import seed_services

SEEDS = [seed_admin, seed_services, seed_business_hours]


async def run_seeds() -> None:
    for seed in SEEDS:
        await seed()


async def main() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    try:
        await run_seeds()
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
