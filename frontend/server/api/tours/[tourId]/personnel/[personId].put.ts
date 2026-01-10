import { defineEventHandler, getRouterParam, readBody, createError } from "h3"
import { Person } from "../../../../../types/app";
import { db } from "../../../../db";


export default defineEventHandler(async (event) => {
  const tourId = getRouterParam(event, "tourId") as string;
  const personId = getRouterParam(event, "personId") as string;
  const patch = await readBody<Partial<Person>>(event);

  const idx = db.people.findIndex(p => p.id === personId && p.tourId === tourId);
  if (idx === -1) throw createError({ statusCode: 404, statusMessage: "Person not found" });

  db.people[idx] = { ...db.people[idx], ...patch };
  return db.people[idx];
});
