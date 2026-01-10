import { defineEventHandler, getRouterParam, readBody } from "h3"
import { ScheduleEvent } from "../../../../../types/app"
import { db } from "../../../../db";

export default defineEventHandler(async (event) => {
  const dayId = getRouterParam(event, "dayId") as string;
  const body = await readBody<{
    create: Omit<ScheduleEvent, "id">[];
    update: ScheduleEvent[];
    delete: string[];
  }>(event);

  const delSet = new Set(body.delete ?? []);
  db.schedule.splice(0, db.schedule.length, ...db.schedule.filter(e => !delSet.has(e.id)));

  for (const u of body.update ?? []) {
    const idx = db.schedule.findIndex(e => e.id === u.id);
    if (idx !== -1) db.schedule[idx] = { ...u, dayId };
  }

  for (const c of body.create ?? []) {
    db.schedule.push({ ...c, id: db.id("e"), dayId });
  }

  return { ok: true };
});
