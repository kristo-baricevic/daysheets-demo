from django.core.management.base import BaseCommand
from core.models import Hotel

HOTEL_CHAINS = [
    "Marriott",
    "Courtyard by Marriott",
    "Residence Inn",
    "Hilton",
    "DoubleTree",
    "Hyatt",
    "Hyatt Place",
    "Hyatt Regency",
    "Sheraton",
    "Westin",
    "Four Seasons",
    "Ritz-Carlton",
    "Holiday Inn",
    "Holiday Inn Express",
    "Kimpton",
    "W Hotels",
    "Aloft",
    "Fairmont",
    "Best Western",
    "Omni",
]

CITIES = [
    ("New York", "NY"),
    ("Los Angeles", "CA"),
    ("Chicago", "IL"),
    ("San Francisco", "CA"),
    ("Seattle", "WA"),
    ("Austin", "TX"),
    ("Nashville", "TN"),
    ("Atlanta", "GA"),
    ("Boston", "MA"),
    ("Denver", "CO"),
    ("Portland", "OR"),
    ("San Diego", "CA"),
    ("Las Vegas", "NV"),
    ("Phoenix", "AZ"),
    ("Dallas", "TX"),
    ("Houston", "TX"),
    ("Miami", "FL"),
    ("Orlando", "FL"),
    ("New Orleans", "LA"),
    ("Minneapolis", "MN"),
]

class Command(BaseCommand):
    help = "Seed fake hotel data for development"

    def handle(self, *args, **options):
        created = 0

        for city, state in CITIES:
            for chain in HOTEL_CHAINS:
                name = f"{chain} {city}"

                if Hotel.objects.filter(name=name, city=city, state=state).exists():
                    continue

                Hotel.objects.create(
                    name=name,
                    address1=f"123 {city} Ave",
                    city=city,
                    state=state,
                    postal="00000",
                    source="seed",
                )

                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} hotels"))
