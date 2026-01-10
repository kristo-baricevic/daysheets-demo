from rest_framework import serializers
from core.models import Tour, Day, Venue, ScheduleEvent, Contact, Note, Group, Person


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id", "name", "subtitle"]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "address1", "city", "state", "postal"]


class DaySerializer(serializers.ModelSerializer):
    tourId = serializers.UUIDField(source="tour_id", read_only=True)
    venueId = serializers.UUIDField(source="venue_id", read_only=True)
    dateISO = serializers.SerializerMethodField()
    dayType = serializers.CharField(source="day_type")

    class Meta:
        model = Day
        fields = ["id", "tourId", "dateISO", "dayType", "city", "state", "venueId", "tz"]

    def get_dateISO(self, obj: Day) -> str:
        return obj.date.isoformat()


class ScheduleEventSerializer(serializers.ModelSerializer):
    dayId = serializers.UUIDField(source="day_id", read_only=True)
    startLocal = serializers.TimeField(source="start_local", allow_null=True, required=False)
    endLocal = serializers.TimeField(source="end_local", allow_null=True, required=False)

    class Meta:
        model = ScheduleEvent
        fields = ["id", "dayId", "name", "startLocal", "endLocal", "status", "associations", "notes"]


class ContactSerializer(serializers.ModelSerializer):
    dayId = serializers.UUIDField(source="day_id", read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "dayId", "name", "role", "phone", "email"]


class NoteSerializer(serializers.ModelSerializer):
    dayId = serializers.UUIDField(source="day_id", read_only=True)
    lastEditedBy = serializers.CharField(source="last_edited_by")
    lastEditedAtISO = serializers.DateTimeField(source="last_edited_at")

    class Meta:
        model = Note
        fields = ["id", "dayId", "title", "body", "lastEditedBy", "lastEditedAtISO"]


class GroupSerializer(serializers.ModelSerializer):
    tourId = serializers.UUIDField(source="tour_id", read_only=True)

    class Meta:
        model = Group
        fields = ["id", "tourId", "name"]


class PersonSerializer(serializers.ModelSerializer):
    tourId = serializers.UUIDField(source="tour_id", read_only=True)
    roleTitle = serializers.CharField(source="role_title")
    groupId = serializers.UUIDField(source="group_id", allow_null=True, required=False)

    class Meta:
        model = Person
        fields = ["id", "tourId", "name", "roleTitle", "email", "phone", "groupId", "permission", "connected"]


class PersonWriteSerializer(serializers.ModelSerializer):
    roleTitle = serializers.CharField(source="role_title", required=False, allow_blank=True)
    groupId = serializers.UUIDField(source="group_id", allow_null=True, required=False)

    class Meta:
        model = Person
        fields = ["name", "roleTitle", "email", "phone", "groupId", "permission", "connected"]
