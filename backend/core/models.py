from django.db import models

# Create your models here.
import uuid
from django.db import models


class Tour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=64, blank=True, default="")
    postal = models.CharField(max_length=32, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Day(models.Model):
    class DayType(models.TextChoices):
        SHOW = "show", "Show Day"
        TRAVEL = "travel", "Travel Day"
        OFF = "off", "Day Off"
        REHEARSAL = "rehearsal", "Rehearsal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="days")
    date = models.DateField()
    day_type = models.CharField(max_length=16, choices=DayType.choices)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=64, blank=True, default="")
    tz = models.CharField(max_length=64, default="America/Los_Angeles")
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="days")
    aftershow = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["tour", "date"]),
        ]
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.tour.name} {self.date.isoformat()}"


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=32, default="red")

    class Meta:
        unique_together = [("tour", "name")]
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Person(models.Model):
    class Permission(models.TextChoices):
        OWNER = "owner", "owner"
        EDIT = "edit", "edit"
        READ = "read", "read"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="people")
    name = models.CharField(max_length=128)
    role_title = models.CharField(max_length=128, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=64, blank=True, default="")
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, related_name="people")
    permission = models.CharField(max_length=16, choices=Permission.choices, default=Permission.READ)
    connected = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ScheduleEvent(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "todo"
        DONE = "done", "done"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255)
    start_local = models.TimeField(null=True, blank=True)
    end_local = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.TODO)
    associations = models.JSONField(default=list, blank=True)  # [{type:"group"|"person", id:"..."}]
    notes = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["day", "start_local"]),
        ]
        ordering = ["start_local", "name"]

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    phone = models.CharField(max_length=64, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    class Meta:
        ordering = ["role", "name"]

    def __str__(self) -> str:
        return f"{self.role}: {self.name}"


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, default="")
    last_edited_by = models.CharField(max_length=128, blank=True, default="")
    last_edited_at = models.DateTimeField(auto_now=True)
    visibility = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-last_edited_at"]

    def __str__(self) -> str:
        return self.title

class ScheduleTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey("core.Tour", on_delete=models.CASCADE, related_name="schedule_templates")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class ScheduleTemplateEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(ScheduleTemplate, on_delete=models.CASCADE, related_name="events")
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)

    start_local = models.CharField(max_length=5, blank=True, default="")
    end_local = models.CharField(max_length=5, blank=True, default="")

    notes = models.TextField(blank=True, default="")
    associations = models.JSONField(default=list, blank=True)

    start_tz = models.CharField(max_length=64, blank=True, default="")
    end_tz = models.CharField(max_length=64, blank=True, default="")

class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey("core.Tour", null=True, blank=True, on_delete=models.SET_NULL, related_name="hotels")

    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")
    state = models.CharField(max_length=80, blank=True, default="")
    postal = models.CharField(max_length=40, blank=True, default="")

    place_id = models.CharField(max_length=255, blank=True, default="", db_index=True)
    source = models.CharField(max_length=40, blank=True, default="db")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["tour", "name"]),
            models.Index(fields=["place_id"]),
        ]

class DayLodging(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.OneToOneField("core.Day", on_delete=models.CASCADE, related_name="lodging")
    hotel = models.ForeignKey("core.Hotel", on_delete=models.PROTECT, related_name="day_lodgings")

    check_in_iso = models.DateTimeField(null=True, blank=True)
    check_out_iso = models.DateTimeField(null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    updated_at = models.DateTimeField(auto_now=True)


class DayLodgingGuest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lodging = models.ForeignKey("core.DayLodging", on_delete=models.CASCADE, related_name="guests")
    person = models.ForeignKey("core.Person", on_delete=models.CASCADE, related_name="lodging_guests")

    class Meta:
        unique_together = [("lodging", "person")]
        indexes = [models.Index(fields=["lodging", "person"])]
