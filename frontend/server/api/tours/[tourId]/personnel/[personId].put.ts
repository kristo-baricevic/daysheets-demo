import { defineEventHandler, getRouterParam, readBody, createError } from "h3"
import type { Person } from "../../../../../types/app"
import { db } from "../../../../db"

export default defineEventHandler(async (event) => {
  const tourId = getRouterParam(event, "tourId") as string
  const personId = getRouterParam(event, "personId") as string

  const patch = await readBody<Partial<Person>>(event)

  const current = db.people.find(
    p => p.id === personId && p.tourId === tourId
  )

  if (!current) {
    throw createError({ statusCode: 404, statusMessage: "Person not found" })
  }

  const { id, tourId: _tourId, ...safePatch } = patch

  Object.assign(current, safePatch)

  return current
})
