import { defineEventHandler, getRouterParam } from "h3"
import { db } from "../../../../db";

export default defineEventHandler((event) => {
  const tourId = getRouterParam(event, "tourId") as string;
  const personId = getRouterParam(event, "personId") as string;

  const before = db.people.length;
  db.people.splice(0, db.people.length, ...db.people.filter(p => !(p.tourId === tourId && p.id === personId)));

  return { ok: db.people.length !== before };
});
