import { useRuntimeConfig } from "nuxt/app";
import { $fetch } from "ofetch";
import type { DayContext } from "~~/types/app";

type UUID = string;

export type Tour = { id: UUID; name: string; subtitle: string };

export type Day = {
  id: UUID;
  tourId: UUID;
  dateISO: string;
  dayType: "show" | "travel" | "off" | "rehearsal";
  city: string;
  state: string;
  venueId: UUID;
  tz: string;
};

export type ScheduleEvent = {
  id: UUID;
  dayId: UUID;
  name: string;
  startLocal: string | null;
  endLocal: string | null;
  status: "todo" | "done";
  associations: Array<{ type: "group" | "person"; id: UUID }>;
  notes: string;
};

export type Venue = {
  id: UUID;
  name: string;
  address1: string;
  city: string;
  state: string;
  postal: string;
};

export type Contact = {
  id: UUID;
  dayId: UUID;
  name: string;
  role: string;
  phone: string;
  email: string;
};

export type Note = {
  [x: string]: any;
  id: UUID;
  dayId: UUID;
  title: string;
  body: string;
  lastEditedBy: string;
  lastEditedAtISO: string;
};

export type GroupColor = "red" | "gold" | "indigo" | "green" | "blue" | "purple";

export type Group = {
  id: UUID;
  tourId: UUID;
  name: string;
  color?: GroupColor;
};

export type Person = {
  id: UUID;
  tourId: UUID;
  name: string;
  roleTitle: string;
  email: string;
  phone: string;
  groupId: UUID | null;
  permission: "owner" | "edit" | "read";
  connected: boolean;
};

export type HotelOption = {
  key: string;
  id?: string;
  name: string;
  address1?: string;
  city?: string;
  state?: string;
  postal?: string;
  placeId?: string;
  source?: string;
  addressLine: string;
};

export type DayLodging = {
  id: UUID;
  dayId: UUID;
  hotelId?: UUID | null;
  name: string;
  address1: string;
  city: string;
  state: string;
  postal: string;
  checkInISO: string;
  checkOutISO: string;
  checkInLocal: string | null;
  checkOutLocal: string | null;
  confirmationNumber: string | null;
  notes: string;
  associations: Array<{ type: "group" | "person"; id: UUID }>;
};

