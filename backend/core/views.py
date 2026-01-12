from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.db.models import Q, Case, When, IntegerField

from rest_framework import generics

from core.models import Tour, Day, ScheduleEvent, Group, Person, ScheduleTemplate, Hotel, DayLodging, DayLodgingGuest
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
    ScheduleTemplateCreateSerializer,
    HotelSearchResultSerializer,
    DayLodgingSerializer
)
import json


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
        day = (
            Day.objects
            .select_related("venue")
            .prefetch_related("lodging__guests__person")
            .get(id=day_id)
        )

        lodging = getattr(day, "lodging", None)

        return Response(
            {
                "venue": VenueSerializer(day.venue).data,
                "contacts": ContactSerializer(day.contacts.all(), many=True).data,
                "notes": NoteSerializer(day.notes.all(), many=True).data,
                "lodging": (
                    DayLodgingSerializer(lodging).data if lodging else None
                ),
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

def _fetch_mapbox_hotels(q: str, limit: int = 8):
    token = getattr(settings, "MAPBOX_ACCESS_TOKEN", "") or ""
    if not token:
        return []

    params = {
        "access_token": token,
        "limit": str(limit),
        "types": "poi",
        "autocomplete": "true",
        "language": "en",
    }
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{q}.json?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "daysheets-demo"})
    with urlopen(req, timeout=4) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)

    out = []
    for f in data.get("features", [])[:limit]:
        place_id = f.get("id", "") or ""
        text = f.get("text", "") or ""
        place_name = f.get("place_name", "") or ""
        ctx = f.get("context", []) or []

        city = ""
        state = ""
        postal = ""

        for c in ctx:
            cid = c.get("id", "") or ""
            if cid.startswith("place."):
                city = c.get("text", "") or ""
            if cid.startswith("region."):
                state = c.get("text", "") or ""
            if cid.startswith("postcode."):
                postal = c.get("text", "") or ""

        out.append(
            {
                "key": f"ext:{place_id or text}",
                "id": None,
                "name": text or place_name,
                "address1": place_name,
                "city": city,
                "state": state,
                "postal": postal,
                "placeId": place_id,
                "source": "external",
                "addressLine": place_name,
            }
        )
    return out


class HotelSearchView(APIView):
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        tour_id = (request.query_params.get("tourId") or "").strip()

        if not q:
            return Response([], status=status.HTTP_200_OK)

        qs = Hotel.objects.all()

        if tour_id:
            qs = qs.filter(Q(tour_id=tour_id) | Q(tour__isnull=True))
            qs = qs.annotate(
                _prio=Case(
                    When(tour_id=tour_id, then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            ).order_by("_prio", "name")
        else:
            qs = qs.order_by("name")

        qs = qs.filter(
            Q(name__icontains=q)
            | Q(address1__icontains=q)
            | Q(city__icontains=q)
            | Q(state__icontains=q)
            | Q(postal__icontains=q)
        )[:20]

        local = HotelSearchResultSerializer(qs, many=True).data

        ext = []
        if len(local) < 8:
            ext = _fetch_mapbox_hotels(q, limit=8)

        seen = set()
        merged = []

        for x in local:
            k = x.get("key") or ""
            seen.add(k)
            pid = x.get("placeId") or ""
            if pid:
                seen.add(f"ext:{pid}")
            merged.append(x)

        for x in ext:
            k = x.get("key") or ""
            if k in seen:
                continue
            merged.append(x)

        return Response(merged[:20], status=status.HTTP_200_OK)

class SaveDayLodgingView(APIView):
    def post(self, request, day_id):
        day = Day.objects.select_related("tour").get(id=day_id)

        body = request.data or {}
        hotel_in = body.get("hotel") or {}

        hotel_id = hotel_in.get("id") or None
        place_id = (hotel_in.get("placeId") or hotel_in.get("place_id") or "").strip()

        if hotel_id:
            hotel = Hotel.objects.get(id=hotel_id)
        else:
            hotel = None
            if place_id:
                hotel = Hotel.objects.filter(place_id=place_id).first()
            if not hotel:
                name = (hotel_in.get("name") or "").strip()
                if not name:
                    return Response({"detail": "hotel.name is required"}, status=status.HTTP_400_BAD_REQUEST)

                hotel = Hotel.objects.create(
                    tour=day.tour,
                    name=name,
                    address1=(hotel_in.get("address1") or "").strip(),
                    city=(hotel_in.get("city") or "").strip(),
                    state=(hotel_in.get("state") or "").strip(),
                    postal=(hotel_in.get("postal") or "").strip(),
                    place_id=place_id,
                    source=(hotel_in.get("source") or "external").strip() or "external",
                )

        check_in_iso = parse_datetime(body.get("checkInISO") or "") if body.get("checkInISO") else None
        check_out_iso = parse_datetime(body.get("checkOutISO") or "") if body.get("checkOutISO") else None
        rooms = body.get("rooms", None)
        notes = body.get("notes", "") or ""

        lodging, _ = DayLodging.objects.update_or_create(
            day=day,
            defaults={
                "hotel": hotel,
                "check_in_iso": check_in_iso,
                "check_out_iso": check_out_iso,
                "rooms": rooms if rooms not in ["", None] else None,
                "notes": notes,
            },
        )

        incoming_guests = body.get("guests") or []
        person_ids = []
        for g in incoming_guests:
            pid = g.get("personId") or g.get("person_id")
            if pid:
                person_ids.append(pid)

        DayLodgingGuest.objects.filter(lodging=lodging).delete()

        if person_ids:
            people = {str(p.id): p for p in Person.objects.filter(id__in=person_ids)}
            to_create = []
            for pid in person_ids:
                p = people.get(str(pid))
                if p:
                    to_create.append(DayLodgingGuest(lodging=lodging, person=p))
            if to_create:
                DayLodgingGuest.objects.bulk_create(to_create)

        lodging = DayLodging.objects.select_related("hotel").prefetch_related("guests").get(id=lodging.id)
        return Response(DayLodgingSerializer(lodging).data, status=status.HTTP_200_OK)

    def delete(self, request, day_id):
        day = Day.objects.get(id=day_id)
        DayLodging.objects.filter(day=day).delete()
        return Response({"ok": True}, status=status.HTTP_200_OK)


class TourGroups(APIView):
    def get(self, request, tour_id):
        groups = Group.objects.filter(tour_id=tour_id).order_by("name")
        return Response(GroupSerializer(groups, many=True).data)

    def post(self, request, tour_id):
        name = (request.data.get("name") or "").strip()
        if not name:
            return Response({"detail": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.create(tour_id=tour_id, name=name)
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class TourGroupsDetail(APIView):
    def put(self, request, tour_id, group_id):
        group = Group.objects.get(id=group_id, tour_id=tour_id)

        name = request.data.get("name")
        color = request.data.get("color")

        if name is not None:
            name = name.strip()
            if not name:
                return Response({"detail": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
            group.name = name

        if color is not None:
            group.color = (color or "red").strip() or "red"

        group.save()
        return Response(GroupSerializer(group).data)

    def delete(self, request, tour_id, group_id):
        Group.objects.filter(id=group_id, tour_id=tour_id).delete()
        return Response({"ok": True})
