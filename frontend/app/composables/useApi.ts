import { useRuntimeConfig } from "nuxt/app"
import { $fetch } from "ofetch"


type UUID = string

export type Tour = { id: UUID; name: string; subtitle: string }

export type Day = {
  id: UUID
  tourId: UUID
  dateISO: string
  dayType: "show" | "travel" | "off" | "rehearsal"
  city: string
  state: string
  venueId: UUID
  tz: string
}

export type ScheduleEvent = {
  id: UUID
  dayId: UUID
  name: string
  startLocal: string | null
  endLocal: string | null
  status: "todo" | "done"
  associations: Array<{ type: "group" | "person"; id: UUID }>
  notes: string
}

export type Venue = {
  id: UUID
  name: string
  address1: string
  city: string
  state: string
  postal: string
}

export type Contact = {
  id: UUID
  dayId: UUID
  name: string
  role: string
  phone: string
  email: string
}

export type Note = {
  id: UUID
  dayId: UUID
  title: string
  body: string
  lastEditedBy: string
  lastEditedAtISO: string
}

export type Group = {
  id: UUID
  tourId: UUID
  name: string
}

export type Person = {
  id: UUID
  tourId: UUID
  name: string
  roleTitle: string
  email: string
  phone: string
  groupId: UUID | null
  permission: "owner" | "edit" | "read"
  connected: boolean
}

export const useApi = () => {
  const { public: { apiBase } } = useRuntimeConfig()

  /* Tours */
  const getTours = () =>
    $fetch<Tour[]>(`${apiBase}/tours/`)

  const getTourDays = (tourId: UUID) =>
    $fetch<Day[]>(`${apiBase}/tours/${tourId}/days/`)

  /* Day schedule */
  const getDaySchedule = (dayId: UUID) =>
    $fetch<ScheduleEvent[]>(`${apiBase}/days/${dayId}/schedule/`)

  const batchUpdateDaySchedule = (
    dayId: UUID,
    payload: {
      create?: Partial<ScheduleEvent>[]
      update?: Partial<ScheduleEvent>[]
      delete?: UUID[]
    }
  ) =>
    $fetch<{ ok: boolean }>(
      `${apiBase}/days/${dayId}/schedule/batch/`,
      { method: "POST", body: payload }
    )

  /* Right column context */
  const getDayContext = (dayId: UUID) =>
    $fetch<{
      venue: Venue
      contacts: Contact[]
      notes: Note[]
    }>(`${apiBase}/days/${dayId}/context/`)

  /* Personnel */
  const getTourPersonnel = (tourId: UUID) =>
    $fetch<{ groups: Group[]; people: Person[] }>(
      `${apiBase}/tours/${tourId}/personnel/`
    )

  const createPerson = (tourId: UUID, payload: Partial<Person>) =>
    $fetch<Person>(
      `${apiBase}/tours/${tourId}/personnel/`,
      { method: "POST", body: payload }
    )

  const updatePerson = (
    tourId: UUID,
    personId: UUID,
    payload: Partial<Person>
  ) =>
    $fetch<Person>(
      `${apiBase}/tours/${tourId}/personnel/${personId}/`,
      { method: "PUT", body: payload }
    )

  const deletePerson = (tourId: UUID, personId: UUID) =>
    $fetch<{ ok: boolean }>(
      `${apiBase}/tours/${tourId}/personnel/${personId}/`,
      { method: "DELETE" }
    )

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
  }
}
