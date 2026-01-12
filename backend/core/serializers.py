from rest_framework import serializers
from core.models import Tour, Day, Venue, ScheduleEvent, Contact, Note, Group, Person, ScheduleTemplate, ScheduleTemplateEvent

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


class ScheduleTemplateEventSerializer(serializers.ModelSerializer):
    startLocal = serializers.CharField(source="start_local", required=False, allow_blank=True)
    endLocal = serializers.CharField(source="end_local", required=False, allow_blank=True)
    startTz = serializers.CharField(source="start_tz", required=False, allow_blank=True)
    endTz = serializers.CharField(source="end_tz", required=False, allow_blank=True)

    class Meta:
        model = ScheduleTemplateEvent
        fields = ["order", "name", "startLocal", "endLocal", "notes", "associations", "startTz", "endTz"]

class ScheduleTemplateSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    eventCount = serializers.SerializerMethodField()
    events = ScheduleTemplateEventSerializer(many=True, read_only=True)

    class Meta:
        model = ScheduleTemplate
        fields = ["id", "name", "createdAt", "eventCount", "events"]

    def get_eventCount(self, obj):
        return obj.events.count()

class ScheduleTemplateCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    events = ScheduleTemplateEventSerializer(many=True)

    def create(self, validated_data):
        day = self.context["day"]
        template = ScheduleTemplate.objects.create(tour=day.tour, name=validated_data["name"])

        events = validated_data.get("events", [])
        rows = []
        for idx, e in enumerate(events):
            rows.append(
                ScheduleTemplateEvent(
                    template=template,
                    order=e.get("order", idx),
                    name=e["name"],
                    start_local=e.get("start_local", ""),
                    end_local=e.get("end_local", ""),
                    notes=e.get("notes", ""),
                    associations=e.get("associations", []),
                    start_tz=e.get("start_tz", ""),
                    end_tz=e.get("end_tz", ""),
                )
            )

        ScheduleTemplateEvent.objects.bulk_create(rows)
        return template
