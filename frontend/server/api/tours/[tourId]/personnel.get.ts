import { defineEventHandler, getRouterParam } from "h3"
import { db } from "../../../db";

export default defineEventHandler((event) => {
  const tourId = getRouterParam(event, "tourId") as string;
  return {
    groups: db.groups.filter(g => g.tourId === tourId),
    people: db.people.filter(p => p.tourId === tourId),
  };
});
