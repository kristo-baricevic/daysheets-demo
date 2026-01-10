from django.core.management.base import BaseCommand
from core.models import Tour, Venue, Day, Group, Person, ScheduleEvent, Contact, Note
from datetime import date, time


class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        Tour.objects.all().delete()
        Venue.objects.all().delete()

        tour = Tour.objects.create(name="Bob Marley Hologram", subtitle="World Tour: West Coast")

        forum = Venue.objects.create(
            name="The Kia Forum",
            address1="3900 W Manchester Blvd",
            city="Inglewood",
            state="CA",
            postal="90305",
        )

        d1 = Day.objects.create(tour=tour, date=date(2026, 1, 8), day_type="off", city="Los Angeles", state="CA", venue=forum, tz="America/Los_Angeles")
        d2 = Day.objects.create(tour=tour, date=date(2026, 1, 9), day_type="show", city="Inglewood", state="CA", venue=forum, tz="America/Los_Angeles")

        g1 = Group.objects.create(tour=tour, name="Artist Party")
        g2 = Group.objects.create(tour=tour, name="Band Party")

        Person.objects.create(tour=tour, name="Emily Taylor", role_title="Photographer", email="emily@example.com", phone="+44 20 7946 1423", group=g1, permission="read", connected=True)
        Person.objects.create(tour=tour, name="Frankie Davis", role_title="Tour Manager", email="frankie@example.com", phone="610-608-1173", group=g2, permission="owner", connected=True)

        ScheduleEvent.objects.create(day=d2, name="Bus Call for Venue", start_local=time(6, 0), status="done", associations=[{"type": "group", "id": str(g2.id)}])
        ScheduleEvent.objects.create(day=d2, name="Load In", start_local=time(7, 0), status="todo", associations=[{"type": "group", "id": str(g2.id)}])
        ScheduleEvent.objects.create(day=d2, name="Sound Check", start_local=time(16, 0), status="todo", associations=[{"type": "group", "id": str(g2.id)}])
        ScheduleEvent.objects.create(day=d2, name="Doors", start_local=time(19, 0), status="todo", associations=[])
        ScheduleEvent.objects.create(day=d2, name="BB ON STAGE", start_local=time(21, 0), end_local=time(22, 30), status="todo", associations=[])
        ScheduleEvent.objects.create(day=d2, name="Load Out", start_local=time(22, 30), status="todo", associations=[{"type": "group", "id": str(g2.id)}])

        Contact.objects.create(day=d2, name="Dustin Francis", role="Runner", phone="(310) 555-0789")
        Contact.objects.create(day=d2, name="Nancy Wright", role="Local PM", phone="(310) 555-1259", email="nancy@example.com")

        Note.objects.create(day=d2, title="Crew Notes", body="First show today. Buses depart at 6:00 AM. Breakfast will be up.", last_edited_by="Frankie Davis")

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
