
import { defineEventHandler, getRouterParam, readBody  } from "h3"
import type { Person } from "../../../../types/app";
import { db } from "../../../db";

export default defineEventHandler(async (event) => {
  const tourId = getRouterParam(event, "tourId") as string;
  const body = await readBody<Omit<Person, "id">>(event);

  const created: Person = { ...body, id: db.id("p"), tourId };
  db.people.push(created);
  return created;
});