export const useApi = () => {
  const {
    public: { apiBase },
  } = useRuntimeConfig();

  /* Tours */
  const getTours = () => $fetch<Tour[]>(`${apiBase}/tours/`);

  const getTourDays = (tourId: UUID) => $fetch<Day[]>(`${apiBase}/tours/${tourId}/days/`);

  /* Day schedule */
  const getDaySchedule = (dayId: UUID) =>
    $fetch<ScheduleEvent[]>(`${apiBase}/days/${dayId}/schedule/`);

  const batchUpdateDaySchedule = (
    dayId: UUID,
    payload: {
      create?: Partial<ScheduleEvent>[];
      update?: Partial<ScheduleEvent>[];
      delete?: UUID[];
    }
  ) =>
    $fetch<{ ok: boolean }>(`${apiBase}/days/${dayId}/schedule/batch/`, {
      method: "POST",
      body: payload,
    });

  /* Right column context */
  const getDayContext = (dayId: UUID) => $fetch<DayContext>(`${apiBase}/days/${dayId}/context/`);

  /* Personnel */
  const getTourPersonnel = (tourId: UUID) =>
    $fetch<{ groups: Group[]; people: Person[] }>(`${apiBase}/tours/${tourId}/personnel/`);

  const deleteDayLodging = (dayId: UUID) =>
    $fetch(`${apiBase}/days/${dayId}/lodging/`, { method: "DELETE" });

  const createPerson = (tourId: UUID, payload: Partial<Person>) =>
    $fetch<Person>(`${apiBase}/tours/${tourId}/personnel/`, { method: "POST", body: payload });

  const updatePerson = (tourId: UUID, personId: UUID, payload: Partial<Person>) =>
    $fetch<Person>(`${apiBase}/tours/${tourId}/personnel/${personId}/`, {
      method: "PUT",
      body: payload,
    });

  const deletePerson = (tourId: UUID, personId: UUID) =>
    $fetch<{ ok: boolean }>(`${apiBase}/tours/${tourId}/personnel/${personId}/`, {
      method: "DELETE",
    });

  const getTourScheduleTemplates = (tourId: string) => {
    return $fetch(`${apiBase}/tours/${tourId}/schedule-templates/`);
  };

  const createDayScheduleTemplate = (dayId: string, payload: { name: string; events: any[] }) => {
    return $fetch(`${apiBase}/days/${dayId}/schedule-templates/`, {
      method: "POST",
      body: payload,
    });
  };

  const deleteTourScheduleTemplate = (tourId: string, templateId: string) => {
    return $fetch(`${apiBase}/tours/${tourId}/schedule-templates/${templateId}/`, {
      method: "DELETE",
    });
  };

  const searchHotels = (tourId: UUID, q: string) =>
    $fetch(`${apiBase}/hotels/search/`, {
      params: { q, tourId },
    });

  const saveDayLodging = (
    dayId: UUID,
    payload: Partial<DayLodging> & {
      hotel?: HotelOption;
      associations?: Array<{ type: "group" | "person"; id: UUID }>;
    }
  ) =>
    $fetch<{ ok: boolean; lodging?: DayLodging }>(`${apiBase}/days/${dayId}/lodging/`, {
      method: "POST",
      body: payload,
    });

  const createTourGroup = (tourId: UUID, payload: Partial<Group>) =>
    $fetch<Group>(`${apiBase}/tours/${tourId}/groups/`, { method: "POST", body: payload });

  const updateTourGroup = (tourId: UUID, groupId: UUID, payload: Partial<Group>) =>
    $fetch<Group>(`${apiBase}/tours/${tourId}/groups/${groupId}/`, {
      method: "PUT",
      body: payload,
    });

  const deleteTourGroup = (tourId: UUID, groupId: UUID) =>
    $fetch<{ ok: boolean }>(`${apiBase}/tours/${tourId}/groups/${groupId}/`, { method: "DELETE" });

  const createDayNote = (
    dayId: UUID,
    payload: {
      title: string;
      body: string;
      visibility: { kind: "group" | "person"; id: string }[];
    }
  ) =>
    $fetch<Note>(`${apiBase}/days/${dayId}/notes/`, {
      method: "POST",
      body: payload,
    });

  const deleteDayNote = (dayId: UUID, noteId: UUID) =>
    $fetch(`${apiBase}/days/${dayId}/notes/${noteId}/`, {
      method: "DELETE",
    });

  const updateDayAftershow = (dayId: UUID, aftershow: string) =>
    $fetch(`${apiBase}/days/${dayId}/aftershow/`, {
      method: "POST",
      body: { aftershow },
    });

  const updateDayNote = (
    dayId: UUID,
    noteId: UUID,
    payload: {
      title: string;
      body: string;
      visibility: { kind: "group" | "person"; id: string }[];
    }
  ) =>
    $fetch<Note>(`${apiBase}/days/${dayId}/notes/${noteId}/`, {
      method: "PUT",
      body: payload,
    });

  return {
    getTours,
    getTourDays,
    getDaySchedule,
    batchUpdateDaySchedule,
    getDayContext,
    getTourPersonnel,
    createPerson,
    updatePerson,
    deletePerson,
    getTourScheduleTemplates,
    createDayScheduleTemplate,
    deleteTourScheduleTemplate,
    searchHotels,
    saveDayLodging,
    deleteDayLodging,
    createTourGroup,
    updateTourGroup,
    deleteTourGroup,
    createDayNote,
    deleteDayNote,
    updateDayAftershow,
    updateDayNote,
  };
};
