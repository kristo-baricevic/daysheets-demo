from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework import generics

from core.models import Tour, Day, ScheduleEvent, Group, Person, ScheduleTemplate
from core.serializers import (
    TourSerializer,
    DaySerializer,
    ScheduleEventSerializer,
    VenueSerializer,
    ContactSerializer,
    NoteSerializer,
    GroupSerializer,
    PersonSerializer,
    PersonWriteSerializer,
    ScheduleTemplateSerializer,
    ScheduleTemplateCreateSerializer
)


class ToursList(APIView):
    def get(self, request):
        qs = Tour.objects.all().order_by("name")
        return Response(TourSerializer(qs, many=True).data)


class TourDaysList(APIView):
    def get(self, request, tour_id):
        qs = Day.objects.filter(tour_id=tour_id).order_by("date")
        return Response(DaySerializer(qs, many=True).data)


class DayScheduleList(APIView):
    def get(self, request, day_id):
        qs = ScheduleEvent.objects.filter(day_id=day_id).order_by("start_local", "name")
        return Response(ScheduleEventSerializer(qs, many=True).data)


class DayContext(APIView):
    def get(self, request, day_id):
        day = Day.objects.select_related("venue").get(id=day_id)
        venue = day.venue
        contacts = day.contacts.all()
        notes = day.notes.all()

        return Response(
            {
                "venue": VenueSerializer(venue).data,
                "contacts": ContactSerializer(contacts, many=True).data,
                "notes": NoteSerializer(notes, many=True).data,
            }
        )


class TourPersonnel(APIView):
    def get(self, request, tour_id):
        groups = Group.objects.filter(tour_id=tour_id).order_by("name")
        people = Person.objects.filter(tour_id=tour_id).order_by("name")
        return Response(
            {
                "groups": GroupSerializer(groups, many=True).data,
                "people": PersonSerializer(people, many=True).data,
            }
        )

    def post(self, request, tour_id):
        ser = PersonWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        person = Person.objects.create(tour_id=tour_id, **ser.validated_data)
        return Response(PersonSerializer(person).data, status=status.HTTP_201_CREATED)


class TourPersonnelDetail(APIView):
    def put(self, request, tour_id, person_id):
        person = Person.objects.get(id=person_id, tour_id=tour_id)
        ser = PersonWriteSerializer(person, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        for k, v in ser.validated_data.items():
            setattr(person, k, v)
        person.save()
        return Response(PersonSerializer(person).data)

    def delete(self, request, tour_id, person_id):
        Person.objects.filter(id=person_id, tour_id=tour_id).delete()
        return Response({"ok": True})


class DayScheduleBatch(APIView):
    @transaction.atomic
    def post(self, request, day_id):
        payload = request.data or {}
        create_list = payload.get("create", []) or []
        update_list = payload.get("update", []) or []
        delete_list = payload.get("delete", []) or []

        if not isinstance(create_list, list) or not isinstance(update_list, list) or not isinstance(delete_list, list):
            return Response({"detail": "create/update/delete must be lists"}, status=400)

        ScheduleEvent.objects.filter(id__in=delete_list, day_id=day_id).delete()

        for u in update_list:
            ev_id = u.get("id")
            if not ev_id:
                return Response({"detail": "update items must include id"}, status=400)

            ev = ScheduleEvent.objects.get(id=ev_id, day_id=day_id)
            ser = ScheduleEventSerializer(ev, data=u, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()

        for c in create_list:
            ser = ScheduleEventSerializer(data={**c, "dayId": str(day_id)})
            ser.is_valid(raise_exception=True)
            ScheduleEvent.objects.create(
                day_id=day_id,
                name=ser.validated_data["name"],
                start_local=ser.validated_data.get("start_local"),
                end_local=ser.validated_data.get("end_local"),
                status=ser.validated_data.get("status", "todo"),
                associations=ser.validated_data.get("associations", []),
                notes=ser.validated_data.get("notes", ""),
            )

        return Response({"ok": True})


class TourScheduleTemplateList(generics.ListAPIView):
    serializer_class = ScheduleTemplateSerializer

    def get_queryset(self):
        tour_id = self.kwargs["tour_id"]
        return ScheduleTemplate.objects.filter(tour_id=tour_id).order_by("-created_at")

    def delete(self, request, tour_id, template_id):
        template = get_object_or_404(ScheduleTemplate, id=template_id, tour_id=tour_id)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DayScheduleTemplateCreate(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        day_id = self.kwargs["day_id"]
        day = Day.objects.select_related("tour").get(id=day_id)

        serializer = ScheduleTemplateCreateSerializer(data=request.data, context={"day": day})
        serializer.is_valid(raise_exception=True)
        template = serializer.save()

        out = ScheduleTemplateSerializer(template)
        return Response(out.data, status=status.HTTP_201_CREATED)
