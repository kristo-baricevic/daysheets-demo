import { defineEventHandler, getRouterParam } from "h3"
import { db } from "../../../db";

export default defineEventHandler((event) => {
  const tourId = getRouterParam(event, "tourId") as string;
  return db.days.filter(d => d.tourId === tourId);
});
