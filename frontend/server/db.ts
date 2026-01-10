// server/db.ts

import { Contact, Day, Group, Note, Person, ScheduleEvent, Tour, Venue } from "../types/app";

const tours: Tour[] = [
  { id: "1", name: "Boxer Brigade", subtitle: "World Tour: West Coast" },
];

const venues: Venue[] = [
  {
    id: "v1",
    name: "The Kia Forum",
    address1: "3900 W Manchester Blvd",
    city: "Inglewood",
    state: "CA",
    postal: "90305",
  },
  {
    id: "v2",
    name: "Bill Graham Civic Auditorium",
    address1: "99 Grove St",
    city: "San Francisco",
    state: "CA",
    postal: "94102",
  },
];

const days: Day[] = [
  { id: "d1", tourId: "1", dateISO: "2026-01-08", dayType: "off", city: "Los Angeles", state: "CA", venueId: "v1", tz: "America/Los_Angeles" },
  { id: "d2", tourId: "1", dateISO: "2026-01-09", dayType: "show", city: "Inglewood", state: "CA", venueId: "v1", tz: "America/Los_Angeles" },
  { id: "d3", tourId: "1", dateISO: "2026-01-10", dayType: "show", city: "San Francisco", state: "CA", venueId: "v2", tz: "America/Los_Angeles" },
];

const groups: Group[] = [
  { id: "g1", tourId: "1", name: "Artist Party" },
  { id: "g2", tourId: "1", name: "Band Party" },
];

const people: Person[] = [
  { id: "p1", tourId: "1", name: "Emily Taylor", roleTitle: "Photographer", email: "Emily.Taylor@yabooo.com", phone: "+44 20 7946 1423", groupId: "g1", permission: "read", connected: true },
  { id: "p2", tourId: "1", name: "Frankie Davis", roleTitle: "Tour Manager", email: "frankie@theTM.com", phone: "610-608-1173", groupId: "g2", permission: "owner", connected: true },
];

const schedule: ScheduleEvent[] = [
  { id: "e1", dayId: "d2", name: "Bus Call for Venue", startLocal: "06:00", associations: [{ type: "group", id: "g2" }], status: "done" },
  { id: "e2", dayId: "d2", name: "Load In", startLocal: "07:00", associations: [{ type: "group", id: "g2" }], status: "todo" },
  { id: "e3", dayId: "d2", name: "Sound Check", startLocal: "16:00", associations: [{ type: "group", id: "g2" }], status: "todo" },
  { id: "e4", dayId: "d2", name: "Doors", startLocal: "19:00", associations: [], status: "todo" },
  { id: "e5", dayId: "d2", name: "BB ON STAGE", startLocal: "21:00", endLocal: "22:30", associations: [], status: "todo" },
  { id: "e6", dayId: "d2", name: "Load Out", startLocal: "22:30", associations: [{ type: "group", id: "g2" }], status: "todo" },
];

const contacts: Contact[] = [
  { id: "c1", dayId: "d2", name: "Dustin Francis", role: "Runner", phone: "(310) 555-0789" },
  { id: "c2", dayId: "d2", name: "Nancy Wright", role: "Local PM", phone: "(310) 555-1259", email: "nancy.wright@pmgmail.com" },
];

const notes: Note[] = [
  {
    id: "n1",
    dayId: "d2",
    title: "Crew Notes",
    body: "Our first show today. All crew buses depart at 6:00 AM. Breakfast will be up.",
    lastEditedBy: "Frankie Davis",
    lastEditedAtISO: "2026-01-09T18:34:00Z",
  },
];

const id = (prefix: string) => `${prefix}_${Math.random().toString(16).slice(2)}`;

export const db = {
  tours,
  venues,
  days,
  groups,
  people,
  schedule,
  contacts,
  notes,
  id,
};
