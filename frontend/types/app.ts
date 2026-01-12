// types/app.ts

export type ID = string;

export type DayType = "show" | "travel" | "off" | "rehearsal";

export type PermissionLevel = "owner" | "edit" | "read";

export type Association =
  | { type: "group"; id: ID }
  | { type: "person"; id: ID };

export type Tour = {
  id: ID;
  name: string;
  subtitle?: string;
};

export type Day = {
  id: ID;
  tourId: ID;
  dateISO: string; // "2026-01-09"
  dayType: DayType;
  city: string;
  state?: string;
  venueId: ID;
  tz: string; // "America/Los_Angeles"
};

export type Venue = {
  id: ID;
  name: string;
  address1: string;
  city: string;
  state: string;
  postal: string;
};

export type ScheduleEvent = {
  id: ID;
  dayId: ID;
  name: string;
  startLocal?: string; // "06:00"
  endLocal?: string;   // "10:30"
  status?: "done" | "todo";
  associations: Association[];
  notes?: string;
};

export type Contact = {
  id: ID;
  dayId: ID;
  name: string;
  role: string; // "Local PM", "Runner"
  phone?: string;
  email?: string;
};

export type Note = {
  id: ID;
  dayId: ID;
  title: string;
  body: string;
  lastEditedBy: string;
  lastEditedAtISO: string;
};

export type Group = {
  id: ID;
  tourId: ID;
  name: string;
  color?: string;
};

export type Person = {
  id: ID;
  tourId: ID;
  name: string;
  roleTitle: string;
  email?: string;
  phone?: string;
  groupId?: ID;
  permission: PermissionLevel;
  connected?: boolean;
};

export type DayContext = {
  venue: Venue;
  contacts: Contact[];
  notes: Note[];
  lodging?: DayLodging | null;
  lodgings?: DayLodging[];
};
export type DayLodgingGuest = {
  personId: string;
};

export type Hotel = {
  id: string;
  name: string;
  address1: string;
  city: string;
  state: string;
  postal: string;
  placeId: string;
  source: string;
  addressLine: string;
};

export type DayLodging = {
  id: string;
  hotel: Hotel | null;
  checkInISO: string;
  checkOutISO: string;
  rooms: number | null;
  notes: string;
  guests: DayLodgingGuest[];
  updated_at: string;
};


export type EditLodging = {
  id: string
  hotel: {
    id: string
    name: string
    address1: string
    city: string
    state: string
    postal: string
    placeId?: string
    source?: string
    addressLine: string
  } | null
  checkInISO: string
  checkOutISO: string
  rooms: number | null
  notes: string
  guests: DayLodgingGuest[]
  updated_at: string
}
