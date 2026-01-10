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

    class Meta:
        indexes = [
            models.Index(fields=["tour", "date"]),
        ]
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.tour.name} {self.date.isoformat()}"


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=128)

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

    class Meta:
        ordering = ["-last_edited_at"]

    def __str__(self) -> str:
        return self.title
