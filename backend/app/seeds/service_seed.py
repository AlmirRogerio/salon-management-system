from decimal import Decimal

from app.models import Service

SERVICES = [
    {
        "name": "Corte de Cabelo",
        "description": "Corte feminino com finalizacao.",
        "price": Decimal("50.00"),
        "duration_minutes": 45,
    },
    {
        "name": "Escova",
        "description": "Escova modeladora para todos os tipos de cabelo.",
        "price": Decimal("40.00"),
        "duration_minutes": 40,
    },
    {
        "name": "Hidratacao",
        "description": "Tratamento de hidratacao profunda dos fios.",
        "price": Decimal("70.00"),
        "duration_minutes": 60,
    },
    {
        "name": "Coloracao",
        "description": "Coloracao completa com produtos profissionais.",
        "price": Decimal("120.00"),
        "duration_minutes": 90,
    },
    {
        "name": "Luzes",
        "description": "Mechas e luzes para iluminar os cabelos.",
        "price": Decimal("180.00"),
        "duration_minutes": 120,
    },
    {
        "name": "Progressiva",
        "description": "Alisamento e reducao de volume dos fios.",
        "price": Decimal("200.00"),
        "duration_minutes": 150,
    },
    {
        "name": "Penteado",
        "description": "Penteado para eventos e ocasioes especiais.",
        "price": Decimal("90.00"),
        "duration_minutes": 60,
    },
]


async def seed_services() -> None:
    for data in SERVICES:
        await Service.get_or_create(
            name=data["name"],
            defaults={
                "description": data["description"],
                "price": data["price"],
                "duration_minutes": data["duration_minutes"],
                "active": True,
            },
        )
