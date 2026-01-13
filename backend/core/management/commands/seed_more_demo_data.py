from django.core.management.base import BaseCommand
from core.models import Tour, Venue, Day, Group, Person, ScheduleEvent, Contact, Note
from datetime import date, time


class Command(BaseCommand):
    help = "Append additional demo tour stops and people"

    def handle(self, *args, **kwargs):
        tour = Tour.objects.filter(name="Bob Marley Hologram").first()

        if not tour:
            self.stdout.write(self.style.ERROR("Tour not found. Run original seed first."))
            return

        # Existing groups
        artist_party = Group.objects.get(tour=tour, name="Artist Party")
        band_party = Group.objects.get(tour=tour, name="Band Party")

        # New venues
        chase = Venue.objects.create(
            name="Chase Center",
            address1="1 Warriors Way",
            city="San Francisco",
            state="CA",
            postal="94158",
        )

        moda = Venue.objects.create(
            name="Moda Center",
            address1="1 N Center Ct St",
            city="Portland",
            state="OR",
            postal="97227",
        )

        # New days
        sf_day = Day.objects.create(
            tour=tour,
            date=date(2026, 1, 11),
            day_type="show",
            city="San Francisco",
            state="CA",
            venue=chase,
            tz="America/Los_Angeles",
        )

        portland_day = Day.objects.create(
            tour=tour,
            date=date(2026, 1, 13),
            day_type="show",
            city="Portland",
            state="OR",
            venue=moda,
            tz="America/Los_Angeles",
        )

        # More people
        Person.objects.create(
            tour=tour,
            name="Lena Morales",
            role_title="Lighting Director",
            email="lena@example.com",
            phone="415-555-3381",
            group=band_party,
            permission="edit",
            connected=True,
        )

        Person.objects.create(
            tour=tour,
            name="Jordan Kim",
            role_title="Merch Manager",
            email="jordan@example.com",
            phone="503-555-9912",
            group=artist_party,
            permission="read",
            connected=True,
        )

        # SF schedule
        ScheduleEvent.objects.create(
            day=sf_day,
            name="Bus Call",
            start_local=time(7, 0),
            status="todo",
            associations=[{"type": "group", "id": str(band_party.id)}],
        )

        ScheduleEvent.objects.create(
            day=sf_day,
            name="Show Time",
            start_local=time(20, 30),
            end_local=time(22, 0),
            status="todo",
            associations=[],
        )

        # Portland schedule
        ScheduleEvent.objects.create(
            day=portland_day,
            name="Load In",
            start_local=time(8, 0),
            status="todo",
            associations=[{"type": "group", "id": str(band_party.id)}],
        )

        ScheduleEvent.objects.create(
            day=portland_day,
            name="Show Time",
            start_local=time(20, 0),
            end_local=time(21, 45),
            status="todo",
            associations=[],
        )

        # Notes
        Note.objects.create(
            day=sf_day,
            title="SF Notes",
            body="Venue curfew is strict. Merch cut at 10:15 PM.",
            last_edited_by="Tour Manager",
        )

        Note.objects.create(
            day=portland_day,
            title="Portland Notes",
            body="Rain expected. Load-in dock can flood.",
            last_edited_by="Tour Manager",
        )

        self.stdout.write(self.style.SUCCESS("Appended demo tour stops and people."))
