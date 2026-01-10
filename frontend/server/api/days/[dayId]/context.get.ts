import { db } from "../../../db";
import { defineEventHandler, getRouterParam, createError } from "h3"

export default defineEventHandler((event) => {
  const dayId = getRouterParam(event, "dayId") as string;
  const day = db.days.find(d => d.id === dayId);
  if (!day) throw createError({ statusCode: 404, statusMessage: "Day not found" });

  const venue = db.venues.find(v => v.id === day.venueId);
  if (!venue) throw createError({ statusCode: 404, statusMessage: "Venue not found" });

  return {
    venue,
    contacts: db.contacts.filter(c => c.dayId === dayId),
    notes: db.notes.filter(n => n.dayId === dayId),
  };
});
